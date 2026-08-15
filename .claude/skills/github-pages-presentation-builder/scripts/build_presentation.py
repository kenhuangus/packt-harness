#!/usr/bin/env python3
"""
GitHub Pages Presentation Deck Builder CLI
Compiles a structured slides_data.json file into a standalone, production-ready
single-file HTML presentation with dynamic font scaling and interactive navigation.
"""

import argparse
import json
import os
import re
import sys

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{DECK_TITLE}}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,600&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #F0EEE6;
      --surface: #FAF9F5;
      --surface-tint: #F5E6DF;
      --ink: #141413;
      --ink-muted: #5A5955;
      --accent: #D97757;
      --accent-dk: #BD5D3A;
      --accent-sf: #F5E6DF;
      --rule: #E3E0D6;
      --code-bg: #1E1E1E;
      --code-rule: #333333;
      --font-display: "Playfair Display", Georgia, "Times New Roman", serif;
      --font-body: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      --font-code: "JetBrains Mono", Menlo, Monaco, "Courier New", monospace;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      background-color: var(--bg);
      color: var(--ink);
      font-family: var(--font-body);
      height: 100vh;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      -webkit-font-smoothing: antialiased;
    }

    header {
      background: var(--surface);
      border-bottom: 1px solid var(--rule);
      padding: 0.35rem 1.25rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 10;
      flex-shrink: 0;
      height: 52px;
    }

    .brand {
      font-family: var(--font-display);
      font-weight: 700;
      font-size: 1.05rem;
      color: var(--ink);
      display: flex;
      align-items: center;
      gap: 0.5rem;
      text-decoration: none;
    }
    .brand span { color: var(--accent); }

    .nav-controls {
      display: flex;
      gap: 0.45rem;
      align-items: center;
    }

    button {
      background: var(--surface);
      color: var(--ink);
      border: 1px solid var(--rule);
      padding: 0.35rem 0.65rem;
      border-radius: 6px;
      font-family: var(--font-body);
      font-size: 0.82rem;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.3rem;
      transition: all 0.15s ease;
    }
    button:hover:not(:disabled) {
      background: var(--accent-sf);
      border-color: var(--accent);
      color: var(--accent-dk);
    }
    button:disabled { opacity: 0.4; cursor: not-allowed; }
    button.primary { background: var(--accent); color: #FAF9F5; border-color: var(--accent); }
    button.primary:hover:not(:disabled) { background: var(--accent-dk); }

    .goto-box {
      display: flex;
      align-items: center;
      gap: 0.25rem;
      background: var(--bg);
      padding: 0.12rem 0.25rem;
      border-radius: 8px;
      border: 1px solid var(--rule);
    }
    .goto-input {
      width: 48px;
      background: var(--surface);
      color: var(--ink);
      border: 1px solid var(--rule);
      padding: 0.25rem 0.35rem;
      border-radius: 6px;
      font-family: var(--font-code);
      font-size: 0.80rem;
      font-weight: 750;
      text-align: center;
    }
    select.slide-select {
      background: var(--surface); color: var(--ink); border: 1px solid var(--rule);
      padding: 0.35rem 0.55rem; border-radius: 8px; font-family: var(--font-body);
      font-size: 0.80rem; font-weight: 600; max-width: 290px;
    }

    main {
      flex: 1;
      position: relative;
      overflow: hidden;
    }

    .slide-viewport {
      width: 100%;
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: clamp(0.4rem, 1.2vh, 1.0rem) clamp(0.5rem, 1.5vw, 1.2rem);
    }

    .slide-card {
      background: var(--surface);
      border: 1px solid var(--rule);
      border-radius: 12px;
      width: 100%;
      max-width: 1400px;
      height: 100%;
      max-height: calc(100vh - 72px);
      box-shadow: 0 10px 30px rgba(0,0,0,0.03);
      display: flex;
      flex-direction: column;
      padding: clamp(0.7rem, 1.6vh, 1.4rem) clamp(0.9rem, 2.0vw, 1.8rem);
      position: relative;
      overflow: hidden;
    }

    .slide-header {
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      border-bottom: 1px solid var(--rule);
      padding-bottom: 0.40rem;
      margin-bottom: 0.50rem;
      flex-shrink: 0;
    }

    .slide-title {
      font-family: var(--font-display);
      font-size: clamp(1.2rem, 2.4vw, 1.9rem);
      font-weight: 700;
      color: var(--ink);
      line-height: 1.15;
    }

    .slide-num-badge {
      font-family: var(--font-code);
      font-size: 0.76rem;
      font-weight: 700;
      color: var(--accent-dk);
      background: var(--accent-sf);
      padding: 0.18rem 0.50rem;
      border-radius: 999px;
    }

    .slide-body {
      flex: 1;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      justify-content: flex-start;
      align-items: stretch;
      font-size: calc(clamp(0.92rem, 1.55vw, 1.26rem) * var(--fit-scale, 1));
      line-height: 1.45;
      padding-top: 0.20rem;
    }

    .slide-content-wrapper {
      display: flex;
      flex-direction: column;
      gap: 0.35rem;
      width: 100%;
      height: auto;
    }

    /* Proportional Scalable Bullets */
    .main-bullets { list-style-type: none; padding-left: 0; margin-top: 0.30rem; }
    .primary-bullet {
      font-family: var(--font-display); font-size: 1.14em; font-weight: 700; color: var(--ink);
      margin-top: 0.45em; margin-bottom: 0.18em; display: flex; align-items: baseline; gap: 0.5em;
    }
    .primary-bullet::before {
      content: "◆"; color: var(--accent); font-size: 0.72em; line-height: 1; flex-shrink: 0;
    }
    .sub-bullets {
      list-style-type: none; padding-left: 1.35em; border-left: 2px solid var(--rule);
      margin-left: 0.35em; margin-bottom: 0.45em;
    }
    .sub-bullet {
      font-size: 0.98em; color: var(--ink); margin-bottom: 0.22em; position: relative; padding-left: 1.15em;
      line-height: 1.45;
    }
    .sub-bullet::before {
      content: "›"; position: absolute; left: 0; top: -0.05em; color: var(--accent-dk); font-weight: 900; font-size: 1.25em; line-height: 1;
    }

    /* Tables */
    .slide-table {
      width: 100%; border-collapse: collapse; margin: 0.60rem 0; font-size: 0.90em;
      background: var(--surface); border: 1.5px solid var(--rule); border-radius: 8px; overflow: hidden;
    }
    .slide-table th {
      background: #F0EEE6; color: var(--ink); font-weight: 750; text-align: left;
      padding: 0.55rem 0.85rem; border-bottom: 1.5px solid var(--rule);
    }
    .slide-table td {
      padding: 0.55rem 0.85rem; border-bottom: 1px solid var(--rule); line-height: 1.42;
    }
    .slide-table tr:last-child td { border-bottom: none; }
    .slide-table tr:nth-child(even) td { background: rgba(245, 230, 223, 0.22); }

    /* Code Slide Split Layout */
    .code-slide-container {
      display: grid; grid-template-columns: minmax(0, 1.42fr) minmax(0, 1.05fr);
      gap: 1.15rem; height: 100%; align-items: start;
    }
    .code-editor-window {
      background: var(--code-bg); border-radius: 10px; overflow: hidden;
      border: 1px solid var(--code-rule); box-shadow: 0 4px 16px rgba(0,0,0,0.12);
      display: flex; flex-direction: column; max-height: calc(100vh - 135px);
    }
    .code-editor-header {
      background: #141414; padding: 0.35rem 0.75rem; display: flex; align-items: center;
      gap: 0.70rem; border-bottom: 1px solid #282828; flex-shrink: 0;
    }
    .code-dots { display: flex; gap: 0.30rem; }
    .code-dot { width: 9px; height: 9px; border-radius: 50%; }
    .dot-red { background: #FF5F56; } .dot-yellow { background: #FFBD2E; } .dot-green { background: #27C93F; }
    .code-file-tag { font-family: var(--font-code); font-size: 0.74rem; color: #A0A09A; flex: 1; }
    .code-lang-tag { font-family: var(--font-code); font-size: 0.68rem; background: #2A2A2A; color: var(--accent); padding: 0.10rem 0.40rem; border-radius: 4px; font-weight: 700; }
    .code-block {
      padding: 0.70rem 0.90rem; font-family: var(--font-code); font-size: 0.76rem;
      line-height: 1.38; color: #D4D4D4; overflow-y: auto; flex: 1;
    }
    .code-line-hl { background: rgba(217, 119, 87, 0.20); border-left: 3px solid var(--accent); padding-left: 0.30rem; }

    .code-concepts-column { display: flex; flex-direction: column; gap: 0.60rem; overflow-y: auto; max-height: calc(100vh - 135px); }
    .code-concept-card {
      background: var(--surface); border: 1px solid var(--rule); border-left: 3.5px solid var(--accent);
      border-radius: 8px; padding: 0.65rem 0.90rem;
    }
    .concept-tag { background: var(--accent); color: #FAF9F5; font-size: 0.70rem; font-weight: 750; padding: 0.10rem 0.42rem; border-radius: 4px; font-family: var(--font-code); }
    .concept-card-title { font-weight: 750; font-size: 0.94rem; color: var(--ink); }
    .concept-card-body { font-size: 0.86rem; color: var(--ink); line-height: 1.40; margin-top: 0.20rem; }

    .invariant-card {
      background: #FAF8F2; border: 1.5px solid var(--accent-dk); border-radius: 8px; padding: 0.65rem 0.90rem;
    }
    .invariant-title { font-weight: 800; font-size: 0.90rem; color: var(--accent-dk); margin-bottom: 0.25rem; }

    .progress-bar { height: 3px; background: var(--rule); width: 100%; }
    .progress-fill { height: 100%; background: var(--accent); width: 0%; transition: width 0.3s; }

    .slide-body a { color: var(--accent-dk); font-weight: 650; text-decoration: underline; word-break: break-all; }
    .slide-body a:hover { color: var(--accent); }

    /* Grid View Mode */
    .grid-viewport {
      width: 100%; height: 100%; overflow-y: auto; padding: 1.5rem;
      display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1rem;
    }
    .grid-slide-card {
      background: var(--surface); border: 1px solid var(--rule); border-radius: 10px;
      padding: 1rem; height: 240px; display: flex; flex-direction: column; cursor: pointer;
    }
    .grid-slide-card:hover { border-color: var(--accent); background: var(--accent-sf); }
    .grid-slide-title { font-family: var(--font-display); font-size: 1.05rem; font-weight: 700; margin-bottom: 0.40rem; }
    .grid-slide-body { font-size: 0.80rem; color: var(--ink-muted); overflow: hidden; flex: 1; }
  </style>
</head>
<body>
  <div class="progress-bar"><div class="progress-fill" id="progress-fill"></div></div>
  <header>
    <a href="index.html" class="brand"><span>🏛️</span> {{DECK_TITLE}}</a>
    <div class="nav-controls">
      <select id="slide-select" class="slide-select" onchange="renderSlide(parseInt(this.value))"></select>
      <div class="goto-box">
        <input type="number" id="goto-input" class="goto-input" min="1" max="100" placeholder="1" onkeydown="if(event.key==='Enter') goToSlide()">
        <button id="btn-goto" class="btn-goto" onclick="goToSlide()">Go ➔</button>
      </div>
      <button id="btn-prev" onclick="prevSlide()">‹ Prev</button>
      <button id="btn-next" class="primary" onclick="nextSlide()">Next ›</button>
      <button id="btn-grid" onclick="toggleGridMode()">▦ Grid</button>
      <button id="btn-fullscreen" onclick="toggleFullScreen()">⛶ Fullscreen</button>
    </div>
  </header>

  <main id="main-container">
    <div class="slide-viewport">
      <div class="slide-card">
        <div class="slide-header">
          <div class="slide-title" id="slide-title">Loading presentation...</div>
          <div class="slide-num-badge" id="slide-num-badge">Slide 1 of 1</div>
        </div>
        <div class="slide-body" id="slide-body"></div>
      </div>
    </div>
  </main>

  <script>
    const slidesData = {{SLIDES_JSON}};
    let currentIdx = 0;
    let isGridMode = false;
    const bodyEl = document.getElementById('slide-body');
    const selectEl = document.getElementById('slide-select');

    slidesData.forEach((s, idx) => {
      const opt = document.createElement('option');
      opt.value = idx;
      const title = s.raw_lines && s.raw_lines[0] ? s.raw_lines[0] : `Slide ${s.number}`;
      opt.innerText = `Slide ${s.number}: ${title}`;
      selectEl.appendChild(opt);
    });

    function cleanNumbers(text) {
      if (/^\\d{1,2}:\\d{2}/.test(text.trim())) return text.trim();
      text = text.replace(/^(\\d+[\\.\\)\\:]|\\d+\\s*&\\s*\\d+[\\.\\)\\:])\\s+/, '');
      text = text.replace(/^(Pillar|Layer|Step|Phase|Check)\\s*\\d+[\\.\\)\\:]?\\s+/i, '');
      return text.trim();
    }

    function formatText(text) {
      text = text.replace(/(https?:\\/\\/[^\\s<>"']+)/g, '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>');
      text = text.replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>');
      text = text.replace(/`([^`]+)`/g, '<code>$1</code>');
      return text;
    }

    function renderMarkdownTable(tableLines) {
      const rows = tableLines.filter(l => l.trim().startsWith('|')).map(l => {
        return l.trim().slice(1, -1).split('|').map(c => c.trim());
      });
      if (rows.length < 2) return '';
      const headers = rows[0];
      const dataRows = rows.slice(1).filter(r => !r.every(c => c.match(/^[\\-\\:\\s]+$/)));
      let html = '<table class="slide-table"><thead><tr>';
      headers.forEach(h => { html += `<th>${formatText(h)}</th>`; });
      html += '</tr></thead><tbody>';
      dataRows.forEach(row => {
        html += '<tr>';
        row.forEach(cell => { html += `<td>${formatText(cell)}</td>`; });
        html += '</tr>';
      });
      html += '</tbody></table>';
      return html;
    }

    function formatBullets(lines) {
      const isTable = lines.some(l => l.trim().startsWith('|'));
      if (isTable) {
        const tableLines = lines.filter(l => l.trim().startsWith('|'));
        const otherLines = lines.filter(l => !l.trim().startsWith('|'));
        let h = '';
        if (otherLines.length > 0) h += formatBullets(otherLines);
        if (tableLines.length > 0) h += renderMarkdownTable(tableLines);
        return h;
      }
      let html = '<ul class="main-bullets">';
      lines.forEach(l => {
        const clean = cleanNumbers(l.replace(/^[•\\-\\u2022]\\s*/, ''));
        html += `<li class="primary-bullet">${formatText(clean)}</li>`;
      });
      html += '</ul>';
      return html;
    }

    function renderSlide(idx) {
      if (idx < 0 || idx >= slidesData.length) return;
      currentIdx = idx;
      const slide = slidesData[idx];
      selectEl.value = idx;
      document.getElementById('goto-input').value = idx + 1;
      document.getElementById('slide-title').innerText = slide.raw_lines[0] || `Slide ${slide.number}`;
      document.getElementById('slide-num-badge').innerText = `Slide ${slide.number} of ${slidesData.length}`;
      document.getElementById('btn-prev').disabled = (idx === 0);
      document.getElementById('btn-next').disabled = (idx === slidesData.length - 1);

      let bodyHtml = '<div id="slide-content-wrap" class="slide-content-wrapper">';
      const restLines = slide.raw_lines ? slide.raw_lines.slice(1) : [];
      if (restLines.length > 0) {
        bodyHtml += formatBullets(restLines);
      }
      bodyHtml += '</div>';
      bodyEl.innerHTML = bodyHtml;

      // Dynamic Auto-Fit Scaling
      bodyEl.style.setProperty('--fit-scale', '1.0');
      const wrapper = document.getElementById('slide-content-wrap') || bodyEl;
      const clientH = bodyEl.clientHeight;
      const targetH = clientH * 0.90;
      let scale = 1.0;
      let growIter = 0;
      while (wrapper.offsetHeight < targetH && bodyEl.scrollHeight <= clientH && scale < 3.25 && growIter < 45) {
        scale += 0.05;
        bodyEl.style.setProperty('--fit-scale', scale.toFixed(2));
        growIter++;
      }
      let shrinkIter = 0;
      while ((bodyEl.scrollHeight > clientH || wrapper.offsetHeight > (clientH - 6)) && scale > 0.50 && shrinkIter < 60) {
        scale -= 0.02;
        bodyEl.style.setProperty('--fit-scale', scale.toFixed(2));
        shrinkIter++;
      }

      const pct = ((idx + 1) / slidesData.length) * 100;
      document.getElementById('progress-fill').style.width = pct + '%';
    }

    function nextSlide() { if (currentIdx < slidesData.length - 1) renderSlide(currentIdx + 1); }
    function prevSlide() { if (currentIdx > 0) renderSlide(currentIdx - 1); }
    function goToSlide() {
      const val = parseInt(document.getElementById('goto-input').value, 10);
      if (!isNaN(val) && val >= 1 && val <= slidesData.length) renderSlide(val - 1);
    }
    function toggleFullScreen() {
      if (!document.fullscreenElement) document.documentElement.requestFullscreen();
      else if (document.exitFullscreen) document.exitFullscreen();
    }
    function toggleGridMode() {
      isGridMode = !isGridMode;
      const main = document.getElementById('main-container');
      if (isGridMode) {
        let gridHtml = '<div class="grid-viewport">';
        slidesData.forEach((s, idx) => {
          gridHtml += `
            <div class="grid-slide-card" onclick="isGridMode=false; toggleGridMode(); renderSlide(${idx});">
              <div class="grid-slide-title">${s.number}. ${s.raw_lines[0] || 'Slide'}</div>
              <div class="grid-slide-body">${s.raw_lines.slice(1).join('<br>')}</div>
            </div>
          `;
        });
        gridHtml += '</div>';
        main.innerHTML = gridHtml;
      } else {
        main.innerHTML = `
          <div class="slide-viewport">
            <div class="slide-card">
              <div class="slide-header">
                <div class="slide-title" id="slide-title"></div>
                <div class="slide-num-badge" id="slide-num-badge"></div>
              </div>
              <div class="slide-body" id="slide-body"></div>
            </div>
          </div>
        `;
        renderSlide(currentIdx);
      }
    }

    window.addEventListener('keydown', (e) => {
      if (['INPUT', 'SELECT'].includes(e.target.tagName)) return;
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') { e.preventDefault(); nextSlide(); }
      else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); prevSlide(); }
      else if (e.key === 'g' || e.key === 'G') { e.preventDefault(); document.getElementById('goto-input').focus(); }
      else if (e.key === 'm' || e.key === 'M') { e.preventDefault(); toggleGridMode(); }
      else if (e.key === 'f' || e.key === 'F') { e.preventDefault(); toggleFullScreen(); }
    });

    // Initialize presentation
    renderSlide(0);
  </script>
</body>
</html>
"""

def build_presentation(data_path: str, output_path: str, title: str = "Presentation Slide Deck"):
    with open(data_path, "r", encoding="utf-8") as f:
        slides = json.load(f)

    html_content = HTML_TEMPLATE.replace("{{DECK_TITLE}}", title)
    html_content = html_content.replace("{{SLIDES_JSON}}", json.dumps(slides, ensure_ascii=False))

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"[SUCCESS] Compiled {len(slides)} slides into: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build GitHub Pages HTML Slide Deck")
    parser.add_argument("--data", default="harness_course_presentation/slides_data.json", help="Path to slides JSON data")
    parser.add_argument("--out", default="docs/slides.html", help="Path to output HTML file")
    parser.add_argument("--title", default="Harness Engineering Masterclass", help="Presentation title")
    args = parser.parse_args()

    build_presentation(args.data, args.out, args.title)
