---
theme: custom-theme.css
align: left
code_highlight: monokai
---

# What is Slidr?

Write your presentations in **markdown** and let Slidr transform them into professional HTML slides.

- Simple markdown syntax
- Built-in themes and easily customizable with css
- Live preview with auto-reload
- No complex tools required

---

# Quick Start

## Installation

```bash
pip install slidr
```

## Create a New Project

```bash
slidr new my-presentation
cd my-presentation
```

Your slides live in `deck/deck.md` — just edit and build!

---

# Three Simple Commands

## 1. Create a New Project

```bash
slidr new <project-name>
```

Scaffolds a new presentation directory with starter files.

## 2. Build HTML Slides

```bash
slidr build deck
```

Converts your markdown to `deck/index.html`.

---

# Three Simple Commands

## 3. Live Preview

```bash
slidr serve deck
```

Launches a local server with **live reload** — edit your markdown and see changes instantly.

- Default: `http://localhost:8000`
- Custom port: `slidr serve deck -p 3000`

---

# Writing Slides

## It's Just Markdown

Separate slides with `---` on its own line (three dashes as a horizontal rule).

**Example structure:**
- Write your first slide content
- Add a line with three dashes: `---`
- Write your next slide content
- And repeat

Each section becomes a slide. That's it!

---

# Front Matter Configuration

Configure your deck with YAML front matter at the top of your markdown file.

## How to Use Front Matter

Place YAML configuration at the **very beginning** of your markdown file:

```markdown
`---  # Remove the leading tick, is just here to exemplify
theme: minimal-light
title: My Presentation
align: center
code_highlight: monokai
`---

# Text here

Your content

```

---

## Available Front-matter Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `theme` | string | Specify which theme to use. Built-in: `default`, `minimal-light`, `dark-professional`, `gradient`, `academic`, `code-focused`, `high-contrast`, `corporate-brand`, `retro`. Or use custom CSS path. | `theme: dark-professional` |
| `title` | string | HTML page title (browser tab). Default: `"Slide Deck"` | `title: Introduction to Python` |
| `align` | string | Text alignment for all slides. Values: `left`, `center`, `right`. Default: `left` | `align: center` |
| `code_highlight` | string | Syntax highlighting style. Use any Pygments style (`monokai`, `github`, `dracula`, etc.) or `off` to disable. | `code_highlight: monokai` |

---

# Rich Text Formatting

You can use *italic*, **bold**, and ***bold italic*** text.

Inline code like `slidr build deck` renders beautifully.

> Blockquotes stand out with distinctive styling for emphasis and visual interest.

All standard markdown formatting is supported, provided by [`markdown-it-py`](https://markdown-it-py.readthedocs.io/)

---

# Modern Typography

This theme uses **contemporary web fonts** for a polished look:

- **Outfit** — Bold, geometric headings
- **Inter** — Clean, readable body text
- **JetBrains Mono** — Developer-favorite code font

Custom fonts are easy to integrate. Just reference them in your CSS and ensure font links are in the HTML template.

---

# Lists Are Easy

Unordered lists:

- Build presentations quickly
- Write in plain markdown
- Choose from 8+ themes
- No HTML or CSS knowledge needed

Ordered lists work too:

1. Write your content
2. Run `slidr build`
3. Present with confidence

---

# Code Blocks

Syntax highlighting for code examples:

```python
def build_presentation(deck_path: Path) -> None:
    """Generate HTML slides from markdown."""
    slides = parse_markdown(deck_path / "deck.md")
    theme = resolve_theme_path(deck_path)
    render_slides(slides, theme)
```

It just works for technical presentations or tutorials

---

# More Code Examples

```javascript
// JavaScript example
const slidr = require('slidr');

slidr.build({
  input: 'deck.md',
  theme: 'dark-professional',
  output: 'index.html'
});
```

---

# Math

Inline equations render seamlessly: $E = mc^2$ or $\frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$

Perfect for scientific and academic presentations!

---

# Display Equations

Display equations get their own space:

$$
\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
$$

Complex mathematical notation is fully supported via MathJax.

---

# Built-in Themes

Slidr includes **8 builtin themes**:

- `minimal-light` — Clean and simple
- `dark-professional` — High contrast dark theme
- `gradient` — Vibrant gradient backgrounds
- `academic` — Professional serif typography
- `code-focused` — Optimized for code examples
- `high-contrast` — Maximum readability
- `corporate-brand` — Customizable brand colors
- `retro` — Nostalgic vintage design

---

# Custom Themes

## Create Your Own

Themes are just CSS files. Place a `theme.css` in your `deck/` folder or specify with `--theme`:

```bash
slidr build deck --theme ./custom-theme.css
```

Full control over:
- Colors and gradients
- Typography and fonts
- Layout and spacing
- Animations and transitions

---

# Navigation

Typical **keyboard shortcuts** for presenting:

- **Arrow keys** → Next/Previous slide
- **Space bar** → Next slide
- **Home/End** → First/Last slide

**On-screen controls** for clicking through slides

**Slide counter** shows your progress

---

# Project Structure

```
my-presentation/
├── deck/
│   ├── deck.md         # Your slides (markdown)
│   ├── theme.css       # Optional custom theme
│   └── index.html      # Generated output
```

Simple and organized. Everything in one place.

---

# Why Slidr?

**Focus on content**, not formatting:

- Write in **markdown** you already know
- No PowerPoint or Keynote required
- Version control friendly (it's just text!)
- Fast workflow with live preview
- Beautiful results out of the box

---

# Features at a Glance

- ✨ **Simple:** Markdown → HTML, that's it
- ⚡ **Fast:** Live preview with instant reload
- 🔧 **Customizable:** Create your own themes with CSS
- 📊 **Rich content:** Math, code, images, tables
- 🤖 **AI-Powered:** Use the theme creator skill for custom designs

---

# AI Theme Creation

Slidr includes an **AI skill** called `slidr-theme-creator` for generating custom CSS themes:

**Example requests:**
- "Create a dark theme with purple gradients for tech talks"
- "Generate a minimal corporate theme using our brand colors: #0066cc and #003d7a"
- "Make a high-contrast theme optimized for code presentations"

The skill understands:
- Brand color palettes and corporate identity
- Typography and layout preferences
- Accessibility requirements
- Modern design patterns

---

# Get Started Today

## Install

```bash
pip install slidr
```

## Create

```bash
slidr new presentation
```

## Present

```bash
cd awesome-presentation
slidr serve deck
```

Start creating beautiful presentations with markdown
