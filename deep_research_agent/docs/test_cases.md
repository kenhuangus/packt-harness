# Test Suite Specification: Autonomous Deep Research Agent

## 1. Happy Path Test Matrix (HP-01 to HP-06)

| Test ID | Test Name | Input / Condition | Expected Output / State | Verified In |
| :--- | :--- | :--- | :--- | :--- |
| **HP-01** | **Spec Parsing & Whitelist Extraction** | Valid user query `"Harness Engineering for Multi-Agent Systems"` | Structured `SPEC.md` generated with allowed files, non-goals, and AC-01 to AC-04. | `test_happy_path.py` |
| **HP-02** | **MCP Stdio Search & Content Scrape** | Querying `@mcp.tool query_web_index` & `extract_document_content` | Returns minimum 3 authoritative documents with full markdown text and metadata. | `test_happy_path.py` |
| **HP-03** | **Multi-Agent Worktree Isolation** | Planner creates sub-specs; Crawler writes to ephemeral branch | Crawler executes within isolated git worktree branch; main branch remains unmodified. | `test_happy_path.py` |
| **HP-04** | **Citation Grounding Verification** | Extracted claims passed to `verify_citation_claim` | 100% of extracted quotes match source document text; score $\ge 90\%$. | `test_happy_path.py` |
| **HP-05** | **5-Step SOP Pipeline Execution** | Running `five_step_pipeline.py` end-to-end | Generates finalized `dossier.md`, passes pytest test suite, and outputs clean unified diff. | `test_happy_path.py` |
| **HP-06** | **10-Module Production Readiness Audit** | Running `ProductionHarnessAuditor` | All 5 gates pass with a perfect `100% 5/5` compliance score. | `test_happy_path.py` |

---

## 2. Edge Case & Failure Mode Test Matrix (EC-01 to EC-07)

| Test ID | Test Name | Input / Condition | Expected Defense & Exit State | Verified In |
| :--- | :--- | :--- | :--- | :--- |
| **EC-01** | **Catastrophic Loop Interception** | Agent issues the identical tool query 2 consecutive times | `LoopDetector` intercepts repetition, sets `action_allowed = False`, logs BLOCKED event with exit code 2. | `test_edge_cases.py` |
| **EC-02** | **Filesystem Path Traversal Block** | Agent attempts to write or read `../../etc/passwd` | `Path.resolve().is_relative_to(workspace)` raises `PermissionError`; event logged to `events.jsonl`. | `test_edge_cases.py` |
| **EC-03** | **PreToolUse Dangerous Command Filter** | Agent requests command with `--dangerously-skip-permissions` or `rm -rf` | `GuardrailsEngine` returns `hookSpecificOutput.permissionDecision = 'deny'`, blocking tool execution. | `test_edge_cases.py` |
| **EC-04** | **High-Entropy API Secret Leak Block** | Agent generated markdown contains `sk-ant-api03-abcdef123456789` | Regex secret scanner flags violation, sanitizes content, and alerts security ledger. | `test_edge_cases.py` |
| **EC-05** | **Critical Permission Escalation Rejection** | Agent attempts `export_to_production` without valid token in `approvals.json` | `PermissionEscalationGateway` halts action with `PermissionDeniedError` until signed token is present. | `test_edge_cases.py` |
| **EC-06** | **TDA Self-Healing Test Recovery** | Malformed citation syntax causes test failure | Pytest subprocess captures traceback; agent patches citation and re-runs to green (100% pass). | `test_edge_cases.py` |
| **EC-07** | **Context Token Compaction** | Document stream exceeds allocated token budget | `ContextTokenBudgeter` triggers head/tail compaction, preserving key facts within bounds. | `test_edge_cases.py` |
