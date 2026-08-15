# Navigation, Presentation Controls & Shortcuts

## 1. Top Navigation Bar Components

The top navigation header must contain:
1. **Home / Repository Brand**: Link to home page or documentation hub.
2. **Slide Dropdown Select**: `<select id="slide-select">` with all slide titles for instantaneous navigation.
3. **Go-To Numeric Input**: `<input type="number" id="goto-input" min="1" max="TOTAL">` + `<button id="btn-goto">Go ➔</button>`.
4. **Prev / Next Buttons**: Standard arrow navigation buttons with active and disabled states.
5. **Grid Mode Toggle**: Button to toggle all slides into a 3-column overview grid.
6. **Fullscreen Toggle**: Native browser fullscreen API trigger.
7. **Progress Bar**: Animated bar along top boundary displaying completion percentage.

## 2. Keyboard Control Map

| Key Binding | Action |
| :--- | :--- |
| `ArrowRight` / `Space` / `PageDown` | Advance to Next Slide |
| `ArrowLeft` / `PageUp` | Return to Previous Slide |
| `g` or `G` | Focus numeric Go-To slide input box |
| `m` or `M` | Toggle Grid Overview Mode |
| `f` or `F` | Toggle Native Fullscreen Mode |
| `Escape` | Exit Grid Mode or Fullscreen |
| `Enter` (inside Go-To box) | Jump to entered slide number |

## 3. Implementation Blueprint

```javascript
// Keyboard Event Listener
window.addEventListener('keydown', (e) => {
  if (['INPUT', 'SELECT', 'TEXTAREA'].includes(e.target.tagName)) {
    if (e.key === 'Escape') e.target.blur();
    return;
  }
  if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
    e.preventDefault();
    nextSlide();
  } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
    e.preventDefault();
    prevSlide();
  } else if (e.key === 'g' || e.key === 'G') {
    e.preventDefault();
    const gotoInput = document.getElementById('goto-input');
    if (gotoInput) { gotoInput.focus(); gotoInput.select(); }
  } else if (e.key === 'm' || e.key === 'M') {
    e.preventDefault();
    toggleGridMode();
  } else if (e.key === 'f' || e.key === 'F') {
    e.preventDefault();
    toggleFullScreen();
  }
});
```
