# System & UI Design Specification: Autonomous Deep Research Agent

## 1. System Architecture Diagram

```mermaid
graph TD
    User([User Prompt / Web UI]) --> API[FastAPI / Python HTTP Server]
    API --> SOP[5-Step SOP Orchestrator]
    
    subgraph Harness_Layer [10-Module Harness Scaffolding]
        M3[M3: Spec Parser & Scope Whitelist]
        M1[M1: Loop Detector deque-10]
        M2[M2: Token Budgeter & Path Sandbox]
        M4[M4: PreToolUse Hooks & Secret Scanner]
        M5[M5: Risk Escalation Gateway approvals.json]
        M6[M6: TDA Reliability Pytest Harness]
        M10[M10: 5-Gate Production Readiness Auditor]
    end

    subgraph Agent_Team [M8: Compound Multi-Agent System]
        Planner[Planner Subagent]
        Crawler[Crawler / Scraper Subagent]
        Reviewer[Fact-Checker / Reviewer Subagent]
        Synthesizer[Dossier Synthesizer Subagent]
        Worktree[Ephemeral Git Worktree Isolation]
    end

    subgraph MCP_Infrastructure [M7: Model Context Protocol 2.x]
        MCPServer[MCP Research Server - stdio]
        ToolSearch[@mcp.tool query_web_index]
        ToolScrape[@mcp.tool extract_document_content]
        ToolVerify[@mcp.tool verify_citation_claim]
        ResCache[@mcp.resource research://cache]
    end

    SOP --> M3
    M3 --> Planner
    Planner --> Worktree
    Worktree --> Crawler
    Crawler --> M4
    M4 --> M1
    M1 --> M2
    M2 --> M5
    M5 --> MCPServer
    MCPServer --> ToolSearch
    MCPServer --> ToolScrape
    MCPServer --> ToolVerify
    Crawler --> Reviewer
    Reviewer --> M6
    M6 --> Synthesizer
    Synthesizer --> Dossier[Verified Research Dossier .md]
    Dossier --> M10
    M10 --> UI[Web UI Visualization & Telemetry]
```

---

## 2. Component Architecture & Data Contracts

### 2.1 Spec Contract (`SPEC.md`)
```markdown
# RESEARCH SPECIFICATION: {Research_Title}
## 1. Objective
- Primary Question: {User_Query}
- Target Depth: Multi-hop recursive search (Min 5 authoritative sources)

## 2. Allowed Scope
- In-Scope Files: output/reports/*.md, output/citations/*.json
- Allowed Domains: arxiv.org, github.com, nature.com, ieee.org, docs.python.org

## 3. Explicit Non-Goals
- Blocked Topics: Unverified blog forums, promotional marketing fluff
- Blocked Operations: Database writes, production code modification

## 4. Acceptance Criteria
- AC-01: Every factual claim must be backed by a verified citation ID.
- AC-02: Zero unresolved loop warnings or sandbox violations.
- AC-03: Pytest citation validation suite passes with 100% success.
- AC-04: Unified diff review generated before final dossier export.
```

### 2.2 PreToolUse Hook Contract (Claude Code PascalCase JSON-RPC)
```json
{
  "hookName": "PreToolUse",
  "toolName": "query_web_index",
  "toolInput": {
    "query": "Harness Engineering LLM multi-agent systems",
    "max_results": 5
  },
  "context": {
    "workspace": "deep_research_agent/output",
    "agentRole": "Crawler"
  }
}
```

### 2.3 Escalation Gateway Risk Matrix (`approvals.json`)
```json
{
  "request_id": "REQ-RESEARCH-9842",
  "risk_tier": "CRITICAL",
  "operation": "export_final_dossier_to_production",
  "authorized_by": "lead_researcher_signature",
  "timestamp": "2026-08-16T04:55:00Z",
  "status": "APPROVED",
  "digest": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
}
```

---

## 3. UI/UX Visual Design System

### 3.1 Design Principles & Anti-Cliché Rules
1. **Zero Decorative Fluff**: Every visual element directly represents agent telemetry, citation grounding, or research progress.
2. **No Forbidden Tropes**:
   - ❌ No purple-on-dark backgrounds.
   - ❌ No particle meshes or grid lines.
   - ❌ No headline biscuit pills with pulsing dots.
   - ❌ No over-nested unrounded cards.
3. **High-Contrast Curated HSL Tokens**:
   - **Background Dark**: `hsl(222, 47%, 10%)` | **Background Light**: `hsl(210, 40%, 98%)`
   - **Card Dark**: `hsl(217, 33%, 15%)` | **Card Light**: `hsl(0, 0%, 100%)`
   - **Card Border Dark**: `hsl(215, 25%, 24%)` | **Card Border Light**: `hsl(214, 32%, 88%)`
   - **Primary Accent**: `hsl(168, 80%, 42%)` (Teal Emerald)
   - **Secondary Accent**: `hsl(214, 95%, 60%)` (Electric Sapphire)
   - **Warning**: `hsl(38, 92%, 50%)` (Amber Gold)
   - **Danger**: `hsl(0, 72%, 51%)` (Crimson Red)

### 3.2 UI Screen Layout (3-Column Responsive Grid)
```
+-----------------------------------------------------------------------------------------------+
| [Logo: ⚛️ DEEP RESEARCH AGENT]  [5-Gate Scorecard: 100%] [Risk Tier: LOW] [Theme Toggle 🌙]  |
+-----------------------------------------------------------------------------------------------+
| LEFT PANEL (320px)            | CENTER PANEL (Flexible)        | RIGHT PANEL (380px)          |
|-------------------------------|--------------------------------|------------------------------|
| [🔍 Search Query Input]       | [🗺️ Live Research Graph]       | [📑 Synthesized Dossier]     |
| [Depth: Deep Multi-Hop v]     | - Topic Node (Root)            | # Executive Summary          |
| [▶ Run Deep Research]         |   ├─ Sub-query 1 (Verified)    | ## Key Findings & Metrics    |
|                               |   └─ Sub-query 2 (Scraping)    | [Copy Markdown] [Export PDF] |
| [📌 5-Step SOP Pipeline]      |--------------------------------|------------------------------|
| (1) Spec Contract      [✔]    | [📚 Verified Citations Grid]   | [⚡ Live Telemetry & Audit]  |
| (2) Worktree Sandbox   [✔]    | [Card 1: ArXiv 2026] [Score:98]| events.jsonl Stream:         |
| (3) Guardrails & AST   [✔]    | - Direct Quote extracted...    | [12:00:01] PreToolUse ALLOW  |
| (4) Pytest TDA Loop    [✔]    | [Card 2: Nature AI]  [Score:95]| [12:00:02] Token Budget 42%  |
| (5) Unified Review     [✔]    | - Direct Quote extracted...    | [12:00:03] Pytest 4/4 PASS   |
+-----------------------------------------------------------------------------------------------+
```

### 3.3 Dynamic Micro-Interactions & State Transitions
- **Idle State**: Clean input card with pre-filled sample research prompts (e.g. *"Autonomous Harness Engineering vs Prompting"*).
- **Executing State**: The 5-Step SOP nodes light up sequentially with emerald glow; the live research graph animates new branch nodes using SVG cubic bezier curves.
- **Completed State**: The markdown dossier renders with syntax-highlighted code blocks, clickable citation superscripts (`[^1]`), and an interactive citation inspector modal.
