# Product Requirements Document (PRD): Autonomous Deep Research Agent

## 1. Executive Summary & Vision
The **Autonomous Deep Research Agent** is an enterprise-grade, deterministic research intelligence system. It conducts recursive multi-hop investigations across web resources, structured databases, and academic literature, synthesizing comprehensive research reports with verified source citations, interactive citation graphs, and verifiable factual claims. 

Unlike naive probabilistic agents that suffer from hallucination, infinite loop traps, token window exhaustion, and unverified data mutations, this Deep Research Agent is engineered using the complete **10-Module Harness Architecture**:
1. **Runtime Loop & Traversal Interception** (Module 1: `LoopDetector` with `deque(maxlen=10)` call signatures, command sanitization).
2. **5 Golden Pillars Governance** (Module 2: Memory files `CLAUDE.md`/`AGENTS.md`, scoped tools, `Path.resolve().is_relative_to()` sandboxing, 20/20/50/10 token budgeter, and `events.jsonl` audit logging).
3. **Machine-Verifiable Research Specifications** (Module 3: `SPEC.md` constraints, explicit topic non-goals, source whitelists).
4. **Deterministic Guardrails & Hook Contracts** (Module 4: Claude Code `PreToolUse` JSON-RPC contracts, secret filtering, AST syntax verification).
5. **Risk-Tiered Permission Escalation Gateway** (Module 5: 4-tier risk matrix `LOW`, `MEDIUM`, `HIGH`, `CRITICAL` with cryptographic signed ledger `approvals.json` gating external exports and system mutations).
6. **Test-Driven Agent (TDA) Reliability Layer** (Module 6: Red-Repair-Green automated test loops, subprocess traceback capture, and persistent anti-regression testing).
7. **Model Context Protocol (MCP 2.x) Integration** (Module 7: `@mcp.tool()` search and scrape primitives, `@mcp.resource()` cache endpoints, stdio child process IPC, and live `aisuite` synthesis).
8. **Compound Engineering & Multi-Agent Teams** (Module 8: Specialized Planner, Implementer/Crawler, Reviewer/Fact-Checker roles with ephemeral `git worktree` isolation, and Compound Orchestrator 2-round cross-review protocols).
9. **Practical 5-Step SOP Execution Pipeline** (Module 9: `Spec First -> Sandbox -> Guardrails -> Pytest -> Human Unified Diff Review`).
10. **Automated Production Readiness Auditing** (Module 10: 5-Gate Compliance Scorecard verifying 100% harness maturity).

---

## 2. Target Personas & Use Cases
- **Enterprise Research Analysts**: Need thorough, multi-source competitive intelligence dossiers without factual hallucinations or ungrounded claims.
- **AI & Software Architects**: Need systematic technology assessments, library comparisons, and RFC evaluations with verifiable code snippets and benchmarks.
- **Compliance & Security Officers**: Need strict data provenance, immutable audit trails (`events.jsonl`), and cryptographic human sign-off on published findings.

---

## 3. Core Functional Requirements (FR)

### FR-01: Research Decomposition & Spec Formulation (Module 3 & 8)
- The agent must parse the primary user research prompt into a structured `SPEC.md` defining:
  - **Objective**: Target research questions, depth, and output formatting.
  - **Scope & Whitelists**: Allowed search domains, APIs, and document types.
  - **Non-Goals**: Explicitly blocked topics, off-limits directories, and unverified forums to prevent topic drift.
  - **Acceptance Criteria**: Machine-verifiable criteria (e.g., minimum 5 unique authoritative sources, 0 broken citation links, 100% claims backed by extracted quotes).

### FR-02: Scoped Tool Execution & Sandbox Containment (Module 1 & 2)
- All filesystem reads and writes must be constrained to the designated research workspace using `Path.resolve().is_relative_to(workspace_root)`. Any attempt at path traversal (`../../etc/passwd` or system directories) must raise an immediate `PermissionError`.
- Tool calls must be monitored by a `LoopDetector`. If the same query or tool parameters are repeated $\ge 2$ times without progress, execution is halted with exit code 2.

### FR-03: Model Context Protocol (MCP 2.x) Research Server (Module 7)
- The agent must communicate with an internal stdio MCP research server exposing:
  - `@mcp.tool() query_web_index(query: str, max_results: int)`: Search local and remote knowledge indexes.
  - `@mcp.tool() extract_document_content(doc_id: str)`: Fetch and clean full-text markdown.
  - `@mcp.tool() verify_citation_claim(claim: str, source_id: str)`: Cross-check factual grounding.
  - `@mcp.resource("research://cache/{query_hash}")`: Retrieve cached search graph representations.

### FR-04: Multi-Agent Role Handoffs & Worktree Isolation (Module 8)
- Complex research tasks are divided among specialized subagents:
  - **Planner Agent**: Decomposes high-level prompt into sub-queries and assigns research tracks.
  - **Crawler/Implementer Agent**: Executes search queries and extracts evidence within an isolated ephemeral git worktree branch.
  - **Reviewer / Fact-Checker Agent**: Evaluates draft findings against extracted evidence, verifies claim-to-source mapping, and checks for hallucination.
  - **Synthesizer Agent**: Assembles final markdown dossier with interactive citation metadata.
- Worktrees are cleanly torn down upon task completion, logging metrics to `telemetry.jsonl`.

### FR-05: Guardrails, Secret Scanning & Hook Contracts (Module 4)
- Incoming tool requests must pass through a `PreToolUse` hook contract in PascalCase JSON-RPC format.
- Generated reports and code blocks must undergo AST syntax checks and regex secret scanning to prevent API key leaks (e.g., regex patterns matching `sk-ant-api03`, `AKIA...`).

### FR-06: Permission Escalation Gateway (Module 5)
- Tool operations are categorized by risk:
  - `LOW`: Local read, internal cache lookup (Auto-approved).
  - `MEDIUM`: Document ingestion, disk writes inside workspace (Logged & Auto-approved).
  - `HIGH`: External API network calls, third-party search queries (Logged with rate limiting).
  - `CRITICAL`: Exporting final research report to production directories, sending external emails, or git branch pushes (Requires cryptographic token in `approvals.json`).

### FR-07: Test-Driven Reliability & Self-Healing Loop (Module 6)
- The agent executes an automated TDA Red-Repair-Green test harness:
  - Validates citation integrity via pytest.
  - If a citation or synthesis error occurs, captures stderr tracebacks and prompts the model for targeted repair.
  - Persists regression tests to guarantee durability.

### FR-08: Interactive, High-Aesthetics UI (Design System)
- A modern, fluid, responsive Web UI providing:
  - **Live Research Graph**: Real-time visualization of query branches, sub-nodes, and source nodes.
  - **Step-by-Step Progress Timeline**: Real-time display of the 5-Step SOP pipeline.
  - **Citation Card Grid**: Interactive view of extracted evidence, author credibility scores, and direct quotes.
  - **Dossier Markdown & Export**: High-density markdown reader with copy, export, and citation link jump.
  - **Harness Telemetry & Event Log**: Live stream of `events.jsonl` audit records, token budgets, and risk tier badges.

---

## 4. Non-Functional Requirements (NFR)
- **Deterministic Portability**: Works standalone on Windows, macOS, and Linux without requiring external cloud databases.
- **Latency & Concurrency**: Multi-hop search execution under 5 seconds for local mock sources; full report generation under 15 seconds.
- **Zero Drift**: Research output must adhere 100% to `SPEC.md` acceptance criteria.
- **Visual Excellence**: Professional light/dark mode UI with HSL curated palette, no forbidden clichés (no unrounded nested boxes, no purple on dark, no textureless cards).
