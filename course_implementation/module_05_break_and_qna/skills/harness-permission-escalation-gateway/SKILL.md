---
name: harness-permission-escalation-gateway
description: Evaluates tool requests against a 4-tier risk matrix (LOW, MEDIUM, HIGH, CRITICAL), auto-approving safe reads, auditing sandboxed writes, and strictly requiring signed approvals.json tokens for critical operations (git_push). Use when gating sensitive tools, establishing human-in-the-loop workflows, or generating pending action artifacts.
allowed-tools: Read, Write, Glob, Grep
---

# Harness Permission Escalation Gateway

Evaluates tool requests against a 4-tier risk matrix (LOW, MEDIUM, HIGH, CRITICAL), auto-approving safe reads, auditing sandboxed writes, and strictly requiring signed approvals.json tokens for critical operations (git_push). Use when gating sensitive tools, establishing human-in-the-loop workflows, or generating pending action artifacts.

## Structure & Available Components
- `scripts/`: Executable helper tools for this skill.
- `references/`: Architectural rules, patterns, and guides.
- `assets/`: Config templates and validation schemas.

## When to Use
Trigger this skill when:
- Operating within `module_05_break_and_qna` or applying its design patterns.
- Auditing, executing, or enforcing harness guarantees for this domain.

## How to Use
1. Consult references in `references/` for specifications and policies.
2. Execute scripts in `scripts/` to validate inputs and enforce constraints.
3. Apply configurations in `assets/` for standardized settings.

## Key Files & Implementation (GitHub Links)
- [https://github.com/kenhuangus/packt-harness/tree/main/.claude/skills/harness-permission-escalation-gateway/](https://github.com/kenhuangus/packt-harness/tree/main/.claude/skills/harness-permission-escalation-gateway/)
- [https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-permission-escalation-gateway/SKILL.md](https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-permission-escalation-gateway/SKILL.md)
- [https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_05_break_and_qna/](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_05_break_and_qna/)
