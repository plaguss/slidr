# Slidr HTML Structure Reference

## Overview

Slidr generates HTML slides from markdown. Each slide is a `<div class="slide">` containing the rendered markdown content. Understanding this structure is essential for creating effective CSS themes.

## HTML Template Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <!-- MathJax for LaTeX rendering -->
    <style>
        {{ css_content }}
        /* Alignment utility classes */
    </style>
</head>
<body class="slidr-align-{{ alignment }}">
    <div class="slides-container">
        <div class="slide active"><!-- First slide content --></div>
        <div class="slide"><!-- Second slide content --></div>
        <!-- More slides... -->
    </div>

    <div class="controls">
        <button id="prev-btn">‹</button>
        <button id="next-btn">›</button>
    </div>

    <div class="slide-counter">
        <span id="current-slide">1</span> / <span id="total-slides">3</span>
    </div>

    <script>/* Navigation logic */</script>
</body>
</html>
```

## Key CSS Classes and Elements

### Layout Structure

- **`html, body`**: Root elements - set to 100% width/height for fullscreen slides
- **`.slides-container`**: Wrapper for all slides - typically 100% width/height with `overflow: hidden`
- **`.slide`**: Individual slide container
  - Only one has `.active` class at a time (the visible slide)
  - Inactive slides typically use `display: none`
  - Common properties: `width: 100%`, `height: 100%`, `padding`, `background`
- **`.slide.active`**: The currently visible slide - typically `display: flex`

### Alignment Classes (on `<body>`)

The body element has one of these classes based on front matter:

- **`body.slidr-align-left`**: Left-aligned slides
- **`body.slidr-align-center`**: Center-aligned slides (default)
- **`body.slidr-align-right`**: Right-aligned slides

These affect `.slide` alignment and text-align properties.

### Navigation Controls

- **`.controls`**: Container for navigation buttons (typically fixed at bottom center)
- **`.controls button`**: Previous/next buttons (`#prev-btn`, `#next-btn`)
- **`.slide-counter`**: Slide number display (typically fixed at top-right)

### Content Elements Within Slides

Markdown content is rendered as standard HTML elements within each `.slide`:

- **Headings**: `h1`, `h2`, `h3`, `h4`, `h5`, `h6`
- **Paragraphs**: `p`
- **Lists**: `ul`, `ol`, `li`
- **Code**: `code` (inline), `pre` (blocks)
- **Quotes**: `blockquote`
- **Emphasis**: `em`, `strong`
- **Links**: `a`
- **Images**: `img`
- **Tables**: `table`, `thead`, `tbody`, `tr`, `th`, `td`

### Math Rendering

MathJax is included for LaTeX equations. Equations are rendered inside the slide content, so style them appropriately with your theme colors.

## Typical CSS Structure

A theme typically defines styles in this order:

1. **Reset/Base**: `*`, `html, body`
2. **Layout**: `.slides-container`, `.slide`, `.slide.active`
3. **Alignment**: `.slidr-align-*` body classes affecting `.slide`
4. **Content**: Typography for `h1`-`h6`, `p`, `li`, `code`, etc.
5. **Navigation**: `.controls`, `.slide-counter`
6. **Animations** (optional): Transitions for `.slide.active`

## CSS Cascade Rules

- All theme CSS is inlined in a `<style>` tag
- Slidr adds alignment utilities after your theme CSS (can be overridden with `!important`)
- Users can override themes with `deck/theme.css` in their project

## Example Minimal Theme Structure

```css
/* 1. Reset */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* 2. Layout */
html, body {
  width: 100%;
  height: 100%;
  font-family: sans-serif;
}

.slides-container {
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.slide {
  width: 100%;
  height: 100%;
  display: none;
  flex-direction: column;
  justify-content: center;
  padding: 60px;
  background: white;
  color: black;
}

.slide.active {
  display: flex;
}

/* 3. Content */
.slide h1 { font-size: 3em; }
.slide p { font-size: 1.2em; line-height: 1.6; }
/* ... more content styles ... */

/* 4. Navigation */
.controls { /* position, style */ }
.slide-counter { /* position, style */ }
```

## Common Patterns

### Fullscreen Slides

```css
html, body {
  width: 100%;
  height: 100%;
  overflow: hidden;
}
```

### Vertical Centering

```css
.slide {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
```

### Background Variations

```css
/* Gradient */
.slide {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Image */
.slide {
  background: url('background.jpg') center/cover no-repeat;
}

/* Per-slide backgrounds (using nth-child) */
.slide:nth-child(1) { background: #667eea; }
.slide:nth-child(2) { background: #764ba2; }
```

### Transitions/Animations

```css
.slide {
  animation: none; /* default */
}

.slide.active {
  display: flex;
  animation: fadeIn 0.5s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
```

## Responsive Considerations

Slidr slides are typically designed for presentation on large screens, but consider:

- Font sizes in `em` or `rem` for scalability
- Padding/margins that work across screen sizes
- Navigation controls that remain accessible on smaller screens

```css
@media (max-width: 768px) {
  .slide {
    padding: 30px;
    font-size: 1.5em;
  }
  .slide h1 {
    font-size: 2em;
  }
}
```
