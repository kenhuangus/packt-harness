---
name: github-pages-presentation-builder
description: 'Builds interactive, production-grade GitHub Pages HTML presentations with dynamic text auto-scaling (minimizing empty space without vertical overflow), multi-format slides (code labs with line highlighting, agent skill manifests, comparison tables, vector diagrams), mandatory GitHub repository links for code/tests, and presentation controls (Go-To slide jump, dropdown select, grid view, fullscreen, keyboard shortcuts).'
version: 1.0.0
author: Harness Engineering Team
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# GitHub Pages Presentation Deck Builder

## Overview
A comprehensive, end-to-end framework and automation tool for generating interactive, single-page presentation slide decks optimized for GitHub Pages and web browsers. It enforces a high-contrast warm editorial aesthetic, dynamic text scaling that eliminates excessive empty space without vertical scrolling, mandatory deep-linking to GitHub source code and test suites, and full keyboard-driven navigation controls.

## Structure & Progressive Disclosure
- `SKILL.md`: Main execution guide and principles.
- `scripts/`:
  - `scripts/build_presentation.py`: Python CLI generator compiling slide data into single-file production HTML.
  - `scripts/verify_presentation_qa.py`: Playwright automated test script verifying 0 vertical overflows, link validity, and proper viewport scaling.
- `references/`:
  - `references/design_system.md`: Palette tokens, typography, SVG diagrams, and CSS rules.
  - `references/dynamic_scaling_engine.md`: Mathematical auto-scaler algorithm, wrapper content measurements, and proportional `em` bullet scaling.
  - `references/navigation_and_controls.md`: Keyboard bindings, Go-To numeric jump box, dropdown switcher, and grid overview mode.
  - `references/mandatory_github_links.md`: Rules for linking source files, test suites, and skill manifests.
- `assets/`:
  - `assets/slides_data_schema.json`: JSON schema definition for slide datasets.
  - `assets/template.html`: Jinja/Python string template for presentation generation.
  - `assets/sample_slides.json`: Complete 4-slide demonstration dataset illustrating all supported slide types.

---

## When to Use
Trigger this skill whenever you need to:
1. Generate an interactive presentation or slide deck for GitHub Pages from structured data, notes, or course outlines.
2. Build an educational presentation covering software engineering, architecture, code labs, or multi-agent workflows.
3. Fix, redesign, or enhance an existing HTML slide deck with scalable typography, high contrast, and responsive layout.
4. Ensure zero vertical overflow and elimination of scrollbars while maximizing text size and readability across diverse resolutions.

---

## Core Engineering Requirements & Invariants

### 1. Visual Hierarchy & Warm Editorial Palette
- **Surfaces**: Clean warm ivory card surface (`#FAF9F5`) on light warm canvas (`#F0EEE6`) with subtle border lines (`#E3E0D6`).
- **Accents**: Terracotta primary (`#D97757`), deep terracotta (`#BD5D3A`), soft terracotta tint (`#F5E6DF`).
- **Typography**: Serif display headings (*Playfair Display / Georgia*), crisp sans-serif body (*Inter*), monospaced code (*JetBrains Mono*).
- **High Contrast**: Ensure dark ink text (`#141413`) on light backgrounds. Never use dark text on dark terracotta rectangles.

### 2. Dynamic Text Auto-Sizing (Zero Empty Space & Zero Overflow)
- **Top-Aligned Natural Flow**: Never use artificial vertical stretch (`space-evenly` / `space-around`) to pad empty slides. All slides flow naturally from the top header downward.
- **Dynamic Content Sizing**: Measure the actual inner content wrapper (`#slide-content-wrap`) and scale the font size up to `3.25x` until content fills **>= 80% to 92% of the card height**.
- **Auto-Fit Shrink Loop**: If scaled content exceeds the card container client height, dynamically shrink font size by `0.02` decrements until `wrapper.offsetHeight <= clientH - 6` and `scrollHeight <= clientH`, guaranteeing **0 vertical scrollbars and 0 text clipping**.
- **Proportional Bullet Indicators**: Always use relative `em` units for bullet points (`.primary-bullet::before` at `0.72em`, `.sub-bullet::before` at `1.25em`) so icons scale proportionally alongside enlarged text.

### 3. Navigation Controls & Header Suite
- **Dropdown Selector**: Instant slide jumper displaying slide number and title.
- **Go-To Slide Box**: Number input (`#goto-input`) with `Go ➔` button and `Enter` key listener.
- **Grid View Mode**: Toggleable overview displaying all slide cards in a responsive grid.
- **Keyboard Shortcuts**:
  - `ArrowRight` / `Space` / `PageDown`: Next slide
  - `ArrowLeft` / `PageUp`: Previous slide
  - `g` / `G`: Focus Go-To slide input box
  - `m` / `M`: Toggle Grid View mode
  - `f` / `F`: Toggle Fullscreen mode
- **Progress Bar**: Horizontal top bar tracking completion percentage.

### 4. Mandatory GitHub Deep Links for Technical Artifacts
- **Code Slides**:
  - File tag in the editor header must link directly to the source file on GitHub.
  - The `🛡️ Execution & Control Invariant` card must provide explicit GitHub links to both:
    1. The source code file (`https://github.com/<org>/<repo>/blob/main/<path>`).
    2. The automated test suite (`https://github.com/<org>/<repo>/tree/main/<module>/tests`).
- **Agent Skill Slides**:
  - Must provide clickable links to both the skill directory and the canonical `SKILL.md` manifest.

---

## Step-by-Step Workflow

1. **Prepare Slide Data (`slides_data.json`)**:
   - Organize slides into structured JSON adhering to `assets/slides_data_schema.json`.
   - Support slide types: `concept`, `code`, `skill`, `comparison`, and `reference_tables`.
2. **Compile Presentation**:
   - Run `python scripts/build_presentation.py --data slides_data.json --out docs/slides.html`.
3. **Validate in Playwright**:
   - Execute `python scripts/verify_presentation_qa.py --url docs/slides.html`.
   - Ensure `0 vertical overflows` across all slides and confirm that all links and scaling metrics pass.
4. **Deploy to GitHub Pages**:
   - Save production HTML to `docs/slides.html` and commit/push to the repository `main` branch.
