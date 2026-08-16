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
    elif 'WHAT IS AN AGENT SKILL' in title_upper or 'WHAT IS A SKILL' in title_upper:
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
    elif num == 1 or 'MASTERCLASS' in title_upper:
        return '''<svg viewBox="0 0 800 130" class="slide-svg">
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#BD5D3A"/>
    </marker>
  </defs>
  <rect x="15" y="10" width="210" height="110" rx="12" fill="#FAF9F5" stroke="#D97757" stroke-width="2.2"/>
  <text x="120" y="45" fill="#141413" font-family="Inter" font-size="15" font-weight="800" text-anchor="middle">Probabilistic LLM</text>
  <text x="120" y="70" fill="#6B6B63" font-family="Inter" font-size="12" text-anchor="middle">Reasoning &amp; Generation</text>
  <text x="120" y="95" fill="#BD5D3A" font-family="Inter" font-size="11" font-weight="700" text-anchor="middle">⚠ Non-Deterministic Output</text>
  
  <path d="M225 65 L340 65" stroke="#BD5D3A" stroke-width="3" stroke-dasharray="5 3" marker-end="url(#arrow)"/>
  <rect x="240" y="38" width="90" height="24" rx="6" fill="#F5E6DF" stroke="#BD5D3A" stroke-width="1.5"/>
  <text x="285" y="54" fill="#BD5D3A" font-family="Inter" font-size="11" font-weight="800" text-anchor="middle">Harness ➔</text>
  
  <rect x="350" y="5" width="435" height="120" rx="14" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2.5"/>
  <text x="567" y="34" fill="#141413" font-family="Inter" font-size="15" font-weight="800" text-anchor="middle">Deterministic Harness Control System</text>
  <g transform="translate(365, 48)">
    <rect x="0" y="0" width="92" height="62" rx="8" fill="#F0EEE6" stroke="#E3E0D6"/>
    <text x="46" y="27" fill="#141413" font-family="Inter" font-size="11" font-weight="700" text-anchor="middle">Memory</text>
    <text x="46" y="48" fill="#6B6B63" font-family="Inter" font-size="10" text-anchor="middle">CLAUDE.md</text>
  </g>
  <g transform="translate(467, 48)">
    <rect x="0" y="0" width="92" height="62" rx="8" fill="#F0EEE6" stroke="#E3E0D6"/>
    <text x="46" y="27" fill="#141413" font-family="Inter" font-size="11" font-weight="700" text-anchor="middle">Sandbox</text>
    <text x="46" y="48" fill="#6B6B63" font-family="Inter" font-size="10" text-anchor="middle">Path Scoping</text>
  </g>
  <g transform="translate(569, 48)">
    <rect x="0" y="0" width="98" height="62" rx="8" fill="#F0EEE6" stroke="#E3E0D6"/>
    <text x="49" y="27" fill="#141413" font-family="Inter" font-size="11" font-weight="700" text-anchor="middle">Hooks &amp; AST</text>
    <text x="49" y="48" fill="#6B6B63" font-family="Inter" font-size="10" text-anchor="middle">Pre/Post Guards</text>
  </g>
  <g transform="translate(677, 48)">
    <rect x="0" y="0" width="98" height="62" rx="8" fill="#F0EEE6" stroke="#E3E0D6"/>
    <text x="49" y="27" fill="#141413" font-family="Inter" font-size="11" font-weight="700" text-anchor="middle">Tests</text>
    <text x="49" y="48" fill="#6B6B63" font-family="Inter" font-size="10" text-anchor="middle">Pytest Loop</text>
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
    elif re.match(r'^MODULE\s+\d+', title.strip(), re.IGNORECASE):
        mod_match = re.search(r'\d+', title)
        m_num = int(mod_match.group(0)) if mod_match else 1
        return f'''<svg viewBox="0 0 800 110" class="slide-svg">
  <rect x="15" y="6" width="770" height="98" rx="14" fill="#FAF9F5" stroke="#D97757" stroke-width="2.5"/>
  <circle cx="70" cy="55" r="30" fill="#F5E6DF" stroke="#D97757" stroke-width="2.5"/>
  <text x="70" y="64" fill="#141413" font-family="Inter" font-size="20" font-weight="900" text-anchor="middle">M{m_num}</text>
  <text x="120" y="46" fill="#141413" font-family="Inter" font-size="17" font-weight="800">MODULE {m_num} SPECIFICATION &amp; PRODUCTION BLUEPRINT</text>
  <text x="120" y="74" fill="#6B6B63" font-family="Inter" font-size="12.5">Verified Implementation in course_implementation/ | Deterministic Control Architecture</text>
</svg>'''
    elif '5 HARNESS PILLARS' in title_upper or '5 PILLARS' in title_upper:
        return '''<svg viewBox="0 0 800 100" class="slide-svg">
  <g transform="translate(10, 5)">
    <rect x="0" y="0" width="140" height="88" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
    <text x="70" y="28" fill="#141413" font-family="Inter" font-size="12" font-weight="800" text-anchor="middle">Pillar 1: Memory</text>
    <text x="70" y="52" fill="#6B6B63" font-family="Inter" font-size="10.5" text-anchor="middle">CLAUDE.md</text>
    <text x="70" y="72" fill="#6B6B63" font-family="Inter" font-size="10.5" text-anchor="middle">AGENTS.md Rules</text>
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
    elif '4-LAYER' in title_upper:
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
    elif 'PERMISSION MODES' in title_upper or 'RISK TIERS' in title_upper:
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

    /* Slide 1 Custom Links Layout with 50% Reduced Text Size */
    .slide-1-links-card {
      margin-top: 0.85rem;
      background: var(--surface);
      border: 1.5px solid var(--rule);
      border-radius: 10px;
      padding: 0.65rem 1.0rem;
      display: flex;
      flex-direction: column;
      gap: 0.40rem;
      font-size: 0.30em; /* Reduced by half */
      box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    .slide-1-link-item {
      display: flex;
      align-items: center;
      gap: 0.50rem;
      font-size: 1.0em;
      line-height: 1.40;
    }
    .slide-1-link-label {
      font-weight: 750;
      color: var(--ink);
      white-space: nowrap;
    }
    .slide-1-link-url {
      font-family: var(--font-code);
      color: var(--accent-dk);
      text-decoration: underline;
      text-underline-offset: 3px;
      word-break: break-all;
    }
    .slide-1-link-url:hover {
      color: var(--accent);
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
        <input type="number" id="goto-input" min="1" max="86" placeholder="#" class="goto-input" title="Enter slide number (1-86)" onkeydown="if(event.key==='Enter') jumpToEnteredSlide()">
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
          <div id="slide-num-badge" class="slide-num-badge">Slide 1 / 85</div>
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
      const keywords = ['CLAUDE.md', 'AGENTS.md', 'SPEC.md', 'pytest', 'events.jsonl', 'telemetry.jsonl', 'rm -rf', 'write_file', 'read_file', '.claude-plugin/plugin.json', 'SKILL.md', 'mcp_client_runner.py', 'mcp_server_demo.py', 'core_harness_stack.py', 'guardrails_engine.py', 'spec_driven_verifier.py', 'tda_reliability_pipeline.py', 'multi_agent_team_simulator.py', 'five_step_sop_pipeline.py', 'production_harness_audit.py', 'is_relative_to()', 'ast.parse()', 'PreToolUse', 'PostToolUse', 'MCPServer', 'permissionDecision', 'approvals.json', 'ZeroDivisionError', 'pending_push.json', 'scripts/', 'references/', 'assets/', '.claude/workflows/'];
      
      text = text.replace(
        /(https?:\\/\\/[^\\s<>"']+)/g,
        (match) => {
          let url = match.replace(/[\\.\\,\\;\\:\\)]+$/, '');
          let trailing = match.slice(url.length);
          return `<a href="${url}" target="_blank" rel="noopener noreferrer">${url}</a>${trailing}`;
        }
      );
      
      keywords.forEach(kw => {
        text = text.replaceAll(kw, `<code>${kw}</code>`);
      });
      return text;
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
                  <span class="concept-tag" style="background:var(--accent-sf); color:var(--accent-dk); border:1px solid var(--accent-dk);">🛡️ GUARANTEE</span>
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
        
        const fileGithubUrl = `https://github.com/kenhuangus/packt-harness/blob/main/${primaryFile}`;
        const testsGithubUrl = `https://github.com/kenhuangus/packt-harness/tree/main/${moduleFolder}/tests`;
        
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
                <div class="code-lang-tag">${slide.code_language || 'PYTHON'}</div>
              </div>
              <div class="code-block">${slide.highlighted_code}</div>
            </div>
            <div class="code-concepts-column">
              ${formatCodeConcepts(rawBullets)}
              <div class="invariant-card">
                <div class="invariant-title">🛡️ Execution &amp; Control Invariant</div>
                <div style="margin-bottom:0.35rem; color:var(--ink); font-size:0.86rem;">Verified directly against runnable tests in GitHub:</div>
                <div style="display:flex; flex-direction:column; gap:0.25rem; font-size:0.84rem;">
                  <div>📄 <strong>Source File:</strong> <a href="${fileGithubUrl}" target="_blank" rel="noopener noreferrer"><code>${primaryFile}</code> ↗</a></div>
                  <div>🧪 <strong>Test Suite:</strong> <a href="${testsGithubUrl}" target="_blank" rel="noopener noreferrer"><code>${moduleFolder}/tests/</code> ↗</a></div>
                </div>
              </div>
            </div>
          </div>
        `;
      } else if (slide.number === 1) {
        bodyHtml += `
          <div id="slide-content-wrap" class="slide-content-wrapper slide-1-wrapper">
            ${svgMap[1] || ''}
            <div class="slide-1-links-card">
              <div class="slide-1-link-item">
                <span class="slide-1-link-label">🐙 GitHub:</span>
                <a href="https://github.com/kenhuangus/packt-harness" target="_blank" rel="noopener noreferrer" class="slide-1-link-url">https://github.com/kenhuangus/packt-harness</a>
              </div>
              <div class="slide-1-link-item">
                <span class="slide-1-link-label">🌐 Site:</span>
                <a href="https://kenhuangus.github.io/packt-harness/slides.html#1" target="_blank" rel="noopener noreferrer" class="slide-1-link-url">https://kenhuangus.github.io/packt-harness/slides.html#1</a>
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
      } else if (slide.number === 83 || (slide.raw_lines && slide.raw_lines[0] && slide.raw_lines[0].includes('Capstone Project'))) {
        const tableLines = slide.raw_lines.filter(l => l.trim().startsWith('|') && l.trim().endsWith('|'));
        bodyHtml += `
          <div id="slide-content-wrap" class="capstone-layout-grid">
            <div class="capstone-info-card">
              <div class="ref-table-card-header">
                ⚡ Local Execution &amp; Model-Driven Zero-API Engine
              </div>
              <div class="capstone-info-body">
                <div class="capstone-section">
                  <div class="capstone-section-title">💻 How to Run Locally (Web UI &amp; Server)</div>
                  <div class="capstone-cmd-box">
                    <div><code>python deep_research_agent/server.py 8090</code> <span class="cmd-note">➔ Open <a href="http://localhost:8090/" target="_blank" rel="noopener noreferrer">http://localhost:8090/</a></span></div>
                    <div><code>pytest deep_research_agent/tests/ -v</code> <span class="cmd-note">➔ 14/14 automated TDA tests passing</span></div>
                    <div><code>packt-harness audit</code> <span class="cmd-note">➔ 100% Score (5/5 Gates Certified)</span></div>
                  </div>
                </div>

                <div class="capstone-section">
                  <div class="capstone-section-title">🌐 Zero-API Public Search Providers (No Keys / No Auth)</div>
                  <div class="capstone-providers-grid">
                    <div class="provider-pill">📄 <strong>arXiv:</strong> Open science preprints Atom API</div>
                    <div class="provider-pill">📚 <strong>OpenAlex:</strong> Global scholarly index &amp; DOIs</div>
                    <div class="provider-pill">🌐 <strong>Wikipedia:</strong> Encyclopedia REST API</div>
                    <div class="provider-pill">💬 <strong>HackerNews:</strong> Algolia community discussions</div>
                    <div class="provider-pill">🐙 <strong>GitHub Repos:</strong> Playwright browser crawler</div>
                    <div class="provider-pill">🎥 <strong>YouTube Talks:</strong> Playwright browser crawler</div>
                  </div>
                </div>

                <div class="capstone-section">
                  <div class="capstone-section-title">🧠 Model-Driven Autonomous Search (Query Presets)</div>
                  <div class="capstone-text-desc">
                    UI presets provide <strong>pure query text strings</strong> (hypotheses) without hardcoded results. The <strong>Planner subagent</strong> decomposes queries into multi-hop investigation tracks, invokes live MCP search tools across Zero-API providers, and the <strong>Synthesizer model</strong> constructs an evidence-grounded dossier with citation confidence and unified diff.
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
        const maxScale = (wrapper.querySelector('.sub-bullets') || wrapper.querySelector('.capstone-layout-grid')) ? 1.25 : (wrapper.querySelector('.main-bullets') ? 1.50 : 3.25);
        
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
