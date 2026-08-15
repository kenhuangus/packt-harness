---
name: harness-tda-reliability-pipeline
description: Executes deterministic test-driven agent (TDA) feedback loops via isolated pytest subprocesses, captures exact failure tracebacks into repair prompts, and appends anti-regression tests to prevent feature breakage. Use when running automated code repair, verifying test assertions, or preventing regressions.
allowed-tools: Bash, Read, Write, Glob, Grep
---

# Harness Tda Reliability Pipeline

Executes deterministic test-driven agent (TDA) feedback loops via isolated pytest subprocesses, captures exact failure tracebacks into repair prompts, and appends anti-regression tests to prevent feature breakage. Use when running automated code repair, verifying test assertions, or preventing regressions.

## Structure & Available Components
- `scripts/`: Executable helper tools for this skill.
- `references/`: Architectural rules, patterns, and guides.
- `assets/`: Config templates and validation schemas.

## When to Use
Trigger this skill when:
- Operating within `module_06_tests_as_reliability_layer` or applying its design patterns.
- Auditing, executing, or enforcing harness guarantees for this domain.

## How to Use
1. Consult references in `references/` for specifications and policies.
2. Execute scripts in `scripts/` to validate inputs and enforce constraints.
3. Apply configurations in `assets/` for standardized settings.

## Key Files & Implementation (GitHub Links)
- [https://github.com/kenhuangus/packt-harness/tree/main/.claude/skills/harness-tda-reliability-pipeline/](https://github.com/kenhuangus/packt-harness/tree/main/.claude/skills/harness-tda-reliability-pipeline/)
- [https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-tda-reliability-pipeline/SKILL.md](https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-tda-reliability-pipeline/SKILL.md)
- [https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_06_tests_as_reliability_layer/](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_06_tests_as_reliability_layer/)
