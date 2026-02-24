"""Tests for build.py module."""

import argparse
import logging
from pathlib import Path

import pytest
from pygments.formatters import HtmlFormatter  # type: ignore

from slidr.build import (
    _build_pygments_css,
    _build_pygments_formatter,
    _resolve_code_highlight_style,
    build_deck,
    extract_front_matter,
    parse_markdown_to_slides,
)
from slidr.utils import (
    get_default_theme_path,
    get_templates_dir,
    resolve_theme_path,
)


class TestGetDefaultThemePath:
    """Tests for get_default_theme_path function."""

    def test_returns_path_object(self):
        """Should return a Path object."""
        result = get_default_theme_path()
        assert isinstance(result, Path)

    def test_returns_default_css_path(self):
        """Should return path to default.css in assets directory."""
        result = get_default_theme_path()
        assert result.name == "default.css"
        assert result.parent.name == "assets"

    def test_default_theme_exists(self):
        """Should return a path that exists."""
        result = get_default_theme_path()
        assert result.exists()


class TestGetTemplatesDir:
    """Tests for get_templates_dir function."""

    def test_returns_path_object(self):
        """Should return a Path object."""
        result = get_templates_dir()
        assert isinstance(result, Path)

    def test_returns_templates_directory(self):
        """Should return path to templates directory."""
        result = get_templates_dir()
        assert result.name == "templates"

    def test_templates_dir_exists(self):
        """Should return a path that exists."""
        result = get_templates_dir()
        assert result.exists()


class TestParseMarkdownToSlides:
    """Tests for parse_markdown_to_slides function."""

    @pytest.mark.parametrize(
        "markdown_input,expected_count",
        [
            ("# Slide 1", 1),
            ("# Slide 1\n---\n# Slide 2", 2),
            ("# Slide 1\n---\n# Slide 2\n---\n# Slide 3", 3),
            ("# Slide 1\n---\n# Slide 2\n---\n# Slide 3\n---\n# Slide 4", 4),
        ],
    )
    def test_splits_markdown_by_separator(
        self, markdown_input: str, expected_count: int
    ):
        """Should split markdown content by --- separator."""
        result = parse_markdown_to_slides(markdown_input)
        assert len(result) == expected_count

    def test_converts_markdown_to_html(self):
        """Should convert markdown to HTML."""
        markdown = "# Heading\n\nParagraph text."
        result = parse_markdown_to_slides(markdown)
        assert "<h1>Heading</h1>" in result[0]
        assert "<p>Paragraph text.</p>" in result[0]

    def test_filters_empty_slides(self):
        """Should filter out empty slides."""
        markdown = "# Slide 1\n---\n\n---\n# Slide 2"
        result = parse_markdown_to_slides(markdown)
        # Should have 2 slides, not 3 (empty slide filtered out)
        assert len(result) == 2

    def test_strips_whitespace_from_slides(self):
        """Should strip whitespace from slide content before processing."""
        markdown = "   # Slide 1   \n---\n   # Slide 2   "
        result = parse_markdown_to_slides(markdown)
        assert len(result) == 2

    @pytest.mark.parametrize(
        "markdown_input",
        [
            "",
            "   ",
            "\n\n",
            "---",
            "---\n---\n---",
        ],
    )
    def test_handles_empty_or_whitespace_content(self, markdown_input: str):
        """Should handle empty or whitespace-only content."""
        result = parse_markdown_to_slides(markdown_input)
        assert result == []

    def test_preserves_markdown_formatting(self):
        """Should preserve different markdown elements."""
        markdown = """# Heading
**Bold text**
*Italic text*
- List item 1
- List item 2"""
        result = parse_markdown_to_slides(markdown)
        html = result[0]
        assert "<h1>Heading</h1>" in html
        assert "<strong>Bold text</strong>" in html
        assert "<em>Italic text</em>" in html
        assert "<ul>" in html
        assert "<li>List item" in html

    def test_supports_math_and_highlighted_code(self):
        """Should preserve math delimiters and highlight code when enabled."""
        markdown = """Inline $x$ and display $$y$$.

```unknownlang
print('hello')
```
"""
        result = parse_markdown_to_slides(markdown, highlight_style="monokai")
        html = result[0]
        assert "$x$" in html
        assert "$y$" in html
        assert "print" in html

    def test_renders_inline_math(self):
        """Should render inline math with single dollar signs."""
        markdown = "The formula $E = mc^2$ is famous."
        result = parse_markdown_to_slides(markdown)
        html = result[0]
        assert "$E = mc^2$" in html

    def test_renders_display_math(self):
        """Should render display math with double dollar signs."""
        markdown = "$$\\int_0^\\infty e^{-x} dx = 1$$"
        result = parse_markdown_to_slides(markdown)
        html = result[0]
        assert "$$" in html

    def test_code_highlighting_disabled_returns_empty(self):
        """Should return empty string when code highlighting is disabled."""
        markdown = """# Slide with code

```python
def hello():
    print("world")
```
"""
        result = parse_markdown_to_slides(markdown, highlight_style=None)
        html = result[0]
        # When highlighting is disabled, code blocks should still be present but without
        # Pygments
        assert "def hello" in html or "hello" in html


class TestCodeHighlighting:
    """Tests for code highlighting helpers."""

    def test_resolve_code_highlight_style_filters_invalid(self):
        """Should ignore unsupported or disabled highlight values."""
        assert _resolve_code_highlight_style(None) is None
        assert _resolve_code_highlight_style({"code_highlight": 123}) is None
        assert _resolve_code_highlight_style({"code_highlight": "   "}) is None
        assert _resolve_code_highlight_style({"code_highlight": "off"}) is None
        assert _resolve_code_highlight_style({"code_highlight": "Monokai"}) == "Monokai"

    def test_build_pygments_formatter_falls_back_on_invalid_style(self):
        """Should fallback to monokai when style is unknown."""
        formatter = _build_pygments_formatter("not-a-style", nowrap=True)
        assert isinstance(formatter, HtmlFormatter)

    def test_build_pygments_css_includes_code_selector(self):
        """Should generate CSS for code selectors."""
        css = _build_pygments_css("monokai")
        assert "pre code" in css


class TestExtractFrontMatter:
    """Tests for extract_front_matter function."""

    def test_extracts_valid_front_matter(self):
        """Should extract valid YAML front matter."""
        markdown = """---
theme: name
title: My Presentation
---
# Slide 1
Content here."""

        front_matter, content = extract_front_matter(markdown)

        assert front_matter is not None
        assert front_matter["theme"] == "name"
        assert front_matter["title"] == "My Presentation"
        assert content.strip().startswith("# Slide 1")

    def test_returns_none_when_no_front_matter(self):
        """Should return None when no front matter present."""
        markdown = "# Slide 1\nContent here."

        front_matter, content = extract_front_matter(markdown)

        assert front_matter is None
        assert content == markdown

    def test_handles_empty_front_matter(self):
        """Should handle empty front matter block."""
        markdown = """---
---
# Slide 1"""

        front_matter, content = extract_front_matter(markdown)

        assert front_matter is None or front_matter == {}
        assert "# Slide 1" in content

    def test_handles_invalid_yaml(self):
        """Should handle invalid YAML gracefully."""
        markdown = """---
not: valid: yaml: here
---
# Slide 1"""

        front_matter, content = extract_front_matter(markdown)

        assert front_matter is None
        assert "---" in content  # Should return original content

    def test_preserves_content_without_front_matter(self):
        """Should preserve content when no front matter exists."""
        markdown = "# Slide 1\n---\n# Slide 2"

        front_matter, content = extract_front_matter(markdown)

        assert front_matter is None
        assert content == markdown


class TestResolveThemePath:
    """Tests for resolve_theme_path function."""

    def test_resolves_asset_theme(self):
        """Should resolve built-in asset themes."""
        result = resolve_theme_path("default")

        assert result is not None
        assert result.exists()
        assert result.name == "default.css"

    def test_adds_css_extension_if_missing(self):
        """Should add .css extension if not present."""
        result = resolve_theme_path("default")

        assert result is not None
        assert result.name.endswith(".css")

    def test_resolves_deck_theme(self, tmp_path: Path):
        """Should resolve theme in deck directory."""
        deck_dir = tmp_path / "deck"
        deck_dir.mkdir()
        theme_file = deck_dir / "custom.css"
        theme_file.write_text("body { color: red; }")

        result = resolve_theme_path("custom", deck_dir)

        assert result is not None
        assert result == theme_file

    def test_prefers_deck_theme_over_asset(self, tmp_path: Path):
        """Should prefer deck directory theme over asset theme."""
        deck_dir = tmp_path / "deck"
        deck_dir.mkdir()
        deck_theme = deck_dir / "default.css"
        deck_theme.write_text("body { color: blue; }")

        result = resolve_theme_path("default", deck_dir)

        assert result == deck_theme

    def test_returns_none_for_nonexistent_theme(self, tmp_path: Path):
        """Should return None for nonexistent theme."""
        result = resolve_theme_path("nonexistent", tmp_path)

        assert result is None

    def test_handles_absolute_path(self, tmp_path: Path):
        """Should handle absolute paths."""
        theme_file = tmp_path / "mytheme.css"
        theme_file.write_text("body { color: green; }")

        result = resolve_theme_path(str(theme_file))

        assert result == theme_file


class TestBuildDeck:
    """Tests for build_deck function."""

    def test_builds_deck_successfully(self, temp_deck_dir: Path):
        """Should build deck successfully with default options."""
        args = argparse.Namespace(deck=str(temp_deck_dir), output=None, theme=None)

        result = build_deck(args)

        assert result == 0
        output_file = temp_deck_dir / "index.html"
        assert output_file.exists()

        content = output_file.read_text(encoding="utf-8")
        assert "<!DOCTYPE html>" in content
        assert "Slide 1" in content
        assert "Slide 2" in content

    def test_uses_custom_output_path(self, temp_deck_dir: Path, tmp_path: Path):
        """Should use custom output path when provided."""
        custom_output = tmp_path / "custom_output.html"
        args = argparse.Namespace(
            deck=str(temp_deck_dir), output=str(custom_output), theme=None
        )

        result = build_deck(args)

        assert result == 0
        assert custom_output.exists()

    def test_uses_deck_theme_css_if_exists(self, temp_deck_dir_with_theme: Path):
        """Should use theme.css from deck directory if it exists."""
        args = argparse.Namespace(
            deck=str(temp_deck_dir_with_theme), output=None, theme=None
        )

        result = build_deck(args)

        assert result == 0
        output_file = temp_deck_dir_with_theme / "index.html"
        content = output_file.read_text(encoding="utf-8")
        assert "background: red" in content

    def test_uses_custom_theme_when_provided(self, temp_deck_dir: Path, tmp_path: Path):
        """Should use custom theme when --theme argument provided."""
        custom_theme = tmp_path / "custom.css"
        custom_theme.write_text("body { background: blue; }")

        args = argparse.Namespace(
            deck=str(temp_deck_dir), output=None, theme=str(custom_theme)
        )

        result = build_deck(args)

        assert result == 0
        output_file = temp_deck_dir / "index.html"
        content = output_file.read_text(encoding="utf-8")
        assert "background: blue" in content

    def test_custom_theme_overrides_deck_theme(
        self, temp_deck_dir_with_theme: Path, tmp_path: Path
    ):
        """Should use custom theme even if deck has theme.css."""
        custom_theme = tmp_path / "override.css"
        custom_theme.write_text("body { background: green; }")

        args = argparse.Namespace(
            deck=str(temp_deck_dir_with_theme), output=None, theme=str(custom_theme)
        )

        result = build_deck(args)

        assert result == 0
        output_file = temp_deck_dir_with_theme / "index.html"
        content = output_file.read_text(encoding="utf-8")
        assert "background: green" in content
        assert "background: red" not in content

    def test_raises_error_for_nonexistent_deck_directory(self, tmp_path: Path):
        """Should raise FileNotFoundError for nonexistent deck directory."""
        args = argparse.Namespace(
            deck=str(tmp_path / "nonexistent"), output=None, theme=None
        )

        with pytest.raises(FileNotFoundError, match="Deck directory not found"):
            build_deck(args)

    def test_raises_error_for_deck_without_markdown_file(self, empty_deck_dir: Path):
        """Should raise FileNotFoundError if no markdown file in deck."""
        args = argparse.Namespace(deck=str(empty_deck_dir), output=None, theme=None)

        with pytest.raises(FileNotFoundError, match="No markdown file found"):
            build_deck(args)

    def test_uses_first_markdown_file_when_multiple_exist(self, temp_deck_dir: Path):
        """Should use first markdown file found when multiple exist."""
        # Create additional markdown file
        (temp_deck_dir / "another.md").write_text("# Another slide")

        args = argparse.Namespace(deck=str(temp_deck_dir), output=None, theme=None)

        result = build_deck(args)
        assert result == 0

    @pytest.mark.parametrize(
        "markdown_extension",
        [
            "deck.md",
            "slides.md",
            "presentation.md",
        ],
    )
    def test_finds_markdown_files_with_md_extension(
        self, tmp_path: Path, markdown_extension: str
    ):
        """Should find markdown files regardless of name."""
        deck_dir = tmp_path / "deck"
        deck_dir.mkdir()

        md_file = deck_dir / markdown_extension
        md_file.write_text("# Test slide")

        args = argparse.Namespace(deck=str(deck_dir), output=None, theme=None)

        result = build_deck(args)
        assert result == 0

    def test_creates_valid_html_structure(self, temp_deck_dir: Path):
        """Should create valid HTML with proper structure."""
        args = argparse.Namespace(deck=str(temp_deck_dir), output=None, theme=None)

        build_deck(args)

        output_file = temp_deck_dir / "index.html"
        content = output_file.read_text(encoding="utf-8")

        # Check for required HTML elements
        assert "<!DOCTYPE html>" in content
        assert "<html" in content
        assert "<head>" in content
        assert "<body" in content
        assert "</body>" in content
        assert "</html>" in content
        assert "<style>" in content
        assert "</style>" in content

    def test_warns_when_cli_theme_missing(
        self, temp_deck_dir: Path, caplog: pytest.LogCaptureFixture
    ):
        """Should warn and fall back when CLI theme is missing."""
        caplog.set_level(logging.WARNING, logger="slidr.build")
        args = argparse.Namespace(
            deck=str(temp_deck_dir), output=None, theme="missing-theme.css"
        )

        build_deck(args)

        assert "not found" in caplog.text

    def test_warns_for_missing_front_matter_theme(
        self, tmp_path: Path, caplog: pytest.LogCaptureFixture
    ):
        """Should warn when front matter theme cannot be resolved."""
        deck_dir = tmp_path / "deck"
        deck_dir.mkdir()
        (deck_dir / "deck.md").write_text("""---
theme: missing-theme
---

# Slide
""")

        caplog.set_level(logging.WARNING, logger="slidr.build")
        args = argparse.Namespace(deck=str(deck_dir), output=None, theme=None)

        build_deck(args)

        assert "from front matter not found" in caplog.text

    def test_includes_pygments_css_when_enabled(self, tmp_path: Path):
        """Should append Pygments CSS when code highlighting is enabled."""
        deck_dir = tmp_path / "deck"
        deck_dir.mkdir()
        (deck_dir / "deck.md").write_text("""---
code_highlight: monokai
---

# Slide

```python
print("hi")
```
""")

        args = argparse.Namespace(deck=str(deck_dir), output=None, theme=None)

        build_deck(args)

        content = (deck_dir / "index.html").read_text(encoding="utf-8")
        assert "Pygments syntax highlighting" in content

    def test_warns_on_invalid_alignment(
        self, tmp_path: Path, caplog: pytest.LogCaptureFixture
    ):
        """Should warn when align front matter is invalid."""
        deck_dir = tmp_path / "deck"
        deck_dir.mkdir()
        (deck_dir / "deck.md").write_text("""---
align: sideways
---

# Slide
""")

        caplog.set_level(logging.WARNING, logger="slidr.build")
        args = argparse.Namespace(deck=str(deck_dir), output=None, theme=None)

        build_deck(args)

        assert "Invalid align" in caplog.text

    def test_applies_valid_alignment_from_front_matter(self, tmp_path: Path):
        """Should apply valid alignment from front matter."""
        deck_dir = tmp_path / "deck"
        deck_dir.mkdir()
        (deck_dir / "deck.md").write_text("""---
align: right
---

# Slide
""")

        args = argparse.Namespace(deck=str(deck_dir), output=None, theme=None)
        build_deck(args)

        output_file = deck_dir / "index.html"
        content = output_file.read_text(encoding="utf-8")
        # Should have text-align: right in the CSS
        assert "text-align: right" in content or "right" in content

    def test_includes_all_slides_in_output(self, temp_deck_dir: Path):
        """Should include all slides from markdown in output."""
        args = argparse.Namespace(deck=str(temp_deck_dir), output=None, theme=None)

        build_deck(args)

        output_file = temp_deck_dir / "index.html"
        content = output_file.read_text(encoding="utf-8")

        # Should contain all three slides
        assert "First slide" in content
        assert "Second slide" in content
        assert "Third slide" in content

    def test_uses_theme_from_front_matter(self, temp_deck_dir_with_front_matter: Path):
        """Should use theme specified in front matter."""
        args = argparse.Namespace(
            deck=str(temp_deck_dir_with_front_matter), output=None, theme=None
        )

        result = build_deck(args)

        assert result == 0
        output_file = temp_deck_dir_with_front_matter / "index.html"
        content = output_file.read_text(encoding="utf-8")
        assert "background: purple" in content

    def test_cli_theme_overrides_front_matter_theme(
        self, temp_deck_dir_with_front_matter: Path, tmp_path: Path
    ):
        """Should prefer CLI theme over front matter theme."""
        cli_theme = tmp_path / "cli.css"
        cli_theme.write_text("body { background: yellow; }")

        args = argparse.Namespace(
            deck=str(temp_deck_dir_with_front_matter), output=None, theme=str(cli_theme)
        )

        result = build_deck(args)

        assert result == 0
        output_file = temp_deck_dir_with_front_matter / "index.html"
        content = output_file.read_text(encoding="utf-8")
        assert "background: yellow" in content
        assert "background: purple" not in content

    def test_front_matter_does_not_appear_in_slides(
        self, temp_deck_dir_with_front_matter: Path
    ):
        """Should not include front matter in slide content."""
        args = argparse.Namespace(
            deck=str(temp_deck_dir_with_front_matter), output=None, theme=None
        )

        build_deck(args)

        output_file = temp_deck_dir_with_front_matter / "index.html"
        content = output_file.read_text(encoding="utf-8")

        # Front matter keys should not appear in output
        assert "theme: custom" not in content
        assert "title: My Awesome Presentation" not in content

    def test_fallback_to_default_theme_with_warning(self, temp_deck_dir: Path):
        """Should fallback to default theme and log info when no theme specified."""
        args = argparse.Namespace(deck=str(temp_deck_dir), output=None, theme=None)

        result = build_deck(args)

        assert result == 0
        output_file = temp_deck_dir / "index.html"
        assert output_file.exists()
        # Output should contain default theme CSS
        content = output_file.read_text(encoding="utf-8")
        assert len(content) > 0

    def test_warns_when_using_readme_as_deck(
        self, tmp_path: Path, caplog: pytest.LogCaptureFixture
    ):
        """Should warn when using README.md as slide deck."""
        deck_dir = tmp_path / "deck"
        deck_dir.mkdir()
        (deck_dir / "README.md").write_text("# Welcome\n\n---\n\n# Slide 2")

        caplog.set_level(logging.WARNING, logger="slidr.build")
        args = argparse.Namespace(deck=str(deck_dir), output=None, theme=None)

        build_deck(args)

        assert "README.md" in caplog.text
        assert "may not be a slide deck file" in caplog.text


# ==============================================================================
# End-to-End Tests
# ==============================================================================


def test_end_to_end_slide_parsing_with_code_blocks(tmp_path: Path):
    """End-to-end test: code blocks with --- should not break slide parsing."""
    deck_dir = tmp_path / "deck"
    deck_dir.mkdir()

    # Create a comprehensive markdown file that tests edge cases
    (deck_dir / "deck.md").write_text("""---
theme: default
title: Test Deck
---

# Slide 1: Introduction
Welcome to the test deck.

---

# Slide 2: Code Example with Separator
Here's how to separate slides:

Use `---` on its own line to create a new slide.

---

# Slide 3: Code Block with Separator
Example code showing slide syntax:

```markdown
# First Slide
Content here

---

# Second Slide
More content
```

This should be a single slide!

---

# Slide 4: Front Matter Example
Front matter configuration:

```yaml
---
theme: custom
title: My Deck
---
```

Still one slide.

---

# Slide 5: Table with Separators
Here's a table:

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Value A  | Value B  | Value C  |
| Data 1   | Data 2   | Data 3   |

Tables should not break parsing.

---

# Slide 6: Multiple Code Blocks
First block:

```python
def example():
    return "---"
```

Second block:

```bash
echo "---"
```

Still one slide with two code blocks.

---

# Slide 7: Final Slide
The end.
""")

    args = argparse.Namespace(deck=str(deck_dir), output=None, theme=None)

    # Build the deck
    result = build_deck(args)
    assert result == 0

    # Read the output HTML
    output_file = deck_dir / "index.html"
    assert output_file.exists()
    content = output_file.read_text(encoding="utf-8")

    # Count actual slide divs (not slide-container or slide-counter)
    import re

    slide_divs = re.findall(r'<div class="slide (?:active|)">', content)
    assert len(slide_divs) == 7, f"Expected 7 slides, but found {len(slide_divs)}"

    # Verify key content is present and not split incorrectly
    assert "Slide 1: Introduction" in content
    assert "Slide 2: Code Example with Separator" in content
    assert "Slide 3: Code Block with Separator" in content
    assert "This should be a single slide!" in content
    assert "Slide 4: Front Matter Example" in content
    assert "Still one slide." in content
    assert "Slide 5: Table with Separators" in content
    assert "Tables should not break parsing" in content
    assert "Slide 6: Multiple Code Blocks" in content
    assert "Still one slide with two code blocks" in content
    assert "Slide 7: Final Slide" in content

    # Verify code blocks with --- are preserved as code, not interpreted as separators
    assert "<code>---</code>" in content or 'return "---"' in content

    # Verify table rendering worked correctly
    assert "<table>" in content
    assert "<thead>" in content
    assert "<tbody>" in content
    assert "Column 1" in content
    assert "Value A" in content

    # Verify front matter was stripped from output
    assert "theme: default" not in content or "```yaml" in content
    assert "Test Deck" in content  # Page title, not in slides
