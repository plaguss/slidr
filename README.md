# slidr

Slide generator with markdown.

## For users

These steps are for people who just want to create and present slides. You do not need a Python dev setup.

### Install (tool)
Install the CLI once and keep it available on your PATH.
```bash
uv tool install slidr
```

### Run without installing
Use this if you only need `slidr` occasionally or just want it to run without pointing to a specific directory.
```bash
uvx slidr new my-deck
uvx slidr build my-deck/deck
uvx slidr serve my-deck/deck -p 8000
```

### Basic workflow
Create a project, build HTML, and run a local preview server.
```bash
slidr new my-deck
cd my-deck
slidr build deck
slidr serve deck -p 8000
```

Slides are written in `deck/deck.md` using `---` as slide separators. The build step generates `deck/index.html`.

### Customization

#### Custom Themes
Create a `theme.css` file in your `deck/` directory to customize the appearance:

```bash
# Your project structure
my-deck/
  deck/
    deck.md
    theme.css      # Your custom theme
    index.html
```

You can also use built-in themes by specifying them in front matter:
```markdown
---
theme: dark-professional
---
# First Slide
```

Available built-in themes: `default`, `dark-professional`, `minimal-light`, `corporate-brand`, `high-contrast`, `code-focused`, `academic`, `gradient`, `retro`.

#### Custom Fonts
To use custom web fonts in your theme:

1. **Define fonts in your CSS** (e.g., `deck/theme.css`):
```css
/* Apply fonts to elements */
html, body {
  font-family: 'Inter', sans-serif;
}

.slide h1, .slide h2, .slide h3 {
  font-family: 'Outfit', sans-serif;
}

.slide code, .slide pre code {
  font-family: 'JetBrains Mono', monospace;
}
```

2. **Font loading is handled automatically** - Slidr's template includes popular web fonts preloaded. If you need additional fonts, you'll need to modify the `slides.html` template to add `<link>` tags.

**Important**: Do not use `@import` statements in your CSS for web fonts, as they don't work reliably in inline styles. Font links must be added to the HTML template.

#### Front Matter Configuration

Configure your deck with YAML front matter at the top of your markdown file. Front matter must be placed at the very beginning of the file, enclosed by `---` delimiters:

```markdown
---
theme: dark-professional
title: My Awesome Presentation
align: center
code_highlight: monokai
---

# First Slide
Content starts here...
```

**Available Front Matter Fields:**

- **`theme`** (string) - Specify which theme to use for your slides
  - Built-in themes: `default`, `dark-professional`, `minimal-light`, `corporate-brand`, `high-contrast`, `code-focused`, `academic`, `gradient`, `retro`
  - Custom themes: Path to a CSS file (e.g., `custom-theme.css`, `./themes/corporate.css`)
  - Priority order: CLI `--theme` argument > front matter `theme` > `deck/theme.css` > default theme

- **`title`** (string) - Set the HTML page title (appears in browser tab)
  - Default: `"Slide Deck"`
  - Example: `title: Introduction to Python`

- **`align`** (string) - Control text alignment for all slides
  - Valid values: `left`, `center`, `right`
  - Default: `left`
  - Example: `align: center`

- **`code_highlight`** (string) - Configure syntax highlighting for code blocks
  - Accepts any [Pygments style name](https://pygments.org/styles/) (e.g., `monokai`, `github`, `dracula`, `solarized-dark`, `nord`)
  - Disable highlighting: Use `off`, `false`, `no`, or `none`
  - Default: No highlighting unless specified
  - Example: `code_highlight: monokai`

**Example with all fields:**

```markdown
---
theme: dark-professional
title: Advanced Python Techniques
align: left
code_highlight: dracula
---

# Welcome
This is my first slide...

---

# Code Example
```python
def hello():
    print("Hello, world!")
```
```

#### AI-Powered Theme Creation

Slidr includes the **slidr-theme-creator** AI skill that can generate custom CSS themes based on your requirements:

**Example requests to AI agents:**
- "Create a dark theme with blue gradients and modern fonts"
- "Generate a corporate theme using brand colors #0066cc and #003d7a"
- "Make a minimal light theme optimized for readability"
- "Design a code-focused theme with syntax highlighting colors"

The skill understands design patterns, accessibility requirements, brand identity, and modern web aesthetics. See [.agents/skills/slidr-theme-creator/SKILL.md](.agents/skills/slidr-theme-creator/SKILL.md) for details.

## Development

These steps are for contributors who are changing the codebase or running tests.

### Install (editable)
Create a local virtual environment and install in editable mode.
```bash
uv venv
uv pip install -e .
```

### Test
Install dev dependencies and run the test suite with pytest.
```bash
uv pip install -e .[dev]
pytest
```

### pre-commit
Install hooks to keep formatting and checks consistent before commits.
```bash
uv pip install pre-commit
pre-commit install
pre-commit run --all-files
```

## Alternatives

I just wanted to use my own for no special reason, but these are some alternatives (almost surely they do the same or better).

- https://sli.dev/
- https://marpit.marp.app/
- https://martenbe.github.io/mkslides/#/
