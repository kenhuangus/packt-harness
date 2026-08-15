---
name: harness-core-stack-sandbox
description: Enforces least-privilege tool allowlists, path sandboxing via is_relative_to(),
allowed-tools: Read, Write, Glob, Grep
---

# Harness Core Stack Sandbox

Enforces least-privilege tool allowlists, path sandboxing via is_relative_to(), post-edit secret scanning, context token budgeting, and append-only event tracing. Use when sandboxing agent tool invocations, setting up file system isolation, or establishing audit trails in events.jsonl.

## Structure & Available Components
- `scripts/`: Executable helper tools for this skill.
- `references/`: Architectural rules, patterns, and guides.
- `assets/`: Config templates and validation schemas.

## When to Use
Trigger this skill when:
- Operating within `module_02_core_harness_stack` or applying its design patterns.
- Auditing, executing, or enforcing harness guarantees for this domain.

## How to Use
1. Consult references in `references/` for specifications and policies.
2. Execute scripts in `scripts/` to validate inputs and enforce constraints.
3. Apply configurations in `assets/` for standardized settings.

## Key Files & Implementation (GitHub Links)
- [https://github.com/kenhuangus/packt-harness/tree/main/.claude/skills/harness-core-stack-sandbox/](https://github.com/kenhuangus/packt-harness/tree/main/.claude/skills/harness-core-stack-sandbox/)
- [https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-core-stack-sandbox/SKILL.md](https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-core-stack-sandbox/SKILL.md)
- [https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_02_core_harness_stack/](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_02_core_harness_stack/)
