# Slidr Theme Examples

All example themes are now available as built-in themes in `src/slidr/assets/`. 

## Usage

Use them directly by name:
```bash
slidr build deck --theme minimal-light
slidr build deck --theme dark-professional
slidr build deck --theme gradient
```

Or in markdown front matter:
```markdown
---
theme: code-focused
---
```

## Customizing Themes

To customize a built-in theme:

1. Read the source from `src/slidr/assets/[theme-name].css`
2. Copy the CSS to a new file in your deck directory
3. Modify colors, fonts, spacing as needed
4. Apply with `slidr build deck --theme your-custom-theme.css`

---

## Available Built-in Themes

### 1. minimal-light.css
**Location:** `src/slidr/assets/minimal-light.css`  
**Description:** Clean, simple, black text on white background  
**Best for:** Professional presentations, readability-first content

### 2. dark-professional.css
**Location:** `src/slidr/assets/dark-professional.css`  
**Description:** Dark background with light text, blue accents  
**Best for:** Modern tech presentations, evening/low-light venues

### 3. corporate-brand.css
**Location:** `src/slidr/assets/corporate-brand.css`  
**Description:** Template with CSS variables for easy brand customization  
**Best for:** Corporate presentations, brand-aligned content  
**Note:** Edit the CSS variables at the top to match your brand colors

### 4. high-contrast.css
**Location:** `src/slidr/assets/high-contrast.css`  
**Description:** Maximum readability with bright colors on black  
**Best for:** Accessibility, large venues, vision-impaired audiences

### 5. gradient.css
**Location:** `src/slidr/assets/gradient.css`  
**Description:** Vibrant gradient backgrounds that change per slide  
**Best for:** Creative presentations, eye-catching visuals

### 6. academic.css
**Location:** `src/slidr/assets/academic.css`  
**Description:** Professional serif theme for research presentations  
**Best for:** Academic conferences, research papers, formal settings

### 7. code-focused.css
**Location:** `src/slidr/assets/code-focused.css`  
**Description:** Dark theme optimized for code examples (VS Code-like)  
**Best for:** Developer talks, coding tutorials, technical presentations

### 8. retro.css
**Location:** `src/slidr/assets/retro.css`  
**Description:** Nostalgic vintage design with warm colors  
**Best for:** Fun presentations, creative content, retro themes

---

## Quick Customization Tips

### Corporate Branding
Start with `corporate-brand.css` and modify the CSS variables:
```css
:root {
  --brand-primary: #YOUR-COLOR;
  --brand-secondary: #YOUR-COLOR;
  --brand-accent: #YOUR-COLOR;
}
```

### Dark Theme
Start with `dark-professional.css` or `code-focused.css` and adjust colors.

### Minimal/Clean
Start with `minimal-light.css` and adjust typography/spacing.

### Eye-Catching
Start with `gradient.css` and customize the gradient colors.
