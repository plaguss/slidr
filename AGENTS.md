# Slidr - AI Coding Instructions

## Project Overview
Slidr is a markdown-to-HTML slide deck generator with a CLI. Users create presentations by writing markdown files with `---` as slide separators. The tool provides three commands: `new` (scaffold projects), `build` (generate HTML), and `serve` (live preview with auto-rebuild).

## Architecture

### Command Flow
- Entry: `slidr` command → [main.py](../src/slidr/main.py) → [cli.py](../src/slidr/cli.py) `create_parser()`
- CLI dispatches to dedicated modules: [new.py](../src/slidr/new.py), [build.py](../src/slidr/build.py), [serve.py](../src/slidr/serve.py)
- Each command function receives `argparse.Namespace` and returns exit code (0 = success)

### Core Pipeline (Build)
1. **Parse markdown**: `parse_markdown_to_slides()` splits on `---`, converts each to HTML via `markdown-it-py`
2. **Extract front matter**: `extract_front_matter()` parses YAML metadata from start of file
3. **Load theme**: Theme resolution follows priority order:
   - CLI `--theme` argument (highest)
   - Front matter `theme` field
   - `deck/theme.css` if exists
   - Default theme from assets (lowest)
4. **Render template**: [slides.html](../src/slidr/templates/slides.html) (Jinja2) injects slides + CSS inline
5. **Write output**: `index.html` in deck directory

### Serve Architecture
- HTTP server on localhost (default port 8000) serving from deck directory
- Separate thread runs `watchfiles` monitoring deck folder
- Debounced rebuilds (1 second) on file changes
- Ctrl+C triggers graceful shutdown via `KeyboardInterrupt`

### Package Resources
Access bundled assets/templates via `Path(__file__).parent`:
```python
PACKAGE_DIR = Path(__file__).parent
ASSETS_DIR = PACKAGE_DIR / "assets"
TEMPLATES_DIR = PACKAGE_DIR / "templates"
```

Theme files can be resolved from:
- Built-in assets directory (e.g., `default.css`)
- Custom files in deck directory
- Absolute paths
Use `resolve_theme_path()` to find themes across these locations.

## Project Conventions

### Code Style
- **Type hints**: Required for all function signatures (see [build.py](../src/slidr/build.py), [serve.py](../src/slidr/serve.py))
- **Paths**: Use `pathlib.Path` exclusively, never string paths
- **Logging**: Import via `get_logger(__name__)` from [logging_utils.py](../src/slidr/logging_utils.py), not `print()`
- **Docstrings**: Google style with Args/Returns/Raises sections
- Use absolute imports instead of relative ones
- Use always modern, idiomatic, concise Python
- End-to-end type-safety and test coverage
- Thoughtful, tasteful, consistent API design
- Delightful developer experience

### Project Structure Pattern
User projects follow this layout (created by `new`):
```
my-presentation/
  deck/
    deck.md         # Markdown with slides
    theme.css       # CSS overrides
    index.html      # Generated output
```

### Documentation

When the user refers to "docs" or "documentation", this means both the README.md and the deck/deck.md, both should include the updates for the users to keep track.

### Markdown Parsing
- Slide separator: `---` (horizontal rule)
- Uses `markdown-it-py` with `front_matter_plugin`
- Supports YAML front matter at the beginning of the file for metadata
- Front matter format:
  ```markdown
  ---
  theme: custom-theme
  ---
  # First Slide
  ```
- Each slide rendered independently, wrapped in `.slide` div
- Front matter is extracted before slide parsing and not included in output

## Critical Developer Knowledge

### Running Locally
```bash
# Install dependencies (requires Python 3.14+)
uv pip install -e .

# Test workflow
slidr new test-deck
cd test-deck
slidr build deck
slidr serve deck -p 8001
```

### Template Customization
[slides.html](../src/slidr/templates/slides.html) uses Jinja2 with embedded JavaScript for keyboard navigation (Arrow keys, Space). CSS inlined via `{{ css_content|safe }}` - no external stylesheets.

**Critical**: The `|safe` filter is required to prevent HTML escaping of CSS content, which would break font-family declarations and other CSS with quotes.

### Font Loading Architecture
Custom fonts must be loaded via `<link>` tags in the HTML `<head>`, not via `@import` in CSS:

**Why**: When CSS is inlined in `<style>` tags:
1. `@import` statements may not work reliably
2. Even if they work, URLs can be HTML-escaped, breaking the import

**Implementation**:
1. Add Google Fonts (or other web fonts) as `<link>` tags in [slides.html](../src/slidr/templates/slides.html)
2. Use preconnect hints for performance:
   ```html
   <link rel="preconnect" href="https://fonts.googleapis.com">
   <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
   <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
   ```
3. Reference fonts in theme CSS with standard `font-family` declarations
4. CSS content is marked as safe (`{{ css_content|safe }}`) to preserve quotes in font names

## Common Tasks

### Adding a New Command
1. Create `src/slidr/mycommand.py` with function accepting `argparse.Namespace`
2. Import in [cli.py](../src/slidr/cli.py): `from slidr.cmd_name import mycommand`
3. Add subparser in `create_parser()`
4. Use `get_logger(__name__)` for output, not `print()`

### Modifying Slide Rendering
- Change HTML structure: Edit [templates/slides.html](../src/slidr/templates/slides.html) Jinja2 template
- Change default styling: Edit [assets/default.css](../src/slidr/assets/default.css)
- Add custom fonts: Add `<link>` tags to [templates/slides.html](../src/slidr/templates/slides.html), then reference in theme CSS
- Adjust markdown parsing: Modify `parse_markdown_to_slides()` in [build.py](../src/slidr/build.py)
- Change front matter handling: Modify `extract_front_matter()` in [build.py](../src/slidr/build.py)
- Adjust theme resolution: Modify `resolve_theme_path()` in [utils.py](../src/slidr/utils.py)

## Development Workflow

### Setting Up Development Environment
```bash
# Clone and navigate to project
cd slidr

# Install dependencies with development tools
uv add --dev pytest pytest-cov pytest-mock

# Activate virtual environment (Windows)
.\.venv\Scripts\Activate.ps1

# Activate virtual environment (Unix/macOS)
source .venv/bin/activate

# Install package in editable mode
uv pip install -e .
```

### Running Tests
The project has comprehensive test coverage using pytest:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=slidr --cov-report=html

# Run specific test file
pytest tests/test_build.py

# Run specific test class
pytest tests/test_build.py::TestBuildDeck

# Run specific test
pytest tests/test_build.py::TestBuildDeck::test_builds_deck_successfully

# Run with short traceback on failures
pytest --tb=short
```

## Skills

Slidr includes the following skills:

### slidr-theme-creator

**Purpose**: Create custom CSS themes for Slidr slide presentations. This is the primary tool for design customization and theme generation.

**Use this skill when users need to:**
- Create new themes from scratch based on requirements
- Customize existing themes with brand colors and fonts
- Apply corporate identity or brand guidelines
- Modify slide styling, layouts, and visual design
- Create specialized themes: dark themes, minimal themes, corporate themes, high-contrast themes, code-focused themes, or any CSS customization

**Capabilities:**
- Generate complete theme CSS files
- Understand design patterns and modern web aesthetics
- Apply accessibility guidelines (WCAG compliance)
- Customize typography, colors, layouts, backgrounds
- Create responsive and professional slide designs

**Location**: [.agents/skills/slidr-theme-creator/SKILL.md](.agents/skills/slidr-theme-creator/SKILL.md)
