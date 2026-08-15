---
name: harness-guardrails-and-hooks
description: Implements Claude Code PascalCase PreToolUse and PostToolUse deterministic hook interceptors to block dangerous CLI flags, parse AST syntax, and prevent multi-vendor credential leaks. Use when configuring .claude/settings.json hooks or auditing pre/post tool execution policies.
allowed-tools: Read, Write, Glob, Grep
---

# Harness Guardrails And Hooks

Implements Claude Code PascalCase PreToolUse and PostToolUse deterministic hook interceptors to block dangerous CLI flags, parse AST syntax, and prevent multi-vendor credential leaks. Use when configuring .claude/settings.json hooks or auditing pre/post tool execution policies.

## Structure & Available Components
- `scripts/`: Executable helper tools for this skill.
- `references/`: Architectural rules, patterns, and guides.
- `assets/`: Config templates and validation schemas.

## When to Use
Trigger this skill when:
- Operating within `module_04_guardrails_and_hooks` or applying its design patterns.
- Auditing, executing, or enforcing harness guarantees for this domain.

## How to Use
1. Consult references in `references/` for specifications and policies.
2. Execute scripts in `scripts/` to validate inputs and enforce constraints.
3. Apply configurations in `assets/` for standardized settings.

## Key Files & Implementation (GitHub Links)
- [https://github.com/kenhuangus/packt-harness/tree/main/.claude/skills/harness-guardrails-and-hooks/](https://github.com/kenhuangus/packt-harness/tree/main/.claude/skills/harness-guardrails-and-hooks/)
- [https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-guardrails-and-hooks/SKILL.md](https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-guardrails-and-hooks/SKILL.md)
- [https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_04_guardrails_and_hooks/](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_04_guardrails_and_hooks/)
