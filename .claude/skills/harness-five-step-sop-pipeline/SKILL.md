---
name: harness-five-step-sop-pipeline
description: Runs an end-to-end 5-step Standard Operating Procedure (SOP) pipeline
allowed-tools: Bash, Read, Write, Glob, Grep
---

# Harness Five Step Sop Pipeline

Runs an end-to-end 5-step Standard Operating Procedure (SOP) pipeline combining Spec First (1), Constrained Sandbox Execution (2), Deterministic AST/Secret Guardrails (3), Subprocess Pytest Verification (4), and Unified Diff Human Review (5). Use when executing end-to-end feature pipelines or auditing workflow rigor before PR submission.

## Structure & Available Components
- `scripts/`: Executable helper tools for this skill.
- `references/`: Architectural rules, patterns, and guides.
- `assets/`: Config templates and validation schemas.

## When to Use
Trigger this skill when:
- Operating within `module_09_practical_workflow_pattern` or applying its design patterns.
- Auditing, executing, or enforcing harness guarantees for this domain.

## How to Use
1. Consult references in `references/` for specifications and policies.
2. Execute scripts in `scripts/` to validate inputs and enforce constraints.
3. Apply configurations in `assets/` for standardized settings.

## Key Files & Implementation (GitHub Links)
- [https://github.com/kenhuangus/packt-harness/tree/main/.claude/skills/harness-five-step-sop-pipeline/](https://github.com/kenhuangus/packt-harness/tree/main/.claude/skills/harness-five-step-sop-pipeline/)
- [https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-five-step-sop-pipeline/SKILL.md](https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-five-step-sop-pipeline/SKILL.md)
- [https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_09_practical_workflow_pattern/](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_09_practical_workflow_pattern/)
