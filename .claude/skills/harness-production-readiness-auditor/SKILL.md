---
name: harness-production-readiness-auditor
description: Programmatically audits codebases across 5 objective readiness gates: Memory Files (CLAUDE.md, AGENTS.md), PreToolUse Hook Registrations (.claude/settings.json), Automated Test Runners, MCP Tool/Resource AST Declarations, and Subagent Definitions. Use when benchmarking repository harness readiness, scoring CI/CD pipelines, or verifying enterprise control compliance.
allowed-tools: Read, Glob, Grep, Bash
---

# Production Harness Readiness Auditor (Module 10 Skill)

This skill evaluates a repository against the 5 objective harness engineering readiness gates, generating verifiable compliance evidence and automated pass/fail results for CI/CD pipelines.

## When to Use
- Before deploying coding agents in production repositories.
- In CI/CD pipelines as an automated gate to ensure harness memory files, hooks, and test runners are present and valid.
- When generating an objective 0–100% harness readiness scorecard.

## How to Use
1. **Auditing the 5 Core Gates**:
   - `Gate 1 (Memory Files)`: Validates existence of `CLAUDE.md` and `AGENTS.md`.
   - `Gate 2 (PreToolUse Hooks)`: Checks `.claude/settings.json` for valid hook matchers.
   - `Gate 3 (Test Runner)`: Verifies test runner scripts and live `pytest` exit codes.
   - `Gate 4 (MCP Scoped Tools)`: AST-walks python code to verify `@mcp.tool` and `@mcp.resource`.
   - `Gate 5 (Subagent Definitions)`: Verifies agent frontmatter configurations and worktree isolation.

2. **Run Programmatic Audit**:
   ```python
   auditor = ProductionHarnessAuditor(repo_root)
   scorecard = auditor.run_full_audit()
   print(f"Overall Harness Score: {scorecard.overall_percentage}%")
   ```

3. **Verification**:
   ```bash
   python course_implementation/module_10_closing_and_principles/production_harness_audit.py
   ```

## Key Files & Implementation
- `course_implementation/module_10_closing_and_principles/production_harness_audit.py`
- `run_all_modules.py`
