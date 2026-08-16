"""
Generates Publication-Grade Architecture and Flow Diagrams in SVG and 4K PNG
with a crisp, clean WHITE BACKGROUND design system.
"""

import asyncio
from pathlib import Path
import shutil
from playwright.async_api import async_playwright

DOCS_DIR = Path("deep_research_agent/docs")
DOCS_DIR.mkdir(parents=True, exist_ok=True)
ARTIFACT_DIR = Path(r"C:\Users\kenhu\.gemini\antigravity-cli\brain\34f929e5-1335-4eeb-a7ac-dfb192af729a")

# 1. System Architecture Diagram SVG (White Background, 1920 x 1080)
ARCHITECTURE_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="100%" height="100%" style="background-color: #ffffff; font-family: 'Inter', -apple-system, sans-serif;">
  <defs>
    <filter id="shadowArchWhite" x="-2%" y="-2%" width="104%" height="104%">
      <feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="#000000" flood-opacity="0.08"/>
    </filter>
  </defs>

  <!-- Canvas Header -->
  <rect x="0" y="0" width="1920" height="110" fill="#f8fafc" />
  <line x1="0" y1="110" x2="1920" y2="110" stroke="#059669" stroke-width="3" />
  
  <text x="60" y="55" fill="#0f172a" font-size="34" font-weight="800" letter-spacing="-0.5px">⚛️ Autonomous Deep Research Agent — System Architecture</text>
  <text x="60" y="90" fill="#475569" font-size="18" font-weight="600">10-Module Harness Stack: Spec-Driven Contracts, Model Context Protocol (MCP 2.x), Multi-Agent Worktrees, &amp; TDA Verification</text>
  
  <rect x="1510" y="32" width="350" height="48" rx="8" fill="#ecfdf5" stroke="#059669" stroke-width="2"/>
  <text x="1685" y="62" fill="#047857" font-size="18" font-weight="800" text-anchor="middle">5-Gate Scorecard: 100% Certified</text>

  <!-- ==================== LAYER 1: UI & PRESENTATION ==================== -->
  <g transform="translate(60, 140)" filter="url(#shadowArchWhite)">
    <rect width="1800" height="150" rx="14" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect width="1800" height="40" rx="14" fill="#f1f5f9"/>
    <text x="30" y="27" fill="#1d4ed8" font-size="16" font-weight="800">LAYER 1: USER INTERACTION &amp; DASHBOARD (Web UI 2.0)</text>
    
    <!-- Component 1.1 -->
    <rect x="30" y="55" width="410" height="75" rx="8" fill="#f8fafc" stroke="#2563eb" stroke-width="2"/>
    <text x="50" y="85" fill="#0f172a" font-size="17" font-weight="700">Research Controller</text>
    <text x="50" y="112" fill="#475569" font-size="14">Objective Input, Depth Presets, 1-Click Chips</text>

    <!-- Component 1.2 -->
    <rect x="470" y="55" width="410" height="75" rx="8" fill="#f8fafc" stroke="#059669" stroke-width="2"/>
    <text x="490" y="85" fill="#0f172a" font-size="17" font-weight="700">Interactive SVG Research Graph</text>
    <text x="490" y="112" fill="#475569" font-size="14">Live Multi-Hop Node Expansion &amp; State Links</text>

    <!-- Component 1.3 -->
    <rect x="910" y="55" width="410" height="75" rx="8" fill="#f8fafc" stroke="#d97706" stroke-width="2"/>
    <text x="930" y="85" fill="#0f172a" font-size="17" font-weight="700">Citation &amp; Evidence Matrix</text>
    <text x="930" y="112" fill="#475569" font-size="14">Confidence Badges, Primary Quotes, Domains</text>

    <!-- Component 1.4 -->
    <rect x="1350" y="55" width="420" height="75" rx="8" fill="#f8fafc" stroke="#7c3aed" stroke-width="2"/>
    <text x="1370" y="85" fill="#0f172a" font-size="17" font-weight="700">Dossier, Diff &amp; Scorecard Tabs</text>
    <text x="1370" y="112" fill="#475569" font-size="14">Markdown Reader, Line Diffs, 5-Gate Audit</text>
  </g>

  <!-- ==================== LAYER 2: HARNESS GOVERNANCE & SECURITY ==================== -->
  <g transform="translate(60, 320)" filter="url(#shadowArchWhite)">
    <rect width="1800" height="150" rx="14" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect width="1800" height="40" rx="14" fill="#f1f5f9"/>
    <text x="30" y="27" fill="#047857" font-size="16" font-weight="800">LAYER 2: HARNESS GOVERNANCE, CONTRACTS &amp; GUARDRAILS (Modules 1, 2, 3, 4, 5)</text>

    <!-- Component 2.1 -->
    <rect x="30" y="55" width="410" height="75" rx="8" fill="#f8fafc" stroke="#059669" stroke-width="2"/>
    <text x="50" y="85" fill="#0f172a" font-size="17" font-weight="700">Memory &amp; Spec Contracts</text>
    <text x="50" y="112" fill="#475569" font-size="14">CLAUDE.md Invariants, SPEC.md Whitelists</text>

    <!-- Component 2.2 -->
    <rect x="470" y="55" width="410" height="75" rx="8" fill="#f8fafc" stroke="#dc2626" stroke-width="2"/>
    <text x="490" y="85" fill="#0f172a" font-size="17" font-weight="700">PreToolUse Hooks &amp; AST Guard</text>
    <text x="490" y="112" fill="#475569" font-size="14">Deny Dangerous CLI, Scan High-Entropy Keys</text>

    <!-- Component 2.3 -->
    <rect x="910" y="55" width="410" height="75" rx="8" fill="#f8fafc" stroke="#d97706" stroke-width="2"/>
    <text x="930" y="85" fill="#0f172a" font-size="17" font-weight="700">Permission Escalation Gateway</text>
    <text x="930" y="112" fill="#475569" font-size="14">4-Tier Matrix, HMAC Signatures in approvals.json</text>

    <!-- Component 2.4 -->
    <rect x="1350" y="55" width="420" height="75" rx="8" fill="#f8fafc" stroke="#2563eb" stroke-width="2"/>
    <text x="1370" y="85" fill="#0f172a" font-size="17" font-weight="700">Token Budgeter &amp; Loop Trap</text>
    <text x="1370" y="112" fill="#475569" font-size="14">20/20/50/10 Budgeting, SHA-256 Rolling Deque</text>
  </g>

  <!-- ==================== LAYER 3: ORCHESTRATION & COMPOUND MULTI-AGENTS ==================== -->
  <g transform="translate(60, 500)" filter="url(#shadowArchWhite)">
    <rect width="1800" height="150" rx="14" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect width="1800" height="40" rx="14" fill="#f1f5f9"/>
    <text x="30" y="27" fill="#b45309" font-size="16" font-weight="800">LAYER 3: COMPOUND MULTI-AGENT ORCHESTRATOR &amp; 5-STEP SOP (Modules 8 &amp; 9)</text>

    <!-- Component 3.1 -->
    <rect x="30" y="55" width="330" height="75" rx="8" fill="#f8fafc" stroke="#2563eb" stroke-width="2"/>
    <text x="50" y="85" fill="#0f172a" font-size="17" font-weight="700">Planner Subagent</text>
    <text x="50" y="112" fill="#475569" font-size="14">Multi-Hop Query Decomposition</text>

    <!-- Component 3.2 -->
    <rect x="390" y="55" width="330" height="75" rx="8" fill="#f8fafc" stroke="#059669" stroke-width="2"/>
    <text x="410" y="85" fill="#0f172a" font-size="17" font-weight="700">Crawler Subagent</text>
    <text x="410" y="112" fill="#475569" font-size="14">Parallel Index Harvest &amp; Ingest</text>

    <!-- Component 3.3 -->
    <rect x="750" y="55" width="330" height="75" rx="8" fill="#f8fafc" stroke="#7c3aed" stroke-width="2"/>
    <text x="770" y="85" fill="#0f172a" font-size="17" font-weight="700">Fact-Checker Subagent</text>
    <text x="770" y="112" fill="#475569" font-size="14">Claim Audit &amp; Grounding Math</text>

    <!-- Component 3.4 -->
    <rect x="1110" y="55" width="330" height="75" rx="8" fill="#f8fafc" stroke="#d97706" stroke-width="2"/>
    <text x="1130" y="85" fill="#0f172a" font-size="17" font-weight="700">Synthesizer Subagent</text>
    <text x="1130" y="112" fill="#475569" font-size="14">Academic Dossier Assembly</text>

    <!-- Component 3.5 -->
    <rect x="1470" y="55" width="300" height="75" rx="8" fill="#f8fafc" stroke="#db2777" stroke-width="2"/>
    <text x="1490" y="85" fill="#0f172a" font-size="17" font-weight="700">Ephemeral Worktrees</text>
    <text x="1490" y="112" fill="#475569" font-size="14">Git Isolation &amp; Clean Teardown</text>
  </g>

  <!-- ==================== LAYER 4: INTEGRATION & MODEL CONTEXT PROTOCOL (MCP 2.x) ==================== -->
  <g transform="translate(60, 680)" filter="url(#shadowArchWhite)">
    <rect width="1800" height="150" rx="14" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect width="1800" height="40" rx="14" fill="#f1f5f9"/>
    <text x="30" y="27" fill="#6d28d9" font-size="16" font-weight="800">LAYER 4: MODEL CONTEXT PROTOCOL (MCP 2.x) &amp; LIVE DATA SOURCES (Module 7)</text>

    <!-- Component 4.1 -->
    <rect x="30" y="55" width="410" height="75" rx="8" fill="#f8fafc" stroke="#7c3aed" stroke-width="2"/>
    <text x="50" y="85" fill="#0f172a" font-size="17" font-weight="700">MCP Research Server</text>
    <text x="50" y="112" fill="#475569" font-size="14">JSON-RPC 2.0 Stdio IPC Process</text>

    <!-- Component 4.2 -->
    <rect x="470" y="55" width="410" height="75" rx="8" fill="#f8fafc" stroke="#2563eb" stroke-width="2"/>
    <text x="490" y="85" fill="#0f172a" font-size="17" font-weight="700">Live arXiv Open Science API</text>
    <text x="490" y="112" fill="#475569" font-size="14">Peer-Reviewed Papers &amp; Preprints</text>

    <!-- Component 4.3 -->
    <rect x="910" y="55" width="410" height="75" rx="8" fill="#f8fafc" stroke="#059669" stroke-width="2"/>
    <text x="930" y="85" fill="#0f172a" font-size="17" font-weight="700">Live Wikipedia REST API</text>
    <text x="930" y="112" fill="#475569" font-size="14">Real-Time Global Encyclopedia Indexes</text>

    <!-- Component 4.4 -->
    <rect x="1350" y="55" width="420" height="75" rx="8" fill="#f8fafc" stroke="#d97706" stroke-width="2"/>
    <text x="1370" y="85" fill="#0f172a" font-size="17" font-weight="700">Local Vector &amp; Cache Store</text>
    <text x="1370" y="112" fill="#475569" font-size="14">Deterministic Offline Grounding &amp; Fallbacks</text>
  </g>

  <!-- ==================== LAYER 5: VERIFICATION, TDA & AUDIT SCORECARD ==================== -->
  <g transform="translate(60, 860)" filter="url(#shadowArchWhite)">
    <rect width="1800" height="150" rx="14" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect width="1800" height="40" rx="14" fill="#f1f5f9"/>
    <text x="30" y="27" fill="#047857" font-size="16" font-weight="800">LAYER 5: TEST RELIABILITY, TELEMETRY &amp; PRODUCTION READINESS (Modules 6 &amp; 10)</text>

    <!-- Component 5.1 -->
    <rect x="30" y="55" width="410" height="75" rx="8" fill="#f8fafc" stroke="#059669" stroke-width="2"/>
    <text x="50" y="85" fill="#0f172a" font-size="17" font-weight="700">Pytest TDA Reliability Loop</text>
    <text x="50" y="112" fill="#475569" font-size="14">Red-Repair-Green Cycles, Anti-Regression</text>

    <!-- Component 5.2 -->
    <rect x="470" y="55" width="410" height="75" rx="8" fill="#f8fafc" stroke="#2563eb" stroke-width="2"/>
    <text x="490" y="85" fill="#0f172a" font-size="17" font-weight="700">5-Gate Production Auditor</text>
    <text x="490" y="112" fill="#475569" font-size="14">Memory, Hooks, Tests, MCP, Subagents</text>

    <!-- Component 5.3 -->
    <rect x="910" y="55" width="410" height="75" rx="8" fill="#f8fafc" stroke="#d97706" stroke-width="2"/>
    <text x="930" y="85" fill="#0f172a" font-size="17" font-weight="700">Unified Diff Engine</text>
    <text x="930" y="112" fill="#475569" font-size="14">Line-by-Line Markdown Mutation Review</text>

    <!-- Component 5.4 -->
    <rect x="1350" y="55" width="420" height="75" rx="8" fill="#f8fafc" stroke="#7c3aed" stroke-width="2"/>
    <text x="1370" y="85" fill="#0f172a" font-size="17" font-weight="700">Structured Telemetry Stream</text>
    <text x="1370" y="112" fill="#475569" font-size="14">events.jsonl &amp; telemetry.jsonl Audit Trail</text>
  </g>

  <!-- Connective Arrows & Flow Indicators -->
  <path d="M 960 290 L 960 320" stroke="#2563eb" stroke-width="3" stroke-dasharray="6,4"/>
  <path d="M 960 470 L 960 500" stroke="#059669" stroke-width="3" stroke-dasharray="6,4"/>
  <path d="M 960 650 L 960 680" stroke="#d97706" stroke-width="3" stroke-dasharray="6,4"/>
  <path d="M 960 830 L 960 860" stroke="#7c3aed" stroke-width="3" stroke-dasharray="6,4"/>
</svg>
"""

# 2. Execution Flow Diagram SVG (White Background, 1920 x 1080)
FLOW_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="100%" height="100%" style="background-color: #ffffff; font-family: 'Inter', -apple-system, sans-serif;">
  <defs>
    <filter id="shadowFlowWhite" x="-2%" y="-2%" width="104%" height="104%">
      <feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="#000000" flood-opacity="0.08"/>
    </filter>
    <marker id="arrowBlue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#2563eb"/>
    </marker>
    <marker id="arrowGreen" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#059669"/>
    </marker>
    <marker id="arrowAmber" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#d97706"/>
    </marker>
    <marker id="arrowPurple" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#7c3aed"/>
    </marker>
    <marker id="arrowRed" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#dc2626"/>
    </marker>
  </defs>

  <!-- Canvas Header -->
  <rect x="0" y="0" width="1920" height="110" fill="#f8fafc" />
  <line x1="0" y1="110" x2="1920" y2="110" stroke="#2563eb" stroke-width="3" />
  
  <text x="60" y="55" fill="#0f172a" font-size="34" font-weight="800" letter-spacing="-0.5px">🔄 Autonomous Deep Research Agent — End-to-End Execution Flow</text>
  <text x="60" y="90" fill="#475569" font-size="18" font-weight="600">Deterministic 8-Stage Execution Pipeline from User Hypothesis to 5-Gate Certified Research Dossier</text>
  
  <rect x="1510" y="32" width="350" height="48" rx="8" fill="#eff6ff" stroke="#2563eb" stroke-width="2"/>
  <text x="1685" y="62" fill="#1d4ed8" font-size="18" font-weight="800" text-anchor="middle">SOP Pipeline: 100% Deterministic</text>

  <!-- ==================== TOP ROW: STAGES 1 TO 4 ==================== -->
  
  <!-- Step 1 -->
  <g transform="translate(60, 150)" filter="url(#shadowFlowWhite)">
    <rect width="410" height="400" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect width="410" height="50" rx="12" fill="#eff6ff"/>
    <text x="25" y="33" fill="#1d4ed8" font-size="18" font-weight="800">STAGE 1: SPEC CONTRACT</text>
    
    <text x="25" y="85" fill="#0f172a" font-size="16" font-weight="700">1. User Query &amp; Invariants</text>
    <text x="25" y="115" fill="#334155" font-size="14">
      <tspan x="25" dy="0">• Ingests user research objective</tspan>
      <tspan x="25" dy="24">• Formulates machine SPEC.md</tspan>
      <tspan x="25" dy="24">• Declares allowed whitelists &amp; goals</tspan>
      <tspan x="25" dy="24">• Enforces CLAUDE.md memory rules</tspan>
    </text>
    
    <rect x="25" y="270" width="360" height="105" rx="6" fill="#f8fafc" stroke="#2563eb" stroke-width="1.5"/>
    <text x="40" y="298" fill="#047857" font-size="14" font-family="monospace" font-weight="800">✅ INVARIANT CHECK</text>
    <text x="40" y="324" fill="#334155" font-size="13">SpecVerifier.is_file_allowed()</text>
    <text x="40" y="346" fill="#64748b" font-size="13">Non-whitelisted mutations DENIED</text>
  </g>

  <!-- Arrow 1 -> 2 -->
  <line x1="475" y1="350" x2="515" y2="350" stroke="#2563eb" stroke-width="5" marker-end="url(#arrowBlue)"/>

  <!-- Step 2 -->
  <g transform="translate(520, 150)" filter="url(#shadowFlowWhite)">
    <rect width="410" height="400" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect width="410" height="50" rx="12" fill="#ecfdf5"/>
    <text x="25" y="33" fill="#047857" font-size="18" font-weight="800">STAGE 2: WORKTREE SANDBOX</text>
    
    <text x="25" y="85" fill="#0f172a" font-size="16" font-weight="700">2. Ephemeral Isolation &amp; Crawl</text>
    <text x="25" y="115" fill="#334155" font-size="14">
      <tspan x="25" dy="0">• Spawns ephemeral git worktree</tspan>
      <tspan x="25" dy="24">• Planner splits 4 multi-hop tracks</tspan>
      <tspan x="25" dy="24">• Invokes Crawler subagent in parallel</tspan>
      <tspan x="25" dy="24">• Zero risk to main branch repository</tspan>
    </text>
    
    <rect x="25" y="270" width="360" height="105" rx="6" fill="#f8fafc" stroke="#059669" stroke-width="1.5"/>
    <text x="40" y="298" fill="#047857" font-size="14" font-family="monospace" font-weight="800">✅ ISOLATION CHECK</text>
    <text x="40" y="324" fill="#334155" font-size="13">WorktreeIsolation.add(role)</text>
    <text x="40" y="346" fill="#64748b" font-size="13">Path.resolve().is_relative_to()</text>
  </g>

  <!-- Arrow 2 -> 3 -->
  <line x1="935" y1="350" x2="975" y2="350" stroke="#059669" stroke-width="5" marker-end="url(#arrowGreen)"/>

  <!-- Step 3 -->
  <g transform="translate(980, 150)" filter="url(#shadowFlowWhite)">
    <rect width="410" height="400" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect width="410" height="50" rx="12" fill="#f5f3ff"/>
    <text x="25" y="33" fill="#6d28d9" font-size="18" font-weight="800">STAGE 3: MCP 2.x CRAWL</text>
    
    <text x="25" y="85" fill="#0f172a" font-size="16" font-weight="700">3. Live APIs &amp; Primary Sources</text>
    <text x="25" y="115" fill="#334155" font-size="14">
      <tspan x="25" dy="0">• JSON-RPC 2.0 stdio IPC queries</tspan>
      <tspan x="25" dy="24">• Live Wikipedia REST search API</tspan>
      <tspan x="25" dy="24">• Live arXiv Open Science preprints</tspan>
      <tspan x="25" dy="24">• Extracts grounding quotes &amp; DOIs</tspan>
    </text>
    
    <rect x="25" y="270" width="360" height="105" rx="6" fill="#f8fafc" stroke="#7c3aed" stroke-width="1.5"/>
    <text x="40" y="298" fill="#6d28d9" font-size="14" font-family="monospace" font-weight="800">✅ MCP TOOL DISPATCH</text>
    <text x="40" y="324" fill="#334155" font-size="13">@mcp.tool query_web_index()</text>
    <text x="40" y="346" fill="#64748b" font-size="13">8 Primary citations harvested</text>
  </g>

  <!-- Arrow 3 -> 4 -->
  <line x1="1395" y1="350" x2="1435" y2="350" stroke="#7c3aed" stroke-width="5" marker-end="url(#arrowPurple)"/>

  <!-- Step 4 -->
  <g transform="translate(1440, 150)" filter="url(#shadowFlowWhite)">
    <rect width="410" height="400" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect width="410" height="50" rx="12" fill="#fef2f2"/>
    <text x="25" y="33" fill="#b91c1c" font-size="18" font-weight="800">STAGE 4: GUARDRAILS SCAN</text>
    
    <text x="25" y="85" fill="#0f172a" font-size="16" font-weight="700">4. PreToolUse &amp; Entropy Guard</text>
    <text x="25" y="115" fill="#334155" font-size="14">
      <tspan x="25" dy="0">• Intercepts dangerous CLI commands</tspan>
      <tspan x="25" dy="24">• Scans for API secrets (Shannon entropy)</tspan>
      <tspan x="25" dy="24">• AST syntax validation of code blocks</tspan>
      <tspan x="25" dy="24">• Rolling SHA-256 loop trap detection</tspan>
    </text>
    
    <rect x="25" y="270" width="360" height="105" rx="6" fill="#f8fafc" stroke="#dc2626" stroke-width="1.5"/>
    <text x="40" y="298" fill="#b91c1c" font-size="14" font-family="monospace" font-weight="800">✅ SECURITY ENFORCEMENT</text>
    <text x="40" y="324" fill="#334155" font-size="13">permissionDecision: 'deny' on violation</text>
    <text x="40" y="346" fill="#64748b" font-size="13">Zero secrets or loop traps permitted</text>
  </g>

  <!-- Downward Arrow from Step 4 to Step 5 -->
  <line x1="1645" y1="555" x2="1645" y2="595" stroke="#dc2626" stroke-width="5" marker-end="url(#arrowRed)"/>

  <!-- ==================== BOTTOM ROW: STAGES 8 TO 5 (RIGHT TO LEFT) ==================== -->

  <!-- Step 5 -->
  <g transform="translate(1440, 600)" filter="url(#shadowFlowWhite)">
    <rect width="410" height="400" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect width="410" height="50" rx="12" fill="#ecfdf5"/>
    <text x="25" y="33" fill="#047857" font-size="18" font-weight="800">STAGE 5: PYTEST TDA LOOP</text>
    
    <text x="25" y="85" fill="#0f172a" font-size="16" font-weight="700">5. Red-Repair-Green Testing</text>
    <text x="25" y="115" fill="#334155" font-size="14">
      <tspan x="25" dy="0">• Executes automated pytest test suite</tspan>
      <tspan x="25" dy="24">• Verifies citation schemas &amp; quotes</tspan>
      <tspan x="25" dy="24">• Appends anti-regression guard tests</tspan>
      <tspan x="25" dy="24">• Closes loop with 100% pass verification</tspan>
    </text>
    
    <rect x="25" y="270" width="360" height="105" rx="6" fill="#f8fafc" stroke="#059669" stroke-width="1.5"/>
    <text x="40" y="298" fill="#047857" font-size="14" font-family="monospace" font-weight="800">✅ TDA VERIFICATION</text>
    <text x="40" y="324" fill="#334155" font-size="13">pytest deep_research_agent/tests -v</text>
    <text x="40" y="346" fill="#64748b" font-size="13">13/13 Assertions PASSED (100%)</text>
  </g>

  <!-- Arrow 5 -> 6 (Leftward) -->
  <line x1="1435" y1="800" x2="1395" y2="800" stroke="#059669" stroke-width="5" marker-end="url(#arrowGreen)"/>

  <!-- Step 6 -->
  <g transform="translate(980, 600)" filter="url(#shadowFlowWhite)">
    <rect width="410" height="400" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect width="410" height="50" rx="12" fill="#fffbeb"/>
    <text x="25" y="33" fill="#b45309" font-size="18" font-weight="800">STAGE 6: FACT-CHECK &amp; SYNTHESIS</text>
    
    <text x="25" y="85" fill="#0f172a" font-size="16" font-weight="700">6. Multi-Agent Synthesis</text>
    <text x="25" y="115" fill="#334155" font-size="14">
      <tspan x="25" dy="0">• Fact-checker audits match confidence</tspan>
      <tspan x="25" dy="24">• Filters low-relevance noise &amp; tokens</tspan>
      <tspan x="25" dy="24">• Synthesizes 5 Golden Pillars dossier</tspan>
      <tspan x="25" dy="24">• Builds quantitative comparative matrix</tspan>
    </text>
    
    <rect x="25" y="270" width="360" height="105" rx="6" fill="#f8fafc" stroke="#d97706" stroke-width="1.5"/>
    <text x="40" y="298" fill="#b45309" font-size="14" font-family="monospace" font-weight="800">✅ ACADEMIC SYNTHESIS</text>
    <text x="40" y="324" fill="#334155" font-size="13">MultiAgentResearchTeam.run_synthesizer()</text>
    <text x="40" y="346" fill="#64748b" font-size="13">~17,000 chars publication dossier</text>
  </g>

  <!-- Arrow 6 -> 7 (Leftward) -->
  <line x1="975" y1="800" x2="935" y2="800" stroke="#d97706" stroke-width="5" marker-end="url(#arrowAmber)"/>

  <!-- Step 7 -->
  <g transform="translate(520, 600)" filter="url(#shadowFlowWhite)">
    <rect width="410" height="400" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect width="410" height="50" rx="12" fill="#eff6ff"/>
    <text x="25" y="33" fill="#1d4ed8" font-size="18" font-weight="800">STAGE 7: UNIFIED DIFF &amp; AUDIT</text>
    
    <text x="25" y="85" fill="#0f172a" font-size="16" font-weight="700">7. Human Review &amp; 5 Gates</text>
    <text x="25" y="115" fill="#334155" font-size="14">
      <tspan x="25" dy="0">• Computes line-by-line unified diff</tspan>
      <tspan x="25" dy="24">• Human inspects exact mutations</tspan>
      <tspan x="25" dy="24">• ProductionHarnessAuditor runs 5 gates</tspan>
      <tspan x="25" dy="24">• Memory, Hooks, Tests, MCP, Subagents</tspan>
    </text>
    
    <rect x="25" y="270" width="360" height="105" rx="6" fill="#f8fafc" stroke="#2563eb" stroke-width="1.5"/>
    <text x="40" y="298" fill="#1d4ed8" font-size="14" font-family="monospace" font-weight="800">✅ 5-GATE AUDIT PASSED</text>
    <text x="40" y="324" fill="#334155" font-size="13">ProductionHarnessAuditor.audit_all()</text>
    <text x="40" y="346" fill="#64748b" font-size="13">Score: 100% (5/5 Gates Certified)</text>
  </g>

  <!-- Arrow 7 -> 8 (Leftward) -->
  <line x1="515" y1="800" x2="475" y2="800" stroke="#2563eb" stroke-width="5" marker-end="url(#arrowBlue)"/>

  <!-- Step 8 -->
  <g transform="translate(60, 600)" filter="url(#shadowFlowWhite)">
    <rect width="410" height="400" rx="12" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>
    <rect width="410" height="50" rx="12" fill="#ecfdf5"/>
    <text x="25" y="33" fill="#047857" font-size="18" font-weight="800">STAGE 8: PUBLICATION &amp; UI</text>
    
    <text x="25" y="85" fill="#0f172a" font-size="16" font-weight="700">8. Final Output &amp; Teardown</text>
    <text x="25" y="115" fill="#334155" font-size="14">
      <tspan x="25" dy="0">• Writes output/dossier.md to disk</tspan>
      <tspan x="25" dy="24">• Emits events.jsonl &amp; telemetry logs</tspan>
      <tspan x="25" dy="24">• Renders live graph &amp; dossier in UI</tspan>
      <tspan x="25" dy="24">• Cleans up ephemeral worktree branch</tspan>
    </text>
    
    <rect x="25" y="270" width="360" height="105" rx="6" fill="#f8fafc" stroke="#059669" stroke-width="1.5"/>
    <text x="40" y="298" fill="#047857" font-size="14" font-family="monospace" font-weight="800">✅ PIPELINE COMPLETE</text>
    <text x="40" y="324" fill="#334155" font-size="13">WorktreeIsolation.remove()</text>
    <text x="40" y="346" fill="#64748b" font-size="13">Dossier Delivered &amp; Verified</text>
  </g>
</svg>
"""


async def generate_all_diagrams():
    print("=" * 80)
    print("GENERATING WHITE BACKGROUND ARCHITECTURE & FLOW DIAGRAMS")
    print("=" * 80)

    # 1. Save SVG files
    arch_svg_path = DOCS_DIR / "architecture_diagram.svg"
    flow_svg_path = DOCS_DIR / "flow_diagram.svg"

    with open(arch_svg_path, "w", encoding="utf-8") as f:
        f.write(ARCHITECTURE_SVG)
    print(f"[OK] Saved {arch_svg_path}")

    with open(flow_svg_path, "w", encoding="utf-8") as f:
        f.write(FLOW_SVG)
    print(f"[OK] Saved {flow_svg_path}")

    # 2. Render 4K PNGs using Playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            device_scale_factor=2.0,  # 3840x2160 Ultra-High-Resolution
        )
        page = await context.new_page()

        # Render Architecture Diagram PNG
        arch_html = f"<!DOCTYPE html><html><body style='margin:0;padding:0;background:#ffffff;'>{ARCHITECTURE_SVG}</body></html>"
        await page.set_content(arch_html)
        await page.wait_for_timeout(500)
        arch_png_path = DOCS_DIR / "architecture_diagram.png"
        await page.screenshot(path=str(arch_png_path))
        print(f"[OK] Rendered 4K PNG {arch_png_path} ({arch_png_path.stat().st_size} bytes)")

        # Render Flow Diagram PNG
        flow_html = f"<!DOCTYPE html><html><body style='margin:0;padding:0;background:#ffffff;'>{FLOW_SVG}</body></html>"
        await page.set_content(flow_html)
        await page.wait_for_timeout(500)
        flow_png_path = DOCS_DIR / "flow_diagram.png"
        await page.screenshot(path=str(flow_png_path))
        print(f"[OK] Rendered 4K PNG {flow_png_path} ({flow_png_path.stat().st_size} bytes)")

        # Copy to Artifact Directory for UI preview
        shutil.copy(arch_png_path, ARTIFACT_DIR / "architecture_diagram.png")
        shutil.copy(flow_png_path, ARTIFACT_DIR / "flow_diagram.png")
        print("[OK] Copied white background diagrams to artifact directory.")

        await browser.close()

    print("\n" + "=" * 80)
    print(">>> WHITE BACKGROUND ARCHITECTURE & FLOW DIAGRAMS GENERATED <<<")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    asyncio.run(generate_all_diagrams())
