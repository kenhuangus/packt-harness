---
name: harness-compound-multi-agent-worktrees
description: Orchestrates specialized Planner, Implementer, and Reviewer multi-agent teams, isolating coding execution in ephemeral Git worktrees (isolation: worktree) and slicing sub-specs to minimize context windows. Use when coordinating multi-agent workflows, isolating concurrent git workspaces, or recording runs to telemetry.jsonl.
allowed-tools: Bash, Read, Write, Glob, Grep
---

# Harness Compound Multi Agent Worktrees

Orchestrates specialized Planner, Implementer, and Reviewer multi-agent teams, isolating coding execution in ephemeral Git worktrees (isolation: worktree) and slicing sub-specs to minimize context windows. Use when coordinating multi-agent workflows, isolating concurrent git workspaces, or recording runs to telemetry.jsonl.

## Structure & Available Components
- `scripts/`: Executable helper tools for this skill.
- `references/`: Architectural rules, patterns, and guides.
- `assets/`: Config templates and validation schemas.

## When to Use
Trigger this skill when:
- Operating within `module_08_compound_engineering` or applying its design patterns.
- Auditing, executing, or enforcing harness guarantees for this domain.

## How to Use
1. Consult references in `references/` for specifications and policies.
2. Execute scripts in `scripts/` to validate inputs and enforce constraints.
3. Apply configurations in `assets/` for standardized settings.

## Key Files & Implementation (GitHub Links)
- [https://github.com/kenhuangus/packt-harness/tree/main/.claude/skills/harness-compound-multi-agent-worktrees/](https://github.com/kenhuangus/packt-harness/tree/main/.claude/skills/harness-compound-multi-agent-worktrees/)
- [https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-compound-multi-agent-worktrees/SKILL.md](https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-compound-multi-agent-worktrees/SKILL.md)
- [https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_08_compound_engineering/](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_08_compound_engineering/)
