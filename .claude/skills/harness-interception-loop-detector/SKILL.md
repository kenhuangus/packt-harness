---
name: harness-interception-loop-detector
description: Intercepts destructive shell commands and breaks repeating execution retry loops before token waste or data loss occurs. Use when running untrusted or automated agent command loops, auditing shell tool calls, or debugging stuck test-fix iterations.
allowed-tools: Bash, Read, Grep
---

# Harness Interception Loop Detector

Intercepts destructive shell commands and breaks repeating execution retry loops before token waste or data loss occurs. Use when running untrusted or automated agent command loops, auditing shell tool calls, or debugging stuck test-fix iterations.

## Structure & Available Components
- `scripts/`: Executable helper tools for this skill.
- `references/`: Architectural rules, patterns, and guides.
- `assets/`: Config templates and validation schemas.

## When to Use
Trigger this skill when:
- Operating within `module_01_why_harness_engineering` or applying its design patterns.
- Auditing, executing, or enforcing harness guarantees for this domain.

## How to Use
1. Consult references in `references/` for specifications and policies.
2. Execute scripts in `scripts/` to validate inputs and enforce constraints.
3. Apply configurations in `assets/` for standardized settings.

## Key Files & Implementation (GitHub Links)
- [https://github.com/kenhuangus/packt-harness/tree/main/.claude/skills/harness-interception-loop-detector/](https://github.com/kenhuangus/packt-harness/tree/main/.claude/skills/harness-interception-loop-detector/)
- [https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-interception-loop-detector/SKILL.md](https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-interception-loop-detector/SKILL.md)
- [https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_01_why_harness_engineering/](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_01_why_harness_engineering/)
