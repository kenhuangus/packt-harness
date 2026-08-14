import json
import re
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(ROOT_DIR, 'harness_course_presentation', 'slides_data.json')
with open(data_path, 'r', encoding='utf-8') as f:
    slides = json.load(f)

# Helper function to generate dynamic themed SVGs for any slide number
def generate_svg_for_slide(num, title):
    if num == 1:
        return '''<svg viewBox="0 0 800 180" style="width:100%; max-height:180px; margin:0.75rem 0;">
  <rect x="20" y="30" width="220" height="130" rx="16" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
  <text x="130" y="75" fill="#141413" font-family="Inter" font-size="16" font-weight="800" text-anchor="middle">Probabilistic LLM</text>
  <text x="130" y="100" fill="#6B6B63" font-family="Inter" font-size="12" text-anchor="middle">Token Proposals &amp; Reasoner</text>
  <text x="130" y="125" fill="#141413" font-family="Inter" font-size="11" text-anchor="middle">⚠ Hallucination Traps</text>
  <path d="M240 95 L340 95" stroke="#D97757" stroke-width="4" stroke-dasharray="6 4"/>
  <text x="290" y="85" fill="#141413" font-family="Inter" font-size="11" font-weight="700" text-anchor="middle">Proposals</text>
  <rect x="350" y="15" width="430" height="160" rx="16" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2.5"/>
  <text x="565" y="45" fill="#141413" font-family="Inter" font-size="16" font-weight="800" text-anchor="middle">Deterministic Harness Scaffolding</text>
  <rect x="370" y="65" width="115" height="45" rx="8" fill="#F0EEE6" stroke="#E3E0D6"/>
  <text x="427" y="87" fill="#141413" font-family="Inter" font-size="11" font-weight="700" text-anchor="middle">Memory</text>
  <rect x="500" y="65" width="115" height="45" rx="8" fill="#F0EEE6" stroke="#E3E0D6"/>
  <text x="557" y="87" fill="#141413" font-family="Inter" font-size="11" font-weight="700" text-anchor="middle">Sandbox</text>
  <rect x="630" y="65" width="135" height="45" rx="8" fill="#F0EEE6" stroke="#E3E0D6"/>
  <text x="697" y="87" fill="#141413" font-family="Inter" font-size="11" font-weight="700" text-anchor="middle">Hooks &amp; AST</text>
  <rect x="435" y="120" width="120" height="40" rx="8" fill="#F0EEE6" stroke="#E3E0D6"/>
  <text x="495" y="145" fill="#141413" font-family="Inter" font-size="11" font-weight="700" text-anchor="middle">TDA Pytest</text>
  <rect x="570" y="120" width="120" height="40" rx="8" fill="#F0EEE6" stroke="#E3E0D6"/>
  <text x="630" y="145" fill="#141413" font-family="Inter" font-size="11" font-weight="700" text-anchor="middle">JSONL Logs</text>
</svg>'''
    elif num in [3, 9, 15, 22, 30, 32, 38, 46, 54, 59]:
        mod_map = {3:1, 9:2, 15:3, 22:4, 30:5, 32:6, 38:7, 46:8, 54:9, 59:10}
        m_num = mod_map.get(num, 1)
        return f'''<svg viewBox="0 0 800 110" style="width:100%; max-height:110px; margin:0.5rem 0;">
  <rect x="20" y="10" width="760" height="90" rx="14" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
  <circle cx="70" cy="55" r="26" fill="#F5E6DF" stroke="#D97757" stroke-width="2"/>
  <text x="70" y="63" fill="#141413" font-family="Inter" font-size="17" font-weight="900" text-anchor="middle">M{m_num}</text>
  <text x="120" y="48" fill="#141413" font-family="Inter" font-size="16" font-weight="800">MODULE {m_num} OBJECTIVES &amp; SPECIFICATION</text>
  <text x="120" y="74" fill="#6B6B63" font-family="Inter" font-size="12">Verified Production Implementation in course_implementation/ | Harness Systems Architecture</text>
</svg>'''
    elif num == 2:
        return '''<svg viewBox="0 0 800 130" style="width:100%; max-height:130px; margin:0.5rem 0;">
  <rect x="20" y="10" width="360" height="110" rx="12" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
  <text x="200" y="42" fill="#141413" font-family="Inter" font-size="14" font-weight="800" text-anchor="middle">PART 1: FOUNDATIONS &amp; CONTROL</text>
  <text x="200" y="67" fill="#6B6B63" font-family="Inter" font-size="11" text-anchor="middle">09:00 AM - 10:20 AM</text>
  <text x="200" y="92" fill="#141413" font-family="Inter" font-size="11" text-anchor="middle">Modules 1–5: Foundations, Control &amp; Break</text>
  <path d="M380 65 L420 65" stroke="#BD5D3A" stroke-width="3" stroke-dasharray="4 4"/>
  <rect x="420" y="10" width="360" height="110" rx="12" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
  <text x="600" y="42" fill="#141413" font-family="Inter" font-size="14" font-weight="800" text-anchor="middle">PART 2: RELIABILITY &amp; TEAMS</text>
  <text x="600" y="67" fill="#6B6B63" font-family="Inter" font-size="11" text-anchor="middle">10:20 AM - 11:30 AM</text>
  <text x="600" y="95" fill="#141413" font-family="Inter" font-size="11" text-anchor="middle">Modules 6–10: TDA, MCP &amp; Multi-Agent Teams</text>
</svg>'''
    elif num == 10:
        return '''<svg viewBox="0 0 800 120" style="width:100%; max-height:120px; margin:0.5rem 0;">
  <g transform="translate(10, 5)">
    <rect x="0" y="0" width="140" height="105" rx="10" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <circle cx="70" cy="30" r="16" fill="#F5E6DF" stroke="#D97757"/>
    <text x="70" y="35" fill="#141413" font-family="Inter" font-size="13" font-weight="800" text-anchor="middle">P1</text>
    <text x="70" y="65" fill="#141413" font-family="Inter" font-size="11" font-weight="700" text-anchor="middle">Memory Files</text>
    <text x="70" y="85" fill="#6B6B63" font-family="Inter" font-size="10" text-anchor="middle">CLAUDE/AGENTS</text>
  </g>
  <g transform="translate(170, 5)">
    <rect x="0" y="0" width="140" height="105" rx="10" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <circle cx="70" cy="30" r="16" fill="#F5E6DF" stroke="#BD5D3A"/>
    <text x="70" y="35" fill="#141413" font-family="Inter" font-size="13" font-weight="800" text-anchor="middle">P2</text>
    <text x="70" y="65" fill="#141413" font-family="Inter" font-size="11" font-weight="700" text-anchor="middle">Scoped Tools</text>
    <text x="70" y="85" fill="#6B6B63" font-family="Inter" font-size="10" text-anchor="middle">Path Sandbox</text>
  </g>
  <g transform="translate(330, 5)">
    <rect x="0" y="0" width="140" height="105" rx="10" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <circle cx="70" cy="30" r="16" fill="#F5E6DF" stroke="#BD5D3A"/>
    <text x="70" y="35" fill="#141413" font-family="Inter" font-size="13" font-weight="800" text-anchor="middle">P3</text>
    <text x="70" y="65" fill="#141413" font-family="Inter" font-size="11" font-weight="700" text-anchor="middle">Hooks &amp; AST</text>
    <text x="70" y="85" fill="#6B6B63" font-family="Inter" font-size="10" text-anchor="middle">Pre/Post Tool Hooks</text>
  </g>
  <g transform="translate(490, 5)">
    <rect x="0" y="0" width="140" height="105" rx="10" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <circle cx="70" cy="30" r="16" fill="#F5E6DF" stroke="#BD5D3A"/>
    <text x="70" y="35" fill="#141413" font-family="Inter" font-size="13" font-weight="800" text-anchor="middle">P4</text>
    <text x="70" y="65" fill="#141413" font-family="Inter" font-size="11" font-weight="700" text-anchor="middle">Testing Loop</text>
    <text x="70" y="85" fill="#6B6B63" font-family="Inter" font-size="10" text-anchor="middle">Pytest Traceback</text>
  </g>
  <g transform="translate(650, 5)">
    <rect x="0" y="0" width="140" height="105" rx="10" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <circle cx="70" cy="30" r="16" fill="#F5E6DF" stroke="#BD5D3A"/>
    <text x="70" y="35" fill="#141413" font-family="Inter" font-size="13" font-weight="800" text-anchor="middle">P5</text>
    <text x="70" y="65" fill="#141413" font-family="Inter" font-size="11" font-weight="700" text-anchor="middle">JSONL Tracing</text>
    <text x="70" y="85" fill="#6B6B63" font-family="Inter" font-size="10" text-anchor="middle">Audit Logs</text>
  </g>
</svg>'''
    elif num == 23:
        return '''<svg viewBox="0 0 800 150" style="width:100%; max-height:150px; margin:0.5rem 0;">
  <rect x="40" y="5" width="720" height="26" rx="6" fill="#F0EEE6" stroke="#D97757" stroke-width="2"/>
  <text x="60" y="22" fill="#141413" font-family="Inter" font-size="11" font-weight="800">System Prompt Rules</text>
  <text x="340" y="22" fill="#6B6B63" font-family="Inter" font-size="10">CLAUDE.md / AGENTS.md Guidelines</text>
  <rect x="40" y="36" width="720" height="26" rx="6" fill="#F0EEE6" stroke="#BD5D3A" stroke-width="2"/>
  <text x="60" y="53" fill="#141413" font-family="Inter" font-size="11" font-weight="800">Tool Schemas</text>
  <text x="340" y="53" fill="#6B6B63" font-family="Inter" font-size="10">JSON Schema Validation &amp; Argument Typing</text>
  <rect x="40" y="67" width="720" height="26" rx="6" fill="#F0EEE6" stroke="#D97757" stroke-width="2"/>
  <text x="60" y="84" fill="#141413" font-family="Inter" font-size="11" font-weight="800">Interceptors &amp; Hooks</text>
  <text x="340" y="84" fill="#6B6B63" font-family="Inter" font-size="10">PreToolUse shell guard &amp; PostToolUse AST linters</text>
  <rect x="40" y="98" width="720" height="26" rx="6" fill="#F0EEE6" stroke="#D97757" stroke-width="2"/>
  <text x="60" y="115" fill="#141413" font-family="Inter" font-size="11" font-weight="800">OS Sandboxing</text>
  <text x="340" y="115" fill="#6B6B63" font-family="Inter" font-size="10">Path Isolation &amp; Chroot Workspace Boundary</text>
</svg>'''
    elif num == 27:
        return '''<svg viewBox="0 0 800 120" style="width:100%; max-height:120px; margin:0.5rem 0;">
  <g transform="translate(20, 10)">
    <rect x="0" y="0" width="170" height="95" rx="10" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="85" y="35" fill="#141413" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">READ ONLY</text>
    <text x="85" y="57" fill="#6B6B63" font-family="Inter" font-size="10" text-anchor="middle">plan</text>
    <text x="85" y="77" fill="#6B6B63" font-family="Inter" font-size="10" font-weight="700" text-anchor="middle">NO MUTATIONS</text>
  </g>
  <g transform="translate(210, 10)">
    <rect x="0" y="0" width="170" height="95" rx="10" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <text x="85" y="35" fill="#141413" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">REVIEWED</text>
    <text x="85" y="57" fill="#6B6B63" font-family="Inter" font-size="10" text-anchor="middle">default / acceptEdits</text>
    <text x="85" y="77" fill="#141413" font-family="Inter" font-size="10" font-weight="700" text-anchor="middle">ALLOW · ASK · DENY</text>
  </g>
  <g transform="translate(400, 10)">
    <rect x="0" y="0" width="170" height="95" rx="10" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <text x="85" y="35" fill="#141413" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">AUTOMATION</text>
    <text x="85" y="57" fill="#6B6B63" font-family="Inter" font-size="10" text-anchor="middle">auto / dontAsk</text>
    <text x="85" y="77" fill="#141413" font-family="Inter" font-size="9" font-weight="700" text-anchor="middle">SAFETY OR ALLOWLIST</text>
  </g>
  <g transform="translate(590, 10)">
    <rect x="0" y="0" width="190" height="95" rx="10" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <text x="95" y="35" fill="#141413" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">ISOLATED ONLY</text>
    <text x="95" y="57" fill="#6B6B63" font-family="Inter" font-size="10" text-anchor="middle">bypassPermissions</text>
    <text x="95" y="77" fill="#141413" font-family="Inter" font-size="9" font-weight="700" text-anchor="middle">SKIPS PERMISSION LAYER</text>
  </g>
</svg>'''
    elif num == 33:
        return '''<svg viewBox="0 0 800 120" style="width:100%; max-height:120px; margin:0.5rem 0;">
  <rect x="30" y="10" width="160" height="90" rx="10" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
  <text x="110" y="40" fill="#141413" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">Failing Test</text>
  <text x="110" y="65" fill="#6B6B63" font-family="Inter" font-size="10" text-anchor="middle">From SPEC.md</text>
  <path d="M190 55 L230 55" stroke="#BD5D3A" stroke-width="3"/>
  <rect x="230" y="10" width="160" height="90" rx="10" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
  <text x="310" y="40" fill="#141413" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">Agent Edit</text>
  <text x="310" y="65" fill="#6B6B63" font-family="Inter" font-size="10" text-anchor="middle">Code Proposal</text>
  <path d="M390 55 L430 55" stroke="#D97757" stroke-width="3"/>
  <rect x="430" y="10" width="160" height="90" rx="10" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
  <text x="510" y="40" fill="#141413" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">Pytest Runner</text>
  <text x="510" y="65" fill="#6B6B63" font-family="Inter" font-size="10" text-anchor="middle">Capture Traceback</text>
  <path d="M590 55 L630 55" stroke="#BD5D3A" stroke-width="3"/>
  <rect x="630" y="10" width="140" height="90" rx="10" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
  <text x="700" y="40" fill="#141413" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">Repair Prompt</text>
  <text x="700" y="65" fill="#6B6B63" font-family="Inter" font-size="10" text-anchor="middle">Auto Feedback</text>
</svg>'''
    elif num == 55:
        return '''<svg viewBox="0 0 800 110" style="width:100%; max-height:110px; margin:0.5rem 0;">
  <g transform="translate(15, 10)">
    <rect x="0" y="0" width="140" height="85" rx="10" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="70" y="38" fill="#141413" font-family="Inter" font-size="11" font-weight="800" text-anchor="middle">Spec First</text>
    <text x="70" y="58" fill="#6B6B63" font-family="Inter" font-size="10" text-anchor="middle">Validate SPEC.md</text>
  </g>
  <g transform="translate(170, 10)">
    <rect x="0" y="0" width="140" height="85" rx="10" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <text x="70" y="38" fill="#141413" font-family="Inter" font-size="11" font-weight="800" text-anchor="middle">Sandbox</text>
    <text x="70" y="58" fill="#6B6B63" font-family="Inter" font-size="10" text-anchor="middle">Scoped Execution</text>
  </g>
  <g transform="translate(325, 10)">
    <rect x="0" y="0" width="140" height="85" rx="10" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="70" y="38" fill="#141413" font-family="Inter" font-size="11" font-weight="800" text-anchor="middle">Hooks</text>
    <text x="70" y="58" fill="#6B6B63" font-family="Inter" font-size="10" text-anchor="middle">Pre/Post Hooks</text>
  </g>
  <g transform="translate(480, 10)">
    <rect x="0" y="0" width="140" height="85" rx="10" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <text x="70" y="38" fill="#141413" font-family="Inter" font-size="11" font-weight="800" text-anchor="middle">Tests</text>
    <text x="70" y="58" fill="#6B6B63" font-family="Inter" font-size="10" text-anchor="middle">Pytest Runner</text>
  </g>
  <g transform="translate(635, 10)">
    <rect x="0" y="0" width="150" height="85" rx="10" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="75" y="38" fill="#141413" font-family="Inter" font-size="11" font-weight="800" text-anchor="middle">Human Review</text>
    <text x="75" y="58" fill="#6B6B63" font-family="Inter" font-size="10" text-anchor="middle">PR Sanity Merge</text>
  </g>
</svg>'''
    elif num == 61:
        return '''<svg viewBox="0 0 800 110" style="width:100%; max-height:110px; margin:0.5rem 0;">
  <rect x="40" y="10" width="720" height="90" rx="14" fill="#FAF9F5" stroke="#D97757" stroke-width="2.5"/>
  <text x="400" y="38" fill="#141413" font-family="Inter" font-size="15" font-weight="900" text-anchor="middle">PRODUCTION READINESS SCORECARD: 100% PASS</text>
  <text x="400" y="60" fill="#141413" font-family="Inter" font-size="11" text-anchor="middle">✓ Memory (AGENTS.md)  ✓ Sandboxing  ✓ PreToolUse  ✓ TDA Loop  ✓ MCP Governance</text>
  <text x="400" y="80" fill="#6B6B63" font-family="Inter" font-size="10" text-anchor="middle">Verified Harness Engineering Control &amp; Reliability Framework</text>
</svg>'''
    else:
        # ponytail: no generic placeholder diagram. Slides without a bespoke
        # SVG render as clean text-only; the old scaffold repeated the same
        # "INPUT CONTEXT / VERIFIED / 100% Pass Rate" graphic on ~44 slides.
        return ''

svg_all_63 = {}
for s in slides:
    num = s['number']
    title = s['raw_lines'][0] if s['raw_lines'] else f'Slide {num}'
    svg_all_63[num] = generate_svg_for_slide(num, title)

svg_json = json.dumps(svg_all_63)

html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Packt Masterclass Presentation: 63 Interactive HTML Slides</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #F0EEE6;
      --surface: #FAF9F5;
      --ink: #141413;
      --ink-muted: #6B6B63;
      --rule: #E3E0D6;
      --accent: #D97757;
      --accent-dk: #BD5D3A;
      --accent-sf: #F5E6DF;
      --font-display: ui-serif, Georgia, "Times New Roman", serif;
      --font-body: -apple-system, "Segoe UI", Inter, system-ui, sans-serif;
      --font-code: ui-monospace, "JetBrains Mono", Menlo, monospace;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: var(--font-body);
      background: var(--bg);
      color: var(--ink);
      height: 100vh;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }

    header {
      height: 54px;
      flex: 0 0 54px;
      background: var(--surface);
      border-bottom: 1px solid var(--rule);
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0 1.5rem;
      z-index: 50;
      gap: 1rem;
      overflow-x: auto;
    }
    .header-left { display: flex; align-items: center; gap: 0.8rem; flex: 0 0 auto; }
    .brand-logo {
      width: 36px; height: 36px;
      background: var(--accent-sf); color: var(--ink); border: 1px solid var(--rule);
      border-radius: 10px; font-weight: 800; display: flex; align-items: center; justify-content: center;
    }
    .brand-title { font-weight: 650; font-size: 1rem; white-space: nowrap; }

    .controls { display: flex; align-items: center; gap: 0.55rem; flex: 0 0 auto; }
    .btn {
      background: var(--surface); border: 1px solid var(--rule); color: var(--ink);
      padding: 0.46rem 0.82rem; border-radius: 10px; font-weight: 600; font-size: 0.82rem;
      cursor: pointer; transition: background-color 0.16s, border-color 0.16s; text-decoration: none;
      white-space: nowrap;
    }
    .btn:hover { background: var(--accent-sf); border-color: var(--accent); }
    .btn:focus-visible, .slide-select:focus-visible { outline: 2px solid var(--accent-dk); outline-offset: 2px; }
    .btn-primary { background: var(--accent); border-color: var(--accent); color: var(--ink); }
    .btn-primary:hover { background: var(--accent-sf); border-color: var(--accent-dk); color: var(--ink); }
    
    select.slide-select {
      background: var(--surface); color: var(--ink); border: 1px solid var(--rule);
      padding: 0.45rem 0.7rem; border-radius: 10px; font-family: var(--font-body);
      font-size: 0.82rem; font-weight: 600;
      max-width: 320px;
    }

    main {
      flex: 1;
      position: relative;
      overflow: hidden;
    }

    .slide-viewport {
      width: 100%; height: 100%;
      display: flex; justify-content: center; align-items: center;
      padding: clamp(0.45rem, 1.2vw, 0.9rem);
    }
    .slide-card {
      width: 100%; max-width: 1360px; height: 100%; max-height: none;
      background: var(--surface); border: 1px solid var(--rule);
      border-radius: 12px; padding: clamp(1.1rem, 2.2vw, 1.8rem); display: flex; flex-direction: column;
      position: relative;
    }
    .slide-header {
      display: flex; justify-content: space-between; align-items: center;
      gap: 1.25rem; margin-bottom: 0.7rem; border-bottom: 1px solid var(--rule); padding-bottom: 0.7rem;
    }
    .slide-title {
      min-width: 0; font-family: var(--font-display); font-size: clamp(1.85rem, 3.4vw, 2.55rem);
      font-weight: 650; line-height: 1.08; letter-spacing: -0.02em; color: var(--ink);
    }
    .slide-num-badge {
      background: var(--accent-sf); color: var(--ink); border: 1px solid var(--rule);
      padding: 0.32rem 0.78rem; border-radius: 9999px; font-size: 0.8rem; font-weight: 750; white-space: nowrap;
    }
    .slide-body {
      --fit-scale: 1;
      --slide-body-base-size: 1.42rem;
      flex: 1; min-height: 0; overflow: hidden; padding-right: 0.35rem;
      font-size: calc(var(--slide-body-base-size) * var(--fit-scale));
      color: var(--ink); line-height: 1.38;
    }
    .slide-body > svg {
      display: block; width: 100% !important; height: auto; max-width: 100%;
      max-height: min(12vh, 110px) !important;
    }

    /* Visual Hierarchy: Parent vs Sub Bullets (NO NUMBERS) */
    .main-bullets { list-style-type: none; padding-left: 0; margin-top: 0.35rem; }
    .main-bullets.dense-columns {
      column-count: 2; column-gap: clamp(1.5rem, 4vw, 3rem); column-fill: balance;
    }
    .bullet-group, .primary-bullet, .sub-bullets, .sub-bullet {
      break-inside: avoid; page-break-inside: avoid;
    }
    .primary-bullet {
      font-family: var(--font-display); font-size: 1.18em; font-weight: 700; color: var(--ink);
      margin-top: 0.62em; margin-bottom: 0.22em; display: flex; align-items: center; gap: 0.55em;
    }
    .primary-bullet::before {
      content: "◆"; color: var(--accent); font-size: 0.68rem;
    }
    .sub-bullets {
      list-style-type: none; padding-left: 1.35em; border-left: 1px solid var(--rule);
      margin-left: 0.32em; margin-bottom: 0.7em;
    }
    .sub-bullet {
      font-size: 1.02em; color: var(--ink); margin-bottom: 0.28em; position: relative; padding-left: 1em;
    }
    .sub-bullet::before {
      content: "›"; position: absolute; left: 0; color: var(--accent-dk); font-weight: 800; font-size: 1.1rem; line-height: 1;
    }
    .slide-body a {
      color: var(--accent-dk);
      font-weight: 650;
      text-decoration: underline;
      word-break: break-all;
    }
    .slide-body a:hover { color: var(--accent); }

    code {
      background: var(--accent-sf); border: 1px solid var(--rule);
      color: var(--ink); padding: 0.12rem 0.38rem; border-radius: 6px;
      font-family: var(--font-code); font-size: 0.86em; font-weight: 600;
      overflow-wrap: anywhere;
    }

    .grid-viewport {
      width: 100%; height: 100%; overflow-y: auto; padding: clamp(1rem, 3vw, 2rem);
      display: grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr)); gap: 1rem;
    }
    .grid-slide-card {
      background: var(--surface); border: 1px solid var(--rule);
      border-radius: 12px; padding: 1.35rem; height: 290px; display: flex; flex-direction: column;
      cursor: pointer; transition: border-color 0.16s, background-color 0.16s;
    }
    .grid-slide-card:hover { background: var(--accent-sf); border-color: var(--accent); }
    .grid-slide-title {
      font-family: var(--font-display); font-size: 1.2rem; line-height: 1.15;
      font-weight: 650; margin-bottom: 0.6rem; color: var(--ink);
    }
    .grid-slide-body { flex: 1; overflow: hidden; font-size: 0.85rem; line-height: 1.5; color: var(--ink-muted); }

    .progress-bar { height: 3px; background: var(--rule); width: 100%; }
    .progress-fill { height: 100%; background: var(--accent); width: 0%; transition: width 0.3s; }

    @media (max-width: 980px) {
      header { padding: 0 0.8rem; }
      .brand-title { display: none; }
      select.slide-select { max-width: 210px; }
    }
    @media (max-height: 760px) {
      .slide-card { padding: 0.95rem 1.2rem; }
      .primary-bullet { margin-top: 0.48rem; }
      .slide-body { --slide-body-base-size: 1.28rem; line-height: 1.34; }
    }
  </style>
</head>
<body>

  <header>
    <div class="header-left">
      <div class="brand-logo">HE</div>
      <div class="brand-title">Harness Engineering Presentation Slides</div>
    </div>
    <div class="controls">
      <a href="index.html" class="btn">🏠 Home Site</a>
      <button class="btn" onclick="toggleMode()"><span id="mode-icon">📜</span> <span id="mode-text">Grid View</span></button>
      <button class="btn" onclick="prevSlide()">❮ Prev</button>
      <select id="slide-select" class="slide-select" onchange="goToSlide(this.value)"></select>
      <button class="btn" onclick="nextSlide()">Next ❯</button>
      <button class="btn btn-primary" onclick="toggleFullscreen()">⛶ Fullscreen</button>
    </div>
  </header>

  <div class="progress-bar"><div id="progress-fill" class="progress-fill"></div></div>

  <main>
    <div id="presentation-mode" class="slide-viewport">
      <div class="slide-card">
        <div class="slide-header">
          <div id="slide-title" class="slide-title">Slide Title</div>
          <div id="slide-num-badge" class="slide-num-badge">Slide 1 / 63</div>
        </div>
        <div id="slide-body" class="slide-body"></div>
      </div>
    </div>

    <div id="grid-mode" class="grid-viewport" style="display:none;"></div>
  </main>

  <script>
    const slidesData = ''' + json.dumps(slides) + ''';
    const svgMap = ''' + svg_json + ''';

    let currentIdx = 0;
    let isGridMode = false;
    let fitSequence = 0;
    let resizeTimer = null;

    const DENSE_BULLET_MIN_LINES = 10;
    const FIT_MIN = 0.90;
    const FIT_STEP = 0.02;
    const FIT_MAX_ITERATIONS = 10;
    const bodyEl = document.getElementById('slide-body');

    const selectEl = document.getElementById('slide-select');
    slidesData.forEach((s, idx) => {
      const opt = document.createElement('option');
      opt.value = idx;
      opt.innerText = `Slide ${s.number}: ${s.raw_lines[0] || 'Slide'}`;
      selectEl.appendChild(opt);
    });

    function cleanNumbers(text) {
      // A leading clock time is not list numbering: keep "09:00 AM - 11:30 AM" intact.
      if (/^\\d{1,2}:\\d{2}/.test(text.trim())) return text.trim();
      text = text.replace(/^(\\d+[\\.\\)\\:]|\\d+\\s*&\\s*\\d+[\\.\\)\\:])\\s*/, '');
      text = text.replace(/^(Pillar|Layer|Step|Phase|Check)\\s*\\d+[\\.\\)\\:]?\\s*/i, '');
      return text.trim();
    }

    function formatTextWithCode(text) {
      const keywords = ['CLAUDE.md', 'AGENTS.md', 'SPEC.md', 'pytest', 'events.jsonl', 'telemetry.jsonl', 'rm -rf', 'write_file', 'read_file', '.claude-plugin/plugin.json', 'SKILL.md', 'mcp_client_runner.py', 'mcp_server_demo.py', 'core_harness_stack.py', 'guardrails_engine.py', 'spec_driven_verifier.py', 'tda_reliability_pipeline.py', 'multi_agent_team_simulator.py', 'five_step_sop_pipeline.py', 'production_harness_audit.py'];
      keywords.forEach(kw => {
        text = text.replaceAll(kw, `<code>${kw}</code>`);
      });
      return text.replace(
        /(https:\\/\\/[^\\s<]+)/g,
        '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>'
      );
    }

    function formatBullets(lines) {
      if (!lines || lines.length === 0) return '';
      const populatedLines = lines.filter(line => line.trim());
      const denseClass = populatedLines.length >= DENSE_BULLET_MIN_LINES ? ' dense-columns' : '';
      let html = `<ul class="main-bullets${denseClass}">`;
      let groupOpen = false;
      let subListOpen = false;

      populatedLines.forEach(line => {
        const trimmed = line.trim();
        const isSub = trimmed.startsWith('•') || trimmed.startsWith('-') || trimmed.startsWith('\ufffd');
        let cleanText = trimmed.replace(/^[•\-\ufffd]\s*/, '').trim();
        cleanText = cleanNumbers(cleanText);
        const labUrl = cleanText.match(/^Lab demo:\\s*(https:\\/\\/[^\\s]+)/i);
        if (labUrl) {
          cleanText = `<a href="${labUrl[1]}" target="_blank" rel="noopener noreferrer">Lab demo: open this module README</a>`;
        } else {
          cleanText = formatTextWithCode(cleanText);
        }

        if (!cleanText) return;

        if (isSub) {
          if (!groupOpen) {
            html += '<li class="bullet-group">';
            groupOpen = true;
          }
          if (!subListOpen) {
            html += '<ul class="sub-bullets">';
            subListOpen = true;
          }
          html += `<li class="sub-bullet">${cleanText}</li>`;
        } else {
          if (subListOpen) {
            html += '</ul>';
            subListOpen = false;
          }
          if (groupOpen) html += '</li>';
          html += `<li class="bullet-group"><div class="primary-bullet">${cleanText}</div>`;
          groupOpen = true;
        }
      });

      if (subListOpen) html += '</ul>';
      if (groupOpen) html += '</li>';
      html += '</ul>';
      return html;
    }

    function bodyOverflows() {
      return bodyEl.scrollHeight > bodyEl.clientHeight + 1 ||
             bodyEl.scrollWidth > bodyEl.clientWidth + 1;
    }

    function fitSlideBody() {
      if (isGridMode || bodyEl.clientHeight === 0) return;

      let scale = 1;
      let iterations = 0;
      bodyEl.style.setProperty('--fit-scale', '1');
      bodyEl.dataset.fitScale = '1.00';
      bodyEl.dataset.fitOverflow = 'false';

      while (bodyOverflows() && scale > FIT_MIN && iterations < FIT_MAX_ITERATIONS) {
        scale = Math.max(FIT_MIN, scale - FIT_STEP);
        bodyEl.style.setProperty('--fit-scale', scale.toFixed(2));
        bodyEl.dataset.fitScale = scale.toFixed(2);
        iterations += 1;
      }

      const stillOverflows = bodyOverflows();
      bodyEl.dataset.fitOverflow = String(stillOverflows);
      if (stillOverflows) {
        console.warn(
          `[slide-fit] Slide ${slidesData[currentIdx].number} still overflows at scale ${scale.toFixed(2)}`
        );
      }
    }

    function scheduleFit() {
      const sequence = ++fitSequence;
      const fontsReady = document.fonts && document.fonts.ready
        ? document.fonts.ready.catch(() => {})
        : Promise.resolve();

      fontsReady.then(() => {
        requestAnimationFrame(() => {
          requestAnimationFrame(() => {
            if (sequence === fitSequence) fitSlideBody();
          });
        });
      });
    }

    function renderSlide(idx) {
      if (idx < 0) idx = 0;
      if (idx >= slidesData.length) idx = slidesData.length - 1;
      currentIdx = idx;

      const slide = slidesData[idx];
      selectEl.value = idx;

      const title = slide.raw_lines[0] || `Slide ${slide.number}`;
      document.getElementById('slide-title').innerText = title;
      document.getElementById('slide-num-badge').innerText = `Slide ${slide.number} of ${slidesData.length}`;

      let bodyHtml = '';
      if (svgMap[slide.number]) {
        bodyHtml += svgMap[slide.number];
      }

      const restLines = slide.raw_lines.slice(1);
      if (restLines.length > 0) {
        bodyHtml += formatBullets(restLines);
      }

      bodyEl.style.setProperty('--fit-scale', '1');
      bodyEl.dataset.fitScale = '1.00';
      bodyEl.dataset.fitOverflow = 'pending';
      bodyEl.innerHTML = bodyHtml;
      bodyEl.dataset.columns = bodyEl.querySelector('.dense-columns') ? '2' : '1';
      
      const pct = ((idx + 1) / slidesData.length) * 100;
      document.getElementById('progress-fill').style.width = pct + '%';
      scheduleFit();
    }

    function renderGrid() {
      const gridContainer = document.getElementById('grid-mode');
      gridContainer.innerHTML = '';
      slidesData.forEach((slide, idx) => {
        const card = document.createElement('div');
        card.className = 'grid-slide-card';
        card.onclick = () => { isGridMode = true; toggleMode(); renderSlide(idx); };
        
        let title = slide.raw_lines[0] || `Slide ${slide.number}`;
        let body = slide.raw_lines.slice(1, 5).join(' ');
        
        card.innerHTML = `
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
            <span style="font-size:0.8rem; color:var(--ink); font-weight:800;">SLIDE ${slide.number}</span>
          </div>
          <div class="grid-slide-title">${title}</div>
          <div class="grid-slide-body">${body}...</div>
        `;
        gridContainer.appendChild(card);
      });
    }

    function prevSlide() { renderSlide(currentIdx - 1); }
    function nextSlide() { renderSlide(currentIdx + 1); }
    function goToSlide(val) { renderSlide(parseInt(val)); }

    function toggleMode() {
      isGridMode = !isGridMode;
      document.getElementById('presentation-mode').style.display = isGridMode ? 'none' : 'flex';
      document.getElementById('grid-mode').style.display = isGridMode ? 'grid' : 'none';
      document.getElementById('mode-text').innerText = isGridMode ? 'Presentation Mode' : 'Grid View';
      document.getElementById('mode-icon').innerText = isGridMode ? '📺' : '📜';
      if (isGridMode) renderGrid();
      else scheduleFit();
    }

    function toggleFullscreen() {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen();
      } else {
        if (document.exitFullscreen) document.exitFullscreen();
      }
    }

    document.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') nextSlide();
      if (e.key === 'ArrowLeft' || e.key === 'PageUp') prevSlide();
      if (e.key === 'f' || e.key === 'F') toggleFullscreen();
      if (e.key === 'm' || e.key === 'M') toggleMode();
    });
    window.addEventListener('resize', () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(scheduleFit, 150);
    });
    document.addEventListener('fullscreenchange', scheduleFit);

    renderSlide(0);
  </script>
</body>
</html>'''

out_docs = os.path.join(ROOT_DIR, 'docs', 'slides.html')
out_root = os.path.join(ROOT_DIR, 'slides.html')

with open(out_docs, 'w', encoding='utf-8') as f:
    f.write(html_template)

with open(out_root, 'w', encoding='utf-8') as f:
    f.write(html_template)

print(f"SUCCESSFULLY GENERATED HTML SLIDES WITHOUT AISUITE / QWEN REFERENCES!")
