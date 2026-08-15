---
name: harness-spec-driven-development
description: Parses and enforces immutable SPEC.md contracts, bounding agent writes
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Harness Spec Driven Development

Parses and enforces immutable SPEC.md contracts, bounding agent writes strictly to allowed files, blocking non-goals, and validating AST syntax before accepting code changes. Use when scoping features, preventing architectural drift, or validating code proposals against specifications.

## Structure & Available Components
- `scripts/`: Executable helper tools for this skill.
- `references/`: Architectural rules, patterns, and guides.
- `assets/`: Config templates and validation schemas.

## When to Use
Trigger this skill when:
- Operating within `module_03_spec_driven_development` or applying its design patterns.
- Auditing, executing, or enforcing harness guarantees for this domain.

## How to Use
1. Consult references in `references/` for specifications and policies.
2. Execute scripts in `scripts/` to validate inputs and enforce constraints.
3. Apply configurations in `assets/` for standardized settings.

## Key Files & Implementation (GitHub Links)
- [https://github.com/kenhuangus/packt-harness/tree/main/.claude/skills/harness-spec-driven-development/](https://github.com/kenhuangus/packt-harness/tree/main/.claude/skills/harness-spec-driven-development/)
- [https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-spec-driven-development/SKILL.md](https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-spec-driven-development/SKILL.md)
- [https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_03_spec_driven_development/](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_03_spec_driven_development/)
