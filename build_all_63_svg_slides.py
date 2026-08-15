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
    
    if num == 1 or 'MASTERCLASS' in title_upper:
        return '''<svg viewBox="0 0 800 130" style="width:100%; max-height:130px; margin:0.4rem 0;">
  <rect x="15" y="15" width="220" height="100" rx="12" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
  <text x="125" y="50" fill="#141413" font-family="Inter" font-size="14" font-weight="800" text-anchor="middle">Probabilistic LLM</text>
  <text x="125" y="72" fill="#6B6B63" font-family="Inter" font-size="11" text-anchor="middle">Token Proposals &amp; Reasoner</text>
  <text x="125" y="94" fill="#BD5D3A" font-family="Inter" font-size="10" font-weight="700" text-anchor="middle">⚠ Hallucinations &amp; Loops</text>
  <path d="M235 65 L335 65" stroke="#D97757" stroke-width="3" stroke-dasharray="6 4"/>
  <text x="285" y="55" fill="#BD5D3A" font-family="Inter" font-size="10" font-weight="700" text-anchor="middle">Proposals</text>
  <rect x="345" y="10" width="440" height="110" rx="14" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2.5"/>
  <text x="565" y="35" fill="#141413" font-family="Inter" font-size="14" font-weight="800" text-anchor="middle">Deterministic Harness Control System</text>
  <g transform="translate(360, 48)">
    <rect x="0" y="0" width="95" height="55" rx="8" fill="#F0EEE6" stroke="#E3E0D6"/>
    <text x="47" y="24" fill="#141413" font-family="Inter" font-size="10" font-weight="700" text-anchor="middle">Memory</text>
    <text x="47" y="42" fill="#6B6B63" font-family="Inter" font-size="9" text-anchor="middle">CLAUDE.md</text>
  </g>
  <g transform="translate(465, 48)">
    <rect x="0" y="0" width="95" height="55" rx="8" fill="#F0EEE6" stroke="#E3E0D6"/>
    <text x="47" y="24" fill="#141413" font-family="Inter" font-size="10" font-weight="700" text-anchor="middle">Sandbox</text>
    <text x="47" y="42" fill="#6B6B63" font-family="Inter" font-size="9" text-anchor="middle">Path Scoping</text>
  </g>
  <g transform="translate(570, 48)">
    <rect x="0" y="0" width="95" height="55" rx="8" fill="#F0EEE6" stroke="#E3E0D6"/>
    <text x="47" y="24" fill="#141413" font-family="Inter" font-size="10" font-weight="700" text-anchor="middle">Hooks &amp; AST</text>
    <text x="47" y="42" fill="#6B6B63" font-family="Inter" font-size="9" text-anchor="middle">Pre/Post Guards</text>
  </g>
  <g transform="translate(675, 48)">
    <rect x="0" y="0" width="95" height="55" rx="8" fill="#F0EEE6" stroke="#E3E0D6"/>
    <text x="47" y="24" fill="#141413" font-family="Inter" font-size="10" font-weight="700" text-anchor="middle">Tests</text>
    <text x="47" y="42" fill="#6B6B63" font-family="Inter" font-size="9" text-anchor="middle">Pytest Loop</text>
  </g>
</svg>'''
    elif num == 2 or 'COURSE MASTER MAP' in title_upper:
        return '''<svg viewBox="0 0 800 110" style="width:100%; max-height:110px; margin:0.4rem 0;">
  <rect x="20" y="10" width="365" height="90" rx="12" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
  <text x="202" y="38" fill="#141413" font-family="Inter" font-size="13" font-weight="800" text-anchor="middle">PART 1: FOUNDATIONS &amp; CONTROL</text>
  <text x="202" y="60" fill="#6B6B63" font-family="Inter" font-size="10" text-anchor="middle">Modules 1–5: Core Scaffolding, SDD &amp; Gateways</text>
  <text x="202" y="82" fill="#BD5D3A" font-family="Inter" font-size="10" font-weight="700" text-anchor="middle">Deterministic Execution &amp; Interception</text>
  <path d="M385 55 L415 55" stroke="#BD5D3A" stroke-width="3" stroke-dasharray="4 4"/>
  <rect x="415" y="10" width="365" height="90" rx="12" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
  <text x="597" y="38" fill="#141413" font-family="Inter" font-size="13" font-weight="800" text-anchor="middle">PART 2: RELIABILITY &amp; TEAMS</text>
  <text x="597" y="60" fill="#6B6B63" font-family="Inter" font-size="10" text-anchor="middle">Modules 6–10: TDA, MCP, Multi-Agent &amp; Audit</text>
  <text x="597" y="82" fill="#D97757" font-family="Inter" font-size="10" font-weight="700" text-anchor="middle">100% Production Readiness Scorecard</text>
</svg>'''
    elif re.match(r'^MODULE\s+\d+$', title.strip()):
        mod_match = re.search(r'\d+', title)
        m_num = int(mod_match.group(0)) if mod_match else 1
        return f'''<svg viewBox="0 0 800 100" style="width:100%; max-height:100px; margin:0.3rem 0;">
  <rect x="20" y="10" width="760" height="80" rx="12" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
  <circle cx="65" cy="50" r="24" fill="#F5E6DF" stroke="#D97757" stroke-width="2"/>
  <text x="65" y="57" fill="#141413" font-family="Inter" font-size="16" font-weight="900" text-anchor="middle">M{m_num}</text>
  <text x="110" y="44" fill="#141413" font-family="Inter" font-size="15" font-weight="800">MODULE {m_num} SPECIFICATION &amp; PRODUCTION BLUEPRINT</text>
  <text x="110" y="68" fill="#6B6B63" font-family="Inter" font-size="11">Verified Implementation in course_implementation/ | Deterministic Control Architecture</text>
</svg>'''
    elif '5 HARNESS PILLARS' in title_upper or '5 PILLARS' in title_upper:
        return '''<svg viewBox="0 0 800 100" style="width:100%; max-height:100px; margin:0.3rem 0;">
  <g transform="translate(10, 5)">
    <rect x="0" y="0" width="140" height="85" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="1.8"/>
    <text x="70" y="30" fill="#141413" font-family="Inter" font-size="11" font-weight="800" text-anchor="middle">Pillar 1: Memory</text>
    <text x="70" y="52" fill="#6B6B63" font-family="Inter" font-size="9.5" text-anchor="middle">CLAUDE.md</text>
    <text x="70" y="68" fill="#6B6B63" font-family="Inter" font-size="9.5" text-anchor="middle">AGENTS.md Rules</text>
  </g>
  <g transform="translate(165, 5)">
    <rect x="0" y="0" width="140" height="85" rx="8" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="1.8"/>
    <text x="70" y="30" fill="#141413" font-family="Inter" font-size="11" font-weight="800" text-anchor="middle">Pillar 2: Sandbox</text>
    <text x="70" y="52" fill="#6B6B63" font-family="Inter" font-size="9.5" text-anchor="middle">Least Privilege</text>
    <text x="70" y="68" fill="#6B6B63" font-family="Inter" font-size="9.5" text-anchor="middle">Path is_relative_to</text>
  </g>
  <g transform="translate(320, 5)">
    <rect x="0" y="0" width="140" height="85" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="1.8"/>
    <text x="70" y="30" fill="#141413" font-family="Inter" font-size="11" font-weight="800" text-anchor="middle">Pillar 3: Hooks</text>
    <text x="70" y="52" fill="#6B6B63" font-family="Inter" font-size="9.5" text-anchor="middle">Secret Filtering</text>
    <text x="70" y="68" fill="#6B6B63" font-family="Inter" font-size="9.5" text-anchor="middle">AST Syntax Check</text>
  </g>
  <g transform="translate(475, 5)">
    <rect x="0" y="0" width="140" height="85" rx="8" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="1.8"/>
    <text x="70" y="30" fill="#141413" font-family="Inter" font-size="11" font-weight="800" text-anchor="middle">Pillar 4: Budget</text>
    <text x="70" y="52" fill="#6B6B63" font-family="Inter" font-size="9.5" text-anchor="middle">Head/Tail Compacting</text>
    <text x="70" y="68" fill="#6B6B63" font-family="Inter" font-size="9.5" text-anchor="middle">Context Window Cap</text>
  </g>
  <g transform="translate(630, 5)">
    <rect x="0" y="0" width="155" height="85" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="1.8"/>
    <text x="77" y="30" fill="#141413" font-family="Inter" font-size="11" font-weight="800" text-anchor="middle">Pillar 5: Tracing</text>
    <text x="77" y="52" fill="#6B6B63" font-family="Inter" font-size="9.5" text-anchor="middle">events.jsonl Audit</text>
    <text x="77" y="68" fill="#6B6B63" font-family="Inter" font-size="9.5" text-anchor="middle">ISO UTC Timestamps</text>
  </g>
</svg>'''
    elif '4-LAYER' in title_upper:
        return '''<svg viewBox="0 0 800 100" style="width:100%; max-height:100px; margin:0.3rem 0;">
  <g transform="translate(15, 8)">
    <rect x="0" y="0" width="175" height="80" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="1.8"/>
    <text x="87" y="28" fill="#141413" font-family="Inter" font-size="11" font-weight="800" text-anchor="middle">1. System Prompt</text>
    <text x="87" y="48" fill="#6B6B63" font-family="Inter" font-size="9.5" text-anchor="middle">Standing Guidelines</text>
    <text x="87" y="65" fill="#6B6B63" font-family="Inter" font-size="9" text-anchor="middle">CLAUDE.md / AGENTS.md</text>
  </g>
  <g transform="translate(205, 8)">
    <rect x="0" y="0" width="175" height="80" rx="8" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="1.8"/>
    <text x="87" y="28" fill="#141413" font-family="Inter" font-size="11" font-weight="800" text-anchor="middle">2. Tool Schemas</text>
    <text x="87" y="48" fill="#6B6B63" font-family="Inter" font-size="9.5" text-anchor="middle">JSON Schema Typing</text>
    <text x="87" y="65" fill="#6B6B63" font-family="Inter" font-size="9.5" text-anchor="middle">Strict Argument Checks</text>
  </g>
  <g transform="translate(395, 8)">
    <rect x="0" y="0" width="185" height="80" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="1.8"/>
    <text x="92" y="28" fill="#141413" font-family="Inter" font-size="11" font-weight="800" text-anchor="middle">3. Pre/Post Hooks</text>
    <text x="92" y="48" fill="#BD5D3A" font-family="Inter" font-size="9.5" font-weight="700" text-anchor="middle">PreToolUse Shell Deny</text>
    <text x="92" y="65" fill="#BD5D3A" font-family="Inter" font-size="9.5" font-weight="700" text-anchor="middle">PostToolUse AST / Secrets</text>
  </g>
  <g transform="translate(595, 8)">
    <rect x="0" y="0" width="185" height="80" rx="8" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="1.8"/>
    <text x="92" y="28" fill="#141413" font-family="Inter" font-size="11" font-weight="800" text-anchor="middle">4. OS Sandboxing</text>
    <text x="92" y="48" fill="#141413" font-family="Inter" font-size="9.5" font-weight="700" text-anchor="middle">Path is_relative_to</text>
    <text x="92" y="65" fill="#6B6B63" font-family="Inter" font-size="9" text-anchor="middle">Process Isolation</text>
  </g>
</svg>'''
    elif 'PERMISSION MODES' in title_upper or 'RISK TIERS' in title_upper:
        return '''<svg viewBox="0 0 800 100" style="width:100%; max-height:100px; margin:0.3rem 0;">
  <g transform="translate(15, 8)">
    <rect x="0" y="0" width="175" height="80" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="1.8"/>
    <text x="87" y="28" fill="#141413" font-family="Inter" font-size="11" font-weight="800" text-anchor="middle">LOW RISK</text>
    <text x="87" y="48" fill="#6B6B63" font-family="Inter" font-size="9.5" text-anchor="middle">read_file, list_dir, grep</text>
    <text x="87" y="66" fill="#141413" font-family="Inter" font-size="9.5" font-weight="700" text-anchor="middle">✓ Auto-Approved</text>
  </g>
  <g transform="translate(205, 8)">
    <rect x="0" y="0" width="175" height="80" rx="8" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="1.8"/>
    <text x="87" y="28" fill="#141413" font-family="Inter" font-size="11" font-weight="800" text-anchor="middle">MEDIUM RISK</text>
    <text x="87" y="48" fill="#6B6B63" font-family="Inter" font-size="9.5" text-anchor="middle">write_file, run_test</text>
    <text x="87" y="66" fill="#141413" font-family="Inter" font-size="9.5" font-weight="700" text-anchor="middle">✓ Logged &amp; Approved</text>
  </g>
  <g transform="translate(395, 8)">
    <rect x="0" y="0" width="185" height="80" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="1.8"/>
    <text x="92" y="28" fill="#141413" font-family="Inter" font-size="11" font-weight="800" text-anchor="middle">HIGH RISK</text>
    <text x="92" y="48" fill="#6B6B63" font-family="Inter" font-size="9.5" text-anchor="middle">pip_install</text>
    <text x="92" y="66" fill="#BD5D3A" font-family="Inter" font-size="9.5" font-weight="700" text-anchor="middle">⚠ Intent Logged Alert</text>
  </g>
  <g transform="translate(595, 8)">
    <rect x="0" y="0" width="185" height="80" rx="8" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="1.8"/>
    <text x="92" y="28" fill="#141413" font-family="Inter" font-size="11" font-weight="800" text-anchor="middle">CRITICAL RISK</text>
    <text x="92" y="48" fill="#BD5D3A" font-family="Inter" font-size="9.5" font-weight="700" text-anchor="middle">git_push, db_drop</text>
    <text x="92" y="66" fill="#BD5D3A" font-family="Inter" font-size="9.5" font-weight="800" text-anchor="middle">⛔ approvals.json Ledger</text>
  </g>
</svg>'''
    elif 'TDA LOOP' in title_upper:
        return '''<svg viewBox="0 0 800 100" style="width:100%; max-height:100px; margin:0.3rem 0;">
  <rect x="15" y="10" width="165" height="80" rx="10" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
  <text x="97" y="36" fill="#141413" font-family="Inter" font-size="11" font-weight="800" text-anchor="middle">1. RED: Failing Test</text>
  <text x="97" y="58" fill="#6B6B63" font-family="Inter" font-size="9.5" text-anchor="middle">From SPEC.md Criteria</text>
  <path d="M180 50 L215 50" stroke="#BD5D3A" stroke-width="3"/>
  <rect x="215" y="10" width="165" height="80" rx="10" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
  <text x="297" y="36" fill="#141413" font-family="Inter" font-size="11" font-weight="800" text-anchor="middle">2. Agent Edit</text>
  <text x="297" y="58" fill="#6B6B63" font-family="Inter" font-size="9.5" text-anchor="middle">Code Implementation</text>
  <path d="M380 50 L415 50" stroke="#D97757" stroke-width="3"/>
  <rect x="415" y="10" width="175" height="80" rx="10" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
  <text x="502" y="36" fill="#141413" font-family="Inter" font-size="11" font-weight="800" text-anchor="middle">3. Pytest Subprocess</text>
  <text x="502" y="58" fill="#BD5D3A" font-family="Inter" font-size="9.5" font-weight="700" text-anchor="middle">Extract Real Traceback</text>
  <path d="M590 50 L625 50" stroke="#BD5D3A" stroke-width="3"/>
  <rect x="625" y="10" width="160" height="80" rx="10" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="2"/>
  <text x="705" y="36" fill="#141413" font-family="Inter" font-size="11" font-weight="800" text-anchor="middle">4. Anti-Regression</text>
  <text x="705" y="58" fill="#141413" font-family="Inter" font-size="9.5" font-weight="700" text-anchor="middle">Lock Test in Suite</text>
</svg>'''
    elif 'FIVE-STEP SOP' in title_upper:
        return '''<svg viewBox="0 0 800 95" style="width:100%; max-height:95px; margin:0.3rem 0;">
  <g transform="translate(10, 8)">
    <rect x="0" y="0" width="145" height="75" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="1.8"/>
    <text x="72" y="28" fill="#141413" font-family="Inter" font-size="10.5" font-weight="800" text-anchor="middle">1. Spec First</text>
    <text x="72" y="48" fill="#6B6B63" font-family="Inter" font-size="9" text-anchor="middle">parse_spec(SPEC.md)</text>
  </g>
  <g transform="translate(165, 8)">
    <rect x="0" y="0" width="145" height="75" rx="8" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="1.8"/>
    <text x="72" y="28" fill="#141413" font-family="Inter" font-size="10.5" font-weight="800" text-anchor="middle">2. Sandbox</text>
    <text x="72" y="48" fill="#6B6B63" font-family="Inter" font-size="9" text-anchor="middle">ScopeEnforcer write</text>
  </g>
  <g transform="translate(320, 8)">
    <rect x="0" y="0" width="145" height="75" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="1.8"/>
    <text x="72" y="28" fill="#141413" font-family="Inter" font-size="10.5" font-weight="800" text-anchor="middle">3. Guardrails</text>
    <text x="72" y="48" fill="#6B6B63" font-family="Inter" font-size="9" text-anchor="middle">AST &amp; Secret Scan</text>
  </g>
  <g transform="translate(475, 8)">
    <rect x="0" y="0" width="145" height="75" rx="8" fill="#FAF9F5" stroke="#BD5D3A" stroke-width="1.8"/>
    <text x="72" y="28" fill="#141413" font-family="Inter" font-size="10.5" font-weight="800" text-anchor="middle">4. Test Loop</text>
    <text x="72" y="48" fill="#6B6B63" font-family="Inter" font-size="9" text-anchor="middle">Pytest Subprocess</text>
  </g>
  <g transform="translate(630, 8)">
    <rect x="0" y="0" width="155" height="75" rx="8" fill="#FAF9F5" stroke="#D97757" stroke-width="1.8"/>
    <text x="77" y="28" fill="#141413" font-family="Inter" font-size="10.5" font-weight="800" text-anchor="middle">5. Human Review</text>
    <text x="77" y="48" fill="#141413" font-family="Inter" font-size="9" font-weight="700" text-anchor="middle">Diff &amp; PR Merge</text>
  </g>
</svg>'''
    elif 'SCORECARD' in title_upper or 'WRAP-UP' in title_upper or 'READINESS' in title_upper:
        return '''<svg viewBox="0 0 800 100" style="width:100%; max-height:100px; margin:0.3rem 0;">
  <rect x="20" y="10" width="760" height="80" rx="12" fill="#FAF9F5" stroke="#D97757" stroke-width="2"/>
  <text x="400" y="38" fill="#141413" font-family="Inter" font-size="14" font-weight="900" text-anchor="middle">PRODUCTION READINESS SCORECARD: 100% PASS</text>
  <text x="400" y="60" fill="#141413" font-family="Inter" font-size="11" font-weight="700" text-anchor="middle">✓ Memory (AGENTS.md)  ✓ Sandboxing  ✓ PreToolUse Hooks  ✓ TDA Pytest  ✓ MCP Tools</text>
  <text x="400" y="78" fill="#6B6B63" font-family="Inter" font-size="9.5" text-anchor="middle">Verified Harness Engineering Control &amp; Reliability Framework (10 Modules)</text>
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
  <title>Packt Masterclass Presentation: 72 Interactive Code & Architecture Slides</title>
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
      height: 52px;
      flex: 0 0 52px;
      background: var(--surface);
      border-bottom: 1px solid var(--rule);
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0 1.2rem;
      z-index: 50;
      gap: 1rem;
      overflow-x: auto;
    }
    .header-left { display: flex; align-items: center; gap: 0.8rem; flex: 0 0 auto; }
    .brand-logo {
      width: 34px; height: 34px;
      background: var(--accent-sf); color: var(--ink); border: 1px solid var(--rule);
      border-radius: 8px; font-weight: 800; display: flex; align-items: center; justify-content: center;
      font-size: 0.9rem;
    }
    .brand-title { font-weight: 650; font-size: 0.95rem; white-space: nowrap; }

    .controls { display: flex; align-items: center; gap: 0.5rem; flex: 0 0 auto; }
    .btn {
      background: var(--surface); border: 1px solid var(--rule); color: var(--ink);
      padding: 0.42rem 0.75rem; border-radius: 8px; font-weight: 600; font-size: 0.8rem;
      cursor: pointer; transition: background-color 0.16s, border-color 0.16s; text-decoration: none;
      white-space: nowrap;
    }
    .btn:hover { background: var(--accent-sf); border-color: var(--accent); }
    .btn:focus-visible, .slide-select:focus-visible { outline: 2px solid var(--accent-dk); outline-offset: 2px; }
    .btn-primary { background: var(--accent); border-color: var(--accent); color: var(--ink); font-weight: 700; }
    .btn-primary:hover { background: var(--accent-sf); border-color: var(--accent-dk); color: var(--ink); }
    
    select.slide-select {
      background: var(--surface); color: var(--ink); border: 1px solid var(--rule);
      padding: 0.42rem 0.65rem; border-radius: 8px; font-family: var(--font-body);
      font-size: 0.8rem; font-weight: 600;
      max-width: 340px;
    }

    main {
      flex: 1;
      position: relative;
      overflow: hidden;
    }

    .slide-viewport {
      width: 100%; height: 100%;
      display: flex; justify-content: center; align-items: center;
      padding: clamp(0.4rem, 1vw, 0.8rem);
    }
    .slide-card {
      width: 100%; max-width: 1360px; height: 100%;
      background: var(--surface); border: 1px solid var(--rule);
      border-radius: 12px; padding: clamp(1rem, 2vw, 1.6rem); display: flex; flex-direction: column;
      position: relative; overflow: hidden;
    }
    .slide-header {
      display: flex; justify-content: space-between; align-items: center;
      gap: 1rem; margin-bottom: 0.5rem; border-bottom: 1px solid var(--rule); padding-bottom: 0.5rem;
      flex: 0 0 auto;
    }
    .slide-title-wrap { min-width: 0; }
    .slide-title {
      font-family: var(--font-display); font-size: clamp(1.4rem, 2.5vw, 1.95rem);
      font-weight: 650; line-height: 1.15; letter-spacing: -0.015em; color: var(--ink);
    }
    .slide-num-badge {
      background: var(--accent-sf); color: var(--ink); border: 1px solid var(--rule);
      padding: 0.28rem 0.7rem; border-radius: 9999px; font-size: 0.78rem; font-weight: 750; white-space: nowrap;
      flex: 0 0 auto;
    }
    .slide-body {
      --fit-scale: 1;
      --slide-body-base-size: 1.15rem;
      flex: 1; min-height: 0; overflow-y: auto; padding-right: 0.35rem;
      font-size: calc(var(--slide-body-base-size) * var(--fit-scale));
      color: var(--ink); line-height: 1.45;
    }
    .slide-body > svg {
      display: block; width: 100% !important; height: auto; max-width: 100%;
      margin-bottom: 0.5rem;
    }

    /* Enhanced Code Slide Layout with Line-Level Highlights */
    .code-slide-container {
      display: grid;
      grid-template-columns: minmax(0, 1.35fr) minmax(0, 1.05fr);
      gap: 1.15rem;
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
      max-height: calc(100vh - 170px);
    }
    .code-editor-header {
      background: #242320;
      border-bottom: 1px solid var(--code-rule);
      padding: 0.45rem 0.8rem;
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
      width: 10px; height: 10px; border-radius: 50%;
    }
    .dot-red { background: #E06C75; }
    .dot-yellow { background: #E5C07B; }
    .dot-green { background: #98C379; }
    .code-file-tag {
      font-family: var(--font-code);
      font-size: 0.75rem;
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
      font-size: 0.68rem;
      padding: 0.15rem 0.45rem;
      border-radius: 4px;
      font-weight: 600;
      text-transform: uppercase;
    }

    .code-block {
      background: var(--code-bg);
      color: #FAF9F5;
      font-family: var(--font-code);
      font-size: 0.80rem;
      line-height: 1.44;
      padding: 0.5rem 0;
      margin: 0;
      overflow-x: auto;
      overflow-y: auto;
    }

    .code-line {
      display: flex;
      align-items: baseline;
      padding: 0.08rem 0.6rem;
      transition: background-color 0.15s;
    }
    .code-line:hover {
      background: rgba(255, 255, 255, 0.04);
    }
    .code-line-hl {
      background: rgba(217, 119, 87, 0.22);
      border-left: 3.5px solid var(--accent);
      padding-left: calc(0.6rem - 3.5px);
    }
    .line-num {
      color: #5C5C56;
      width: 24px;
      flex: 0 0 24px;
      text-align: right;
      margin-right: 8px;
      font-size: 0.75rem;
      user-select: none;
    }
    .code-line-hl .line-num {
      color: var(--accent);
      font-weight: 700;
    }
    .key-badge {
      background: var(--accent);
      color: #FAF9F5;
      font-size: 0.60rem;
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
      gap: 0.65rem;
      overflow-y: auto;
      max-height: calc(100vh - 170px);
      padding-right: 0.25rem;
    }
    .code-concepts-list {
      display: flex;
      flex-direction: column;
      gap: 0.6rem;
    }
    .code-concept-card {
      background: var(--surface);
      border: 1px solid var(--rule);
      border-left: 3.5px solid var(--accent);
      border-radius: 8px;
      padding: 0.65rem 0.85rem;
      box-shadow: 0 1px 4px rgba(0,0,0,0.03);
    }
    .concept-card-head {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      margin-bottom: 0.3rem;
      flex-wrap: wrap;
    }
    .concept-tag {
      background: var(--accent);
      color: #FAF9F5;
      font-size: 0.68rem;
      font-weight: 750;
      padding: 0.12rem 0.45rem;
      border-radius: 4px;
      font-family: var(--font-code);
      letter-spacing: 0.02em;
      white-space: nowrap;
    }
    .concept-name {
      font-family: var(--font-display);
      font-size: 0.96rem;
      font-weight: 700;
      color: var(--ink);
    }
    .concept-card-text {
      font-size: 0.84rem;
      color: var(--ink);
      line-height: 1.42;
    }

    .invariant-card {
      background: var(--surface);
      border: 1px solid var(--rule);
      border-left: 3.5px solid var(--accent-dk);
      border-radius: 8px;
      padding: 0.65rem 0.85rem;
      font-size: 0.82rem;
      color: var(--ink-muted);
      line-height: 1.4;
    }
    .invariant-title {
      font-family: var(--font-display);
      font-size: 0.94rem;
      font-weight: 700;
      color: var(--ink);
      margin-bottom: 0.25rem;
      display: flex;
      align-items: center;
      gap: 0.35rem;
    }

    /* Visual Hierarchy: Parent vs Sub Bullets */
    .main-bullets { list-style-type: none; padding-left: 0; margin-top: 0.35rem; }
    .main-bullets.dense-columns {
      column-count: 2; column-gap: clamp(1.2rem, 3vw, 2.5rem); column-fill: balance;
    }
    .bullet-group, .primary-bullet, .sub-bullets, .sub-bullet {
      break-inside: avoid; page-break-inside: avoid;
    }
    .primary-bullet {
      font-family: var(--font-display); font-size: 1.12em; font-weight: 700; color: var(--ink);
      margin-top: 0.55em; margin-bottom: 0.2em; display: flex; align-items: center; gap: 0.5em;
    }
    .primary-bullet::before {
      content: "◆"; color: var(--accent); font-size: 0.65rem;
    }
    .sub-bullets {
      list-style-type: none; padding-left: 1.25em; border-left: 1px solid var(--rule);
      margin-left: 0.3em; margin-bottom: 0.55em;
    }
    .sub-bullet {
      font-size: 0.96em; color: var(--ink); margin-bottom: 0.24em; position: relative; padding-left: 0.9em;
    }
    .sub-bullet::before {
      content: "›"; position: absolute; left: 0; color: var(--accent-dk); font-weight: 800; font-size: 1.05rem; line-height: 1;
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
      font-family: var(--font-code); font-size: 0.86em; font-weight: 600;
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
      header { padding: 0 0.8rem; }
      .brand-title { display: none; }
      select.slide-select { max-width: 210px; }
    }
  </style>
</head>
<body>

  <header>
    <div class="header-left">
      <div class="brand-logo">HE</div>
      <div class="brand-title">Harness Engineering Masterclass Slides</div>
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
          <div class="slide-title-wrap">
            <div id="slide-title" class="slide-title">Slide Title</div>
          </div>
          <div id="slide-num-badge" class="slide-num-badge">Slide 1 / 72</div>
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
      text = text.replace(/^(\\d+[\\.\\)\\:]|\\d+\\s*&\\s*\\d+[\\.\\)\\:])\\s*/, '');
      text = text.replace(/^(Pillar|Layer|Step|Phase|Check)\\s*\\d+[\\.\\)\\:]?\\s*/i, '');
      return text.trim();
    }

    function formatTextWithCode(text) {
      const keywords = ['CLAUDE.md', 'AGENTS.md', 'SPEC.md', 'pytest', 'events.jsonl', 'telemetry.jsonl', 'rm -rf', 'write_file', 'read_file', '.claude-plugin/plugin.json', 'SKILL.md', 'mcp_client_runner.py', 'mcp_server_demo.py', 'core_harness_stack.py', 'guardrails_engine.py', 'spec_driven_verifier.py', 'tda_reliability_pipeline.py', 'multi_agent_team_simulator.py', 'five_step_sop_pipeline.py', 'production_harness_audit.py', 'is_relative_to()', 'ast.parse()', 'PreToolUse', 'PostToolUse', 'MCPServer', 'permissionDecision', 'approvals.json', 'ZeroDivisionError', 'pending_push.json'];
      keywords.forEach(kw => {
        text = text.replaceAll(kw, `<code>${kw}</code>`);
      });
      return text.replace(
        /(https:\\/\\/[^\\s<]+)/g,
        '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>'
      );
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
        let cleanText = trimmed.replace(/^[•\\-\\ufffd]\\s*/, '').trim();
        cleanText = cleanNumbers(cleanText);
        const labUrl = cleanText.match(/^Lab demo:\\s*(https:\\/\\/[^\\s]+)/i);
        if (labUrl) {
          cleanText = `<a href="${labUrl[1]}" target="_blank" rel="noopener noreferrer">🔗 Lab demo: open this module in GitHub</a>`;
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

      if (slide.slide_type === 'code' && slide.highlighted_code) {
        const fileTag = slide.code_filename || 'source.py';
        const rawBullets = slide.raw_lines.slice(1);
        bodyHtml += `
          <div class="code-slide-container">
            <div class="code-editor-window">
              <div class="code-editor-header">
                <div class="code-dots">
                  <div class="code-dot dot-red"></div>
                  <div class="code-dot dot-yellow"></div>
                  <div class="code-dot dot-green"></div>
                </div>
                <div class="code-file-tag">📄 ${fileTag}</div>
                <div class="code-lang-tag">${slide.code_language || 'PYTHON'}</div>
              </div>
              <div class="code-block">${slide.highlighted_code}</div>
            </div>
            <div class="code-concepts-column">
              ${formatCodeConcepts(rawBullets)}
              <div class="invariant-card">
                <div class="invariant-title">🛡️ Execution &amp; Control Invariant</div>
                Verified directly against tests in <code>${fileTag.split('/')[1] || 'course_implementation'}</code>.
              </div>
            </div>
          </div>
        `;
      } else {
        const restLines = slide.raw_lines.slice(1);
        if (restLines.length > 0) {
          bodyHtml += formatBullets(restLines);
        }
      }

      bodyEl.innerHTML = bodyHtml;
      
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
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') nextSlide();
      if (e.key === 'ArrowLeft' || e.key === 'PageUp') prevSlide();
      if (e.key === 'f' || e.key === 'F') toggleFullscreen();
      if (e.key === 'm' || e.key === 'M') toggleMode();
    });

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

print(f"SUCCESSFULLY GENERATED {len(slides)} INTERACTIVE HTML SLIDES WITH ENHANCED CODE CONCEPTS & CLEAN SYNTAX HIGHLIGHTING!")
