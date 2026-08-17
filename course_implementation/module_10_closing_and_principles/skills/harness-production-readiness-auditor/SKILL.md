---
name: harness-production-readiness-auditor
description: 'Programmatically audits codebases across 5 objective readiness gates:
  Memory Files (CLAUDE.md, AGENTS.md), PreToolUse Hooks, Automated Test Runners, MCP
  Tool Declarations, and Subagent Definitions. Trigger when benchmarking repository
  readiness, scoring CI/CD pipelines, or verifying enterprise control compliance.'
version: 1.0.0
author: Harness Engineering Team
allowed-tools: Read, Grep, Bash
---

# Harness Production Readiness Auditor

## Overview
Programmatic 5-gate production readiness auditor that benchmarks repository harness compliance on an objective 5-gate scorecard.

## Structure & Progressive Disclosure
- `scripts/`: Executable helper and verification tools.
- `references/`: Detailed specifications, guides, and architectural rules.
- `assets/`: Configuration templates and machine-readable schemas.

## When to Use
- When benchmarking repository readiness for autonomous coding agents.
- When running automated CI/CD audits against harness engineering standards.
- When certifying production compliance across memory, hooks, tests, MCP, and subagents.

## Required Inputs
- Target repository root directory.
- Scorecard rubric criteria (`references/production-scorecard-rubric.md`).

## Instructions
Run all commands from the repository root.
1. Gate 1 (Memory): Verify presence and structure of `CLAUDE.md` and `AGENTS.md`.
2. Gate 2 (Hooks): Verify PreToolUse hooks registered in `.claude/settings.json`.
3. Gate 3 (Tests): Verify automated test runner exits with code 0.
4. Gate 4 (MCP): Verify `@mcp.tool` and `@mcp.resource` AST declarations.
5. Gate 5 (Subagents): Verify subagent YAML frontmatter configurations.
6. Execute `python .claude/skills/harness-production-readiness-auditor/scripts/run_audit.py` to calculate gate compliance score.
7. Consult `references/production-scorecard-rubric.md` for scoring rubric.

## Output Format
Always format output adhering to this structure:
```json
{
  "target_repo": "packt-harness",
  "passed_gates": "5/5",
  "gates": {
    "memory_files": "PASS",
    "hooks": "PASS",
    "test_runner": "PASS",
    "mcp_declarations": "PASS",
    "subagents": "PASS"
  },
  "certification": "PRODUCTION_READY"
}
```

## Examples
### Running Production Readiness Audit
```python
from scripts.run_audit import run_audit

run_audit(".")  # Audits repository and returns readiness scorecard
```

## Key Implementation Links (GitHub)
- [https://github.com/kenhuangus/packt-harness/tree/main/.claude/skills/harness-production-readiness-auditor/](https://github.com/kenhuangus/packt-harness/tree/main/.claude/skills/harness-production-readiness-auditor/)
- [https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-production-readiness-auditor/SKILL.md](https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-production-readiness-auditor/SKILL.md)
- [https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_10_closing_and_principles/](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_10_closing_and_principles/)
