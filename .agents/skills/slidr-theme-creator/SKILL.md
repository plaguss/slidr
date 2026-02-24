---
name: slidr-theme-creator
description: Create custom CSS themes for Slidr slide presentations. Use this skill when working with Slidr and users need to create new themes, customize existing themes, apply brand colors, or modify slide styling. Covers dark themes, minimal themes, corporate/brand themes, high-contrast themes, code-focused themes, and any CSS customization for Slidr HTML slides.
license: MIT
---

# Slidr Theme Creator

Create custom CSS themes for Slidr slide presentations.

## Quick Start

Slidr themes are CSS files that style the HTML slides. To create a theme:

1. **Understand the HTML structure** - See [references/html-structure.md](references/html-structure.md) for all CSS classes and elements
2. **Start with a built-in theme** - Slidr includes 8 built-in themes you can use as-is or customize
3. **Customize** - Modify colors, fonts, layouts to match requirements
4. **Apply** - Use with `slidr build deck --theme your-theme.css`

## Built-in Themes

Slidr includes these ready-to-use themes in `src/slidr/assets/`:

1. **minimal-light.css** - Clean, simple, black text on white background
2. **dark-professional.css** - Dark background with light text, high contrast
3. **corporate-brand.css** - Template with CSS variables for brand colors (customize this)
4. **high-contrast.css** - Maximum readability with bright colors on black
5. **gradient.css** - Vibrant gradient backgrounds that change per slide
6. **academic.css** - Professional serif theme for academic/research presentations
7. **code-focused.css** - Dark theme optimized for code examples (VS Code-like)
8. **retro.css** - Nostalgic vintage design with warm colors

Use them directly:
```bash
slidr build deck --theme minimal-light
slidr build deck --theme dark-professional
```

Or in markdown front matter:
```markdown
---
theme: gradient
---
```

To customize a built-in theme, copy it from the assets directory and modify it.

## Theme Application Methods

Themes can be applied in three ways (in order of precedence):

1. **CLI argument**: `slidr build deck --theme custom-theme.css` (highest priority)
2. **Front matter**: Add `theme: custom-theme` in markdown file's YAML front matter
3. **Project file**: Place `theme.css` in `deck/` directory
4. **Default**: Falls back to built-in default theme

## Core Theme Structure

Every theme must define:

```css
/* 1. Reset and base */
*, html, body { /* reset styles */ }

/* 2. Layout containers */
.slides-container { /* fullscreen container */ }
.slide { /* individual slide (hidden by default) */ }
.slide.active { /* visible slide (display: flex) */ }

/* 3. Content typography */
.slide h1, .slide h2, .slide h3 { /* headings */ }
.slide p, .slide li { /* text */ }
.slide code, .slide pre { /* code blocks */ }

/* 4. Navigation */
.controls { /* arrow buttons */ }
.slide-counter { /* slide numbers */ }
```

## Common Customization Tasks

### Change Brand Colors

Replace gradient/background colors and adjust text for contrast:

```css
.slide {
  background: linear-gradient(135deg, #YOUR-PRIMARY 0%, #YOUR-SECONDARY 100%);
  color: #YOUR-TEXT-COLOR;
}

.slide h1 {
  color: #YOUR-HEADING-COLOR;
}
```

For complex brand theming, use CSS custom properties:

```css
:root {
  --brand-primary: #0066cc;
  --brand-secondary: #003d7a;
  --brand-accent: #00a3e0;
}

.slide {
  background: linear-gradient(135deg, var(--brand-primary), var(--brand-secondary));
}

.slide h2 {
  color: var(--brand-accent);
}
```

### Change Typography

```css
html, body {
  font-family: 'Your Font', 'Fallback Font', sans-serif;
}

.slide h1 {
  font-size: 3.5em;  /* Adjust heading sizes */
  font-weight: 700;
}

.slide p {
  font-size: 1.2em;  /* Adjust body text size */
  line-height: 1.8;  /* Adjust line spacing */
}
```

### Change Slide Layout

By default slides center content. Adjust with flexbox:

```css
/* Left-aligned slides */
.slide {
  align-items: flex-start;
  text-align: left;
  justify-content: flex-start;
}

/* Top-aligned slides */
.slide {
  justify-content: flex-start;
  align-items: center;
}

/* Custom padding/margins */
.slide {
  padding: 80px 120px; /* Adjust whitespace */
}
```

### Add Slide-Specific Backgrounds

Use `:nth-child()` to style individual slides:

```css
.slide:nth-child(1) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.slide:nth-child(2) {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

/* Pattern repeats for additional slides */
.slide:nth-child(n+3) {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}
```

### Style Code Blocks

Slidr includes both inline `code` and block `pre` elements:

```css
.slide code {
  background: rgba(0, 0, 0, 0.2);
  color: #ffcc00;
  padding: 4px 8px;
  border-radius: 4px;
  font-family: 'JetBrains Mono', 'Courier New', monospace;
}

.slide pre {
  background: rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 25px;
  border-radius: 10px;
  font-size: 0.85em;
  text-align: left;
}
```

### Customize Navigation Controls

```css
.controls {
  position: fixed;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
}

.controls button {
  background: #your-color;
  color: #text-color;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.controls button:hover {
  opacity: 0.8;
  transform: scale(1.05);
}
```

### Add Animations

```css
.slide.active {
  display: flex;
  animation: slideIn 0.5s ease-in-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(100%);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}
```

## Alignment System

Slidr supports alignment via front matter (`align: left|center|right`). This adds a class to `<body>`:

- `body.slidr-align-left`
- `body.slidr-align-center`
- `body.slidr-align-right`

Override Slidr's default alignment utilities in your theme:

```css
body.slidr-align-left .slide {
  align-items: flex-start;
  text-align: left;
}

body.slidr-align-center .slide {
  align-items: center;
  text-align: center;
}
```

## Testing Themes

1. Create or modify a `.css` file with your theme
2. Build with `slidr build deck --theme your-theme.css`
3. Open `deck/index.html` in a browser
4. Use `slidr serve deck` for live reload during development

## Reference Files

- **[references/html-structure.md](references/html-structure.md)** - Complete CSS class reference, HTML structure, common patterns
- **Built-in themes** - See `src/slidr/assets/` for 8 ready-to-use themes (listed above in Built-in Themes section)

## Workflow

When creating a theme from scratch:

1. **Clarify requirements** - Ask about:
   - Brand colors/fonts if corporate
   - Target audience (academic, developer, executive, etc.)
   - Tone (professional, playful, minimal, bold)
   - Whether code blocks are prominent

2. **Select starting template** - Choose a built-in theme to customize:
   - Corporate → Use `corporate-brand.css` (has CSS variables ready)
   - Dark background → Use `dark-professional.css`
   - Lots of code → Use `code-focused.css`
   - Simple → Use `minimal-light.css`
   - Vivid → Use `gradient.css`
   - Academic → Use `academic.css`
   - Fun/vintage → Use `retro.css`
   - Accessibility → Use `high-contrast.css`

3. **Get the theme file** - Read the built-in theme from `src/slidr/assets/[theme-name].css`

4. **Customize** - Modify the theme CSS:
   - Replace color values with brand colors
   - Adjust fonts to brand fonts
   - Tweak spacing/sizing as needed
   - Add animations if desired

5. **Create file** - Write the customized CSS to a `.css` file in the user's deck directory

6. **Test** - Have user build and preview: `slidr build deck --theme your-theme.css && slidr serve deck`

When modifying an existing theme:

1. **Read current theme** - Load `deck/theme.css` or the specified theme file
2. **Identify changes needed** - Based on user request
3. **Apply modifications** - Edit the CSS file
4. **Test** - Have user rebuild and preview

## Tips

- **Contrast**: Ensure text has sufficient contrast with backgrounds for readability
- **Fonts**: Web-safe fonts work everywhere; Google Fonts require internet
- **Responsive**: Most slide decks are fullscreen, but consider smaller screens if needed
- **Animation**: Use sparingly; excessive animation can be distracting
- **Consistency**: Maintain consistent spacing, colors, and typography throughout
- **Code readability**: For developer presentations, prioritize code block styling
- **MathJax**: Math equations inherit slide colors - test with equations if user needs them
