"""Build HTML from markdown deck."""

import argparse
import re
import time
from collections.abc import Callable
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markdown_it import MarkdownIt
from mdit_py_plugins.dollarmath import dollarmath_plugin
from mdit_py_plugins.front_matter import front_matter_plugin
from pygments import highlight as pygments_highlight
from pygments.formatters import HtmlFormatter  # type: ignore
from pygments.lexers import TextLexer, get_lexer_by_name  # type: ignore
from pygments.util import ClassNotFound

from .logging_utils import get_logger
from .utils import get_default_theme_path, get_templates_dir, resolve_theme_path

logger = get_logger(__name__)


COMMON_NON_DECK_FILES = {"readme.md", "agents.md", "contributing.md", "changelog.md"}


def extract_front_matter(markdown_content: str) -> tuple[dict | None, str]:
    """Extract YAML front matter from markdown content.

    Front matter is expected at the very beginning of the file in the format:
    ---
    key: value
    ---

    Args:
        markdown_content: Raw markdown content

    Returns:
        Tuple of (front_matter_dict, remaining_content)
        - front_matter_dict: Parsed YAML as dict, or None if no front matter
        - remaining_content: Markdown content without front matter
    """
    # Pattern to match front matter at the start of the file
    pattern = r"^---\s*\n(.*?)\n---\s*\n"
    match = re.match(pattern, markdown_content, re.DOTALL)

    if match:
        yaml_content = match.group(1)
        try:
            front_matter = yaml.safe_load(yaml_content)
            # Remove front matter from content
            remaining_content = markdown_content[match.end() :]
            return front_matter, remaining_content
        except yaml.YAMLError as e:
            logger.warning(f"Failed to parse front matter YAML: {e}")
            return None, markdown_content

    return None, markdown_content


def _resolve_code_highlight_style(front_matter: dict | None) -> str | None:
    """Resolve Pygments style from front matter.

    Args:
        front_matter: Parsed front matter data.

    Returns:
        Pygments style name or None to disable highlighting.
    """
    if not isinstance(front_matter, dict):
        return None

    raw_value = front_matter.get("code_highlight")
    if not isinstance(raw_value, str):
        return None

    normalized = raw_value.strip()
    if not normalized:
        return None

    if normalized.lower() in {"off", "false", "no", "none"}:
        return None

    return normalized


def _build_pygments_formatter(style: str | None, *, nowrap: bool) -> HtmlFormatter:
    """Build a Pygments HTML formatter.

    Args:
        style: Optional Pygments style name.
        nowrap: Whether to omit wrapping tags.

    Returns:
        HtmlFormatter configured for the requested style.
    """
    resolved_style = style or "monokai"
    try:
        return HtmlFormatter(style=resolved_style, nowrap=nowrap)
    except ClassNotFound:
        logger.warning(
            "Unknown Pygments style '%s'. Falling back to 'monokai'.", resolved_style
        )
        return HtmlFormatter(style="monokai", nowrap=nowrap)


def _build_pygments_css(style: str | None) -> str:
    """Build CSS for Pygments-highlighted code blocks.

    Args:
        style: Optional Pygments style name.

    Returns:
        CSS string.
    """
    formatter = _build_pygments_formatter(style, nowrap=True)
    return formatter.get_style_defs("pre code")


def _math_renderer(text: str, meta: dict) -> str:
    """Render math content with delimiters for MathJax.

    Args:
        text: Math content text.
        meta: Metadata about the math block (e.g., display_mode).

    Returns:
        Rendered math with appropriate delimiters.
    """
    if meta.get("display_mode"):
        return f"$${text}$$"
    return f"${text}$"


def _create_code_highlighter(
    highlight_style: str | None,
) -> Callable:
    """Create a code highlighting function for markdown-it.

    Args:
        highlight_style: Optional Pygments style name.

    Returns:
        A callable that highlights code blocks.
    """
    formatter: HtmlFormatter | None = None

    def highlight_code(code: str, lang: str, attrs: str) -> str:
        """Highlight code blocks with Pygments when enabled."""
        nonlocal formatter
        if highlight_style is None:
            return ""

        if formatter is None:
            formatter = _build_pygments_formatter(highlight_style, nowrap=True)

        lexer = TextLexer()
        if lang:
            try:
                lexer = get_lexer_by_name(lang)
            except ClassNotFound:
                logger.debug(
                    "Unknown code language '%s'. Falling back to text lexer.", lang
                )

        return pygments_highlight(code, lexer, formatter)

    return highlight_code


def parse_markdown_to_slides(
    markdown_content: str,
    *,
    highlight_style: str | None = None,
) -> list[str]:
    """Parse markdown content into individual slides, separated by ---.

    Slides are separated by --- at the start of a line (with optional whitespace).
    This ensures table separators and other inline --- don't accidentally split slides.
    Code blocks (fenced with ```) are protected from splitting.

    Args:
        markdown_content: Raw markdown content

    Returns:
        List of HTML slides
    """
    # Split slides while respecting code blocks
    slides_raw = _split_slides_respecting_code_blocks(markdown_content)
    slides: list[str] = []

    # Create highlighter function
    highlight_code = _create_code_highlighter(highlight_style)

    # Initialize markdown-it with plugins
    # Use default preset and explicitly enable tables
    md = (
        MarkdownIt("default", options_update={"highlight": highlight_code})
        .enable("table")
        .use(front_matter_plugin)
        .use(dollarmath_plugin, renderer=_math_renderer)
    )

    for slide_content in slides_raw:
        slide_content = slide_content.strip()
        if slide_content:
            # Convert markdown to HTML
            html = md.render(slide_content)
            slides.append(html)

    return slides


def _split_slides_respecting_code_blocks(content: str) -> list[str]:
    """Split markdown content on --- while ignoring those inside code blocks.

    Args:
        content: Markdown content to split.

    Returns:
        List of slide content strings.
    """
    lines = content.split("\n")
    slides: list[str] = []
    current_slide: list[str] = []
    in_code_block = False
    code_fence_pattern = re.compile(r"^\s*```")

    for line in lines:
        # Check if we're entering/exiting a code block
        if code_fence_pattern.match(line):
            in_code_block = not in_code_block
            current_slide.append(line)
        # Check for slide separator (only outside code blocks)
        elif not in_code_block and re.match(r"^\s*---\s*$", line):
            # This is a slide separator
            if current_slide:
                slides.append("\n".join(current_slide))
                current_slide = []
        else:
            current_slide.append(line)

    # Add the last slide if there's content
    if current_slide:
        slides.append("\n".join(current_slide))

    return slides


def _find_markdown_file(deck_dir: Path) -> Path:
    """Find the markdown file in the deck directory.

    Args:
        deck_dir: Path to the deck directory.

    Returns:
        Path to the markdown file found.

    Raises:
        FileNotFoundError: If no markdown file is found.
    """
    md_files = list(deck_dir.glob("*.md"))

    if not md_files:
        raise FileNotFoundError(f"No markdown file found in {deck_dir}")

    md_file = md_files[0]

    # Warn if picking up common non-deck files
    if md_file.name.lower() in COMMON_NON_DECK_FILES:
        logger.warning(f"⚠️  Using '{md_file.name}' - this may not be a slide deck file")
        logger.warning(
            "💡 Consider running from your deck directory or specifying the deck path "
            "explicitly"
        )

    # Show which file we're using
    logger.debug(f"📄 Building from: {md_file.name}")

    # Warn if multiple markdown files exist
    if len(md_files) > 1:
        other_files = [f.name for f in md_files if f != md_file]
        logger.warning(
            f"Multiple markdown files found. Using '{md_file.name}'. "
            f"Others: {', '.join(other_files)}"
        )

    return md_file


def _resolve_theme(
    args: argparse.Namespace,
    deck_dir: Path,
    front_matter: dict | None,
) -> Path:
    """Resolve the theme path with priority order.

    Priority order:
    1. CLI --theme argument (highest priority)
    2. Front matter theme
    3. theme.css in deck directory
    4. Default theme (lowest priority)

    Args:
        args: Parsed command-line arguments.
        deck_dir: Path to the deck directory.
        front_matter: Parsed front matter, if any.

    Returns:
        Path to the resolved theme file.
    """
    theme_path: Path | None = None

    if args.theme:
        # CLI argument takes highest priority
        theme_path = resolve_theme_path(args.theme, deck_dir)
        if not theme_path:
            logger.warning(
                f"Theme '{args.theme}' not found, falling back to next option"
            )

    if not theme_path and front_matter and "theme" in front_matter:
        # Front matter theme
        theme_name = front_matter["theme"]
        logger.debug(f"🎨 Front matter specifies theme: {theme_name}")
        theme_path = resolve_theme_path(theme_name, deck_dir)
        if not theme_path:
            logger.warning(
                f"Theme '{theme_name}' from front matter not found, falling back to "
                "next option"
            )

    if not theme_path:
        # Check for theme.css in deck directory
        deck_theme = deck_dir / "theme.css"
        if deck_theme.exists():
            theme_path = deck_theme

    if not theme_path:
        # Use default theme
        theme_path = get_default_theme_path()
        if not front_matter or "theme" not in front_matter:
            logger.info("No theme specified, using default theme")

    return theme_path


def _build_full_css_content(
    theme_path: Path,
    highlight_style: str | None,
) -> str:
    """Build complete CSS content from theme and optional Pygments highlighting.

    Args:
        theme_path: Path to the theme CSS file.
        highlight_style: Optional Pygments style name.

    Returns:
        Complete CSS content.
    """
    css_content = theme_path.read_text(encoding="utf-8")

    if highlight_style is not None:
        pygments_css = _build_pygments_css(highlight_style)
        # These fixes are put in place to ensure the lines
        # within code blocks are not highlighted individually,
        # which causes some ugly visual effect.
        pygments_fixes = "pre code { display: block; padding: 0; border-radius: 0; line-height: 1.4; }"  # noqa: E501
        css_content = (
            f"{css_content}\n\n/* Pygments syntax highlighting */\n{pygments_css}\n\n"
            f"/* Slidr code block fixes */\n{pygments_fixes}"
        )

    return css_content


def _extract_page_metadata(front_matter: dict | None) -> tuple[str, str]:
    """Extract page title and text alignment from front matter.

    Args:
        front_matter: Parsed front matter, if any.

    Returns:
        Tuple of (page_title, alignment).
    """
    page_title = "Slide Deck"
    alignment = "left"

    if isinstance(front_matter, dict):
        raw_title = front_matter.get("title")
        if isinstance(raw_title, str) and raw_title.strip():
            page_title = raw_title.strip()

        raw_alignment = front_matter.get("align")
        if raw_alignment is not None:
            alignment_value = str(raw_alignment).strip().lower()
            if alignment_value in {"left", "center", "right"}:
                alignment = alignment_value
            else:
                logger.warning(
                    "Invalid align '%s' in front matter. Using '%s'.",
                    alignment_value,
                    alignment,
                )

    return page_title, alignment


def _render_slides_template(
    page_title: str,
    slides: list[str],
    css_content: str,
    alignment: str,
    live_reload: bool,
) -> str:
    """Render the slides HTML template.

    Args:
        page_title: Title for the HTML page.
        slides: List of rendered slide HTML strings.
        css_content: Complete CSS content to inline.
        alignment: Text alignment for slides (left, center, right).
        live_reload: Whether to enable live reload in the template.

    Returns:
        Complete HTML content.
    """
    env = Environment(
        loader=FileSystemLoader(str(get_templates_dir())),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template("slides.html")

    build_id = str(int(time.time() * 1000))

    html_content = template.render(
        title=page_title,
        slides=slides,
        css_content=css_content,
        alignment=alignment,
        build_id=build_id,
        live_reload=live_reload,
    )

    return html_content


def build_deck(args: argparse.Namespace) -> int:
    """
    Build HTML from markdown deck.

    Args:
        args: Parsed command-line arguments containing:
            - deck: Path to the deck folder
            - output: Optional output HTML file path
            - theme: Optional path to custom CSS theme

    Returns:
        Exit code (0 for success)

    Raises:
        FileNotFoundError: If deck directory or markdown file not found
    """
    deck_dir = Path(args.deck)

    if not deck_dir.exists():
        raise FileNotFoundError(f"Deck directory not found: {deck_dir}")

    md_file = _find_markdown_file(deck_dir)

    markdown_content = md_file.read_text(encoding="utf-8")

    front_matter, content_without_front_matter = extract_front_matter(markdown_content)

    highlight_style = _resolve_code_highlight_style(front_matter)
    slides = parse_markdown_to_slides(
        content_without_front_matter,
        highlight_style=highlight_style,
    )

    theme_path = _resolve_theme(args, deck_dir, front_matter)

    css_content = _build_full_css_content(theme_path, highlight_style)

    page_title, alignment = _extract_page_metadata(front_matter)

    live_reload = bool(getattr(args, "live_reload", False))
    html_content = _render_slides_template(
        page_title, slides, css_content, alignment, live_reload
    )

    # Write output
    output_file = Path(args.output) if args.output else deck_dir / "index.html"
    output_file.write_text(html_content, encoding="utf-8")

    logger.info(f"✓ Built slides: {output_file}")

    return 0
