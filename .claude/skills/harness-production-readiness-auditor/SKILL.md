---
name: harness-production-readiness-auditor
description: Programmatically audits codebases across 5 objective readiness gates: Memory Files (CLAUDE.md, AGENTS.md), PreToolUse Hook Registrations (.claude/settings.json), Automated Test Runners, MCP Tool/Resource AST Declarations, and Subagent Definitions. Use when benchmarking repository harness readiness, scoring CI/CD pipelines, or verifying enterprise control compliance.
allowed-tools: Read, Glob, Grep, Bash
---

# Harness Production Readiness Auditor

Programmatically audits codebases across 5 objective readiness gates: Memory Files (CLAUDE.md, AGENTS.md), PreToolUse Hook Registrations (.claude/settings.json), Automated Test Runners, MCP Tool/Resource AST Declarations, and Subagent Definitions. Use when benchmarking repository harness readiness, scoring CI/CD pipelines, or verifying enterprise control compliance.

## Structure & Available Components
- `scripts/`: Executable helper tools for this skill.
- `references/`: Architectural rules, patterns, and guides.
- `assets/`: Config templates and validation schemas.

## When to Use
Trigger this skill when:
- Operating within `module_10_closing_and_principles` or applying its design patterns.
- Auditing, executing, or enforcing harness guarantees for this domain.

## How to Use
1. Consult references in `references/` for specifications and policies.
2. Execute scripts in `scripts/` to validate inputs and enforce constraints.
3. Apply configurations in `assets/` for standardized settings.

## Key Files & Implementation (GitHub Links)
- [https://github.com/kenhuangus/packt-harness/tree/main/.claude/skills/harness-production-readiness-auditor/](https://github.com/kenhuangus/packt-harness/tree/main/.claude/skills/harness-production-readiness-auditor/)
- [https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-production-readiness-auditor/SKILL.md](https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-production-readiness-auditor/SKILL.md)
- [https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_10_closing_and_principles/](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_10_closing_and_principles/)
