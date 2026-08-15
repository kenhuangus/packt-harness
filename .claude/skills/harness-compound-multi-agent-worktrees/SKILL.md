---
name: harness-compound-multi-agent-worktrees
description: Orchestrates specialized Planner, Implementer, and Reviewer multi-agent teams, isolating coding execution in ephemeral Git worktrees (isolation: worktree) and slicing sub-specs to minimize context windows. Use when coordinating multi-agent workflows, isolating concurrent git workspaces, or recording runs to telemetry.jsonl.
allowed-tools: Bash, Read, Write, Glob, Grep
---

# Compound Multi-Agent Engineering & Git Worktree Isolation (Module 8 Skill)

This skill coordinates specialized subagent teams (Planner, Implementer, Reviewer) and isolates file modifications inside dedicated Git worktrees (`isolation: worktree`) to eliminate context fatigue and prevent main-branch pollution.

## When to Use
- When complex tasks exceed a single prompt context window and require division of labor.
- When isolating agent code writes to dedicated Git worktree directories (`git worktree add -b ...`).
- When extracting task-specific sub-specs so subagents receive only relevant requirements.
- When running an independent Reviewer in a fresh context to eliminate self-review bias.

## How to Use
1. **Worktree Sandboxing**:
   ```python
   # Create ephemeral worktree
   subprocess.run(["git", "worktree", "add", "-b", branch_name, worktree_path, "HEAD"], cwd=repo_root)

   # Teardown after run
   subprocess.run(["git", "worktree", "remove", "--force", worktree_path], cwd=repo_root)
   subprocess.run(["git", "branch", "-D", branch_name], cwd=repo_root)
   ```

2. **Sub-Spec Isolation**:
   ```python
   sub_spec = isolator.extract_sub_spec(master_spec, subtask_name)
   # Pass ONLY sub_spec to the implementer
   ```

3. **Verification**:
   ```bash
   python course_implementation/module_08_compound_engineering/multi_agent_team_simulator.py
   ```

## Key Files & Implementation (GitHub Links)
- [https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_08_compound_engineering/multi_agent_team_simulator.py](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_08_compound_engineering/multi_agent_team_simulator.py)
- [https://github.com/kenhuangus/packt-harness/blob/main/.claude/agents/](https://github.com/kenhuangus/packt-harness/blob/main/.claude/agents/)
- [https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-compound-multi-agent-worktrees/SKILL.md](https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-compound-multi-agent-worktrees/SKILL.md)
