# Dynamic Text Scaling & Overflow Elimination Engine

## Problem Statement
Standard presentation templates either:
1. Hardcode fixed font sizes, leaving massive empty white space on brief slides, OR
2. Use artificial vertical stretching (`justify-content: space-evenly`), pushing headers to the top, bullets to the bottom, and creating strange gaps in between.

## The Solution: Content Wrapper Measurement Auto-Scaler
Instead of vertical stretching, all slides start top-aligned. The font size is dynamically scaled up based on measuring the actual inner content wrapper (`#slide-content-wrap`) relative to the viewport card client height (`bodyEl.clientHeight`).

## Mathematical Algorithm

```javascript
// Reset to baseline scale
bodyEl.style.setProperty('--fit-scale', '1.0');
const wrapper = document.getElementById('slide-content-wrap') || bodyEl;
const clientH = bodyEl.clientHeight;
const targetH = clientH * 0.90; // Target 90% vertical card occupancy

let scale = 1.0;
let growIter = 0;

// Phase 1: Grow until content fills 90% of the slide card (up to 3.25x scale)
while (wrapper.offsetHeight < targetH && bodyEl.scrollHeight <= clientH && scale < 3.25 && growIter < 45) {
  scale += 0.05;
  bodyEl.style.setProperty('--fit-scale', scale.toFixed(2));
  growIter++;
}

// Phase 2: If oversized or causing scrollbar, shrink until 0 overflow is guaranteed
let shrinkIter = 0;
while ((bodyEl.scrollHeight > clientH || wrapper.offsetHeight > (clientH - 6)) && scale > 0.50 && shrinkIter < 60) {
  scale -= 0.02;
  bodyEl.style.setProperty('--fit-scale', scale.toFixed(2));
  shrinkIter++;
}
```

## Proportional Bullet Indicators (Using `em` Units)
When text scales from 18px to 68px, bullet point icons must scale proportionally. Never use fixed `rem` or `px` units for bullet pseudo-elements!

```css
/* Scalable Parent & Sub-Bullets */
.primary-bullet {
  font-family: var(--font-display);
  font-size: 1.14em;
  font-weight: 700;
  color: var(--ink);
  margin-top: 0.45em;
  margin-bottom: 0.18em;
  display: flex;
  align-items: baseline;
  gap: 0.5em;
}
.primary-bullet::before {
  content: "◆";
  color: var(--accent);
  font-size: 0.72em;      /* Scales automatically with font-size */
  line-height: 1;
  flex-shrink: 0;
}
.sub-bullets {
  list-style-type: none;
  padding-left: 1.35em;
  border-left: 2px solid var(--rule);
  margin-left: 0.35em;
  margin-bottom: 0.45em;
}
.sub-bullet {
  font-size: 0.98em;
  color: var(--ink);
  margin-bottom: 0.22em;
  position: relative;
  padding-left: 1.15em;
  line-height: 1.45;
}
.sub-bullet::before {
  content: "›";
  position: absolute;
  left: 0;
  top: -0.05em;
  color: var(--accent-dk);
  font-weight: 900;
  font-size: 1.25em;     /* Scales automatically with font-size */
  line-height: 1;
}
```
