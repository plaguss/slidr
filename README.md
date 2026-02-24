# slidr

Create beautiful slide decks from markdown. Just write your slides in markdown, and slidr handles the rest.

## Getting Started

You can use slidr in two ways:

**Install it globally** (recommended if you'll use it regularly):

```bash
uv tool install slidr
```

**Or run it on the fly** (if you're just trying it out):

```bash
uvx slidr new my-deck
uvx slidr build my-deck/deck
uvx slidr serve my-deck/deck -p 8000
```

Either way, here's the typical workflow:

Create a project, build HTML, and run a local preview server.

```bash
slidr new my-deck
cd my-deck
slidr build deck
slidr serve deck
```

Write your slides in `deck/deck.md` using `---` to separate them. When you build, slidr generates an `index.html` file you can open in any browser.

## Example Deck

Want to see Slidr in action? This repository includes an example deck, if you clone the repo, you can navigate to see the generated slides as:

```bash
# Build and serve the example
slidr serve deck
```

View the source in [deck/deck.md](./deck/deck.md) to see how the deck is structured.

## Themes

Slidr comes with a collection of beautiful built-in themes. Use them by specifying the theme in your markdown front matter:

```markdown
---
theme: default
---
# First Slide
```

### Built-in Themes

| | |
|---|---|
| ![default](image.png) `default` | ![minimal-light](image-1.png) `minimal-light` |
| ![dark-professional](image-2.png) `dark-professional` | ![high-contrast](image-3.png) `high-contrast` |

### Custom Themes

Want to make something your own? Create a `theme.css` file in your `deck/` directory:

```bash
# Your project structure
my-deck/
  deck/
    deck.md
    theme.css      # Your custom theme
    index.html
```

#### Using Web Fonts

Want to use custom fonts? It's easy. Add the font definitions to your `theme.css`:

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

Slidr's template includes popular web fonts by default. If you need fonts that aren't included yet, feel free to open a PR—we can add them! Just note that font links need to be added to the HTML template (not as`@import` in CSS, as that doesn't work reliably with inline styles).

## Configuration

Customize your deck using front matter at the top of your markdown file. It's a simple YAML block that controls how your slides look and behave:

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

### Options

- **`theme`** — Which theme to use
  - Built-in: `default`, `minimal-light`, `dark-professional`, `high-contrast`
  - Custom: Path to your own CSS file (e.g., `custom-theme.css`)
  - Priority: CLI argument > front matter > local `deck/theme.css` > default

- **`title`** — Browser tab title (default: `"Slide Deck"`)
  - Example: `title: Introduction to Python`

- **`align`** — Text alignment for all slides (`left`, `center`, `right`; default: `left`)
  - Example: `align: center`

- **`code_highlight`** — Syntax highlighting for code blocks
  - Options: Any [Pygments style name](https://pygments.org/styles/) like `monokai`, `github`, `dracula`, `solarized-dark`, `nord`
  - Disable: `off`, `false`, `no`, or `none`
  - Example: `code_highlight: dracula`

## AI-Powered Theme Creation

Want a custom theme without writing CSS? Use the **slidr-theme-creator** AI skill to generate one based on your needs:

- "Create a dark theme with blue gradients and modern fonts"
- "Generate a corporate theme using brand colors #0066cc and #003d7a"
- "Make a minimal light theme optimized for readability"
- "Design a code-focused theme with syntax highlighting colors"

The skill handles design patterns, accessibility, brand identity, and modern web aesthetics. Learn more in [.agents/skills/slidr-theme-creator/SKILL.md](.agents/skills/slidr-theme-creator/SKILL.md).

## Development

Want to contribute or run slidr locally? Here's how to set up:

**Install in development mode:**

```bash
uv venv
uv pip install -e .
```

**Run tests:**

```bash
uv pip install -e .[dev]
pytest
```

**Set up pre-commit hooks**:

```bash
uv pip install pre-commit
pre-commit install
pre-commit run --all-files
```

## See Also

There are some great alternatives out there, definitely check them out!

- <https://sli.dev/>
- <https://marpit.marp.app/>
- <https://martenbe.github.io/mkslides/#/>
