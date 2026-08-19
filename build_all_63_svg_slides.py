import json
import re
import os
import html

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(ROOT_DIR, 'harness_course_presentation', 'slides_data.json')
with open(data_path, 'r', encoding='utf-8') as f:
    slides = json.load(f)

def highlight_python(code, highlight_lines=None):
    """Convert raw Python code into syntax-highlighted HTML lines with line numbers and key-line badges using single-pass tokenization."""
    if highlight_lines is None:
        highlight_lines = []
    
    kw_list = r'(?:class|def|return|if|elif|else|for|in|raise|import|from|as|None|True|False|not|and|or|async|with|await|try|except|finally|pass|while|break|continue)'
    type_list = r'(?:str|dict|int|list|tuple|bool|set|bytes|Path|subprocess|re|json|ast|sys|os|datetime|timezone|tempfile|shutil|difflib|MCPServer|ClientSession|StdioServerParameters|CourseLLMClient|PermissionError|RuntimeError|ValueError|SyntaxError)'
    
    token_spec = [
        ('COMMENT',   r'#[^\n]*'),
        ('STRING',    r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\'|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\''),
        ('DECORATOR', r'@[A-Za-z0-9_\.]+(?:\([^\)]*\))?'),
        ('DEF_FUNC',  r'\bdef\s+[A-Za-z0-9_]+'),
        ('CLASS_NAME',r'\bclass\s+[A-Za-z0-9_]+'),
        ('KEYWORD',   r'\b' + kw_list + r'\b'),
        ('TYPE',      r'\b' + type_list + r'\b'),
    ]
    
    master_pattern = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_spec))
    
    lines = code.splitlines()
    highlighted_lines = []
    
    for i, line in enumerate(lines, start=1):
        is_highlighted = i in highlight_lines
        last_idx = 0
        line_html_parts = []
        
        for match in master_pattern.finditer(line):
            start, end = match.span()
            if start > last_idx:
                line_html_parts.append(html.escape(line[last_idx:start]))
            
            kind = match.lastgroup
            val = match.group()
            
            if kind == 'COMMENT':
                line_html_parts.append(f'<span class="tok-com">{html.escape(val)}</span>')
            elif kind == 'STRING':
                line_html_parts.append(f'<span class="tok-str">{html.escape(val)}</span>')
            elif kind == 'DECORATOR':
                line_html_parts.append(f'<span class="tok-dec">{html.escape(val)}</span>')
            elif kind == 'DEF_FUNC':
                fn_name = val.split(None, 1)[1]
                line_html_parts.append(f'<span class="tok-kw">def</span> <span class="tok-fn">{html.escape(fn_name)}</span>')
            elif kind == 'CLASS_NAME':
                cls_name = val.split(None, 1)[1]
                line_html_parts.append(f'<span class="tok-kw">class</span> <span class="tok-cls">{html.escape(cls_name)}</span>')
            elif kind == 'KEYWORD':
                line_html_parts.append(f'<span class="tok-kw">{html.escape(val)}</span>')
            elif kind == 'TYPE':
                line_html_parts.append(f'<span class="tok-typ">{html.escape(val)}</span>')
                
            last_idx = end
            
        if last_idx < len(line):
            line_html_parts.append(html.escape(line[last_idx:]))
            
        content_html = ''.join(line_html_parts)
        hl_class = ' code-line-hl' if is_highlighted else ''
        key_badge = '<span class="key-badge">KEY</span>' if is_highlighted else ''
        line_html = f'<div class="code-line{hl_class}"><span class="line-num">{i:2d}</span>{key_badge}<span class="line-code">{content_html}</span></div>'
        highlighted_lines.append(line_html)
        
    return '\n'.join(highlighted_lines)

# Generate dynamic themed SVGs for concept and architecture slides
def generate_svg_for_slide(num, title):
    title_upper = title.upper()
    
    if 'CAPSTONE' in title_upper or 'DEEP RESEARCH' in title_upper:
        return '''<svg viewBox="0 0 800 105" class="slide-svg">
  <g transform="translate(15, 6)">
    <rect x="0" y="0" width="240" height="88" rx="10" fill="#FAF9F5" stroke="#059669" stroke-width="2"/>
    <text x="120" y="28" fill="#141413" font-family="Inter" font-size="12.5" font-weight="800" text-anchor="middle">🔬 Autonomous Research</text>
    <text x="120" y="50" fill="#059669" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">5-Step Deterministic SOP</text>
    <text x="120" y="71" fill="#6B6B63" font-family="Inter" font-size="10" text-anchor="middle">SpecFirst &amp; Ephemeral Worktrees</text>
  </g>
  <g transform="translate(270, 6)">
    <rect x="0" y="0" width="245" height="88" rx="10" fill="#FAF9F5" stroke="#2563eb" stroke-width="2"/>
    <text x="122" y="28" fill="#141413" font-family="Inter" font-size="12.5" font-weight="800" text-anchor="middle">🐙 Zero-API Public Streams</text>
    <text x="122" y="50" fill="#2563eb" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">Playwright GitHub &amp; YouTube</text>
    <text x="122" y="71" fill="#6B6B63" font-family="Inter" font-size="10" text-anchor="middle">arXiv, OpenAlex, HackerNews</text>
  </g>
  <g transform="translate(530, 6)">
    <rect x="0" y="0" width="255" height="88" rx="10" fill="#FAF9F5" stroke="#7c3aed" stroke-width="2"/>
    <text x="127" y="28" fill="#141413" font-family="Inter" font-size="12.5" font-weight="800" text-anchor="middle">🛡️ 100% Production Certified</text>
    <text x="127" y="50" fill="#7c3aed" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">Pytest TDA Self-Healing</text>
    <text x="127" y="71" fill="#6B6B63" font-family="Inter" font-size="10" text-anchor="middle">14/14 Tests &amp; 5-Gate Scorecard</text>
  </g>
</svg>'''
    elif 'GRAPH ENGINEERING VS. DYNAMIC WORKFLOWS' in title_upper or 'GRAPH ENGINEERING VS' in title_upper:
        return '''<svg viewBox="0 0 800 105" class="slide-svg">
  <g transform="translate(15, 6)">
    <rect x="0" y="0" width="355" height="88" rx="10" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <text x="177" y="28" fill="#141413" font-family="Inter" font-size="13" font-weight="800" text-anchor="middle">🌐 Graph Engineering (Blueprint Paradigm)</text>
    <text x="177" y="52" fill="#BD5D3A" font-family="Inter" font-size="11" font-weight="700" text-anchor="middle">Directed Acyclic Graphs (DAGs) &amp; Multi-Agent Topologies</text>
    <text x="177" y="73" fill="#6B6B63" font-family="Inter" font-size="10" text-anchor="middle">Human Architect Design: LangGraph, n8n, Custom Engines</text>
  </g>
  <path d="M375 50 L420 50" stroke="#D97757" stroke-width="3" stroke-dasharray="4 4"/>
  <text x="397" y="42" fill="#BD5D3A" font-family="Inter" font-size="9.5" font-weight="800" text-anchor="middle">RUNTIME</text>
  <g transform="translate(425, 6)">
    <rect x="0" y="0" width="360" height="88" rx="10" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="180" y="28" fill="#141413" font-family="Inter" font-size="13" font-weight="800" text-anchor="middle">⚡ Dynamic Workflows (Claude Code Native)</text>
    <text x="180" y="52" fill="#BD5D3A" font-family="Inter" font-size="11" font-weight="700" text-anchor="middle">Autonomous Background JavaScript Orchestration</text>
    <text x="180" y="73" fill="#6B6B63" font-family="Inter" font-size="10" text-anchor="middle">Fan-Out / Refute / Converge with Heavy Token Isolation</text>
  </g>
</svg>'''
    elif 'ADVANCED REFERENCES' in title_upper or 'AGENTIC SKILLS TOP 10' in title_upper or 'RESOURCES' in title_upper or 'OWASP TOP 10' in title_upper:
        return '''<svg viewBox="0 0 800 105" class="slide-svg">
  <g transform="translate(15, 6)">
    <rect x="0" y="0" width="240" height="88" rx="10" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <text x="120" y="28" fill="#141413" font-family="Inter" font-size="12.5" font-weight="800" text-anchor="middle">🛡️ OWASP Skills Top 10</text>
    <text x="120" y="50" fill="#BD5D3A" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">Agent Failure Modes</text>
    <text x="120" y="71" fill="#6B6B63" font-family="Inter" font-size="10" text-anchor="middle">Prompt Injection &amp; Loop Risks</text>
  </g>
  <g transform="translate(270, 6)">
    <rect x="0" y="0" width="245" height="88" rx="10" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="122" y="28" fill="#141413" font-family="Inter" font-size="12.5" font-weight="800" text-anchor="middle">🏭 Software Factory</text>
    <text x="122" y="50" fill="#BD5D3A" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">Greenfield Skill Delivery</text>
    <text x="122" y="71" fill="#6B6B63" font-family="Inter" font-size="10" text-anchor="middle">Slice DAGs &amp; Release Gates</text>
  </g>
  <g transform="translate(530, 6)">
    <rect x="0" y="0" width="255" height="88" rx="10" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <text x="127" y="28" fill="#141413" font-family="Inter" font-size="12.5" font-weight="800" text-anchor="middle">📚 Substack &amp; Book</text>
    <text x="127" y="50" fill="#141413" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">Ken Huang Publications</text>
    <text x="127" y="71" fill="#6B6B63" font-family="Inter" font-size="10" text-anchor="middle">Production Guides &amp; Insights</text>
  </g>
</svg>'''
    elif 'CORE THESIS' in title_upper or 'TRADITIONAL SE' in title_upper or 'THESIS' in title_upper:
        return '''<svg viewBox="0 0 880 140" class="slide-svg">
  <defs>
    <marker id="thesis-arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#BD5D3A"/>
    </marker>
  </defs>
  <!-- Traditional Software Engineering -->
  <g transform="translate(10, 5)">
    <rect x="0" y="0" width="395" height="128" rx="10" fill="#FAF9F5" stroke="#2563eb" stroke-width="2"/>
    <rect x="0" y="0" width="395" height="28" rx="10" fill="#EBF2FE" stroke="#2563eb" stroke-width="2"/>
    <text x="197" y="19" fill="#1e40af" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">🏛️ TRADITIONAL SOFTWARE ENGINEERING</text>
    <text x="197" y="46" fill="#141413" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">Deterministic IT Systems: Explicit Logic &amp; Repeatable Outputs</text>
    <g transform="translate(12, 56)">
      <rect x="0" y="0" width="180" height="36" rx="5" fill="#FFFFFF" stroke="#E3E0D6"/>
      <text x="90" y="15" fill="#1e3a8a" font-family="Inter" font-size="9" font-weight="750" text-anchor="middle">SDLC · Agile · Architecture</text>
      <text x="90" y="28" fill="#6B6B63" font-family="Inter" font-size="8.5" text-anchor="middle">DevOps · CI/CD · Pyramids</text>
      <rect x="190" y="0" width="180" height="36" rx="5" fill="#FFFFFF" stroke="#E3E0D6"/>
      <text x="280" y="15" fill="#1e3a8a" font-family="Inter" font-size="9" font-weight="750" text-anchor="middle">SRE &amp; Secure-SDLC</text>
      <text x="280" y="28" fill="#6B6B63" font-family="Inter" font-size="8.5" text-anchor="middle">AppSec · SAST/DAST</text>
    </g>
    <rect x="12" y="98" width="370" height="22" rx="4" fill="#EBF2FE" stroke="#bfdbfe"/>
    <text x="197" y="113" fill="#1e40af" font-family="JetBrains Mono" font-size="9.5" font-weight="700" text-anchor="middle">Formula: f(x) ➔ y  [Strict Input-Output Repeatability]</text>
  </g>

  <!-- Paradigm Shift Connector -->
  <g transform="translate(410, 54)">
    <path d="M 0 15 L 56 15" stroke="#BD5D3A" stroke-width="2.5" stroke-dasharray="4 3" marker-end="url(#thesis-arrow)"/>
    <rect x="4" y="3" width="48" height="24" rx="4" fill="#F5E6DF" stroke="#BD5D3A" stroke-width="1.2"/>
    <text x="28" y="15" fill="#BD5D3A" font-family="Inter" font-size="7.5" font-weight="850" text-anchor="middle">PARADIGM</text>
    <text x="28" y="23" fill="#BD5D3A" font-family="Inter" font-size="6.8" font-weight="800" text-anchor="middle">SHIFT</text>
  </g>

  <!-- Harness Engineering -->
  <g transform="translate(475, 5)">
    <rect x="0" y="0" width="395" height="128" rx="10" fill="#FAF9F5" stroke="#059669" stroke-width="2"/>
    <rect x="0" y="0" width="395" height="28" rx="10" fill="#E6F7F0" stroke="#059669" stroke-width="2"/>
    <text x="197" y="19" fill="#047857" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">🛡️ HARNESS ENGINEERING FOR AGENTIC AI</text>
    <text x="197" y="46" fill="#141413" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">Non-Deterministic Systems: Model + Emergent Behavior</text>
    <g transform="translate(12, 56)">
      <rect x="0" y="0" width="180" height="36" rx="5" fill="#FFFFFF" stroke="#E3E0D6"/>
      <text x="90" y="15" fill="#BD5D3A" font-family="Inter" font-size="9" font-weight="750" text-anchor="middle">Probabilistic Core</text>
      <text x="90" y="28" fill="#6B6B63" font-family="Inter" font-size="8.5" text-anchor="middle">Model · Prompts · Context · Tools</text>
      <rect x="190" y="0" width="180" height="36" rx="5" fill="#FFFFFF" stroke="#059669" stroke-width="1.2"/>
      <text x="280" y="15" fill="#047857" font-family="Inter" font-size="9" font-weight="750" text-anchor="middle">Deterministic Control Harness</text>
      <text x="280" y="28" fill="#6B6B63" font-family="Inter" font-size="8.5" text-anchor="middle">Memory · Sandbox · Hooks · TDA</text>
    </g>
    <rect x="12" y="98" width="370" height="22" rx="4" fill="#E6F7F0" stroke="#a7f3d0"/>
    <text x="197" y="113" fill="#047857" font-family="Inter" font-size="9.5" font-weight="800" text-anchor="middle">Goal: Reliable · Observable · Secure · Governable · Manageable</text>
  </g>
</svg>'''
    elif 'EXECUTION LOOPS' in title_upper or 'FAILURE MODE 2' in title_upper or 'RETRY TRAPS' in title_upper:
        return '''<svg viewBox="0 0 800 105" class="slide-svg">
  <g transform="translate(15, 6)">
    <rect x="0" y="0" width="240" height="88" rx="10" fill="#FAF9F5" stroke="#E06C75" stroke-width="2"/>
    <text x="120" y="28" fill="#141413" font-family="Inter" font-size="12.5" font-weight="800" text-anchor="middle">🚨 Hazard: Retry Traps</text>
    <text x="120" y="50" fill="#BD5D3A" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">Infinite Loops &amp; Token Waste</text>
    <text x="120" y="71" fill="#6B6B63" font-family="Inter" font-size="10" text-anchor="middle">Minor Punctuation Tweaks</text>
  </g>
  <g transform="translate(270, 6)">
    <rect x="0" y="0" width="245" height="88" rx="10" fill="#FAF9F5" stroke="#059669" stroke-width="2"/>
    <text x="122" y="28" fill="#141413" font-family="Inter" font-size="12.5" font-weight="800" text-anchor="middle">🛡️ Sliding Window Memory</text>
    <text x="122" y="50" fill="#059669" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">Command History Buffer</text>
    <text x="122" y="71" fill="#6B6B63" font-family="Inter" font-size="10" text-anchor="middle">Tracks Repeated Calls</text>
  </g>
  <g transform="translate(530, 6)">
    <rect x="0" y="0" width="255" height="88" rx="10" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <text x="127" y="28" fill="#141413" font-family="Inter" font-size="12.5" font-weight="800" text-anchor="middle">⚡ LoopDetector Guard</text>
    <text x="127" y="50" fill="#BD5D3A" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">Deterministic Circuit Break</text>
    <text x="127" y="71" fill="#6B6B63" font-family="Inter" font-size="10" text-anchor="middle">Raises RuntimeError &gt; max_retries</text>
  </g>
</svg>'''
    elif 'DANGEROUS TOOLS' in title_upper or 'FAILURE MODE 3' in title_upper:
        return '''<svg viewBox="0 0 800 105" class="slide-svg">
  <g transform="translate(15, 6)">
    <rect x="0" y="0" width="240" height="88" rx="10" fill="#FAF9F5" stroke="#E06C75" stroke-width="2"/>
    <text x="120" y="28" fill="#141413" font-family="Inter" font-size="12.5" font-weight="800" text-anchor="middle">🚨 Hazard: Shell Traps</text>
    <text x="120" y="50" fill="#BD5D3A" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">rm -rf &amp; Unscoped Actions</text>
    <text x="120" y="71" fill="#6B6B63" font-family="Inter" font-size="10" text-anchor="middle">Config &amp; Data Deletion</text>
  </g>
  <g transform="translate(270, 6)">
    <rect x="0" y="0" width="245" height="88" rx="10" fill="#FAF9F5" stroke="#059669" stroke-width="2"/>
    <text x="122" y="28" fill="#141413" font-family="Inter" font-size="12.5" font-weight="800" text-anchor="middle">🛡️ Deterministic Defense</text>
    <text x="122" y="50" fill="#059669" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">PreToolUse AST &amp; Regex</text>
    <text x="122" y="71" fill="#6B6B63" font-family="Inter" font-size="10" text-anchor="middle">Path.is_relative_to() Scope</text>
  </g>
  <g transform="translate(530, 6)">
    <rect x="0" y="0" width="255" height="88" rx="10" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <text x="127" y="28" fill="#141413" font-family="Inter" font-size="12.5" font-weight="800" text-anchor="middle">⚡ Deterministic Setup</text>
    <text x="127" y="50" fill="#BD5D3A" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">Virtualenv + Editable Pip</text>
    <text x="127" y="71" fill="#6B6B63" font-family="Inter" font-size="10" text-anchor="middle">sys.executable Pytest Loop</text>
  </g>
</svg>'''
    elif 'WHAT IS AN AGENT SKILL' in title_upper or 'WHAT IS A SKILL' in title_upper or 'AGENT SKILLS' in title_upper:
        return '''<svg viewBox="0 0 800 115" class="slide-svg">
  <g transform="translate(15, 8)">
    <rect x="0" y="0" width="175" height="92" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="87" y="30" fill="#141413" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">1. SKILL.md (Entry)</text>
    <text x="87" y="54" fill="#BD5D3A" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">YAML Frontmatter</text>
    <text x="87" y="74" fill="#6B6B63" font-family="Inter" font-size="9.5" text-anchor="middle">Prompt Trigger Rules</text>
  </g>
  <g transform="translate(205, 8)">
    <rect x="0" y="0" width="175" height="92" rx="8" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <text x="87" y="30" fill="#141413" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">2. scripts/ (Tools)</text>
    <text x="87" y="54" fill="#141413" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">Executable Helpers</text>
    <text x="87" y="74" fill="#6B6B63" font-family="Inter" font-size="9.5" text-anchor="middle">CLI &amp; Validation Python</text>
  </g>
  <g transform="translate(395, 8)">
    <rect x="0" y="0" width="185" height="92" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="92" y="30" fill="#141413" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">3. references/ (Docs)</text>
    <text x="92" y="54" fill="#141413" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">Domain Knowledge</text>
    <text x="92" y="74" fill="#6B6B63" font-family="Inter" font-size="9.5" text-anchor="middle">Progressive Disclosure</text>
  </g>
  <g transform="translate(595, 8)">
    <rect x="0" y="0" width="185" height="92" rx="8" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <text x="92" y="30" fill="#141413" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">4. assets/ (Schemas)</text>
    <text x="92" y="54" fill="#141413" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">Templates &amp; Configs</text>
    <text x="92" y="74" fill="#6B6B63" font-family="Inter" font-size="9.5" text-anchor="middle">JSON Schemas &amp; State</text>
  </g>
</svg>'''
    elif 'ABOUT THE INSTRUCTOR' in title_upper or 'ABOUT ME' in title_upper or 'KEN HUANG' in title_upper:
        return '''<svg viewBox="0 0 800 110" class="slide-svg">
  <defs>
    <clipPath id="headshot-circle">
      <circle cx="65" cy="55" r="32"/>
    </clipPath>
  </defs>
  <rect x="15" y="6" width="770" height="98" rx="14" fill="#FAF9F5" stroke="#D97757" stroke-width="2.5"/>
  <circle cx="65" cy="55" r="34" fill="#F5E6DF" stroke="#BD5D3A" stroke-width="2.5"/>
  <image href="assets/images/ken-head-shot.png" x="31" y="21" width="68" height="68" clip-path="url(#headshot-circle)" preserveAspectRatio="xMidYMid slice"/>
  <text x="115" y="44" fill="#141413" font-family="Inter" font-size="16.5" font-weight="900">KEN HUANG, CISSP — INSTRUCTOR &amp; AI SAFETY RESEARCHER</text>
  <text x="115" y="68" fill="#6B6B63" font-family="Inter" font-size="12" font-weight="600">Author, Harness Engineering &amp; MAESTRO | Adjunct Professor, University of San Francisco</text>
  <text x="115" y="88" fill="#BD5D3A" font-family="Inter" font-size="11.5" font-weight="750">CSA Fellow &amp; Co-Chair | OWASP AIVSS Lead | AIUC-1 Consortium | Schmidt Sciences</text>
</svg>'''
    elif 'COURSE MASTER MAP' in title_upper:
        return '''<svg viewBox="0 0 800 110" class="slide-svg">
  <rect x="20" y="8" width="365" height="92" rx="12" fill="#FAF9F5" stroke="#D97757" stroke-width="2.2"/>
  <text x="202" y="36" fill="#141413" font-family="Inter" font-size="14" font-weight="800" text-anchor="middle">PART 1: FOUNDATIONS &amp; CONTROL</text>
  <text x="202" y="58" fill="#6B6B63" font-family="Inter" font-size="11" text-anchor="middle">Modules 1–5: Core Scaffolding, SDD &amp; Gateways</text>
  <text x="202" y="78" fill="#BD5D3A" font-family="Inter" font-size="11" font-weight="700" text-anchor="middle">Deterministic Execution &amp; Interception</text>
  <path d="M385 54 L415 54" stroke="#BD5D3A" stroke-width="3.5" stroke-dasharray="4 4"/>
  <rect x="415" y="8" width="365" height="92" rx="12" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2.2"/>
  <text x="597" y="36" fill="#141413" font-family="Inter" font-size="14" font-weight="800" text-anchor="middle">PART 2: RELIABILITY &amp; TEAMS</text>
  <text x="597" y="58" fill="#6B6B63" font-family="Inter" font-size="11" text-anchor="middle">Modules 6–10: TDA, MCP, Multi-Agent &amp; Audit</text>
  <text x="597" y="78" fill="#D97757" font-family="Inter" font-size="11" font-weight="700" text-anchor="middle">5-Gate Production Readiness Scorecard</text>
</svg>'''
    elif 'SPEC-DRIVEN' in title_upper or 'SPEC CONTRACT' in title_upper or 'SPECIFICATION' in title_upper or 'MODULE 3' in title_upper:
        return '''<svg viewBox="0 0 800 100" class="slide-svg">
  <g transform="translate(15, 6)">
    <rect x="0" y="0" width="175" height="86" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="87" y="28" fill="#141413" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">1. SPEC.md Contract</text>
    <text x="87" y="50" fill="#4A4A44" font-family="Inter" font-size="10.5" text-anchor="middle">Immutable File Scope</text>
    <text x="87" y="70" fill="#4A4A44" font-family="Inter" font-size="10" text-anchor="middle">Acceptance Criteria</text>
  </g>
  <g transform="translate(205, 6)">
    <rect x="0" y="0" width="175" height="86" rx="8" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <text x="87" y="28" fill="#141413" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">2. Allowed Scopes</text>
    <text x="87" y="50" fill="#BD5D3A" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">allowed_files Check</text>
    <text x="87" y="70" fill="#4A4A44" font-family="Inter" font-size="10" text-anchor="middle">Blocks database.py</text>
  </g>
  <g transform="translate(395, 6)">
    <rect x="0" y="0" width="185" height="86" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="92" y="28" fill="#141413" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">3. Non-Goal Scans</text>
    <text x="92" y="50" fill="#BD5D3A" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">Scope Violations</text>
    <text x="92" y="70" fill="#BD5D3A" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">Rejects Feature Creep</text>
  </g>
  <g transform="translate(595, 6)">
    <rect x="0" y="0" width="185" height="86" rx="8" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <text x="92" y="28" fill="#141413" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">4. AST Pre-Validation</text>
    <text x="92" y="50" fill="#141413" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">ast.parse() Syntax Check</text>
    <text x="92" y="70" fill="#4A4A44" font-family="Inter" font-size="10" text-anchor="middle">Zero Syntax Errors</text>
  </g>
</svg>'''
    elif 'PILLAR 1: MEMORY' in title_upper or 'MEMORY FILES' in title_upper or 'AUTO MEMORY' in title_upper:
        return '''<svg viewBox="0 0 800 105" class="slide-svg">
  <!-- 1. CLAUDE.md Files (Manual) -->
  <g transform="translate(15, 6)">
    <rect x="0" y="0" width="180" height="90" rx="8" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <text x="90" y="24" fill="#BD5D3A" font-family="Inter" font-size="11" font-weight="800" text-anchor="middle">📝 1. CLAUDE.md (User)</text>
    <text x="90" y="44" fill="#141413" font-family="Inter" font-size="9.5" font-weight="700" text-anchor="middle">Persistent Guidelines</text>
    <text x="90" y="62" fill="#6B6B63" font-family="Inter" font-size="8.5" text-anchor="middle">Rules, Arch &amp; Standards</text>
    <text x="90" y="78" fill="#BD5D3A" font-family="Inter" font-size="8" font-weight="750" text-anchor="middle">Loaded full at session start</text>
  </g>

  <!-- 2. Auto Memory (Autonomous) -->
  <g transform="translate(210, 6)">
    <rect x="0" y="0" width="180" height="90" rx="8" fill="#FAF9F5" stroke="#2563eb" stroke-width="2"/>
    <text x="90" y="24" fill="#1e40af" font-family="Inter" font-size="11" font-weight="800" text-anchor="middle">🧠 2. Auto Memory (Agent)</text>
    <text x="90" y="44" fill="#141413" font-family="Inter" font-size="9.5" font-weight="700" text-anchor="middle">Autonomous Learnings</text>
    <text x="90" y="62" fill="#6B6B63" font-family="Inter" font-size="8.5" text-anchor="middle">MEMORY.md &amp; topic notes</text>
    <text x="90" y="78" fill="#2563eb" font-family="Inter" font-size="8" font-weight="750" text-anchor="middle">First 200 lines / 25KB</text>
  </g>

  <!-- 3. Resolution Hierarchy -->
  <g transform="translate(405, 6)">
    <rect x="0" y="0" width="185" height="90" rx="8" fill="#FAF9F5" stroke="#059669" stroke-width="2"/>
    <text x="92" y="24" fill="#047857" font-family="Inter" font-size="11" font-weight="800" text-anchor="middle">🌲 3. 5-Tier Scope Tree</text>
    <text x="92" y="44" fill="#141413" font-family="Inter" font-size="9.5" font-weight="700" text-anchor="middle">Resolution Order</text>
    <text x="92" y="62" fill="#6B6B63" font-family="Inter" font-size="8.5" text-anchor="middle">Managed ➔ User ➔ Project</text>
    <text x="92" y="78" fill="#047857" font-family="Inter" font-size="8" font-weight="750" text-anchor="middle">Local .md ➔ .claude/rules/</text>
  </g>

  <!-- 4. Imports & AGENTS.md -->
  <g transform="translate(605, 6)">
    <rect x="0" y="0" width="180" height="90" rx="8" fill="#FAF9F5" stroke="#7c3aed" stroke-width="2"/>
    <text x="90" y="24" fill="#7c3aed" font-family="Inter" font-size="11" font-weight="800" text-anchor="middle">🔗 4. Imports &amp; Interop</text>
    <text x="90" y="44" fill="#141413" font-family="Inter" font-size="9.5" font-weight="700" text-anchor="middle">Modular @path Syntax</text>
    <text x="90" y="62" fill="#6B6B63" font-family="Inter" font-size="8.5" text-anchor="middle">4-Hop recursive expansion</text>
    <text x="90" y="78" fill="#7c3aed" font-family="Inter" font-size="8" font-weight="750" text-anchor="middle">@AGENTS.md bridge</text>
  </g>
</svg>'''
    elif 'PILLARS 4 & 5' in title_upper or 'BUDGET & TRACING' in title_upper or 'JSONL TRANSCRIPTS' in title_upper:
        return '''<svg viewBox="0 0 800 105" class="slide-svg">
  <!-- Pillar 4: Token Budgeting & Compaction -->
  <g transform="translate(15, 6)">
    <rect x="0" y="0" width="375" height="92" rx="8" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <text x="187" y="24" fill="#BD5D3A" font-family="Inter" font-size="11.5" font-weight="800" text-anchor="middle">⚡ PILLAR 4: Context Budget &amp; Compaction</text>
    <text x="187" y="44" fill="#141413" font-family="Inter" font-size="10" font-weight="700" text-anchor="middle">20/20/50/10 Allocation (Memory · Spec · Workspace · Headroom)</text>
    <text x="187" y="62" fill="#6B6B63" font-family="Inter" font-size="9" text-anchor="middle">Head/Tail Compaction: First 5 &amp; Last 15 Turns Preserved</text>
    <text x="187" y="78" fill="#BD5D3A" font-family="Inter" font-size="8.5" font-weight="750" text-anchor="middle">Eliminates Context Drift &amp; Prevents OOM Exhaustion</text>
  </g>

  <!-- Pillar 5: Structured Tracing (Claude Code JSONL) -->
  <g transform="translate(410, 6)">
    <rect x="0" y="0" width="375" height="92" rx="8" fill="#FAF9F5" stroke="#059669" stroke-width="2"/>
    <text x="187" y="24" fill="#047857" font-family="Inter" font-size="11.5" font-weight="800" text-anchor="middle">📜 PILLAR 5: Claude Code JSONL Transcripts</text>
    <text x="187" y="44" fill="#141413" font-family="Inter" font-size="10" font-weight="700" text-anchor="middle">~/.claude/projects/&lt;encoded-path&gt;/&lt;session-id&gt;.jsonl</text>
    <text x="187" y="62" fill="#6B6B63" font-family="Inter" font-size="9" text-anchor="middle">Append-Only Events: user · assistant · tool_use · tool_result · usage</text>
    <text x="187" y="78" fill="#047857" font-family="Inter" font-size="8.5" font-weight="750" text-anchor="middle">Direct jq / Python Inspection · Token Attribution &amp; Audit</text>
  </g>
</svg>'''
    elif 'PILLAR 3: HOOKS' in title_upper or 'LIFECYCLE HOOK' in title_upper or '31 DETERMINISTIC' in title_upper or '31-EVENT' in title_upper:
        return '''<svg viewBox="0 0 800 105" class="slide-svg">
  <g transform="translate(10, 5)">
    <rect x="0" y="0" width="122" height="92" rx="8" fill="#FAF9F5" stroke="#2563eb" stroke-width="2"/>
    <text x="61" y="24" fill="#1e40af" font-family="Inter" font-size="11" font-weight="800" text-anchor="middle">1. Session/Turn</text>
    <text x="61" y="44" fill="#141413" font-family="Inter" font-size="9.5" font-weight="700" text-anchor="middle">7 Events</text>
    <text x="61" y="62" fill="#6B6B63" font-family="Inter" font-size="8.5" text-anchor="middle">SessionStart/Stop</text>
    <text x="61" y="78" fill="#6B6B63" font-family="Inter" font-size="8.5" text-anchor="middle">UserPromptSubmit</text>
  </g>
  <g transform="translate(140, 5)">
    <rect x="0" y="0" width="122" height="92" rx="8" fill="#FAF9F5" stroke="#E06C75" stroke-width="2"/>
    <text x="61" y="24" fill="#BD5D3A" font-family="Inter" font-size="11" font-weight="800" text-anchor="middle">2. Tool Loop</text>
    <text x="61" y="44" fill="#141413" font-family="Inter" font-size="9.5" font-weight="700" text-anchor="middle">6 Events</text>
    <text x="61" y="62" fill="#BD5D3A" font-family="Inter" font-size="8.5" font-weight="750" text-anchor="middle">PreToolUse (Deny)</text>
    <text x="61" y="78" fill="#6B6B63" font-family="Inter" font-size="8.5" text-anchor="middle">PostToolUse (AST)</text>
  </g>
  <g transform="translate(270, 5)">
    <rect x="0" y="0" width="125" height="92" rx="8" fill="#FAF9F5" stroke="#7c3aed" stroke-width="2"/>
    <text x="62" y="24" fill="#6d28d9" font-family="Inter" font-size="11" font-weight="800" text-anchor="middle">3. Subagents</text>
    <text x="62" y="44" fill="#141413" font-family="Inter" font-size="9.5" font-weight="700" text-anchor="middle">5 Events</text>
    <text x="62" y="62" fill="#6B6B63" font-family="Inter" font-size="8.5" text-anchor="middle">SubagentStart/Stop</text>
    <text x="62" y="78" fill="#6B6B63" font-family="Inter" font-size="8.5" text-anchor="middle">TaskCompleted DoD</text>
  </g>
  <g transform="translate(403, 5)">
    <rect x="0" y="0" width="125" height="92" rx="8" fill="#FAF9F5" stroke="#059669" stroke-width="2"/>
    <text x="62" y="24" fill="#047857" font-family="Inter" font-size="11" font-weight="800" text-anchor="middle">4. Worktrees</text>
    <text x="62" y="44" fill="#141413" font-family="Inter" font-size="9.5" font-weight="700" text-anchor="middle">7 Events</text>
    <text x="62" y="62" fill="#6B6B63" font-family="Inter" font-size="8.5" text-anchor="middle">WorktreeCreate</text>
    <text x="62" y="78" fill="#6B6B63" font-family="Inter" font-size="8.5" text-anchor="middle">CwdChanged/File</text>
  </g>
  <g transform="translate(536, 5)">
    <rect x="0" y="0" width="122" height="92" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="61" y="24" fill="#BD5D3A" font-family="Inter" font-size="11" font-weight="800" text-anchor="middle">5. Compaction</text>
    <text x="61" y="44" fill="#141413" font-family="Inter" font-size="9.5" font-weight="700" text-anchor="middle">2 Events</text>
    <text x="61" y="62" fill="#6B6B63" font-family="Inter" font-size="8.5" text-anchor="middle">PreCompact Gate</text>
    <text x="61" y="78" fill="#6B6B63" font-family="Inter" font-size="8.5" text-anchor="middle">PostCompact Fact</text>
  </g>
  <g transform="translate(666, 5)">
    <rect x="0" y="0" width="124" height="92" rx="8" fill="#FAF9F5" stroke="#2563eb" stroke-width="2"/>
    <text x="62" y="24" fill="#1e40af" font-family="Inter" font-size="11" font-weight="800" text-anchor="middle">6. MCP / Alerts</text>
    <text x="62" y="44" fill="#141413" font-family="Inter" font-size="9.5" font-weight="700" text-anchor="middle">4 Events</text>
    <text x="62" y="62" fill="#6B6B63" font-family="Inter" font-size="8.5" text-anchor="middle">Elicitation (MCP)</text>
    <text x="62" y="78" fill="#6B6B63" font-family="Inter" font-size="8.5" text-anchor="middle">Notification Push</text>
  </g>
</svg>'''
    elif '5 HARNESS PILLARS' in title_upper or '5 PILLARS' in title_upper:
        return '''<svg viewBox="0 0 800 100" class="slide-svg">
  <g transform="translate(10, 5)">
    <rect x="0" y="0" width="140" height="88" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="70" y="28" fill="#141413" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">Pillar 1: Memory</text>
    <text x="70" y="50" fill="#BD5D3A" font-family="Inter" font-size="9.5" font-weight="700" text-anchor="middle">User vs. Generated</text>
    <text x="70" y="68" fill="#6B6B63" font-family="Inter" font-size="9" text-anchor="middle">Short vs. Long Term</text>
  </g>
  <g transform="translate(165, 5)">
    <rect x="0" y="0" width="140" height="88" rx="8" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <text x="70" y="28" fill="#141413" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">Pillar 2: Sandbox</text>
    <text x="70" y="52" fill="#6B6B63" font-family="Inter" font-size="10.5" text-anchor="middle">Least Privilege</text>
    <text x="70" y="72" fill="#6B6B63" font-family="Inter" font-size="10.5" text-anchor="middle">Path is_relative_to</text>
  </g>
  <g transform="translate(320, 5)">
    <rect x="0" y="0" width="140" height="88" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="70" y="28" fill="#141413" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">Pillar 3: Hooks</text>
    <text x="70" y="52" fill="#6B6B63" font-family="Inter" font-size="10.5" text-anchor="middle">Secret Filtering</text>
    <text x="70" y="72" fill="#6B6B63" font-family="Inter" font-size="10.5" text-anchor="middle">AST Syntax Check</text>
  </g>
  <g transform="translate(475, 5)">
    <rect x="0" y="0" width="140" height="88" rx="8" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <text x="70" y="28" fill="#141413" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">Pillar 4: Budget</text>
    <text x="70" y="52" fill="#6B6B63" font-family="Inter" font-size="10.5" text-anchor="middle">Head/Tail Compact</text>
    <text x="70" y="72" fill="#6B6B63" font-family="Inter" font-size="10.5" text-anchor="middle">Context Window Cap</text>
  </g>
  <g transform="translate(630, 5)">
    <rect x="0" y="0" width="155" height="88" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="77" y="28" fill="#141413" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">Pillar 5: Tracing</text>
    <text x="77" y="52" fill="#6B6B63" font-family="Inter" font-size="10.5" text-anchor="middle">events.jsonl Audit</text>
    <text x="77" y="72" fill="#6B6B63" font-family="Inter" font-size="10.5" text-anchor="middle">ISO UTC Timestamps</text>
  </g>
</svg>'''
    elif '4-LAYER' in title_upper or 'GUARDRAILS' in title_upper or 'MODULE 4' in title_upper:
        return '''<svg viewBox="0 0 800 100" class="slide-svg">
  <g transform="translate(15, 6)">
    <rect x="0" y="0" width="175" height="86" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="87" y="28" fill="#141413" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">1. System Prompt</text>
    <text x="87" y="50" fill="#4A4A44" font-family="Inter" font-size="10.5" text-anchor="middle">Standing Guidelines</text>
    <text x="87" y="70" fill="#4A4A44" font-family="Inter" font-size="10" text-anchor="middle">CLAUDE.md / AGENTS.md</text>
  </g>
  <g transform="translate(205, 6)">
    <rect x="0" y="0" width="175" height="86" rx="8" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <text x="87" y="28" fill="#141413" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">2. Tool Schemas</text>
    <text x="87" y="50" fill="#BD5D3A" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">JSON Schema Typing</text>
    <text x="87" y="70" fill="#4A4A44" font-family="Inter" font-size="10" text-anchor="middle">Strict Argument Checks</text>
  </g>
  <g transform="translate(395, 6)">
    <rect x="0" y="0" width="185" height="86" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="92" y="28" fill="#141413" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">3. Pre/Post Hooks</text>
    <text x="92" y="50" fill="#BD5D3A" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">PreToolUse Shell Deny</text>
    <text x="92" y="70" fill="#BD5D3A" font-family="Inter" font-size="10" font-weight="700" text-anchor="middle">PostToolUse AST / Secrets</text>
  </g>
  <g transform="translate(595, 6)">
    <rect x="0" y="0" width="185" height="86" rx="8" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <text x="92" y="28" fill="#141413" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">4. OS Sandboxing</text>
    <text x="92" y="50" fill="#141413" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">Path is_relative_to</text>
    <text x="92" y="70" fill="#4A4A44" font-family="Inter" font-size="10" text-anchor="middle">Process Isolation</text>
  </g>
</svg>'''
    elif 'EVALUATION' in title_upper or 'SCORE BEHAVIOR' in title_upper:
        return '''<svg viewBox="0 0 800 100" class="slide-svg">
  <g transform="translate(15, 6)">
    <rect x="0" y="0" width="175" height="86" rx="8" fill="#FAF9F5" stroke="#E06C75" stroke-width="2"/>
    <text x="87" y="28" fill="#141413" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">1. The Hard Problem</text>
    <text x="87" y="50" fill="#BD5D3A" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">Non-Deterministic</text>
    <text x="87" y="70" fill="#4A4A44" font-family="Inter" font-size="10" text-anchor="middle">Multi-Turn Trajectories</text>
  </g>
  <g transform="translate(205, 6)">
    <rect x="0" y="0" width="175" height="86" rx="8" fill="#FAF9F5" stroke="#2563eb" stroke-width="2"/>
    <text x="87" y="28" fill="#141413" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">2. SWE-bench &amp; Evals</text>
    <text x="87" y="50" fill="#1e40af" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">Real GitHub Issues</text>
    <text x="87" y="70" fill="#4A4A44" font-family="Inter" font-size="10" text-anchor="middle">Hidden Pytest Asserts</text>
  </g>
  <g transform="translate(395, 6)">
    <rect x="0" y="0" width="185" height="86" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="92" y="28" fill="#141413" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">3. TerminalBench</text>
    <text x="92" y="50" fill="#BD5D3A" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">Interactive CLI</text>
    <text x="92" y="70" fill="#4A4A44" font-family="Inter" font-size="10" text-anchor="middle">Multi-Turn Shell Tasks</text>
  </g>
  <g transform="translate(595, 6)">
    <rect x="0" y="0" width="185" height="86" rx="8" fill="#FAF9F5" stroke="#059669" stroke-width="2"/>
    <text x="92" y="28" fill="#141413" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">4. Automated Scoring</text>
    <text x="92" y="50" fill="#047857" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">Pass Rate &amp; Scope</text>
    <text x="92" y="70" fill="#4A4A44" font-family="Inter" font-size="10" text-anchor="middle">Zero Test Contamination</text>
  </g>
</svg>'''
    elif 'PERMISSION MODES' in title_upper or 'RISK TIERS' in title_upper or 'PERMISSION GATEWAYS' in title_upper or 'MODULE 5' in title_upper:
        return '''<svg viewBox="0 0 800 100" class="slide-svg">
  <g transform="translate(15, 6)">
    <rect x="0" y="0" width="175" height="86" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="87" y="28" fill="#141413" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">LOW RISK</text>
    <text x="87" y="50" fill="#4A4A44" font-family="Inter" font-size="10.5" text-anchor="middle">read_file, list_dir, grep</text>
    <text x="87" y="70" fill="#141413" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">✓ Auto-Approved</text>
  </g>
  <g transform="translate(205, 6)">
    <rect x="0" y="0" width="175" height="86" rx="8" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <text x="87" y="28" fill="#141413" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">MEDIUM RISK</text>
    <text x="87" y="50" fill="#4A4A44" font-family="Inter" font-size="10.5" text-anchor="middle">write_file, run_test</text>
    <text x="87" y="70" fill="#141413" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">✓ Logged &amp; Approved</text>
  </g>
  <g transform="translate(395, 6)">
    <rect x="0" y="0" width="185" height="86" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="92" y="28" fill="#141413" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">HIGH RISK</text>
    <text x="92" y="50" fill="#4A4A44" font-family="Inter" font-size="10.5" text-anchor="middle">pip_install</text>
    <text x="92" y="70" fill="#BD5D3A" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">⚠ Intent Logged Alert</text>
  </g>
  <g transform="translate(595, 6)">
    <rect x="0" y="0" width="185" height="86" rx="8" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <text x="92" y="28" fill="#141413" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">CRITICAL RISK</text>
    <text x="92" y="50" fill="#BD5D3A" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">git_push, db_drop</text>
    <text x="92" y="70" fill="#BD5D3A" font-family="Inter" font-size="10.5" font-weight="800" text-anchor="middle">⛔ approvals.json Ledger</text>
  </g>
</svg>'''
    elif 'PYTEST CAPTURE' in title_upper or 'OBSERVABILITY' in title_upper or 'DUAL-LOOP' in title_upper:
        return '''<svg viewBox="0 0 800 100" class="slide-svg">
  <g transform="translate(15, 6)">
    <rect x="0" y="0" width="365" height="86" rx="8" fill="#FAF9F5" stroke="#2563eb" stroke-width="2"/>
    <text x="182" y="28" fill="#1e40af" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">🔍 OUTER LOOP: Pytest Capture (capfd)</text>
    <text x="182" y="50" fill="#141413" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">"Black Box" Recorder — Customer Acceptance</text>
    <text x="182" y="70" fill="#6B6B63" font-family="Inter" font-size="9.5" text-anchor="middle">Local stdout/stderr, Exit Code 0, Generated Diffs</text>
  </g>
  <path d="M390 49 L410 49" stroke="#BD5D3A" stroke-width="3" stroke-dasharray="3 3"/>
  <text x="400" y="38" fill="#BD5D3A" font-family="Inter" font-size="8.5" font-weight="800" text-anchor="middle">+</text>
  <g transform="translate(420, 6)">
    <rect x="0" y="0" width="365" height="86" rx="8" fill="#FAF9F5" stroke="#059669" stroke-width="2"/>
    <text x="182" y="28" fill="#047857" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">🔬 INNER LOOP: Langfuse / LangSmith / Arize</text>
    <text x="182" y="50" fill="#141413" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">"Glass Box / X-Ray" — Engineer\'s Debugger</text>
    <text x="182" y="70" fill="#6B6B63" font-family="Inter" font-size="9.5" text-anchor="middle">Prompt Chains, Token Costs, Latency &amp; Retries</text>
  </g>
</svg>'''
    elif 'AGENT EXTENSIONS' in title_upper or 'SKILLS, PLUGINS' in title_upper or 'MODULE 7' in title_upper:
        return '''<svg viewBox="0 0 800 100" class="slide-svg">
  <g transform="translate(15, 6)">
    <rect x="0" y="0" width="175" height="86" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="87" y="28" fill="#141413" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">1. Skills (SOPs)</text>
    <text x="87" y="50" fill="#BD5D3A" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">SKILL.md Playbooks</text>
    <text x="87" y="70" fill="#4A4A44" font-family="Inter" font-size="9.5" text-anchor="middle">Progressive Disclosure</text>
  </g>
  <g transform="translate(205, 6)">
    <rect x="0" y="0" width="175" height="86" rx="8" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <text x="87" y="28" fill="#141413" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">2. Plugins (Bundles)</text>
    <text x="87" y="50" fill="#BD5D3A" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">plugin.json Manifest</text>
    <text x="87" y="70" fill="#4A4A44" font-family="Inter" font-size="9.5" text-anchor="middle">Skills + Hooks + Agents</text>
  </g>
  <g transform="translate(395, 6)">
    <rect x="0" y="0" width="185" height="86" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="92" y="28" fill="#141413" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">3. MCP (Tools/Data)</text>
    <text x="92" y="50" fill="#BD5D3A" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">@mcp.tool &amp; Resources</text>
    <text x="92" y="70" fill="#4A4A44" font-family="Inter" font-size="9.5" text-anchor="middle">stdio &amp; Streamable HTTP</text>
  </g>
  <g transform="translate(595, 6)">
    <rect x="0" y="0" width="185" height="86" rx="8" fill="#FAF9F5" stroke="#059669" stroke-width="2"/>
    <text x="92" y="28" fill="#141413" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">4. Subagents</text>
    <text x="92" y="50" fill="#047857" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">.claude/agents/*.md</text>
    <text x="92" y="70" fill="#4A4A44" font-family="Inter" font-size="9.5" text-anchor="middle">Isolated Context Worktrees</text>
  </g>
</svg>'''
    elif 'PLUGIN.JSON' in title_upper or 'MARKETPLACE' in title_upper or 'PLUGIN ARCHITECTURE' in title_upper:
        return '''<svg viewBox="0 0 800 100" class="slide-svg">
  <g transform="translate(15, 6)">
    <rect x="0" y="0" width="365" height="86" rx="8" fill="#FAF9F5" stroke="#2563eb" stroke-width="2"/>
    <text x="182" y="28" fill="#1e40af" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">📁 LOCAL BLUEPRINT: plugin.json</text>
    <text x="182" y="50" fill="#141413" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">Internal Execution &amp; Tool Isolation</text>
    <text x="182" y="70" fill="#6B6B63" font-family="Inter" font-size="9.5" text-anchor="middle">.claude-plugin/plugin.json · Skills, Hooks, Agents &amp; MCP</text>
  </g>
  <path d="M390 49 L410 49" stroke="#BD5D3A" stroke-width="3" stroke-dasharray="3 3"/>
  <text x="400" y="38" fill="#BD5D3A" font-family="Inter" font-size="8.5" font-weight="800" text-anchor="middle">➔</text>
  <g transform="translate(420, 6)">
    <rect x="0" y="0" width="365" height="86" rx="8" fill="#FAF9F5" stroke="#059669" stroke-width="2"/>
    <text x="182" y="28" fill="#047857" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">🌐 PUBLIC REGISTRY: marketplace.json</text>
    <text x="182" y="50" fill="#141413" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">Ecosystem Catalog &amp; Verified Distribution</text>
    <text x="182" y="70" fill="#6B6B63" font-family="Inter" font-size="9.5" text-anchor="middle">Download URLs, Verified Authors &amp; Compatibility</text>
  </g>
</svg>'''
    elif 'MODEL CONTEXT PROTOCOL' in title_upper or 'MCP ARCHITECTURE' in title_upper or 'MCP FOUNDATION' in title_upper or 'MCP PROTOCOL' in title_upper:
        return '''<svg viewBox="0 0 800 110" class="slide-svg">
  <g transform="translate(15, 6)">
    <rect x="0" y="0" width="240" height="96" rx="10" fill="#FAF9F5" stroke="#2563eb" stroke-width="2"/>
    <text x="120" y="24" fill="#1e40af" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">🖥️ MCP HOST</text>
    <text x="120" y="42" fill="#6B6B63" font-family="Inter" font-size="9.5" text-anchor="middle">Claude Code, Cursor, AI Runtime</text>
    <rect x="15" y="52" width="210" height="34" rx="6" fill="#FFFFFF" stroke="#bfdbfe"/>
    <text x="120" y="68" fill="#1e40af" font-family="Inter" font-size="10" font-weight="750" text-anchor="middle">📦 Nested MCP Client</text>
    <text x="120" y="80" fill="#6B6B63" font-family="Inter" font-size="8.5" text-anchor="middle">1-to-1 Protocol Connection</text>
  </g>
  <g transform="translate(265, 16)">
    <path d="M 0 20 L 70 20" stroke="#BD5D3A" stroke-width="2.5"/>
    <path d="M 70 42 L 0 42" stroke="#BD5D3A" stroke-width="2.5" stroke-dasharray="3 3"/>
    <rect x="8" y="2" width="54" height="18" rx="4" fill="#F5E6DF" stroke="#BD5D3A" stroke-width="1"/>
    <text x="35" y="14" fill="#BD5D3A" font-family="Inter" font-size="8" font-weight="800" text-anchor="middle">JSON-RPC</text>
    <text x="35" y="56" fill="#6B6B63" font-family="Inter" font-size="7.5" font-weight="700" text-anchor="middle">stdio / HTTP</text>
    <text x="35" y="66" fill="#BD5D3A" font-family="Inter" font-size="7" font-weight="750" text-anchor="middle">[MRTR Roundtrip]</text>
  </g>
  <g transform="translate(345, 6)">
    <rect x="0" y="0" width="440" height="96" rx="10" fill="#FAF9F5" stroke="#059669" stroke-width="2"/>
    <text x="220" y="24" fill="#047857" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">⚡ MCP SERVER (Stateless Execution)</text>
    <text x="220" y="42" fill="#6B6B63" font-family="Inter" font-size="9.5" text-anchor="middle">Universal Serverless &amp; Cloudflare Workers / AWS Lambda</text>
    <g transform="translate(12, 50)">
      <rect x="0" y="0" width="130" height="36" rx="6" fill="#FFFFFF" stroke="#a7f3d0"/>
      <text x="65" y="16" fill="#047857" font-family="Inter" font-size="9.5" font-weight="750" text-anchor="middle">🛠️ @mcp.tool()</text>
      <text x="65" y="28" fill="#6B6B63" font-family="Inter" font-size="8" text-anchor="middle">Actions &amp; Schemas</text>
      <rect x="142" y="0" width="130" height="36" rx="6" fill="#FFFFFF" stroke="#a7f3d0"/>
      <text x="207" y="16" fill="#047857" font-family="Inter" font-size="9.5" font-weight="750" text-anchor="middle">📄 @mcp.resource()</text>
      <text x="207" y="28" fill="#6B6B63" font-family="Inter" font-size="8" text-anchor="middle">Read-Only URIs</text>
      <rect x="284" y="0" width="130" height="36" rx="6" fill="#FFFFFF" stroke="#a7f3d0"/>
      <text x="349" y="16" fill="#047857" font-family="Inter" font-size="9.5" font-weight="750" text-anchor="middle">💬 @mcp.prompt()</text>
      <text x="349" y="28" fill="#6B6B63" font-family="Inter" font-size="8" text-anchor="middle">Reusable Templates</text>
    </g>
  </g>
</svg>'''
    elif 'SECURING THE MODEL CONTEXT PROTOCOL' in title_upper or 'SECURING MCP' in title_upper or 'THREAT MODELING, 3-ZONE' in title_upper:
        return '''<svg viewBox="0 0 800 105" class="slide-svg">
  <!-- Zone 0: Control Plane -->
  <g transform="translate(10, 5)">
    <rect x="0" y="0" width="180" height="92" rx="8" fill="#FAF9F5" stroke="#7c3aed" stroke-width="2"/>
    <text x="90" y="24" fill="#6d28d9" font-family="Inter" font-size="11.5" font-weight="800" text-anchor="middle">🛡️ ZONE 0: Control Plane</text>
    <text x="90" y="44" fill="#141413" font-family="Inter" font-size="10" font-weight="700" text-anchor="middle">Vault Dynamic Secrets</text>
    <text x="90" y="62" fill="#6B6B63" font-family="Inter" font-size="9" text-anchor="middle">OPA / Cedar Policy Engine</text>
    <text x="90" y="78" fill="#6B6B63" font-family="Inter" font-size="9" text-anchor="middle">OTEL SIEM Audit Bus</text>
  </g>
  <path d="M195 50 L212 50" stroke="#BD5D3A" stroke-width="2.5"/>

  <!-- Zone 1: MCP Server Fleet -->
  <g transform="translate(215, 5)">
    <rect x="0" y="0" width="180" height="92" rx="8" fill="#FAF9F5" stroke="#2563eb" stroke-width="2"/>
    <text x="90" y="24" fill="#1e40af" font-family="Inter" font-size="11.5" font-weight="800" text-anchor="middle">⚡ ZONE 1: MCP Server</text>
    <text x="90" y="44" fill="#141413" font-family="Inter" font-size="10" font-weight="700" text-anchor="middle">mTLS Mesh &amp; DPoP JWT</text>
    <text x="90" y="62" fill="#6B6B63" font-family="Inter" font-size="9" text-anchor="middle">Read-Only Root Filesystem</text>
    <text x="90" y="78" fill="#6B6B63" font-family="Inter" font-size="9" text-anchor="middle">Sidecar OPA Authorization</text>
  </g>
  <path d="M400 50 L417 50" stroke="#BD5D3A" stroke-width="2.5"/>

  <!-- Zone 2: Tool Runtime Sandbox -->
  <g transform="translate(420, 5)">
    <rect x="0" y="0" width="180" height="92" rx="8" fill="#FAF9F5" stroke="#059669" stroke-width="2"/>
    <text x="90" y="24" fill="#047857" font-family="Inter" font-size="11.5" font-weight="800" text-anchor="middle">🔒 ZONE 2: Tool Runtime</text>
    <text x="90" y="44" fill="#141413" font-family="Inter" font-size="10" font-weight="700" text-anchor="middle">gVisor / Firecracker VM</text>
    <text x="90" y="62" fill="#6B6B63" font-family="Inter" font-size="9" text-anchor="middle">Strict Egress Allowlist</text>
    <text x="90" y="78" fill="#6B6B63" font-family="Inter" font-size="9" text-anchor="middle">5-Min Ephemeral Token</text>
  </g>
  <path d="M605 50 L622 50" stroke="#BD5D3A" stroke-width="2.5"/>

  <!-- Zone 3: Downstream Systems -->
  <g transform="translate(625, 5)">
    <rect x="0" y="0" width="165" height="92" rx="8" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <text x="82" y="24" fill="#BD5D3A" font-family="Inter" font-size="11.5" font-weight="800" text-anchor="middle">🏛️ ZONE 3: Downstream</text>
    <text x="82" y="44" fill="#141413" font-family="Inter" font-size="10" font-weight="700" text-anchor="middle">Scoped Target Tokens</text>
    <text x="82" y="62" fill="#6B6B63" font-family="Inter" font-size="9" text-anchor="middle">Postgres, GitHub, Stripe</text>
    <text x="82" y="78" fill="#6B6B63" font-family="Inter" font-size="9" text-anchor="middle">Zero Direct Zone 0 Path</text>
  </g>
</svg>'''
    elif 'COMPARING AGENT EXTENSION' in title_upper or 'MCP VS. CLI' in title_upper or 'COMPARE THEM' in title_upper:
        return '''<svg viewBox="0 0 800 100" class="slide-svg">
  <g transform="translate(10, 5)">
    <rect x="0" y="0" width="145" height="88" rx="8" fill="#FAF9F5" stroke="#2563eb" stroke-width="2"/>
    <text x="72" y="24" fill="#1e40af" font-family="Inter" font-size="11.5" font-weight="800" text-anchor="middle">⚡ MCP</text>
    <text x="72" y="44" fill="#141413" font-family="Inter" font-size="9.5" font-weight="700" text-anchor="middle">Universal Bridge</text>
    <text x="72" y="62" fill="#6B6B63" font-family="Inter" font-size="8.5" text-anchor="middle">For: AI Models</text>
    <text x="72" y="78" fill="#2563eb" font-family="Inter" font-size="8" font-weight="750" text-anchor="middle">JSON-RPC / stdio / HTTP</text>
  </g>
  <g transform="translate(165, 5)">
    <rect x="0" y="0" width="145" height="88" rx="8" fill="#FAF9F5" stroke="#4B5563" stroke-width="2"/>
    <text x="72" y="24" fill="#1F2937" font-family="Inter" font-size="11.5" font-weight="800" text-anchor="middle">💻 CLI</text>
    <text x="72" y="44" fill="#141413" font-family="Inter" font-size="9.5" font-weight="700" text-anchor="middle">Text-Based Terminal</text>
    <text x="72" y="62" fill="#6B6B63" font-family="Inter" font-size="8.5" text-anchor="middle">For: Humans / Scripts</text>
    <text x="72" y="78" fill="#4B5563" font-family="Inter" font-size="8" font-weight="750" text-anchor="middle">Subprocess Shell</text>
  </g>
  <g transform="translate(320, 5)">
    <rect x="0" y="0" width="150" height="88" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="75" y="24" fill="#BD5D3A" font-family="Inter" font-size="11.5" font-weight="800" text-anchor="middle">📦 Skill</text>
    <text x="75" y="44" fill="#141413" font-family="Inter" font-size="9.5" font-weight="700" text-anchor="middle">Packaged Capability</text>
    <text x="75" y="62" fill="#6B6B63" font-family="Inter" font-size="8.5" text-anchor="middle">For: AI Platforms</text>
    <text x="75" y="78" fill="#BD5D3A" font-family="Inter" font-size="8" font-weight="750" text-anchor="middle">SKILL.md / SOP Guides</text>
  </g>
  <g transform="translate(480, 5)">
    <rect x="0" y="0" width="150" height="88" rx="8" fill="#FAF9F5" stroke="#059669" stroke-width="2"/>
    <text x="75" y="24" fill="#047857" font-family="Inter" font-size="11.5" font-weight="800" text-anchor="middle">🔌 Plug-in</text>
    <text x="75" y="44" fill="#141413" font-family="Inter" font-size="9.5" font-weight="700" text-anchor="middle">Feature Add-on</text>
    <text x="75" y="62" fill="#6B6B63" font-family="Inter" font-size="8.5" text-anchor="middle">For: Host Apps</text>
    <text x="75" y="78" fill="#047857" font-family="Inter" font-size="8" font-weight="750" text-anchor="middle">plugin.json Manifest</text>
  </g>
  <g transform="translate(640, 5)">
    <rect x="0" y="0" width="150" height="88" rx="8" fill="#FAF9F5" stroke="#7c3aed" stroke-width="2"/>
    <text x="75" y="24" fill="#6d28d9" font-family="Inter" font-size="11.5" font-weight="800" text-anchor="middle">🪝 Hook</text>
    <text x="75" y="44" fill="#141413" font-family="Inter" font-size="9.5" font-weight="700" text-anchor="middle">Event Code Trigger</text>
    <text x="75" y="62" fill="#6B6B63" font-family="Inter" font-size="8.5" text-anchor="middle">For: Runtimes</text>
    <text x="75" y="78" fill="#6d28d9" font-family="Inter" font-size="8" font-weight="750" text-anchor="middle">settings.json Lifecycle</text>
  </g>
</svg>'''
    elif 'MULTI-AGENT DESIGN PATTERNS' in title_upper or '7 CORE ARCHITECTURAL TOPOLOGIES' in title_upper or 'MULTI-AGENT TOPOLOGIES' in title_upper:
        return '''<svg viewBox="0 0 800 105" class="slide-svg">
  <!-- 1. Orchestrator-Worker -->
  <g transform="translate(6, 6)">
    <rect x="0" y="0" width="106" height="92" rx="7" fill="#FAF9F5" stroke="#2563eb" stroke-width="1.8"/>
    <text x="53" y="20" fill="#1e40af" font-family="Inter" font-size="9.5" font-weight="800" text-anchor="middle">1. Orchestrator</text>
    <text x="53" y="38" fill="#141413" font-family="Inter" font-size="8" font-weight="700" text-anchor="middle">Central Router</text>
    <text x="53" y="56" fill="#6B6B63" font-family="Inter" font-size="7.5" text-anchor="middle">Delegates to N</text>
    <text x="53" y="74" fill="#2563eb" font-family="Inter" font-size="7.5" font-weight="750" text-anchor="middle">Dynamic Routing</text>
  </g>

  <!-- 2. Pipeline -->
  <g transform="translate(119, 6)">
    <rect x="0" y="0" width="106" height="92" rx="7" fill="#FAF9F5" stroke="#059669" stroke-width="1.8"/>
    <text x="53" y="20" fill="#047857" font-family="Inter" font-size="9.5" font-weight="800" text-anchor="middle">2. Pipeline</text>
    <text x="53" y="38" fill="#141413" font-family="Inter" font-size="8" font-weight="700" text-anchor="middle">Sequential Chain</text>
    <text x="53" y="56" fill="#6B6B63" font-family="Inter" font-size="7.5" text-anchor="middle">Stage Boundaries</text>
    <text x="53" y="74" fill="#047857" font-family="Inter" font-size="7.5" font-weight="750" text-anchor="middle">A ➔ B ➔ C Audit</text>
  </g>

  <!-- 3. Fan-out / Fan-in -->
  <g transform="translate(232, 6)">
    <rect x="0" y="0" width="106" height="92" rx="7" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="1.8"/>
    <text x="53" y="20" fill="#BD5D3A" font-family="Inter" font-size="9.5" font-weight="800" text-anchor="middle">3. Fan-Out/In</text>
    <text x="53" y="38" fill="#141413" font-family="Inter" font-size="8" font-weight="700" text-anchor="middle">Map–Reduce</text>
    <text x="53" y="56" fill="#6B6B63" font-family="Inter" font-size="7.5" text-anchor="middle">Parallel Chunks</text>
    <text x="53" y="74" fill="#BD5D3A" font-family="Inter" font-size="7.5" font-weight="750" text-anchor="middle">Reducer Merge</text>
  </g>

  <!-- 4. Critic-Refiner -->
  <g transform="translate(345, 6)">
    <rect x="0" y="0" width="106" height="92" rx="7" fill="#FAF9F5" stroke="#7c3aed" stroke-width="1.8"/>
    <text x="53" y="20" fill="#6d28d9" font-family="Inter" font-size="9.5" font-weight="800" text-anchor="middle">4. Critic-Refiner</text>
    <text x="53" y="38" fill="#141413" font-family="Inter" font-size="8" font-weight="700" text-anchor="middle">Self-Improvement</text>
    <text x="53" y="56" fill="#6B6B63" font-family="Inter" font-size="7.5" text-anchor="middle">Generator + Critic</text>
    <text x="53" y="74" fill="#6d28d9" font-family="Inter" font-size="7.5" font-weight="750" text-anchor="middle">Hard 2-3 Cap</text>
  </g>

  <!-- 5. Hierarchical -->
  <g transform="translate(458, 6)">
    <rect x="0" y="0" width="106" height="92" rx="7" fill="#FAF9F5" stroke="#2563eb" stroke-width="1.8"/>
    <text x="53" y="20" fill="#1e40af" font-family="Inter" font-size="9.5" font-weight="800" text-anchor="middle">5. Hierarchical</text>
    <text x="53" y="38" fill="#141413" font-family="Inter" font-size="8" font-weight="700" text-anchor="middle">Multi-Tier Trees</text>
    <text x="53" y="56" fill="#6B6B63" font-family="Inter" font-size="7.5" text-anchor="middle">Sub-Managers</text>
    <text x="53" y="74" fill="#1e40af" font-family="Inter" font-size="7.5" font-weight="750" text-anchor="middle">Abort Propagate</text>
  </g>

  <!-- 6. Event-Driven -->
  <g transform="translate(571, 6)">
    <rect x="0" y="0" width="106" height="92" rx="7" fill="#FAF9F5" stroke="#059669" stroke-width="1.8"/>
    <text x="53" y="20" fill="#047857" font-family="Inter" font-size="9.5" font-weight="800" text-anchor="middle">6. Event-Driven</text>
    <text x="53" y="38" fill="#141413" font-family="Inter" font-size="8" font-weight="700" text-anchor="middle">Message Bus</text>
    <text x="53" y="56" fill="#6B6B63" font-family="Inter" font-size="7.5" text-anchor="middle">Async Sub/Pub</text>
    <text x="53" y="74" fill="#047857" font-family="Inter" font-size="7.5" font-weight="750" text-anchor="middle">Decoupled Scale</text>
  </g>

  <!-- 7. Sidecar + HITL -->
  <g transform="translate(684, 6)">
    <rect x="0" y="0" width="108" height="92" rx="7" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="1.8"/>
    <text x="54" y="20" fill="#BD5D3A" font-family="Inter" font-size="9.5" font-weight="800" text-anchor="middle">7. Sidecar / HITL</text>
    <text x="54" y="38" fill="#141413" font-family="Inter" font-size="8" font-weight="700" text-anchor="middle">Guard Interceptor</text>
    <text x="54" y="56" fill="#6B6B63" font-family="Inter" font-size="7.5" text-anchor="middle">Risk Threshold</text>
    <text x="54" y="74" fill="#BD5D3A" font-family="Inter" font-size="7.5" font-weight="750" text-anchor="middle">Human Review</text>
  </g>
</svg>'''
    elif 'TEST TIERS' in title_upper or 'VERIFICATION PYRAMID' in title_upper:
        return '''<svg viewBox="0 0 800 105" class="slide-svg">
  <!-- 1. Functional Tiers -->
  <g transform="translate(15, 6)">
    <rect x="0" y="0" width="180" height="90" rx="8" fill="#FAF9F5" stroke="#2563eb" stroke-width="2"/>
    <text x="90" y="24" fill="#1e40af" font-family="Inter" font-size="11" font-weight="800" text-anchor="middle">🧪 1. Unit &amp; Integration</text>
    <text x="90" y="44" fill="#141413" font-family="Inter" font-size="9.5" font-weight="700" text-anchor="middle">Function &amp; Tool Contracts</text>
    <text x="90" y="62" fill="#6B6B63" font-family="Inter" font-size="8.5" text-anchor="middle">Fast, deterministic mocks</text>
    <text x="90" y="78" fill="#2563eb" font-family="Inter" font-size="8" font-weight="750" text-anchor="middle">Schema &amp; AST validation</text>
  </g>

  <!-- 2. System & UI -->
  <g transform="translate(210, 6)">
    <rect x="0" y="0" width="180" height="90" rx="8" fill="#FAF9F5" stroke="#059669" stroke-width="2"/>
    <text x="90" y="24" fill="#047857" font-family="Inter" font-size="11" font-weight="800" text-anchor="middle">🌐 2. E2E &amp; Full UI</text>
    <text x="90" y="44" fill="#141413" font-family="Inter" font-size="9.5" font-weight="700" text-anchor="middle">Multi-Turn Workflows</text>
    <text x="90" y="62" fill="#6B6B63" font-family="Inter" font-size="8.5" text-anchor="middle">Browser automation / DOM</text>
    <text x="90" y="78" fill="#047857" font-family="Inter" font-size="8" font-weight="750" text-anchor="middle">Full artifact verification</text>
  </g>

  <!-- 3. Regression & Scale -->
  <g transform="translate(405, 6)">
    <rect x="0" y="0" width="185" height="90" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="92" y="24" fill="#BD5D3A" font-family="Inter" font-size="11" font-weight="800" text-anchor="middle">⚡ 3. Regression &amp; Scale</text>
    <text x="92" y="44" fill="#141413" font-family="Inter" font-size="9.5" font-weight="700" text-anchor="middle">Permanent Bug Fixtures</text>
    <text x="92" y="62" fill="#6B6B63" font-family="Inter" font-size="8.5" text-anchor="middle">p50/p95/p99 Latency &amp; load</text>
    <text x="92" y="78" fill="#BD5D3A" font-family="Inter" font-size="8" font-weight="750" text-anchor="middle">Concurrency throughput</text>
  </g>

  <!-- 4. Security & Red Teaming -->
  <g transform="translate(605, 6)">
    <rect x="0" y="0" width="180" height="90" rx="8" fill="#FAF9F5" stroke="#E06C75" stroke-width="2"/>
    <text x="90" y="24" fill="#BD5D3A" font-family="Inter" font-size="11" font-weight="800" text-anchor="middle">🛡️ 4. Security / Red Team</text>
    <text x="90" y="44" fill="#141413" font-family="Inter" font-size="9.5" font-weight="700" text-anchor="middle">Pen-Testing &amp; Jailbreaks</text>
    <text x="90" y="62" fill="#6B6B63" font-family="Inter" font-size="8.5" text-anchor="middle">Prompt injection &amp; SSRF</text>
    <text x="90" y="78" fill="#E06C75" font-family="Inter" font-size="8" font-weight="750" text-anchor="middle">Credential leak defense</text>
  </g>
</svg>'''
    elif 'TDA LOOP' in title_upper:
        return '''<svg viewBox="0 0 800 100" class="slide-svg">
  <rect x="15" y="6" width="165" height="86" rx="10" fill="#FAF9F5" stroke="#D97757" stroke-width="2.2"/>
  <text x="97" y="34" fill="#141413" font-family="Inter" font-size="12.5" font-weight="800" text-anchor="middle">1. RED: Failing Test</text>
  <text x="97" y="60" fill="#6B6B63" font-family="Inter" font-size="10.5" text-anchor="middle">From SPEC.md Criteria</text>
  <path d="M180 49 L215 49" stroke="#BD5D3A" stroke-width="3.5"/>
  <rect x="215" y="6" width="165" height="86" rx="10" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2.2"/>
  <text x="297" y="34" fill="#141413" font-family="Inter" font-size="12.5" font-weight="800" text-anchor="middle">2. Agent Edit</text>
  <text x="297" y="60" fill="#6B6B63" font-family="Inter" font-size="10.5" text-anchor="middle">Code Implementation</text>
  <path d="M380 49 L415 49" stroke="#D97757" stroke-width="3.5"/>
  <rect x="415" y="6" width="175" height="86" rx="10" fill="#FAF9F5" stroke="#D97757" stroke-width="2.2"/>
  <text x="502" y="34" fill="#141413" font-family="Inter" font-size="12.5" font-weight="800" text-anchor="middle">3. Pytest Subprocess</text>
  <text x="502" y="60" fill="#BD5D3A" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">Extract Real Traceback</text>
  <path d="M590 49 L625 49" stroke="#BD5D3A" stroke-width="3.5"/>
  <rect x="625" y="6" width="160" height="86" rx="10" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2.2"/>
  <text x="705" y="34" fill="#141413" font-family="Inter" font-size="12.5" font-weight="800" text-anchor="middle">4. Anti-Regression</text>
  <text x="705" y="60" fill="#141413" font-family="Inter" font-size="11.5" font-weight="700" text-anchor="middle">Lock Test in Suite</text>
</svg>'''
    elif 'FIVE-STEP SOP' in title_upper:
        return '''<svg viewBox="0 0 800 100" class="slide-svg">
  <g transform="translate(10, 5)">
    <rect x="0" y="0" width="145" height="86" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="72" y="28" fill="#141413" font-family="Inter" font-size="11.5" font-weight="800" text-anchor="middle">1. Spec First</text>
    <text x="72" y="52" fill="#4A4A44" font-family="Inter" font-size="10" text-anchor="middle">parse_spec(SPEC.md)</text>
  </g>
  <g transform="translate(165, 5)">
    <rect x="0" y="0" width="145" height="86" rx="8" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <text x="72" y="28" fill="#141413" font-family="Inter" font-size="11.5" font-weight="800" text-anchor="middle">2. Sandbox</text>
    <text x="72" y="52" fill="#4A4A44" font-family="Inter" font-size="10" text-anchor="middle">ScopeEnforcer write</text>
  </g>
  <g transform="translate(320, 5)">
    <rect x="0" y="0" width="145" height="86" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="72" y="28" fill="#141413" font-family="Inter" font-size="11.5" font-weight="800" text-anchor="middle">3. Guardrails</text>
    <text x="72" y="52" fill="#4A4A44" font-family="Inter" font-size="10" text-anchor="middle">AST &amp; Secret Scan</text>
  </g>
  <g transform="translate(475, 5)">
    <rect x="0" y="0" width="145" height="86" rx="8" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
    <text x="72" y="28" fill="#141413" font-family="Inter" font-size="11.5" font-weight="800" text-anchor="middle">4. Test Loop</text>
    <text x="72" y="52" fill="#4A4A44" font-family="Inter" font-size="10.5" text-anchor="middle">Pytest Subprocess</text>
  </g>
  <g transform="translate(630, 5)">
    <rect x="0" y="0" width="155" height="86" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="77" y="28" fill="#141413" font-family="Inter" font-size="11.5" font-weight="800" text-anchor="middle">5. Human Review</text>
    <text x="77" y="52" fill="#141413" font-family="Inter" font-size="10.5" font-weight="700" text-anchor="middle">Diff &amp; PR Merge</text>
  </g>
</svg>'''
    elif 'SCORECARD' in title_upper or 'WRAP-UP' in title_upper or 'READINESS' in title_upper:
        return '''<svg viewBox="0 0 800 100" class="slide-svg">
  <rect x="15" y="6" width="770" height="86" rx="14" fill="#FAF9F5" stroke="#D97757" stroke-width="2.5"/>
  <text x="400" y="36" fill="#141413" font-family="Inter" font-size="15" font-weight="900" text-anchor="middle">PRODUCTION READINESS SCORECARD: ALL 5 GATES PASS</text>
  <text x="400" y="58" fill="#141413" font-family="Inter" font-size="12" font-weight="700" text-anchor="middle">✓ Memory (AGENTS.md)  ✓ Sandboxing  ✓ PreToolUse Hooks  ✓ TDA Pytest  ✓ MCP Tools</text>
  <text x="400" y="78" fill="#6B6B63" font-family="Inter" font-size="10.5" text-anchor="middle">Verified Harness Engineering Control &amp; Reliability Framework (10 Modules)</text>
</svg>'''
    else:
        return ''

# Pre-render syntax highlighted code with line numbers and key highlights for all slides that have code_block
for s in slides:
    if s.get('code_block'):
        hl_lines = s.get('highlight_lines', [])
        s['highlighted_code'] = highlight_python(s['code_block'], hl_lines)

svg_all = {}
for s in slides:
    num = s['number']
    title = s['raw_lines'][0] if s.get('raw_lines') else f'Slide {num}'
    svg_all[num] = generate_svg_for_slide(num, title)

svg_json = json.dumps(svg_all)

html_template = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Packt Masterclass Presentation: 85 Interactive Code, Architecture & Skill Slides</title>
  <link rel="icon" type="image/svg+xml" href="favicon.svg">
  <link rel="icon" type="image/png" sizes="192x192" href="favicon.png">
  <link rel="apple-touch-icon" sizes="180x180" href="favicon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #F0EEE6;
      --surface: #FAF9F5;
      --surface-alt: #F5E6DF;
      --ink: #141413;
      --ink-muted: #6B6B63;
      --rule: #E3E0D6;
      --accent: #D97757;
      --accent-dk: #BD5D3A;
      --accent-sf: #F5E6DF;
      --code-bg: #1A1A18;
      --code-rule: #333330;
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
      height: 46px;
      flex: 0 0 46px;
      background: var(--surface);
      border-bottom: 1px solid var(--rule);
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0 1.0rem;
      z-index: 50;
      gap: 0.75rem;
      overflow-x: auto;
    }
    .header-left { display: flex; align-items: center; gap: 0.7rem; flex: 0 0 auto; }
    .brand-logo {
      width: 30px; height: 30px;
      background: var(--accent-sf); color: var(--ink); border: 1px solid var(--rule);
      border-radius: 8px; font-weight: 800; display: flex; align-items: center; justify-content: center;
      font-size: 0.85rem;
    }
    .brand-title { font-weight: 650; font-size: 0.90rem; white-space: nowrap; }

    .controls { display: flex; align-items: center; gap: 0.40rem; flex: 0 0 auto; }
    .btn {
      background: var(--surface); border: 1px solid var(--rule); color: var(--ink);
      padding: 0.35rem 0.65rem; border-radius: 8px; font-weight: 600; font-size: 0.80rem;
      cursor: pointer; transition: background-color 0.16s, border-color 0.16s; text-decoration: none;
      white-space: nowrap;
    }
    .btn:hover { background: var(--accent-sf); border-color: var(--accent); }
    .btn:focus-visible, .slide-select:focus-visible, .goto-input:focus-visible { outline: 2px solid var(--accent-dk); outline-offset: 2px; }
    .btn-primary { background: var(--accent); border-color: var(--accent); color: var(--ink); font-weight: 700; }
    .btn-primary:hover { background: var(--accent-sf); border-color: var(--accent-dk); color: var(--ink); }
    
    .goto-group {
      display: flex;
      align-items: center;
      gap: 0.22rem;
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
      -moz-appearance: textfield;
    }
    .goto-input::-webkit-outer-spin-button,
    .goto-input::-webkit-inner-spin-button {
      -webkit-appearance: none;
      margin: 0;
    }
    .btn-goto {
      padding: 0.26rem 0.50rem;
      font-weight: 700;
      font-size: 0.78rem;
    }

    select.slide-select {
      background: var(--surface); color: var(--ink); border: 1px solid var(--rule);
      padding: 0.35rem 0.55rem; border-radius: 8px; font-family: var(--font-body);
      font-size: 0.80rem; font-weight: 600;
      max-width: 290px;
    }

    main {
      flex: 1;
      position: relative;
      overflow: hidden;
    }

    .slide-viewport {
      width: 100%; height: 100%;
      display: flex; justify-content: center; align-items: center;
      padding: clamp(0.30rem, 0.8vw, 0.70rem);
    }
    .slide-card {
      width: 100%; max-width: 1380px; height: 100%;
      background: var(--surface); border: 1px solid var(--rule);
      border-radius: 12px; padding: clamp(0.80rem, 1.5vw, 1.40rem); display: flex; flex-direction: column;
      position: relative; overflow: hidden;
    }
    .slide-header {
      display: flex; justify-content: space-between; align-items: center;
      gap: 0.8rem; margin-bottom: 0.35rem; border-bottom: 1px solid var(--rule); padding-bottom: 0.35rem;
      flex: 0 0 auto;
    }
    .slide-title-wrap { min-width: 0; }
    .slide-title {
      font-family: var(--font-display); font-size: clamp(1.40rem, 2.2vw, 1.95rem);
      font-weight: 700; line-height: 1.15; letter-spacing: -0.015em; color: var(--ink);
    }
    .slide-num-badge {
      background: var(--accent-sf); color: var(--ink); border: 1px solid var(--rule);
      padding: 0.22rem 0.60rem; border-radius: 9999px; font-size: 0.78rem; font-weight: 750; white-space: nowrap;
      flex: 0 0 auto;
    }
    .slide-body {
      --fit-scale: 1;
      --slide-body-base-size: 1.30rem;
      flex: 1; min-height: 0; overflow-y: auto; padding-right: 0.20rem;
      font-size: calc(var(--slide-body-base-size) * var(--fit-scale));
      line-height: 1.50; color: var(--ink);
    }

    code {
      font-family: var(--font-code);
      background: var(--accent-sf);
      color: var(--accent-dk);
      padding: 0.08rem 0.32rem;
      border-radius: 4px;
      font-size: 0.90em;
      white-space: nowrap;
      border: 1px solid var(--rule);
    }
    pre code, .tree-block code, .code-editor-body code {
      white-space: pre !important;
      background: transparent !important;
      border: none !important;
      padding: 0 !important;
      color: inherit !important;
    }
    .slide-content-wrapper {
      width: 100%;
      display: block;
    }
    .slide-body > svg, .slide-svg {
      display: block; width: 100% !important; height: auto; max-width: 100%;
      margin: 0.35rem 0 0.65rem 0;
    }

    /* Comparison Table Styling */
    .slide-table {
      width: 100%;
      border-collapse: collapse;
      margin: 0.35rem 0 0.60rem 0;
      font-size: 0.88rem;
      background: var(--surface);
      border: 1px solid var(--rule);
      border-radius: 8px;
      overflow: hidden;
      box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    .slide-table th {
      background: var(--accent-sf);
      color: var(--ink);
      font-weight: 750;
      text-align: left;
      padding: 0.45rem 0.70rem;
      border-bottom: 1.5px solid var(--rule);
      font-family: var(--font-display);
      font-size: 0.95rem;
    }
    .slide-table td {
      padding: 0.40rem 0.70rem;
      border-bottom: 1px solid var(--rule);
      color: var(--ink);
      line-height: 1.38;
      vertical-align: middle;
    }
    .slide-table tr:last-child td {
      border-bottom: none;
    }
    .slide-table tr:nth-child(even) td {
      background: rgba(245, 230, 223, 0.25);
    }

    /* Enhanced Code Slide Layout with Line-Level Highlights */
    .code-slide-container {
      display: grid;
      grid-template-columns: minmax(0, 1.32fr) minmax(0, 1.08fr);
      gap: 1.05rem;
      height: 100%;
      align-items: start;
    }
    @media (max-width: 1020px) {
      .code-slide-container {
        grid-template-columns: 1fr;
        height: auto;
      }
    }

    .code-editor-window {
      background: var(--code-bg);
      border: 1px solid var(--code-rule);
      border-radius: 10px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      box-shadow: 0 4px 16px rgba(0,0,0,0.14);
      max-height: calc(100vh - 135px);
    }
    .code-editor-header {
      background: #242320;
      border-bottom: 1px solid var(--code-rule);
      padding: 0.40rem 0.75rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 0.5rem;
    }
    .code-dots {
      display: flex;
      gap: 5px;
      align-items: center;
    }
    .code-dot {
      width: 9px; height: 9px; border-radius: 50%;
    }
    .dot-red { background: #E06C75; }
    .dot-yellow { background: #E5C07B; }
    .dot-green { background: #98C379; }
    .code-file-tag {
      font-family: var(--font-code);
      font-size: 0.78rem;
      color: #A0A09A;
      font-weight: 500;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .code-lang-tag {
      background: #333330;
      color: #D97757;
      font-family: var(--font-code);
      font-size: 0.70rem;
      padding: 0.12rem 0.45rem;
      border-radius: 4px;
      font-weight: 600;
      text-transform: uppercase;
    }

    .code-block {
      background: var(--code-bg);
      color: #FAF9F5;
      font-family: var(--font-code);
      font-size: 0.86rem;
      line-height: 1.42;
      padding: 0.45rem 0;
      margin: 0;
      overflow-x: auto;
      overflow-y: auto;
    }

    .code-line {
      display: flex;
      align-items: baseline;
      padding: 0.06rem 0.55rem;
      transition: background-color 0.15s;
    }
    .code-line:hover {
      background: rgba(255, 255, 255, 0.04);
    }
    .code-line-hl {
      background: rgba(217, 119, 87, 0.22);
      border-left: 3.5px solid var(--accent);
      padding-left: calc(0.55rem - 3.5px);
    }
    .line-num {
      color: #5C5C56;
      width: 24px;
      flex: 0 0 24px;
      text-align: right;
      margin-right: 8px;
      font-size: 0.78rem;
      user-select: none;
    }
    .code-line-hl .line-num {
      color: var(--accent);
      font-weight: 700;
    }
    .key-badge {
      background: var(--accent);
      color: #FAF9F5;
      font-size: 0.62rem;
      font-weight: 800;
      padding: 0.05rem 0.35rem;
      border-radius: 3px;
      margin-right: 8px;
      letter-spacing: 0.03em;
      user-select: none;
      flex: 0 0 auto;
    }
    .line-code {
      flex: 1;
      white-space: pre;
    }

    /* Syntax Highlighting Colors */
    .tok-kw { color: #E58A6D; font-weight: 600; }
    .tok-str { color: #89CA78; }
    .tok-com { color: #7F7F78; font-style: italic; }
    .tok-dec { color: #E5C07B; font-weight: 600; }
    .tok-typ { color: #61AFEF; font-weight: 600; }
    .tok-fn { color: #61AFEF; font-weight: 600; }
    .tok-cls { color: #E5C07B; font-weight: 700; }

    /* Code Slide Dedicated Concepts Column */
    .code-concepts-column {
      display: flex;
      flex-direction: column;
      gap: 0.60rem;
      overflow-y: auto;
      max-height: calc(100vh - 135px);
      padding-right: 0.20rem;
    }
    .code-concepts-list {
      display: flex;
      flex-direction: column;
      gap: 0.55rem;
    }
    .code-concept-card {
      background: var(--surface);
      border: 1px solid var(--rule);
      border-left: 3.5px solid var(--accent);
      border-radius: 8px;
      padding: 0.65rem 0.90rem;
      box-shadow: 0 1px 4px rgba(0,0,0,0.03);
    }
    .concept-card-head {
      display: flex;
      align-items: center;
      gap: 0.45rem;
      margin-bottom: 0.25rem;
      flex-wrap: wrap;
    }
    .concept-tag {
      background: var(--accent);
      color: #FAF9F5;
      font-size: 0.70rem;
      font-weight: 750;
      padding: 0.10rem 0.42rem;
      border-radius: 4px;
      font-family: var(--font-code);
      letter-spacing: 0.02em;
      white-space: nowrap;
    }
    .concept-name {
      font-family: var(--font-display);
      font-size: 1.02rem;
      font-weight: 700;
      color: var(--ink);
    }
    .concept-card-text {
      font-size: 0.92rem;
      color: var(--ink);
      line-height: 1.42;
    }

    .invariant-card {
      background: var(--surface);
      border: 1px solid var(--rule);
      border-left: 3.5px solid var(--accent-dk);
      border-radius: 8px;
      padding: 0.65rem 0.90rem;
      font-size: 0.88rem;
      color: var(--ink-muted);
      line-height: 1.40;
    }
    .invariant-title {
      font-family: var(--font-display);
      font-size: 1.00rem;
      font-weight: 700;
      color: var(--ink);
      margin-bottom: 0.22rem;
      display: flex;
      align-items: center;
      gap: 0.35rem;
    }

    /* Dedicated Skill Slide Layout */
    .skill-slide-layout {
      display: grid;
      grid-template-columns: minmax(0, 1.0fr) minmax(0, 1.15fr);
      gap: 1.25rem;
      height: 100%;
      align-items: start;
    }
    @media (max-width: 980px) {
      .skill-slide-layout {
        grid-template-columns: 1fr;
        height: auto;
      }
    }
    .skill-meta-card {
      background: var(--surface);
      border: 1.5px solid var(--accent);
      border-radius: 10px;
      padding: 1.10rem;
      display: flex;
      flex-direction: column;
      gap: 0.70rem;
      box-shadow: 0 4px 14px rgba(217, 119, 87, 0.08);
    }
    .skill-meta-badge {
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      background: var(--accent-sf);
      color: var(--accent-dk);
      border: 1px solid var(--accent);
      font-family: var(--font-code);
      font-weight: 800;
      font-size: 0.84rem;
      padding: 0.24rem 0.60rem;
      border-radius: 6px;
      width: fit-content;
    }
    .skill-name-heading {
      font-family: var(--font-code);
      font-size: 1.30rem;
      font-weight: 800;
      color: var(--ink);
      word-break: break-all;
    }
    .skill-desc-box {
      background: #FAF8F2;
      border: 1px solid var(--rule);
      border-left: 3.5px solid var(--accent);
      border-radius: 6px;
      padding: 0.70rem 0.90rem;
      font-size: 0.96rem;
      line-height: 1.46;
      color: var(--ink);
    }
    .skill-tools-box {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-size: 0.92rem;
      font-weight: 600;
      color: var(--ink);
    }
    .skill-links-box {
      font-size: 0.88rem;
      color: var(--ink-muted);
      margin-top: 0.3rem;
      line-height: 1.46;
      display: flex;
      flex-direction: column;
      gap: 0.38rem;
      border-top: 1px dashed var(--rule);
      padding-top: 0.55rem;
    }
    .skill-details-column {
      display: flex;
      flex-direction: column;
      gap: 0.70rem;
      overflow-y: auto;
      max-height: calc(100vh - 135px);
    }
    .skill-detail-card {
      background: var(--surface);
      border: 1px solid var(--rule);
      border-left: 3.5px solid var(--accent-dk);
      border-radius: 8px;
      padding: 0.75rem 1.00rem;
    }
    .skill-detail-title {
      font-family: var(--font-display);
      font-size: 1.08rem;
      font-weight: 750;
      color: var(--ink);
      margin-bottom: 0.30rem;
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }
    .skill-detail-body {
      font-size: 0.94rem;
      color: var(--ink);
      line-height: 1.44;
    }

    /* Monospace Tree Display for Structure Slides */
    .tree-block {
      background: var(--code-bg);
      color: #FAF9F5;
      font-family: var(--font-code);
      font-size: 0.86rem;
      line-height: 1.44;
      padding: 0.80rem 1.05rem;
      border-radius: 8px;
      border: 1px solid var(--code-rule);
      margin: 0.45rem 0;
      overflow-x: auto;
    }

    /* Visual Hierarchy: Parent vs Sub Bullets */
    .main-bullets { list-style-type: none; padding-left: 0; margin-top: 0.30rem; }
    .main-bullets.dense-columns {
      column-count: 2; column-gap: clamp(1.2rem, 3vw, 2.5rem); column-fill: balance;
    }
    .bullet-group, .primary-bullet, .sub-bullets, .sub-bullet {
      break-inside: avoid; page-break-inside: avoid;
    }
    .primary-bullet {
      font-family: var(--font-display); font-size: 1.04em; font-weight: 650; color: var(--ink);
      margin-top: 0.35em; margin-bottom: 0.18em; position: relative; padding-left: 1.25em; line-height: 1.46;
    }
    .primary-bullet::before {
      content: "◆"; color: var(--accent); font-size: 0.72em; line-height: 1; position: absolute; left: 0; top: 0.18em;
    }
    .sub-bullets {
      list-style-type: none; padding-left: 1.25em; border-left: 2px solid var(--rule);
      margin-left: 0.40em; margin-top: 0.20em; margin-bottom: 0.40em; display: flex; flex-direction: column; gap: 0.22em;
    }
    .sub-bullet {
      font-size: 0.92em; color: var(--ink); margin-bottom: 0.15em; position: relative; padding-left: 1.15em;
      line-height: 1.42;
    }
    .sub-bullet::before {
      content: "›"; position: absolute; left: 0; top: -0.05em; color: var(--accent-dk); font-weight: 900; font-size: 1.25em; line-height: 1;
    }
    .slide-lead-header {
      font-family: var(--font-display);
      font-size: 1.15em;
      font-weight: 750;
      color: var(--accent-dk);
      margin-top: 0.15em;
      margin-bottom: 0.40em;
      letter-spacing: -0.01em;
      display: flex;
      align-items: center;
      gap: 0.4em;
    }

    /* Capstone Slide 83 Two-Column Grid */
    .capstone-layout-grid {
      display: grid;
      grid-template-columns: minmax(0, 1.08fr) minmax(0, 0.92fr);
      gap: 0.90rem;
      height: 100%;
      align-items: stretch;
    }
    @media (max-width: 1040px) {
      .capstone-layout-grid {
        grid-template-columns: 1fr;
        height: auto;
      }
    }
    .capstone-info-card {
      background: var(--surface);
      border: 1.5px solid var(--rule);
      border-radius: 10px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      box-shadow: 0 3px 12px rgba(0,0,0,0.04);
    }
    .capstone-info-body {
      padding: 0.60rem 0.80rem;
      display: flex;
      flex-direction: column;
      gap: 0.50rem;
      font-size: 0.84rem;
      background: var(--surface);
      flex: 1;
    }
    .capstone-section {
      display: flex;
      flex-direction: column;
      gap: 0.22rem;
    }
    .capstone-section-title {
      font-family: var(--font-display);
      font-size: 0.84rem;
      font-weight: 750;
      color: var(--accent-dk);
    }
    .capstone-cmd-box {
      background: #FAF8F2;
      border: 1px solid var(--rule);
      border-radius: 6px;
      padding: 0.35rem 0.55rem;
      display: flex;
      flex-direction: column;
      gap: 0.22rem;
      font-size: 0.77rem;
    }
    .capstone-cmd-box code {
      font-size: 0.78rem;
      padding: 0.08rem 0.28rem;
    }
    .cmd-note {
      color: var(--ink-muted);
      font-size: 0.75rem;
      margin-left: 0.25rem;
    }
    .capstone-providers-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0.25rem;
      font-size: 0.75rem;
    }
    .provider-pill {
      background: #FAF8F2;
      border: 1px solid var(--rule);
      border-radius: 5px;
      padding: 0.22rem 0.40rem;
      line-height: 1.25;
    }
    .capstone-text-desc {
      font-size: 0.78rem;
      line-height: 1.38;
      color: var(--ink);
      background: #FAF8F2;
      border: 1px solid var(--rule);
      border-radius: 6px;
      padding: 0.35rem 0.55rem;
    }

    /* Slide 3 Course Master Map: Two-Column Part 1 (Left) & Part 2 (Right) */
    .course-map-slide-wrap {
      width: 100%;
      height: 100%;
      display: flex;
      flex-direction: column;
      gap: 0.65rem;
    }
    .course-map-columns-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1.10rem;
      flex: 1;
      align-items: stretch;
    }
    .course-map-part-col {
      background: var(--surface);
      border: 1.5px solid var(--rule);
      border-radius: 8px;
      padding: 0.85rem 1.15rem;
      display: flex;
      flex-direction: column;
      box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    .course-map-part-header {
      font-family: var(--font-display);
      font-size: 1.12rem;
      font-weight: 800;
      color: var(--accent-dk);
      letter-spacing: -0.01em;
      margin-bottom: 0.65rem;
      padding-bottom: 0.40rem;
      border-bottom: 1.5px solid var(--rule);
      display: flex;
      align-items: center;
      gap: 0.45rem;
    }
    .course-map-module-list {
      list-style: none;
      padding: 0;
      margin: 0;
      display: flex;
      flex-direction: column;
      gap: 0.55rem;
      font-size: 1.02rem;
      color: var(--ink);
    }
    .course-map-module-list li {
      display: flex;
      align-items: baseline;
      gap: 0.55rem;
      line-height: 1.40;
    }
    .course-map-module-list .mod-bullet {
      color: var(--accent);
      font-size: 0.75rem;
      flex-shrink: 0;
    }

    /* Reference Slide with Two-Table Layout (Links Table + Screenshot Table) */
    .reference-tables-grid {
      display: grid;
      grid-template-columns: minmax(0, 1.28fr) minmax(0, 1.02fr);
      gap: 1.10rem;
      height: 100%;
      align-items: start;
    }
    @media (max-width: 1040px) {
      .reference-tables-grid {
        grid-template-columns: 1fr;
        height: auto;
      }
    }
    .ref-table-card {
      background: var(--surface);
      border: 1.5px solid var(--rule);
      border-radius: 10px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      box-shadow: 0 3px 12px rgba(0,0,0,0.04);
    }
    .ref-table-card-header {
      background: var(--accent-sf);
      color: var(--ink);
      font-family: var(--font-display);
      font-weight: 750;
      font-size: 1.02rem;
      padding: 0.50rem 0.85rem;
      border-bottom: 1.5px solid var(--rule);
      display: flex;
      align-items: center;
      gap: 0.40rem;
    }
    .ref-table {
      width: 100%;
      border-collapse: collapse;
      margin: 0 !important;
      background: var(--surface);
    }
    .ref-table th {
      background: #F0EEE6;
      color: var(--ink);
      font-weight: 750;
      text-align: left;
      padding: 0.45rem 0.70rem;
      border-bottom: 1.5px solid var(--rule);
      font-size: 0.88rem;
    }
    .ref-table td {
      padding: 0.45rem 0.70rem;
      border-bottom: 1px solid var(--rule);
      font-size: 0.86rem;
      line-height: 1.38;
      vertical-align: middle;
    }
    .ref-table tr:last-child td {
      border-bottom: none;
    }
    .ref-table tr:nth-child(even) td {
      background: rgba(245, 230, 223, 0.22);
    }
    .book-screenshot-link {
      display: flex;
      flex-direction: column;
      align-items: center;
      background: var(--surface);
      border: 1px solid var(--rule);
      border-radius: 8px;
      padding: 0.45rem;
      text-decoration: none;
      box-shadow: 0 3px 12px rgba(0,0,0,0.06);
      transition: transform 0.18s, border-color 0.18s, box-shadow 0.18s;
      max-height: calc(100vh - 170px);
    }
    .book-screenshot-link:hover {
      transform: translateY(-2px);
      border-color: var(--accent);
      box-shadow: 0 6px 20px rgba(217, 119, 87, 0.18);
    }
    .book-screenshot-img {
      max-width: 100%;
      max-height: calc(100vh - 220px);
      height: auto;
      border-radius: 6px;
      border: 1px solid var(--rule);
      object-fit: contain;
    }
    .book-screenshot-badge {
      margin-top: 0.40rem;
      font-size: 0.80rem;
      font-weight: 750;
      color: var(--accent-dk);
      display: flex;
      align-items: center;
      gap: 0.30rem;
    }

    /* Instructor Slide with 8-Book Gallery Grid */
    .instructor-slide-grid {
      display: grid;
      grid-template-columns: minmax(0, 1.02fr) minmax(0, 1.25fr);
      gap: 1.25rem;
      height: 100%;
      align-items: start;
    }
    @media (max-width: 1040px) {
      .instructor-slide-grid {
        grid-template-columns: 1fr;
        height: auto;
      }
    }
    .instructor-info-col {
      display: flex;
      flex-direction: column;
      gap: 0.60rem;
      min-width: 0;
    }
    .instructor-info-col .main-bullets,
    .instructor-info-col .main-bullets.dense-columns,
    .instructor-info-col .bullet-list {
      columns: 1 !important;
      column-gap: 0 !important;
      display: flex;
      flex-direction: column;
      gap: 0.45rem;
      font-size: 0.98rem;
    }
    .instructor-info-col .primary-bullet {
      line-height: 1.50;
      margin-bottom: 0.25rem;
    }
    .author-books-card {
      background: var(--surface);
      border: 1.5px solid var(--rule);
      border-radius: 10px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      box-shadow: 0 3px 12px rgba(0,0,0,0.04);
    }
    .author-books-header {
      background: var(--accent-sf);
      color: var(--ink);
      font-family: var(--font-display);
      font-weight: 750;
      font-size: 0.88rem;
      padding: 0.45rem 0.80rem;
      border-bottom: 1.5px solid var(--rule);
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 0.50rem;
      white-space: nowrap;
    }
    .author-books-header a {
      font-family: var(--font-body);
      font-size: 0.76rem;
      font-weight: 750;
      color: var(--accent-dk);
      text-decoration: underline;
      white-space: nowrap;
      flex-shrink: 0;
    }

    /* Slide 1 Hero & Instructor Cover Layout */
    .slide-1-container {
      width: 100%;
      height: 100%;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 0.85rem;
    }
    .slide-1-hero-card {
      background: var(--surface);
      border: 1.5px solid var(--rule);
      border-left: 5px solid var(--accent);
      border-radius: 12px;
      padding: 1.10rem 1.50rem;
      box-shadow: 0 4px 16px rgba(0,0,0,0.04);
      display: flex;
      flex-direction: column;
      gap: 0.45rem;
    }
    .slide-1-hero-tagline {
      font-family: var(--font-display);
      font-size: 1.25rem;
      font-weight: 700;
      color: var(--accent-dk);
      line-height: 1.35;
    }
    .slide-1-hero-desc {
      font-size: 0.95rem;
      color: var(--ink);
      line-height: 1.45;
    }
    .slide-1-instructor-card {
      background: var(--surface);
      border: 1.5px solid var(--rule);
      border-radius: 12px;
      padding: 1.15rem 1.50rem;
      display: flex;
      align-items: center;
      gap: 1.50rem;
      box-shadow: 0 4px 16px rgba(0,0,0,0.04);
    }
    .slide-1-avatar-wrap {
      position: relative;
      flex-shrink: 0;
    }
    .slide-1-avatar-img {
      width: 100px;
      height: 100px;
      border-radius: 50%;
      object-fit: cover;
      border: 3px solid var(--accent);
      box-shadow: 0 4px 12px rgba(217, 119, 87, 0.25);
      background: var(--surface-alt);
    }
    .slide-1-instructor-info {
      display: flex;
      flex-direction: column;
      gap: 0.35rem;
      flex: 1;
    }
    .slide-1-instructor-badge {
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      background: var(--accent-sf);
      color: var(--accent-dk);
      border: 1px solid var(--accent);
      font-family: var(--font-code);
      font-size: 0.75rem;
      font-weight: 750;
      padding: 0.18rem 0.55rem;
      border-radius: 6px;
      width: fit-content;
      text-transform: uppercase;
      letter-spacing: 0.03em;
    }
    .slide-1-instructor-name {
      font-family: var(--font-display);
      font-size: 1.75rem;
      font-weight: 800;
      color: var(--ink);
      line-height: 1.15;
    }
    .slide-1-instructor-titles {
      display: flex;
      flex-direction: column;
      gap: 0.25rem;
      margin-top: 0.15rem;
    }
    .slide-1-title-item {
      display: flex;
      align-items: center;
      gap: 0.50rem;
      font-size: 1.05rem;
      font-weight: 650;
      color: var(--ink);
    }
    .slide-1-title-item .title-icon {
      font-size: 1.15rem;
      flex-shrink: 0;
    }
    .slide-1-title-highlight {
      color: var(--accent-dk);
      font-weight: 750;
    }
    .slide-1-pillars-row {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 0.75rem;
    }
    @media (max-width: 900px) {
      .slide-1-pillars-row {
        grid-template-columns: repeat(2, 1fr);
      }
      .slide-1-instructor-card {
        flex-direction: column;
        text-align: center;
        align-items: center;
      }
      .slide-1-instructor-badge {
        margin: 0 auto;
      }
      .slide-1-title-item {
        justify-content: center;
      }
    }
    .slide-1-pillar-pill {
      background: var(--surface);
      border: 1px solid var(--rule);
      border-radius: 8px;
      padding: 0.55rem 0.75rem;
      display: flex;
      flex-direction: column;
      gap: 0.15rem;
      box-shadow: 0 2px 6px rgba(0,0,0,0.02);
    }
    .slide-1-pillar-title {
      font-family: var(--font-display);
      font-size: 0.88rem;
      font-weight: 750;
      color: var(--ink);
      display: flex;
      align-items: center;
      gap: 0.35rem;
    }
    .slide-1-pillar-desc {
      font-size: 0.75rem;
      color: var(--ink-muted);
      line-height: 1.30;
    }
    .books-gallery-grid {
      display: grid;
      grid-template-columns: repeat(6, 1fr);
      gap: 0.40rem;
      padding: 0.50rem;
      background: #FAF8F2;
    }
    .book-item-card {
      display: flex;
      flex-direction: column;
      align-items: center;
      background: var(--surface);
      border: 1px solid var(--rule);
      border-radius: 6px;
      padding: 0.25rem 0.20rem;
      text-decoration: none;
      box-shadow: 0 2px 6px rgba(0,0,0,0.04);
      transition: transform 0.16s, border-color 0.16s, box-shadow 0.16s;
    }
    .book-item-card:hover {
      transform: translateY(-2px);
      border-color: var(--accent);
      box-shadow: 0 4px 12px rgba(217, 119, 87, 0.18);
    }
    .book-cover-img {
      width: 100%;
      height: clamp(80px, 11.5vh, 115px);
      object-fit: contain;
      border-radius: 4px;
      border: 0.5px solid var(--rule);
    }
    .book-item-title {
      font-size: 0.58rem;
      font-weight: 700;
      color: var(--ink);
      text-align: center;
      line-height: 1.15;
      margin-top: 0.20rem;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      width: 100%;
      display: block;
    }
    .book-publisher-tag {
      font-size: 0.48rem;
      font-weight: 800;
      color: var(--accent-dk);
      background: var(--accent-sf);
      padding: 0.05rem 0.20rem;
      border-radius: 3px;
      margin-top: 0.12rem;
      text-transform: uppercase;
      letter-spacing: 0.02em;
      white-space: nowrap;
      line-height: 1.1;
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
      color: var(--ink); padding: 0.1rem 0.35rem; border-radius: 5px;
      font-family: var(--font-code); font-size: 0.88em; font-weight: 600;
      overflow-wrap: anywhere;
    }

    /* Slide 3: Course Core Thesis (Traditional SE vs Harness Engineering) */
    .thesis-slide-wrap {
      width: 100%;
      height: 100%;
      display: flex;
      flex-direction: column;
      gap: 0.45rem;
    }
    .thesis-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0.85rem;
      flex: 1;
      align-items: stretch;
    }
    @media (max-width: 1040px) {
      .thesis-grid {
        grid-template-columns: 1fr;
        height: auto;
      }
    }
    .thesis-card {
      background: var(--surface);
      border: 1.5px solid var(--rule);
      border-radius: 9px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    .thesis-card.trad-card {
      border-top: 3.5px solid #2563eb;
    }
    .thesis-card.harn-card {
      border-top: 3.5px solid #059669;
    }
    .thesis-card-header {
      padding: 0.40rem 0.75rem;
      display: flex;
      align-items: center;
      gap: 0.45rem;
      border-bottom: 1.5px solid var(--rule);
    }
    .thesis-card-header.trad-header {
      background: #F0F5FE;
    }
    .thesis-card-header.harn-header {
      background: #E8F8F2;
    }
    .thesis-icon {
      font-size: 1.15rem;
      line-height: 1;
      flex-shrink: 0;
    }
    .thesis-title {
      font-family: var(--font-display);
      font-size: 0.94rem;
      font-weight: 800;
      color: var(--ink);
      line-height: 1.20;
    }
    .thesis-subtitle {
      font-size: 0.72rem;
      color: var(--ink-muted);
      font-weight: 500;
      margin-top: 0.05rem;
    }
    .thesis-badge {
      margin-left: auto;
      font-size: 0.62rem;
      font-weight: 800;
      padding: 0.10rem 0.38rem;
      border-radius: 4px;
      letter-spacing: 0.02em;
      white-space: nowrap;
      flex-shrink: 0;
    }
    .thesis-badge.trad-badge {
      background: #DBEAFE;
      color: #1e40af;
      border: 1px solid #bfdbfe;
    }
    .thesis-badge.harn-badge {
      background: #D1FAE5;
      color: #065F46;
      border: 1px solid #a7f3d0;
    }
    .thesis-card-body {
      padding: 0.45rem 0.70rem;
      display: flex;
      flex-direction: column;
      gap: 0.35rem;
      flex: 1;
      font-size: 0.82rem;
      line-height: 1.38;
      color: var(--ink);
      background: var(--surface);
    }
    .thesis-point {
      background: #FAF8F2;
      border: 1px solid var(--rule);
      border-radius: 5px;
      padding: 0.32rem 0.55rem;
      line-height: 1.34;
      font-size: 0.79rem;
    }
    .trad-card .thesis-point {
      border-left: 3px solid #3b82f6;
    }
    .harn-card .thesis-point {
      border-left: 3px solid #10b981;
    }

    /* Slide 7: Enhanced Setup & Command Blocks with Copy Buttons */
    .setup-slide-grid {
      display: grid;
      grid-template-columns: minmax(0, 0.90fr) minmax(0, 1.35fr);
      gap: 0.95rem;
      height: 100%;
      align-items: start;
    }
    @media (max-width: 1040px) {
      .setup-slide-grid {
        grid-template-columns: 1fr;
        height: auto;
      }
    }
    .setup-left-col {
      display: flex;
      flex-direction: column;
      gap: 0.50rem;
    }
    .failure-mode-card {
      background: var(--surface);
      border: 1.5px solid var(--rule);
      border-radius: 10px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      box-shadow: 0 3px 12px rgba(0,0,0,0.04);
    }
    .failure-mode-header {
      background: var(--accent-sf);
      color: var(--ink);
      font-family: var(--font-display);
      font-weight: 750;
      font-size: 0.96rem;
      padding: 0.42rem 0.75rem;
      border-bottom: 1.5px solid var(--rule);
      display: flex;
      align-items: center;
      gap: 0.40rem;
    }
    .failure-mode-body {
      padding: 0.55rem 0.75rem;
      display: flex;
      flex-direction: column;
      gap: 0.45rem;
      font-size: 0.85rem;
      color: var(--ink);
    }
    .failure-hazard-box {
      background: #FFF5F2;
      border: 1px solid #F5C6BA;
      border-left: 3.5px solid #E06C75;
      border-radius: 6px;
      padding: 0.40rem 0.60rem;
      display: flex;
      flex-direction: column;
      gap: 0.22rem;
    }
    .hazard-title {
      font-weight: 750;
      color: #BD5D3A;
      font-size: 0.82rem;
    }
    .hazard-list {
      list-style-type: none;
      padding-left: 0;
      margin: 0;
      display: flex;
      flex-direction: column;
      gap: 0.18rem;
      font-size: 0.80rem;
    }
    .hazard-list li {
      position: relative;
      padding-left: 1.1rem;
      line-height: 1.32;
    }
    .hazard-list li::before {
      content: "⚠️";
      position: absolute;
      left: 0;
      font-size: 0.72rem;
      top: 0.05rem;
    }
    .defense-box {
      background: #FAF8F2;
      border: 1px solid var(--rule);
      border-left: 3.5px solid #059669;
      border-radius: 6px;
      padding: 0.40rem 0.60rem;
      font-size: 0.80rem;
      line-height: 1.38;
    }
    .defense-title {
      font-weight: 750;
      color: #059669;
      margin-bottom: 0.18rem;
      font-size: 0.82rem;
    }
    .setup-links-box {
      font-size: 0.80rem;
      color: var(--ink-muted);
      line-height: 1.36;
      display: flex;
      flex-direction: column;
      gap: 0.35rem;
      border-top: 1px dashed var(--rule);
      padding-top: 0.45rem;
    }
    .setup-links-box a {
      color: var(--accent-dk);
      font-weight: 650;
      text-decoration: underline;
    }
    .setup-links-box a:hover {
      color: var(--accent);
    }
    .setup-right-col {
      display: flex;
      flex-direction: column;
      gap: 0.45rem;
    }
    .setup-steps-container {
      background: var(--surface);
      border: 1.5px solid var(--rule);
      border-radius: 10px;
      padding: 0.60rem 0.75rem;
      display: flex;
      flex-direction: column;
      gap: 0.42rem;
      box-shadow: 0 3px 12px rgba(0,0,0,0.04);
    }
    .setup-steps-header {
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      gap: 0.5rem;
      border-bottom: 1.5px solid var(--rule);
      padding-bottom: 0.30rem;
      flex-wrap: wrap;
    }
    .setup-steps-header span:first-child {
      font-family: var(--font-display);
      font-weight: 750;
      font-size: 0.94rem;
      color: var(--accent-dk);
    }
    .setup-steps-sub {
      font-size: 0.72rem;
      color: var(--ink-muted);
      font-weight: 500;
    }
    .cmd-step-card {
      background: #FAF8F2;
      border: 1px solid var(--rule);
      border-left: 3.5px solid var(--accent);
      border-radius: 7px;
      padding: 0.35rem 0.55rem;
      display: flex;
      flex-direction: column;
      gap: 0.20rem;
    }
    .cmd-step-head {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 0.4rem;
    }
    .cmd-step-title {
      font-family: var(--font-display);
      font-size: 0.86rem;
      font-weight: 750;
      color: var(--ink);
    }
    .cmd-step-badge {
      font-size: 0.66rem;
      font-weight: 750;
      color: var(--accent-dk);
      background: var(--accent-sf);
      border: 1px solid var(--rule);
      padding: 0.06rem 0.30rem;
      border-radius: 4px;
      white-space: nowrap;
    }
    .cmd-step-desc {
      font-size: 0.75rem;
      color: var(--ink-muted);
      line-height: 1.28;
    }
    .cmd-code-row {
      display: flex;
      align-items: center;
      background: var(--code-bg);
      border: 1px solid var(--code-rule);
      border-radius: 5px;
      padding: 0.25rem 0.50rem;
      gap: 0.45rem;
      position: relative;
    }
    .cmd-code-prompt {
      color: #D97757;
      font-family: var(--font-code);
      font-size: 0.76rem;
      font-weight: 750;
      user-select: none;
      flex-shrink: 0;
    }
    .cmd-code-text {
      flex: 1;
      font-family: var(--font-code) !important;
      font-size: 0.76rem !important;
      color: #FAF9F5 !important;
      background: transparent !important;
      border: none !important;
      padding: 0 !important;
      white-space: pre-wrap !important;
      word-break: break-all;
      line-height: 1.30;
    }
    .cmd-copy-btn {
      background: #2D2C28;
      color: #FAF9F5;
      border: 1px solid #444440;
      border-radius: 4px;
      padding: 0.18rem 0.45rem;
      font-family: var(--font-code);
      font-size: 0.68rem;
      font-weight: 650;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 0.22rem;
      transition: all 0.16s ease;
      user-select: none;
      flex-shrink: 0;
      line-height: 1.2;
    }
    .cmd-copy-btn:hover {
      background: var(--accent);
      border-color: var(--accent);
      color: #FAF9F5;
      transform: translateY(-1px);
    }
    .cmd-copy-btn:active {
      transform: translateY(0);
    }
    .cmd-copy-btn.copied {
      background: #2e7d32 !important;
      border-color: #4caf50 !important;
      color: #ffffff !important;
    }
    .copy-icon {
      font-size: 0.72rem;
      line-height: 1;
    }
    .os-cmd-group {
      display: flex;
      flex-direction: column;
      gap: 0.18rem;
      margin-top: 0.10rem;
    }
    .os-cmd-label {
      font-size: 0.70rem;
      font-weight: 700;
      color: var(--ink);
    }
    .memory-slide-wrap {
      display: flex;
      flex-direction: column;
      gap: 0.55rem;
      width: 100%;
      height: 100%;
    }
    .memory-grid-container {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0.75rem;
      flex: 1;
      min-height: 0;
    }
    .memory-card {
      background: var(--surface);
      border: 1.5px solid var(--rule);
      border-radius: 9px;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    }
    .memory-card-header {
      padding: 0.40rem 0.70rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-family: var(--font-display);
      font-size: 0.84rem;
    }
    .memory-card-body {
      padding: 0.55rem 0.70rem;
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      overflow-y: auto;
    }
    .memory-comp-table th, .memory-comp-table td {
      border: 1px solid var(--rule);
      padding: 0.25rem 0.45rem;
      font-size: 0.76rem;
      line-height: 1.30;
    }

    .grid-viewport {
      width: 100%; height: 100%; overflow-y: auto; padding: clamp(1rem, 2.5vw, 1.8rem);
      display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 1rem;
    }
    .grid-slide-card {
      background: var(--surface); border: 1px solid var(--rule);
      border-radius: 10px; padding: 1.15rem; height: 260px; display: flex; flex-direction: column;
      cursor: pointer; transition: border-color 0.16s, background-color 0.16s;
    }
    .grid-slide-card:hover { background: var(--accent-sf); border-color: var(--accent); }
    .grid-slide-title {
      font-family: var(--font-display); font-size: 1.1rem; line-height: 1.15;
      font-weight: 650; margin-bottom: 0.45rem; color: var(--ink);
    }
    .grid-slide-body { flex: 1; overflow: hidden; font-size: 0.8rem; line-height: 1.45; color: var(--ink-muted); }

    .progress-bar { height: 3px; background: var(--rule); width: 100%; }
    .progress-fill { height: 100%; background: var(--accent); width: 0%; transition: width 0.3s; }

    @media (max-width: 980px) {
      header { padding: 0 0.6rem; }
      .brand-title { display: none; }
      select.slide-select { max-width: 200px; }
    }
  </style>
</head>
<body>

  <header>
    <div class="header-left">
      <img src="assets/images/harness_app_icon.png" alt="Harness Engineering Logo" style="width:28px; height:28px; border-radius:6px; object-fit:cover; display:inline-block;" />
      <div class="brand-title">Harness Engineering Masterclass</div>
    </div>
    <div class="controls">
      <a href="index.html" class="btn">🏠 Home Site</a>
      <button id="btn-grid" class="btn" onclick="toggleMode()"><span id="mode-icon">📜</span> <span id="mode-text">Grid View</span></button>
      <button id="btn-prev" class="btn" onclick="prevSlide()">❮ Prev</button>
      <select id="slide-select" class="slide-select" onchange="goToSlide(this.value)"></select>
      <div class="goto-group">
        <input type="number" id="goto-input" min="1" max="''' + str(len(slides)) + '''" placeholder="#" class="goto-input" title="Enter slide number (1-''' + str(len(slides)) + ''')" onkeydown="if(event.key==='Enter') jumpToEnteredSlide()">
        <button id="btn-goto" class="btn btn-goto" onclick="jumpToEnteredSlide()" title="Jump to entered slide number">Go ➔</button>
      </div>
      <button id="btn-next" class="btn" onclick="nextSlide()">Next ❯</button>
      <button id="btn-fullscreen" class="btn btn-primary" onclick="toggleFullscreen()">⛶ Fullscreen</button>
    </div>
  </header>

  <div class="progress-bar"><div id="progress-fill" class="progress-fill"></div></div>

  <main>
    <div id="presentation-mode" class="slide-viewport">
      <div class="slide-card">
        <div class="slide-header">
          <div class="slide-title-wrap">
            <div id="slide-title" class="slide-title">Slide Title</div>
          </div>
          <div id="slide-num-badge" class="slide-num-badge">Slide 1 / ''' + str(len(slides)) + '''</div>
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

    const DENSE_BULLET_MIN_LINES = 9;
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
      return text.trim();
    }

    function formatTextWithCode(text) {
      const keywords = ['CLAUDE.md', 'AGENTS.md', 'SPEC.md', 'MEMORY.md', 'CLAUDE.local.md', 'pytest', 'events.jsonl', 'telemetry.jsonl', 'rm -rf', 'write_file', 'read_file', '.claude-plugin/plugin.json', 'SKILL.md', 'mcp_client_runner.py', 'mcp_server_demo.py', 'core_harness_stack.py', 'guardrails_engine.py', 'spec_driven_verifier.py', 'tda_reliability_pipeline.py', 'multi_agent_team_simulator.py', 'five_step_sop_pipeline.py', 'production_harness_audit.py', 'is_relative_to()', 'ast.parse()', 'PreToolUse', 'PostToolUse', 'MCPServer', 'permissionDecision', 'approvals.json', 'ZeroDivisionError', 'pending_push.json', 'scripts/', 'references/', 'assets/', '.claude/workflows/'];
      
      text = text.replace(
        /\\[(.*?)\\]\\(((?:https?:\\/\\/|file:\\/\\/\\/)[^\\s<>"']+)\\)/g,
        (match, label, url) => `<a href="${url}" target="_blank" rel="noopener noreferrer">${label}</a>`
      );

      text = text.replace(
        /(https?:\\/\\/[^\\s<>"']+|file:\\/\\/\\/[^\\s<>"']+)/g,
        (match) => {
          let url = match.replace(/[.,;:)]+$/, '');
          let trailing = match.slice(url.length);
          return `<a href="${url}" target="_blank" rel="noopener noreferrer">${url}</a>${trailing}`;
        }
      );
      
      keywords.forEach(kw => {
        text = text.replaceAll(kw, `<code>${kw}</code>`);
      });
      return text;
    }

    function copyCommand(btn, text) {
      if (!btn) return;
      const originalHtml = btn.innerHTML;
      
      function setSuccess() {
        btn.classList.add('copied');
        btn.innerHTML = '<span class="copy-icon">✓</span> Copied!';
        setTimeout(() => {
          btn.classList.remove('copied');
          btn.innerHTML = originalHtml;
        }, 1800);
      }

      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(setSuccess).catch(() => {
          fallbackCopy(text, setSuccess);
        });
      } else {
        fallbackCopy(text, setSuccess);
      }
    }

    function fallbackCopy(text, cb) {
      const textArea = document.createElement('textarea');
      textArea.value = text;
      textArea.style.position = 'fixed';
      textArea.style.left = '-9999px';
      textArea.style.top = '0';
      document.body.appendChild(textArea);
      textArea.focus();
      textArea.select();
      try {
        const successful = document.execCommand('copy');
        if (successful && cb) cb();
      } catch (err) {
        console.error('Fallback copy failed', err);
      }
      document.body.removeChild(textArea);
    }

    function copyCodeFromSlide(btn, slideIdx) {
      const slide = slidesData[slideIdx];
      if (slide && slide.code_block) {
        copyCommand(btn, slide.code_block);
      }
    }

    function formatCodeConcepts(lines) {
      if (!lines || lines.length === 0) return '';
      let html = '<div class="code-concepts-list">';
      
      lines.forEach(line => {
        let trimmed = line.trim();
        if (!trimmed) return;
        if (trimmed.startsWith('File:')) return;
        
        trimmed = trimmed.replace(/^[•\\-\\ufffd]\\s*/, '').trim();
        
        const lineMatch = trimmed.match(/^\\[(Lines?\\s+[\\d\\-,\\s]+)\\]\\s*([^:]+):\\s*(.*)$/i);
        if (lineMatch) {
          const lineTag = lineMatch[1];
          const title = lineMatch[2];
          const desc = formatTextWithCode(lineMatch[3]);
          html += `
            <div class="code-concept-card">
              <div class="concept-card-head">
                <span class="concept-tag">📌 ${lineTag}</span>
                <span class="concept-name">${formatTextWithCode(title)}</span>
              </div>
              <div class="concept-card-text">${desc}</div>
            </div>
          `;
        } else {
          const colonIdx = trimmed.indexOf(':');
          if (colonIdx !== -1 && colonIdx < 40) {
            const title = trimmed.slice(0, colonIdx);
            const desc = formatTextWithCode(trimmed.slice(colonIdx + 1));
            html += `
              <div class="code-concept-card">
                <div class="concept-card-head">
                  <span class="concept-tag" style="background:var(--accent-sf); color:var(--accent-dk); border:1px solid var(--accent-dk);">🛡️ VERIFIED</span>
                  <span class="concept-name">${formatTextWithCode(title)}</span>
                </div>
                <div class="concept-card-text">${desc}</div>
              </div>
            `;
          } else {
            html += `
              <div class="code-concept-card">
                <div class="concept-card-text">${formatTextWithCode(trimmed)}</div>
              </div>
            `;
          }
        }
      });
      
      html += '</div>';
      return html;
    }

    function renderSkillSlide(slide) {
      const name = slide.skill_name || 'harness-skill';
      const tools = slide.allowed_tools || 'Read, Write, Bash';
      const skillFolderUrl = slide.skill_folder_url || `https://github.com/kenhuangus/packt-harness/tree/main/.claude/skills/${name}/`;
      const manifestUrl = slide.skill_manifest_url || `https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/${name}/SKILL.md`;
      
      let desc = '';
      let whenToUse = '';
      let howToUse = '';
      
      slide.raw_lines.forEach(line => {
        const trimmed = line.trim().replace(/^[•\\-\\ufffd]\\s*/, '');
        if (trimmed.startsWith('Skill Description:')) {
          desc = trimmed.replace('Skill Description:', '').trim();
        } else if (trimmed.startsWith('When to Use:')) {
          whenToUse = trimmed.replace('When to Use:', '').trim();
        } else if (trimmed.startsWith('How to Use:')) {
          howToUse = trimmed.replace('How to Use:', '').trim();
        }
      });

      return `
        <div class="skill-slide-layout">
          <div class="skill-meta-card">
            <div class="skill-meta-badge">🤖 CLAUDE CODE / AGENT SKILL</div>
            <div class="skill-name-heading">${name}</div>
            <div class="skill-desc-box">
              <strong>Description:</strong> ${formatTextWithCode(desc)}
            </div>
            <div class="skill-tools-box">
              <span>🛠️ Allowed Tools:</span> <code>${tools}</code>
            </div>
            <div class="skill-links-box">
              <div>📂 <strong>Skill Directory on GitHub:</strong><br>
                <a href="${skillFolderUrl}" target="_blank" rel="noopener noreferrer" style="font-family:var(--font-code); font-size:0.82rem; word-break:break-all;">${skillFolderUrl}</a>
              </div>
              <div>📄 <strong>Skill Playbook Manifest (SKILL.md):</strong><br>
                <a href="${manifestUrl}" target="_blank" rel="noopener noreferrer" style="font-family:var(--font-code); font-size:0.82rem; word-break:break-all;">${manifestUrl}</a>
              </div>
            </div>
          </div>
          
          <div class="skill-details-column">
            <div class="skill-detail-card">
              <div class="skill-detail-title">🎯 When to Use (Trigger Scenarios)</div>
              <div class="skill-detail-body">${formatTextWithCode(whenToUse)}</div>
            </div>
            <div class="skill-detail-card">
              <div class="skill-detail-title">⚡ How to Use (Execution Playbook)</div>
              <div class="skill-detail-body">${formatTextWithCode(howToUse)}</div>
            </div>
            <div class="skill-detail-card">
              <div class="skill-detail-title">📦 Progressive Disclosure Structure</div>
              <div class="skill-detail-body" style="display:flex; flex-direction:column; gap:0.40rem;">
                <div>• <code>scripts/</code>: Standalone executable CLI helpers and validation scripts.</div>
                <div>• <code>references/</code>: Architecture manuals, policy matrices, and rules.</div>
                <div>• <code>assets/</code>: Machine-readable JSON schemas, templates, and state configs.</div>
              </div>
            </div>
          </div>
        </div>
      `;
    }

    function renderMarkdownTable(tableLines, tableClass = 'slide-table') {
      if (!tableLines || tableLines.length < 2) return '';
      const rows = tableLines.map(l => l.split('|').map(c => c.trim()).filter((c, idx, arr) => idx > 0 && idx < arr.length - 1));
      if (rows.length < 2) return '';
      
      const header = rows[0];
      const dataRows = rows.slice(2); // skip separator row
      
      let html = `<table class="${tableClass}"><thead><tr>`;
      header.forEach(h => {
        html += `<th>${formatTextWithCode(h)}</th>`;
      });
      html += '</tr></thead><tbody>';
      
      dataRows.forEach(r => {
        html += '<tr>';
        r.forEach((cell, idx) => {
          const isFirstCol = idx === 0;
          const formattedCell = formatTextWithCode(cell);
          html += `<td>${isFirstCol ? '<strong>' + formattedCell + '</strong>' : formattedCell}</td>`;
        });
        html += '</tr>';
      });
      
      html += '</tbody></table>';
      return html;
    }

    function formatBullets(lines) {
      if (!lines || lines.length === 0) return '';
      
      const hasTree = lines.some(l => l.includes('├──') || l.includes('└──') || l.includes('custom-agent-skill/'));
      const hasTable = lines.some(l => l.trim().startsWith('|') && l.trim().endsWith('|'));
      
      if (hasTree) {
        let beforeTree = [];
        let treeLines = [];
        let afterTree = [];
        let state = 'before';
        
        lines.forEach(l => {
          const trimmed = l.trim();
          if (trimmed.startsWith('custom-agent-skill/') || trimmed.startsWith('├──') || trimmed.startsWith('│') || trimmed.startsWith('└──')) {
            state = 'tree';
            treeLines.push(l);
          } else if (state === 'tree') {
            state = 'after';
            afterTree.push(l);
          } else {
            beforeTree.push(l);
          }
        });
        
        let html = '';
        if (beforeTree.length > 0) html += formatBullets(beforeTree);
        if (treeLines.length > 0) {
          html += `<pre class="tree-block"><code>${treeLines.join('\\n')}</code></pre>`;
        }
        if (afterTree.length > 0) html += formatBullets(afterTree);
        return html;
      }

      if (hasTable) {
        let beforeTable = [];
        let tableLines = [];
        let afterTable = [];
        let state = 'before';
        
        lines.forEach(l => {
          const trimmed = l.trim();
          if (trimmed.startsWith('|') && trimmed.endsWith('|')) {
            state = 'table';
            tableLines.push(trimmed);
          } else if (state === 'table') {
            state = 'after';
            afterTable.push(l);
          } else {
            beforeTable.push(l);
          }
        });
        
        let html = '';
        if (beforeTable.length > 0) html += formatBullets(beforeTable);
        if (tableLines.length > 0) html += renderMarkdownTable(tableLines);
        if (afterTable.length > 0) html += formatBullets(afterTable);
        return html;
      }

      const populatedLines = lines.filter(line => line.trim());
      if (populatedLines.length === 0) return '';

      const hasIndented = populatedLines.some(l => /^\\s{2,}|\\t/.test(l));
      const denseClass = (!hasIndented && populatedLines.length >= DENSE_BULLET_MIN_LINES) ? ' dense-columns' : '';
      let html = '';
      let listOpen = false;
      let groupOpen = false;
      let subListOpen = false;

      populatedLines.forEach((line, idx) => {
        const isIndented = /^\\s{2,}|\\t/.test(line);
        const trimmed = line.trim();
        const hasBullet = /^[•\\-\\*\\ufffd]/.test(trimmed);

        let cleanText = trimmed.replace(/^[•\\-\\*\\ufffd]\\s*/, '').trim();
        cleanText = cleanNumbers(cleanText);

        const labUrl = cleanText.match(/^Lab demo:\\s*(https:\\/\\/[^\\s]+)/i);
        if (labUrl) {
          cleanText = `<a href="${labUrl[1]}" target="_blank" rel="noopener noreferrer">🔗 Lab demo: open this module in GitHub</a>`;
        } else {
          cleanText = formatTextWithCode(cleanText);
        }

        if (!cleanText) return;

        if (!hasBullet && !isIndented) {
          if (subListOpen) { html += '</ul>'; subListOpen = false; }
          if (groupOpen) { html += '</li>'; groupOpen = false; }
          if (listOpen) { html += '</ul>'; listOpen = false; }
          html += `<div class="slide-lead-header">${cleanText}</div>`;
          return;
        }

        if (!listOpen) {
          html += `<ul class="main-bullets${denseClass}">`;
          listOpen = true;
        }

        if (isIndented && hasBullet) {
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
          if (groupOpen) {
            html += '</li>';
          }
          html += `<li class="bullet-group"><div class="primary-bullet">${cleanText}</div>`;
          groupOpen = true;
        }
      });

      if (subListOpen) html += '</ul>';
      if (groupOpen) html += '</li>';
      if (listOpen) html += '</ul>';
      return html;
    }

    function renderSlide(idx) {
      if (idx < 0) idx = 0;
      if (idx >= slidesData.length) idx = slidesData.length - 1;
      currentIdx = idx;

      const slide = slidesData[idx];
      selectEl.value = idx;
      
      const gotoInput = document.getElementById('goto-input');
      if (gotoInput) {
        gotoInput.placeholder = String(slide.number);
      }

      const title = slide.raw_lines[0] || `Slide ${slide.number}`;
      document.getElementById('slide-title').innerText = title;
      document.getElementById('slide-num-badge').innerText = `Slide ${slide.number} of ${slidesData.length}`;

      if (window.location.hash !== '#' + slide.number) {
        history.replaceState(null, '', '#' + slide.number);
      }

      const restLines = slide.raw_lines ? slide.raw_lines.slice(1) : [];
      const isSkill = slide.slide_type === 'skill';
      const isCode = slide.slide_type === 'code';

      let bodyHtml = '';

      if (isSkill) {
        bodyHtml += renderSkillSlide(slide);
      } else if (isCode && slide.highlighted_code) {
        const fileTag = slide.code_filename || 'source.py';
        const rawBullets = slide.raw_lines.slice(1);
        
        const primaryFile = fileTag.split(' & ')[0].trim();
        const pathParts = primaryFile.split('/');
        const moduleFolder = pathParts.length >= 2 ? `${pathParts[0]}/${pathParts[1]}` : 'course_implementation';
        
        let testsRelativePath = `${moduleFolder}/tests`;
        if (slide.test_suite) {
          testsRelativePath = slide.test_suite;
        } else if (slide.number === 22 || moduleFolder.includes('module_03')) {
          testsRelativePath = 'course_implementation/module_03_spec_driven_development/output/tests';
        } else if (slide.number === 45 || moduleFolder.includes('module_09')) {
          testsRelativePath = 'course_implementation/module_09_practical_workflow_pattern/output/tests';
        } else if (slide.number === 50 || primaryFile.startsWith('deep_research_agent')) {
          testsRelativePath = 'deep_research_agent/tests';
        }
        
        const fileGithubUrl = `https://github.com/kenhuangus/packt-harness/blob/main/${primaryFile}`;
        const testsGithubUrl = `https://github.com/kenhuangus/packt-harness/tree/main/${testsRelativePath}`;
        
        bodyHtml += `
          <div class="code-slide-container">
            <div class="code-editor-window">
              <div class="code-editor-header">
                <div class="code-dots">
                  <div class="code-dot dot-red"></div>
                  <div class="code-dot dot-yellow"></div>
                  <div class="code-dot dot-green"></div>
                </div>
                <a href="${fileGithubUrl}" target="_blank" rel="noopener noreferrer" class="code-file-tag" title="Open ${primaryFile} on GitHub" style="color:#A0A09A; text-decoration:none;">
                  📄 ${fileTag} ↗
                </a>
                <div style="display:flex; align-items:center; gap:0.45rem;">
                  <button class="cmd-copy-btn" onclick="copyCodeFromSlide(this, ${idx})" title="Copy Python code">
                    <span class="copy-icon">📋</span> Copy
                  </button>
                  <div class="code-lang-tag">${slide.code_language || 'PYTHON'}</div>
                </div>
              </div>
              <div class="code-block">${slide.highlighted_code}</div>
            </div>
            <div class="code-concepts-column">
              ${formatCodeConcepts(rawBullets)}
              <div class="invariant-card">
                <div class="invariant-title">🛡️ Deterministic Control Architecture</div>
                <div style="margin-bottom:0.35rem; color:var(--ink); font-size:0.86rem;">Verified directly against runnable tests in GitHub:</div>
                <div style="display:flex; flex-direction:column; gap:0.25rem; font-size:0.84rem;">
                  <div>📄 <strong>Source File:</strong> <a href="${fileGithubUrl}" target="_blank" rel="noopener noreferrer"><code>${primaryFile}</code> ↗</a></div>
                  <div>🧪 <strong>Test Suite:</strong> <a href="${testsGithubUrl}" target="_blank" rel="noopener noreferrer"><code>${testsRelativePath}</code> ↗</a></div>
                </div>
              </div>
            </div>
          </div>
        `;
      } else if (slide.number === 1) {
        bodyHtml += `
          <div id="slide-content-wrap" class="slide-1-container">
            <div class="slide-1-hero-card">
              <div class="slide-1-hero-tagline">
                Architecting Deterministic Control Systems for Non-Deterministic AI Agents
              </div>
              <div class="slide-1-hero-desc">
                A comprehensive masterclass in engineering reliable, observable, and secure production agent harnesses with Claude, memory architectures, AST guardrails, TDA self-healing loops, and compound multi-agent teams.
              </div>
            </div>

            <div class="slide-1-instructor-card">
              <div class="slide-1-avatar-wrap">
                <img src="assets/images/ken-head-shot.png" alt="Ken Huang" class="slide-1-avatar-img" />
              </div>
              <div class="slide-1-instructor-info">
                <div class="slide-1-instructor-badge">
                  <span>🎓 Course Instructor</span>
                </div>
                <div class="slide-1-instructor-name">Ken Huang</div>
                <div class="slide-1-instructor-titles">
                  <div class="slide-1-title-item">
                    <span class="title-icon">🏛️</span>
                    <span>Adjunct Professor of <span class="slide-1-title-highlight">University of San Francisco</span></span>
                  </div>
                  <div class="slide-1-title-item">
                    <span class="title-icon">🚀</span>
                    <span>CEO of <span class="slide-1-title-highlight">Distributedapps.ai</span></span>
                  </div>
                </div>
              </div>
            </div>

            <div class="slide-1-pillars-row">
              <div class="slide-1-pillar-pill">
                <div class="slide-1-pillar-title">🛡️ Deterministic Harness</div>
                <div class="slide-1-pillar-desc">Memory, scoped sandboxing &amp; AST hooks</div>
              </div>
              <div class="slide-1-pillar-pill">
                <div class="slide-1-pillar-title">🧪 Test-Driven Reliability</div>
                <div class="slide-1-pillar-desc">Pytest feedback &amp; anti-regression suites</div>
              </div>
              <div class="slide-1-pillar-pill">
                <div class="slide-1-pillar-title">🤖 Multi-Agent Systems</div>
                <div class="slide-1-pillar-desc">Planner, implementer &amp; reviewer worktrees</div>
              </div>
              <div class="slide-1-pillar-pill">
                <div class="slide-1-pillar-title">📜 5-Gate Scorecard</div>
                <div class="slide-1-pillar-desc">100% certified production readiness audit</div>
              </div>
            </div>
          </div>
        `;
      } else if (slide.number === 2) {
        bodyHtml += `
          <div id="slide-content-wrap" class="instructor-slide-grid">
            <div class="instructor-info-col">
              ${svgMap[slide.number] || ''}
              ${restLines.length > 0 ? formatBullets(restLines) : ''}
            </div>
            <div class="author-books-card">
              <div class="author-books-header">
                <span>📚 AI Books &amp; Academic Publications (Springer · Cambridge · Wiley · Packt)</span>
                <a href="https://www.amazon.com/stores/author/B0D3J7L7GN" target="_blank" rel="noopener noreferrer">Amazon Author Page ➔</a>
              </div>
              <div class="books-gallery-grid">
                <a href="https://www.amazon.com/dp/3031900251" target="_blank" rel="noopener noreferrer" class="book-item-card" title="Agentic AI: Theories and Practices (Springer)">
                  <img src="assets/images/books/springer_agentic_ai.jpg" alt="Agentic AI (Springer)" class="book-cover-img" />
                  <div class="book-item-title">Agentic AI</div>
                  <div class="book-publisher-tag">SPRINGER</div>
                </a>
                <a href="https://www.amazon.com/dp/3031448839" target="_blank" rel="noopener noreferrer" class="book-item-card" title="Beyond AI: ChatGPT, Web3, and the Business Landscape of Tomorrow (Springer)">
                  <img src="assets/images/books/springer_beyond_ai.jpg" alt="Beyond AI (Springer)" class="book-cover-img" />
                  <div class="book-item-title">Beyond AI</div>
                  <div class="book-publisher-tag">SPRINGER</div>
                </a>
                <a href="https://www.amazon.com/dp/3031542517" target="_blank" rel="noopener noreferrer" class="book-item-card" title="Generative AI Security: Theories and Practices (Springer)">
                  <img src="assets/images/books/springer_generative_ai_security.jpg" alt="GenAI Security (Springer)" class="book-cover-img" />
                  <div class="book-item-title">GenAI Security</div>
                  <div class="book-publisher-tag">SPRINGER</div>
                </a>
                <a href="https://www.amazon.com/dp/3031901002" target="_blank" rel="noopener noreferrer" class="book-item-card" title="Securing AI Agents: Foundations, Frameworks, and Real-World Deployment (Springer)">
                  <img src="assets/images/books/springer_securing_ai_agents.jpg" alt="Securing AI Agents (Springer)" class="book-cover-img" />
                  <div class="book-item-title">Securing Agents</div>
                  <div class="book-publisher-tag">SPRINGER</div>
                </a>
                <a href="https://www.amazon.com/dp/1009384467" target="_blank" rel="noopener noreferrer" class="book-item-card" title="Web3: Blockchain, the New Economy, and the Self-Sovereign Internet (Cambridge University Press)">
                  <img src="assets/images/books/cambridge_web3.jpg" alt="Web3 (Cambridge UP)" class="book-cover-img" />
                  <div class="book-item-title">Web3 &amp; Economy</div>
                  <div class="book-publisher-tag">CAMBRIDGE</div>
                </a>
                <a href="https://www.amazon.com/dp/1394186524" target="_blank" rel="noopener noreferrer" class="book-item-card" title="Blockchain and Web3: Building Foundations of the Metaverse (Wiley)">
                  <img src="assets/images/books/wiley_blockchain_web3.jpg" alt="Blockchain & Web3 (Wiley)" class="book-cover-img" />
                  <div class="book-item-title">Blockchain Web3</div>
                  <div class="book-publisher-tag">WILEY</div>
                </a>
                <a href="https://www.amazon.com/dp/B0HF3F86YM" target="_blank" rel="noopener noreferrer" class="book-item-card" title="Harness Engineering: Design Patterns for Securing Long-Horizon Multi-Agent AI Systems (Packt / Amazon #1 Best Seller)">
                  <img src="assets/images/books/harness_engineering.jpg" alt="Harness Engineering" class="book-cover-img" />
                  <div class="book-item-title">Harness Eng.</div>
                  <div class="book-publisher-tag">BEST SELLER</div>
                </a>
                <a href="https://www.amazon.com/dp/1807785017" target="_blank" rel="noopener noreferrer" class="book-item-card" title="OpenClaw AI in Production: Architecture, design patterns, and engineering practices (Packt)">
                  <img src="assets/images/books/openclaw_ai_in_production.jpg" alt="OpenClaw AI in Production" class="book-cover-img" />
                  <div class="book-item-title">OpenClaw AI</div>
                  <div class="book-publisher-tag">PACKT</div>
                </a>
                <a href="https://www.amazon.com/dp/B0H8JW9XFN" target="_blank" rel="noopener noreferrer" class="book-item-card" title="Engineering Agentic AI with Claude Fable 5 and Mythos 5">
                  <img src="assets/images/books/engineering_agentic_ai_claude.jpg" alt="Engineering Agentic AI with Claude" class="book-cover-img" />
                  <div class="book-item-title">Agentic Claude</div>
                  <div class="book-publisher-tag">CLAUDE AI</div>
                </a>
                <a href="https://www.amazon.com/dp/1836207034" target="_blank" rel="noopener noreferrer" class="book-item-card" title="LLM Design Patterns: A Practical Guide to Building Robust and Efficient AI Systems (Packt)">
                  <img src="assets/images/books/llm_design_patterns.jpg" alt="LLM Design Patterns" class="book-cover-img" />
                  <div class="book-item-title">LLM Patterns</div>
                  <div class="book-publisher-tag">PACKT</div>
                </a>
                <a href="https://www.amazon.com/dp/B0H13XWS8W" target="_blank" rel="noopener noreferrer" class="book-item-card" title="Agentic AI Harness Pattern: Top 15 Patterns">
                  <img src="assets/images/books/agentic_ai_harness_pattern.jpg" alt="Agentic AI Harness Pattern" class="book-cover-img" />
                  <div class="book-item-title">AI Harness</div>
                  <div class="book-publisher-tag">PATTERNS</div>
                </a>
                <a href="https://www.amazon.com/dp/B0DCBDGNTN" target="_blank" rel="noopener noreferrer" class="book-item-card" title="The Layperson's Handbook to Generative AI">
                  <img src="assets/images/books/laypersons_handbook_genai.jpg" alt="Handbook to GenAI" class="book-cover-img" />
                  <div class="book-item-title">GenAI Guide</div>
                  <div class="book-publisher-tag">HANDBOOK</div>
                </a>
              </div>
            </div>
          </div>
        `;
      } else if (slide.raw_lines && slide.raw_lines[0] && (slide.raw_lines[0].includes('Core Thesis') || slide.raw_lines[0].includes('Traditional SE'))) {
        bodyHtml += `
          <div id="slide-content-wrap" class="thesis-slide-wrap">
            ${svgMap[slide.number] || ''}
            <div class="thesis-grid">
              <div class="thesis-card trad-card">
                <div class="thesis-card-header trad-header">
                  <span class="thesis-icon">🏛️</span>
                  <div>
                    <div class="thesis-title">Traditional Software Engineering</div>
                    <div class="thesis-subtitle">SDLC, DevOps, CI/CD, Testing Pyramids &amp; SRE</div>
                  </div>
                  <span class="thesis-badge trad-badge">DETERMINISTIC SYSTEMS</span>
                </div>
                <div class="thesis-card-body">
                  <div class="thesis-point">
                    <strong>🎯 System Domain:</strong> Built for <strong>deterministic IT systems</strong> where explicit logic and algorithms run on predictable computer hardware.
                  </div>
                  <div class="thesis-point">
                    <strong>⚙️ Frameworks &amp; Practices:</strong> SDLC, Agile, Architecture Patterns, CI/CD pipelines, Unit/Integration Testing Pyramids, SRE, and Secure-SDLC / AppSec.
                  </div>
                  <div class="thesis-point">
                    <strong>🔒 Core Principle:</strong> <strong>Deterministic Repeatability</strong> — identical inputs and state strictly produce identical outputs (<code>f(x) ➔ y</code>).
                  </div>
                </div>
              </div>

              <div class="thesis-card harn-card">
                <div class="thesis-card-header harn-header">
                  <span class="thesis-icon">🛡️</span>
                  <div>
                    <div class="thesis-title">Harness Engineering for Agentic AI</div>
                    <div class="thesis-subtitle">Deterministic Control Systems for Probabilistic Agents</div>
                  </div>
                  <span class="thesis-badge harn-badge">NON-DETERMINISTIC + HARNESS</span>
                </div>
                <div class="thesis-card-body">
                  <div class="thesis-point">
                    <strong>🧠 Probabilistic Emergence:</strong> Behavior emerges probabilistically from foundation models plus prompts, dynamic context, memory, tools, loops, policies, and multi-agent teams.
                  </div>
                  <div class="thesis-point">
                    <strong>🛡️ Deterministic Control Environment:</strong> Engineers the surrounding scaffold: Memory (<code>CLAUDE.md</code>/<code>AGENTS.md</code>), path sandboxing, Pre/Post AST hooks, Pytest TDA loops, and permission gateways.
                  </div>
                  <div class="thesis-point">
                    <strong>🎯 The 5 Production Goals:</strong> Transforms probabilistic model outputs into systems that are <strong>Reliable</strong>, <strong>Observable</strong>, <strong>Secure</strong>, <strong>Governable</strong>, and <strong>Operationally Manageable</strong>.
                  </div>
                </div>
              </div>
            </div>
          </div>
        `;
      } else if (slide.raw_lines && slide.raw_lines[0] && slide.raw_lines[0].includes('COURSE MASTER MAP')) {
        bodyHtml += `
          <div id="slide-content-wrap" class="course-map-slide-wrap">
            ${svgMap[slide.number] || ''}
            <div class="course-map-columns-grid">
              <div class="course-map-part-col">
                <div class="course-map-part-header">
                  <span>🏛️ PART 1: FOUNDATIONS &amp; CONTROL</span>
                </div>
                <ul class="course-map-module-list">
                  <li><span class="mod-bullet">◆</span> <strong>Mod 1:</strong> Why Harness Engineering</li>
                  <li><span class="mod-bullet">◆</span> <strong>Mod 2:</strong> Core Harness Stack</li>
                  <li><span class="mod-bullet">◆</span> <strong>Mod 3:</strong> Spec-Driven Development</li>
                  <li><span class="mod-bullet">◆</span> <strong>Mod 4:</strong> Guardrails &amp; Hooks</li>
                  <li><span class="mod-bullet">◆</span> <strong>Mod 5:</strong> Permission Gateways</li>
                </ul>
              </div>
              <div class="course-map-part-col">
                <div class="course-map-part-header">
                  <span>🚀 PART 2: RELIABILITY &amp; TEAMS</span>
                </div>
                <ul class="course-map-module-list">
                  <li><span class="mod-bullet">◆</span> <strong>Mod 6:</strong> Tests as Reliability</li>
                  <li><span class="mod-bullet">◆</span> <strong>Mod 7:</strong> Agent Extensions (Skills, Plugins, MCP)</li>
                  <li><span class="mod-bullet">◆</span> <strong>Mod 8:</strong> Compound Engineering</li>
                  <li><span class="mod-bullet">◆</span> <strong>Mod 9:</strong> Five-Step SOP</li>
                  <li><span class="mod-bullet">◆</span> <strong>Mod 10:</strong> Principles &amp; Audit</li>
                </ul>
              </div>
            </div>
          </div>
        `;
      } else if (slide.raw_lines && slide.raw_lines[0] && (slide.raw_lines[0].includes('Pillar 1: Memory') || slide.raw_lines[0].includes('How Claude Remembers'))) {
        bodyHtml += `
          <div id="slide-content-wrap" class="memory-slide-wrap">
            ${svgMap[slide.number] || ''}
            <div class="memory-grid-container">
              <!-- Left Column: Dual Memory Architecture -->
              <div class="memory-card">
                <div class="memory-card-header" style="background:#FAF0EA; border-bottom:1.5px solid #F5D3C4;">
                  <span style="color:#BD5D3A; font-weight:800;">🧠 Dual Memory Systems: CLAUDE.md vs. Auto Memory</span>
                  <span style="font-size:0.73rem; background:#BD5D3A; color:#FFF; padding:2px 8px; border-radius:12px; font-weight:700;">Claude Code v2.1+</span>
                </div>
                <div class="memory-card-body">
                  <div style="font-size:0.81rem; color:#2D2C28; margin-bottom:0.45rem; line-height:1.35;">
                    Each Claude Code session starts with a clean context window. Two complementary mechanisms bridge knowledge across sessions:
                  </div>

                  <table class="memory-comp-table" style="width:100%; border-collapse:collapse; font-size:0.77rem; margin-bottom:0.45rem;">
                    <thead>
                      <tr style="background:#F0EEE6; border-bottom:1.5px solid #DDD9CD; text-align:left;">
                        <th style="padding:4px 6px;">Feature</th>
                        <th style="padding:4px 6px; color:#BD5D3A;">CLAUDE.md Files</th>
                        <th style="padding:4px 6px; color:#2563eb;">Auto Memory (MEMORY.md)</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr style="border-bottom:1px solid #EBE8DE;">
                        <td style="padding:3px 6px; font-weight:700;">Who writes it</td>
                        <td style="padding:3px 6px;">You (Developer, Team, Org)</td>
                        <td style="padding:3px 6px;">Claude (Autonomously)</td>
                      </tr>
                      <tr style="border-bottom:1px solid #EBE8DE;">
                        <td style="padding:3px 6px; font-weight:700;">Content</td>
                        <td style="padding:3px 6px;">Coding standards, workflows, architecture</td>
                        <td style="padding:3px 6px;">Build commands, debugging notes, preferences</td>
                      </tr>
                      <tr style="border-bottom:1px solid #EBE8DE;">
                        <td style="padding:3px 6px; font-weight:700;">Scope</td>
                        <td style="padding:3px 6px;">Managed Policy, User, Project, Local</td>
                        <td style="padding:3px 6px;">Per repo (<code>~/.claude/projects/</code>), shared worktrees</td>
                      </tr>
                      <tr style="border-bottom:1px solid #EBE8DE;">
                        <td style="padding:3px 6px; font-weight:700;">Loaded into</td>
                        <td style="padding:3px 6px;">Every session in full at start</td>
                        <td style="padding:3px 6px;">First 200 lines or 25KB of <code>MEMORY.md</code></td>
                      </tr>
                      <tr>
                        <td style="padding:3px 6px; font-weight:700;">Compaction</td>
                        <td style="padding:3px 6px;">Root file re-injected after <code>/compact</code></td>
                        <td style="padding:3px 6px;">Topic notes read on-demand via tools</td>
                      </tr>
                    </tbody>
                  </table>

                  <div style="background:#FAF9F5; border:1px solid #E3E0D6; border-radius:6px; padding:0.35rem 0.55rem; font-size:0.75rem; line-height:1.35;">
                    💡 <strong>Enforcement vs. Context:</strong> Memory files provide behavioral guidance. To strictly block actions regardless of model discretion, enforce with deterministic <code>PreToolUse</code> hooks.
                  </div>

                  <div style="background:#F0F7FF; border:1.2px solid #93C5FD; border-radius:6px; padding:0.30rem 0.55rem; font-size:0.74rem; line-height:1.35; margin-top:0.30rem;">
                    📁 <strong>Live Student Demo (MEMORY.md):</strong><br>
                    <a href="file:///C:/Users/kenhu/.claude/projects/C--Users-kenhu-security-tools/memory/MEMORY.md" target="_blank" rel="noopener noreferrer" style="color:#0369a1; font-weight:700; word-break:break-all;">
                      <code>C:\\Users\\kenhu\\.claude\\projects\\C--Users-kenhu-security-tools\\memory\\MEMORY.md</code> ↗
                    </a>
                  </div>
                </div>
              </div>

              <!-- Right Column: 4-Tier Hierarchy, Rules & Interop -->
              <div class="memory-card">
                <div class="memory-card-header" style="background:#EBF3FA; border-bottom:1.5px solid #C9E0F5;">
                  <span style="color:#1e40af; font-weight:800;">🌲 Scope Hierarchy, Rules &amp; Interoperability</span>
                  <span style="font-size:0.73rem; background:#1e40af; color:#FFF; padding:2px 8px; border-radius:12px; font-weight:700;">Resolution Order</span>
                </div>
                <div class="memory-card-body" style="display:flex; flex-direction:column; gap:0.35rem;">
                  <!-- Scope Hierarchy -->
                  <div style="background:#FAF9F5; border:1px solid #E3E0D6; border-radius:6px; padding:0.35rem 0.55rem; font-size:0.75rem; line-height:1.3;">
                    <strong style="color:#141413;">4-Tier Load Precedence (Broadest ➔ Most Specific):</strong>
                    <div style="display:flex; flex-direction:column; gap:0.12rem; margin-top:0.22rem;">
                      <div>🏛️ <strong>1. Managed Policy:</strong> <code>/etc/claude-code/CLAUDE.md</code> or <code>C:\\Program Files\\ClaudeCode\\CLAUDE.md</code></div>
                      <div>👤 <strong>2. User Instructions:</strong> <code>~/.claude/CLAUDE.md</code> (Personal preferences across all repos)</div>
                      <div>📦 <strong>3. Project Instructions:</strong> <code>./CLAUDE.md</code> or <code>./.claude/CLAUDE.md</code> (Team standards in git)</div>
                      <div>🔒 <strong>4. Local Instructions:</strong> <code>./CLAUDE.local.md</code> (Personal sandbox prefs; gitignored)</div>
                    </div>
                  </div>

                  <!-- Path-Scoped Rules & Imports -->
                  <div style="background:#FAF9F5; border:1px solid #E3E0D6; border-radius:6px; padding:0.35rem 0.55rem; font-size:0.75rem; line-height:1.3;">
                    <strong style="color:#141413;">Modular Rules &amp; Cross-Agent Interoperability:</strong>
                    <ul style="margin:0.2rem 0 0 1rem; padding:0;">
                      <li><strong>Path-Scoped Rules:</strong> <code>.claude/rules/*.md</code> with <code>paths: ["src/api/**/*.ts"]</code> load only when matching files are opened.</li>
                      <li><strong>Modular Imports:</strong> <code>@path/to/import</code> syntax expands up to 4 hops recursively.</li>
                      <li><strong>AGENTS.md Interop:</strong> Claude Code reads <code>CLAUDE.md</code>; use <code>@AGENTS.md</code> or <code>ln -s AGENTS.md CLAUDE.md</code> to share instructions.</li>
                    </ul>
                  </div>

                  <!-- Official Documentation & Research Box -->
                  <div style="background:#F0FDF4; border:1.2px solid #86EFAC; border-radius:6px; padding:0.35rem 0.55rem; font-size:0.75rem; line-height:1.3;">
                    <div style="color:#166534; font-weight:750;">📖 Official Documentation &amp; Live References:</div>
                    <div style="margin-top:0.12rem;">
                      • Docs Index: <a href="https://code.claude.com/docs/llms.txt" target="_blank" rel="noopener noreferrer"><code>https://code.claude.com/docs/llms.txt</code> ↗</a><br>
                      • Memory Guide: <a href="https://code.claude.com/docs/en/memory" target="_blank" rel="noopener noreferrer"><code>https://code.claude.com/docs/en/memory</code> ↗</a><br>
                      • Live Example: <a href="file:///C:/Users/kenhu/.claude/projects/C--Users-kenhu-security-tools/memory/MEMORY.md" target="_blank" rel="noopener noreferrer"><code>MEMORY.md (Real-World Demo)</code> ↗</a><br>
                      • Advanced Research &amp; Benchmarks: <a href="https://kenhuangus.github.io/agent-memory-harness/presentation/#1" target="_blank" rel="noopener noreferrer"><code>Agent Memory Harness Presentation</code> ↗</a>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        `;
      } else if (slide.raw_lines && slide.raw_lines[0] && slide.raw_lines[0].includes('Universal Environment Setup')) {
        bodyHtml += `
          <div id="slide-content-wrap" class="setup-slide-grid">
            <div class="setup-left-col">
              ${svgMap[slide.number] || ''}
              <div class="failure-mode-card">
                <div class="failure-mode-header">
                  <span>🛡️ Failure Mode Analysis &amp; Harness Guardrails</span>
                </div>
                <div class="failure-mode-body">
                  <div class="failure-hazard-box">
                    <div class="hazard-title">🚨 The Hazard (Unsanitized Shell Actions):</div>
                    <ul class="hazard-list">
                      <li><code>rm -rf</code>, <code>sudo</code>, <code>chmod 777</code>, and unvetted shell execution</li>
                      <li>Overwrites config, drops database/files, leaks keys, alters host</li>
                    </ul>
                  </div>
                  <div class="defense-box">
                    <div class="defense-title">🛡️ Deterministic Harness Defense:</div>
                    <div style="font-size:0.79rem; line-height:1.36;">
                      <strong>PreToolUse Interceptor:</strong> Regex &amp; AST analysis block dangerous commands before subprocess creation.<br>
                      <strong>OS Path Sandbox:</strong> <code>Path.is_relative_to()</code> enforces strict workspace file boundaries.
                    </div>
                  </div>
                  <div class="setup-links-box">
                    <div>
                      🔑 <strong>Environment Configuration (.env.example):</strong><br>
                      <a href="https://github.com/kenhuangus/packt-harness/blob/main/.env.example" target="_blank" rel="noopener noreferrer">
                        .env.example (API Keys &amp; Model Providers) ↗
                      </a>
                    </div>
                    <div>
                      🔗 <strong>Interactive Lab Demo:</strong><br>
                      <a href="https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_01_why_harness_engineering/README.md" target="_blank" rel="noopener noreferrer">
                        Module 01: Pre-Hook Interception &amp; Loop Detection ↗
                      </a>
                    </div>
                    <div>
                      💡 <strong>Why the Virtual Environment:</strong><br>
                      <span>Each module executes <code>pytest</code> via <code>sys.executable</code> — ensures tests run against the dedicated project environment without false passes from system PATH.</span>
                    </div>
                    <div>
                      📖 <strong>Full Setup &amp; Multi-Model Keys:</strong><br>
                      <a href="https://github.com/kenhuangus/packt-harness/blob/main/README.md" target="_blank" rel="noopener noreferrer">
                        Packt Masterclass README (Setup, API Keys, Browser Extra) ↗
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="setup-right-col">
              <div class="setup-steps-container">
                <div class="setup-steps-header">
                  <span>⚡ Universal Environment Setup (Run Once)</span>
                  <span class="setup-steps-sub">All 10 module labs execute deterministically with this setup</span>
                </div>

                <div class="cmd-step-card">
                  <div class="cmd-step-head">
                    <span class="cmd-step-title">1️⃣ Step 1: Clone Repository</span>
                    <span class="cmd-step-badge">Required (.git)</span>
                  </div>
                  <div class="cmd-step-desc">Clone the git repository (not a ZIP: Module 8 drives git worktrees and requires <code>.git</code>):</div>
                  <div class="cmd-code-row">
                    <span class="cmd-code-prompt">$</span>
                    <code class="cmd-code-text">git clone https://github.com/kenhuangus/packt-harness.git</code>
                    <button class="cmd-copy-btn" onclick="copyCommand(this, 'git clone https://github.com/kenhuangus/packt-harness.git')" title="Copy Clone Command">
                      <span class="copy-icon">📋</span> Copy
                    </button>
                  </div>
                </div>

                <div class="cmd-step-card">
                  <div class="cmd-step-head">
                    <span class="cmd-step-title">2️⃣ Step 2: Enter Directory &amp; Create Virtual Environment</span>
                    <span class="cmd-step-badge">Python 3.10+</span>
                  </div>
                  <div class="cmd-step-desc">Navigate into <code>packt-harness</code> before creating the isolated <code>.venv</code>:</div>
                  <div class="cmd-code-row" style="margin-bottom:0.25rem;">
                    <span class="cmd-code-prompt">$</span>
                    <code class="cmd-code-text">cd packt-harness</code>
                    <button class="cmd-copy-btn" onclick="copyCommand(this, 'cd packt-harness')" title="Copy cd Command">
                      <span class="copy-icon">📋</span> Copy
                    </button>
                  </div>
                  <div class="cmd-code-row">
                    <span class="cmd-code-prompt">$</span>
                    <code class="cmd-code-text">python -m venv .venv</code>
                    <button class="cmd-copy-btn" onclick="copyCommand(this, 'python -m venv .venv')" title="Copy venv Command">
                      <span class="copy-icon">📋</span> Copy
                    </button>
                  </div>
                </div>

                <div class="cmd-step-card">
                  <div class="cmd-step-head">
                    <span class="cmd-step-title">3️⃣ Step 3: Install in Editable Mode</span>
                    <span class="cmd-step-badge"><code>-e .</code></span>
                  </div>
                  <div class="cmd-step-desc">Install the harness package into the active virtual environment:</div>
                  
                  <div class="os-cmd-group">
                    <div class="os-cmd-label">🪟 Windows (PowerShell / Command Prompt):</div>
                    <div class="cmd-code-row">
                      <span class="cmd-code-prompt">PS&gt;</span>
                      <code class="cmd-code-text">.venv\\\\Scripts\\\\python.exe -m pip install -e .</code>
                      <button class="cmd-copy-btn" onclick="copyCommand(this, '.venv\\\\\\\\Scripts\\\\\\\\python.exe -m pip install -e .')" title="Copy Windows Install Command">
                        <span class="copy-icon">📋</span> Copy
                      </button>
                    </div>
                    
                    <div class="os-cmd-label" style="margin-top:0.25rem;">🍎 macOS / 🐧 Linux (Bash / Zsh):</div>
                    <div class="cmd-code-row">
                      <span class="cmd-code-prompt">$</span>
                      <code class="cmd-code-text">.venv/bin/python -m pip install -e .</code>
                      <button class="cmd-copy-btn" onclick="copyCommand(this, '.venv/bin/python -m pip install -e .')" title="Copy macOS/Linux Install Command">
                        <span class="copy-icon">📋</span> Copy
                      </button>
                    </div>
                  </div>
                </div>

                <div class="cmd-step-card">
                  <div class="cmd-step-head">
                    <span class="cmd-step-title">4️⃣ Step 4: Check &amp; Verify All Modules</span>
                    <span class="cmd-step-badge" style="background:#e8f5e9; color:#2e7d32; border-color:#a5d6a7;">14 Passed ✓</span>
                  </div>
                  <div class="cmd-step-desc">Run the harness test runner across all modules (expects <code>Summary: 14 passed, 0 failed</code>):</div>
                  <div class="cmd-code-row">
                    <span class="cmd-code-prompt">$</span>
                    <code class="cmd-code-text">python run_all_modules.py</code>
                    <button class="cmd-copy-btn" onclick="copyCommand(this, 'python run_all_modules.py')" title="Copy Step 4 Command">
                      <span class="copy-icon">📋</span> Copy
                    </button>
                  </div>
                </div>

              </div>
            </div>
          </div>
        `;
      } else if (slide.number === 49 || slide.number === 83 || (slide.raw_lines && slide.raw_lines[0] && slide.raw_lines[0].includes('Capstone Project'))) {
        const tableLines = slide.raw_lines.filter(l => l.trim().startsWith('|') && l.trim().endsWith('|'));
        bodyHtml += `
          <div id="slide-content-wrap" class="capstone-layout-grid">
            <div class="capstone-info-card">
              <div class="ref-table-card-header">
                ⚡ Setup, Execution &amp; Multi-Provider AI Suite Engine
              </div>
              <div class="capstone-info-body">
                <div class="capstone-section">
                  <div class="capstone-section-title">💻 Step-by-Step Universal Setup (Zero-to-Run for All Students)</div>
                  <div class="capstone-cmd-box" style="background:transparent; border:none; padding:0; gap:0.28rem;">
                    <div class="cmd-code-row">
                      <span class="cmd-code-prompt">1. Clone &amp; CD:</span>
                      <code class="cmd-code-text">git clone https://github.com/kenhuangus/packt-harness.git &amp;&amp; cd packt-harness</code>
                      <button class="cmd-copy-btn" onclick="copyCommand(this, 'git clone https://github.com/kenhuangus/packt-harness.git && cd packt-harness')" title="Copy Command">
                        <span class="copy-icon">📋</span> Copy
                      </button>
                    </div>
                    <div class="cmd-code-row">
                      <span class="cmd-code-prompt">2. Venv (Win):</span>
                      <code class="cmd-code-text">python -m venv .venv ; .venv\\Scripts\\Activate.ps1</code>
                      <button class="cmd-copy-btn" onclick="copyCommand(this, 'python -m venv .venv ; .venv\\\\\\\\Scripts\\\\\\\\Activate.ps1')" title="Copy Windows PowerShell Command">
                        <span class="copy-icon">📋</span> Copy Win
                      </button>
                    </div>
                    <div class="cmd-code-row">
                      <span class="cmd-code-prompt">2. Venv (Mac/Linux):</span>
                      <code class="cmd-code-text">python3 -m venv .venv &amp;&amp; source .venv/bin/activate</code>
                      <button class="cmd-copy-btn" onclick="copyCommand(this, 'python3 -m venv .venv && source .venv/bin/activate')" title="Copy macOS/Linux Command">
                        <span class="copy-icon">📋</span> Copy Mac/Linux
                      </button>
                    </div>
                    <div class="cmd-code-row">
                      <span class="cmd-code-prompt">3. Install:</span>
                      <code class="cmd-code-text">pip install -r requirements.txt &amp;&amp; python -m playwright install chromium</code>
                      <button class="cmd-copy-btn" onclick="copyCommand(this, 'pip install -r requirements.txt && python -m playwright install chromium')" title="Copy Command">
                        <span class="copy-icon">📋</span> Copy
                      </button>
                    </div>
                    <div class="cmd-code-row">
                      <span class="cmd-code-prompt">4. Config:</span>
                      <code class="cmd-code-text">copy .env.example .env (Win) | cp .env.example .env (Mac/Linux)</code>
                      <button class="cmd-copy-btn" onclick="copyCommand(this, 'copy .env.example .env')" title="Copy Windows Config Command">
                        <span class="copy-icon">📋</span> Win
                      </button>
                      <button class="cmd-copy-btn" onclick="copyCommand(this, 'cp .env.example .env')" title="Copy Mac/Linux Config Command">
                        <span class="copy-icon">📋</span> Mac/Linux
                      </button>
                    </div>
                    <div class="cmd-code-row">
                      <span class="cmd-code-prompt">5. Run UI:</span>
                      <code class="cmd-code-text">python deep_research_agent/server.py 8090</code>
                      <button class="cmd-copy-btn" onclick="copyCommand(this, 'python deep_research_agent/server.py 8090')" title="Copy Command">
                        <span class="copy-icon">📋</span> Copy
                      </button>
                    </div>
                    <div class="cmd-code-row">
                      <span class="cmd-code-prompt">6. Test:</span>
                      <code class="cmd-code-text">pytest -v</code>
                      <button class="cmd-copy-btn" onclick="copyCommand(this, 'pytest -v')" title="Copy Command">
                        <span class="copy-icon">📋</span> Copy
                      </button>
                    </div>
                  </div>
                </div>

                <div class="capstone-section">
                  <div class="capstone-section-title">🔑 Universal aisuite Provider Support (.env Configuration)</div>
                  <div class="capstone-providers-grid">
                    <div class="provider-pill">💻 <strong>Local vLLM (Default):</strong> <code>LLM_PROVIDER=openai</code> (Port 8000)</div>
                    <div class="provider-pill">🟢 <strong>OpenAI:</strong> <code>OPENAI_API_KEY=sk-proj...</code></div>
                    <div class="provider-pill">🌐 <strong>OpenRouter:</strong> <code>OPENROUTER_API_KEY=sk-or-...</code></div>
                    <div class="provider-pill">🦙 <strong>Ollama:</strong> <code>LLM_PROVIDER=ollama</code> (Port 11434)</div>
                    <div class="provider-pill">🔵 <strong>Gemini (Google):</strong> <code>GEMINI_API_KEY=AIzaSy...</code></div>
                    <div class="provider-pill">🧡 <strong>Claude (Anthropic):</strong> <code>ANTHROPIC_API_KEY=sk-ant...</code></div>
                  </div>
                </div>

                <div class="capstone-section">
                  <div class="capstone-section-title">🧠 Unified AI Suite &amp; 2-Turn Self-Reflection Engine</div>
                  <div class="capstone-text-desc">
                    One unified client via Andrew Ng's <strong>aisuite</strong>: switch between OpenAI, OpenRouter, Ollama, Google Gemini, and Anthropic Claude via <code>.env</code>. Multi-agent SOP executes <strong>Two-Turn Self-Reflection</strong> (Turn 1: Gap Reflection ➔ Turn 2: Adversarial Audit) across 6 Zero-API public streams.
                  </div>
                </div>
              </div>
            </div>

            <div class="ref-table-card">
              <div class="ref-table-card-header">
                🚀 Capstone Artifacts &amp; Direct Repository Links
              </div>
              ${renderMarkdownTable(tableLines, 'ref-table')}
            </div>
          </div>
        `;
      } else if (slide.number === slidesData.length || (slide.raw_lines && slide.raw_lines[0] && slide.raw_lines[0].includes('Additional References'))) {
        bodyHtml += `
          <div id="slide-content-wrap" class="reference-tables-grid">
            <div class="ref-table-card">
              <div class="ref-table-card-header">📚 Core Resource &amp; Reference Links</div>
              <table class="ref-table">
                <thead>
                  <tr>
                    <th style="width: 44%;">Resource Title</th>
                    <th style="width: 56%;">Direct Access Link</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td><strong>🛡️ OWASP Agentic Skills Top 10 Risks</strong></td>
                    <td><a href="https://www.youtube.com/watch?v=l-uwnCzRRE0" target="_blank" rel="noopener noreferrer">https://www.youtube.com/watch?v=l-uwnCzRRE0</a></td>
                  </tr>
                  <tr>
                    <td><strong>🎯 MAESTRO Threat Modeling Framework</strong></td>
                    <td><a href="https://kenhuangus.github.io/maestro-site/#1" target="_blank" rel="noopener noreferrer">https://kenhuangus.github.io/maestro-site/#1</a></td>
                  </tr>
                  <tr>
                    <td><strong>🚀 DistributedApps.ai Consulting Company</strong></td>
                    <td><a href="https://distributedapps.ai/" target="_blank" rel="noopener noreferrer">https://distributedapps.ai/</a></td>
                  </tr>
                  <tr>
                    <td><strong>🏭 Greenfield Software Factory Skill</strong></td>
                    <td><a href="https://github.com/kenhuangus/greenfield-software-factory" target="_blank" rel="noopener noreferrer">https://github.com/kenhuangus/greenfield-software-factory</a></td>
                  </tr>
                  <tr>
                    <td><strong>✍️ Agentic AI Substack (Ken Huang)</strong></td>
                    <td><a href="https://kenhuangus.substack.com/" target="_blank" rel="noopener noreferrer">https://kenhuangus.substack.com/</a></td>
                  </tr>
                  <tr>
                    <td><strong>📖 Harness Engineering (Amazon Book)</strong></td>
                    <td><a href="https://www.amazon.com/dp/B0HF3F86YM" target="_blank" rel="noopener noreferrer">https://www.amazon.com/dp/B0HF3F86YM</a></td>
                  </tr>
                </tbody>
              </table>
            </div>
            
            <div class="ref-table-card">
              <div class="ref-table-card-header">🏆 Official Amazon Publication (#1 Best Seller)</div>
              <table class="ref-table">
                <thead>
                  <tr>
                    <th style="text-align: center;">Book Cover &amp; Kindle / Paperback Listing</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td style="text-align: center; padding: 0.50rem; background: #FAF8F2;">
                      <a href="https://www.amazon.com/dp/B0HF3F86YM" target="_blank" rel="noopener noreferrer" class="book-screenshot-link" title="Open Harness Engineering Book on Amazon">
                        <img src="assets/images/harness_engineering_book.png" alt="Harness Engineering: Design Patterns for Securing Long-Horizon Multi-Agent AI Systems by Ken Huang" class="book-screenshot-img" />
                        <div class="book-screenshot-badge">📖 Amazon Kindle &amp; Paperback ➔</div>
                      </a>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        `;
      } else {
        bodyHtml += '<div id="slide-content-wrap" class="slide-content-wrapper">';
        if (svgMap[slide.number]) {
          bodyHtml += svgMap[slide.number];
        }
        if (restLines.length > 0) {
          bodyHtml += formatBullets(restLines);
        }
        bodyHtml += '</div>';
      }

      bodyEl.innerHTML = bodyHtml;
      
      // Dynamic Text-Sizing Engine:
      // Maximize font size so text and graphics fill >= 82% to 92% of the card height
      // while guaranteeing ZERO overflow and ZERO scrollbars
      if (!isCode && !isSkill) {
        bodyEl.style.setProperty('--fit-scale', '1.0');
        const wrapper = document.getElementById('slide-content-wrap') || bodyEl;
        const clientH = bodyEl.clientHeight;
        const targetH = clientH * 0.90;
        const maxScale = (wrapper.querySelector('.sub-bullets') || wrapper.querySelector('.capstone-layout-grid') || wrapper.querySelector('.course-map-columns-grid') || wrapper.querySelector('.setup-slide-grid') || wrapper.querySelector('.thesis-grid') || wrapper.querySelector('.slide-1-container')) ? 1.20 : (wrapper.querySelector('.main-bullets') ? 1.50 : 3.25);
        
        let scale = 1.0;
        let growIter = 0;
        while (wrapper.offsetHeight < targetH && bodyEl.scrollHeight <= clientH && scale < maxScale && growIter < 45) {
          scale += 0.05;
          bodyEl.style.setProperty('--fit-scale', scale.toFixed(2));
          growIter++;
        }
        
        // If scaled over client height or causing scroll, scale down until it fits with zero scroll
        let shrinkIter = 0;
        while ((bodyEl.scrollHeight > clientH || wrapper.offsetHeight > (clientH - 6)) && scale > 0.50 && shrinkIter < 60) {
          scale -= 0.02;
          bodyEl.style.setProperty('--fit-scale', scale.toFixed(2));
          shrinkIter++;
        }
      } else {
        bodyEl.style.setProperty('--fit-scale', '1.0');
      }

      const pct = ((idx + 1) / slidesData.length) * 100;
      document.getElementById('progress-fill').style.width = pct + '%';
    }

    function renderGrid() {
      const gridContainer = document.getElementById('grid-mode');
      gridContainer.innerHTML = '';
      slidesData.forEach((slide, idx) => {
        const card = document.createElement('div');
        card.className = 'grid-slide-card';
        card.onclick = () => { isGridMode = true; toggleMode(); renderSlide(idx); };
        
        let title = slide.raw_lines[0] || `Slide ${slide.number}`;
        let body = (slide.raw_lines.slice(1, 4).join(' ') || (slide.code_block ? slide.code_block.slice(0, 120) : '')).replace(/[•\\-#]/g, '');
        let typeBadge = slide.slide_type ? `<span style="background:var(--accent-sf); color:var(--accent-dk); font-size:0.68rem; font-weight:700; padding:2px 6px; border-radius:4px;">${slide.slide_type.toUpperCase()}</span>` : '';
        
        card.innerHTML = `
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
            <span style="font-size:0.75rem; color:var(--ink); font-weight:800;">SLIDE ${slide.number}</span>
            ${typeBadge}
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

    function jumpToEnteredSlide() {
      const input = document.getElementById('goto-input');
      if (!input) return;
      const val = parseInt(input.value, 10);
      if (!isNaN(val) && val >= 1 && val <= slidesData.length) {
        renderSlide(val - 1);
        input.value = '';
      } else {
        alert(`Please enter a slide number between 1 and ${slidesData.length}.`);
      }
    }

    function toggleMode() {
      isGridMode = !isGridMode;
      document.getElementById('presentation-mode').style.display = isGridMode ? 'none' : 'flex';
      document.getElementById('grid-mode').style.display = isGridMode ? 'grid' : 'none';
      document.getElementById('mode-text').innerText = isGridMode ? 'Presentation Mode' : 'Grid View';
      document.getElementById('mode-icon').innerText = isGridMode ? '📺' : '📜';
      if (isGridMode) renderGrid();
    }

    function toggleFullscreen() {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen();
      } else {
        if (document.exitFullscreen) document.exitFullscreen();
      }
    }

    document.addEventListener('keydown', (e) => {
      if (document.activeElement && document.activeElement.tagName === 'INPUT') return;
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') nextSlide();
      if (e.key === 'ArrowLeft' || e.key === 'PageUp') prevSlide();
      if (e.key === 'f' || e.key === 'F') toggleFullscreen();
      if (e.key === 'm' || e.key === 'M') toggleMode();
      if (e.key === 'g' || e.key === 'G') {
        e.preventDefault();
        const gotoInp = document.getElementById('goto-input');
        if (gotoInp) { gotoInp.focus(); gotoInp.select(); }
      }
    });

    window.addEventListener('resize', () => {
      if (!isGridMode) renderSlide(currentIdx);
    });

    function getInitialSlideIndex() {
      const hash = window.location.hash.replace('#', '');
      if (hash) {
        const num = parseInt(hash, 10);
        if (!isNaN(num)) {
          const foundIdx = slidesData.findIndex(s => s.number === num);
          if (foundIdx !== -1) return foundIdx;
        }
      }
      return 0;
    }

    window.addEventListener('hashchange', () => {
      const idx = getInitialSlideIndex();
      if (idx !== currentIdx) renderSlide(idx);
    });

    renderSlide(getInitialSlideIndex());
  </script>
</body>
</html>'''

out_docs = os.path.join(ROOT_DIR, 'docs', 'slides.html')
out_root = os.path.join(ROOT_DIR, 'slides.html')

with open(out_docs, 'w', encoding='utf-8') as f:
    f.write(html_template)

with open(out_root, 'w', encoding='utf-8') as f:
    f.write(html_template)

print(f"SUCCESSFULLY GENERATED {len(slides)} SLIDES WITH WRAPPER DYNAMIC TEXT SIZING!")
