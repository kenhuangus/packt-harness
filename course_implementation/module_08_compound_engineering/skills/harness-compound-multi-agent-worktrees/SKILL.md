---
name: harness-compound-multi-agent-worktrees
description: Orchestrates specialized Planner, Implementer, and Reviewer multi-agent
  teams, isolating coding execution in ephemeral Git worktrees and slicing sub-specs
  to minimize context windows. Trigger when coordinating multi-agent workflows, managing
  git worktrees, or recording multi-agent runs to telemetry.jsonl.
version: 1.0.0
author: Harness Engineering Team
allowed-tools: Bash, Read, Write, Grep
---

# Harness Compound Multi-Agent Worktrees

## Overview
Coordinates specialized Planner, Implementer, and Reviewer subagent teams, isolating workspace modifications inside ephemeral Git worktrees and recording audit telemetry to `telemetry.jsonl`.

## Structure & Progressive Disclosure
- `scripts/`: Executable helper and verification tools.
- `references/`: Detailed specifications, guides, and architectural rules.
- `assets/`: Configuration templates and machine-readable schemas.

## When to Use
- When distributing complex development tasks across specialized subagents.
- When isolating agent code changes in ephemeral Git worktrees (`git worktree add`).
- When tracking multi-agent token usage and completion telemetry in `telemetry.jsonl`.

## Required Inputs
- Feature goal and task description.
- Repository root directory.
- Ephemeral branch and worktree directory path.

## Instructions
Run all commands from the repository root.
1. Dispatch Planner agent to generate a focused sub-spec from the goal.
2. Execute `python .claude/skills/harness-compound-multi-agent-worktrees/scripts/worktree_manager.py` to create an ephemeral Git worktree.
3. Dispatch Implementer agent inside the worktree directory with a scoped context window.
4. Dispatch Reviewer agent in a fresh context window to run pytest assertions and AST checks.
5. Merge verified changes to `main` and delete the ephemeral worktree (`git worktree remove`).
6. Consult `references/multi-agent-team-roles.md` for role specifications.

## Output Format
Always format output adhering to this structure:
```json
{
  "pipeline_status": "COMPLETED",
  "worktree_path": ".worktrees/feature_branch",
  "tokens_consumed": 1670,
  "reviewer_verdict": "APPROVED",
  "commit_hash": "a1b2c3d"
}
```

## Examples
### Managing Ephemeral Git Worktrees
```python
from scripts.worktree_manager import create_worktree, remove_worktree

create_worktree(".", "feat-temp", ".worktrees/temp")
# ... implementer executes code in .worktrees/temp ...
remove_worktree(".", "feat-temp", ".worktrees/temp")
```

## Key Implementation Links (GitHub)
- [https://github.com/kenhuangus/packt-harness/tree/main/.claude/skills/harness-compound-multi-agent-worktrees/](https://github.com/kenhuangus/packt-harness/tree/main/.claude/skills/harness-compound-multi-agent-worktrees/)
- [https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-compound-multi-agent-worktrees/SKILL.md](https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-compound-multi-agent-worktrees/SKILL.md)
- [https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_08_compound_engineering/](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_08_compound_engineering/)
