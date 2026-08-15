# Design System & Aesthetic Tokens

## 1. Color Palette Tokens

```css
:root {
  --bg: #F0EEE6;              /* Outer viewport background (soft stone/warm light) */
  --surface: #FAF9F5;         /* Slide card surface (crisp ivory) */
  --surface-tint: #F5E6DF;    /* Soft terracotta card background */
  --ink: #141413;             /* High contrast primary text */
  --ink-muted: #5A5955;       /* Secondary/meta text */
  --accent: #D97757;          /* Primary terracotta highlight */
  --accent-dk: #BD5D3A;       /* Dark terracotta for high-contrast borders & text */
  --accent-sf: #F5E6DF;       /* Background badge/pill fill */
  --rule: #E3E0D6;            /* Subtle card dividers and borders */
  --code-bg: #1E1E1E;         /* Dark editor window background */
  --code-rule: #333333;       /* Editor border */
  --font-display: "Playfair Display", Georgia, "Times New Roman", serif;
  --font-body: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-code: "JetBrains Mono", Menlo, Monaco, "Courier New", monospace;
}
```

## 2. Card Layout & Viewport Geometry
- Viewport: Full screen container `100vw x 100vh` with `overflow: hidden`.
- Header: Fixed `52px` height containing branding, quick jump dropdown, numeric input, and mode controls.
- Main Slide Area: `calc(100vh - 55px)` with centered slide card (`max-width: 1400px`, `height: calc(100% - 2rem)`).
- Slide Header: Displays category/module title, slide counter badge (`Slide X of Y`), and prominent serif title.
- Slide Body: Top-aligned flex column container (`#slide-body`) with dynamic `--fit-scale` CSS variable.

## 3. High-Contrast Vector Diagrams (SVG)
When generating inline SVG architectural diagrams or pipeline charts:
- Always use light ivory rect fills (`#FAF9F5` or `#FFFFFF`) with dark terracotta stroke borders (`#BD5D3A`, stroke-width `2px` or `2.5px`).
- Box text must use dark terracotta (`#BD5D3A`) or black ink (`#141413`) with `font-weight: 750`.
- Connecting links should include SVG `<marker id="arrow" ...>` arrowheads and label badges indicating payload direction.
- Never use white text inside dark terracotta rectangles or pastel low-contrast fills.
