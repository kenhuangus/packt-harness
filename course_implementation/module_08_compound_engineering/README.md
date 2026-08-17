# Module 8: Compound Engineering

## What this module teaches

One agent that plans, codes, and reviews its own work is a single
point of failure. Compound engineering splits the job into roles with
separate context windows, then records the handoff.

| Role | Job in this demo | Isolation |
| --- | --- | --- |
| Planner (architect) | Turn a spec into two named subtasks | Read-only by design |
| Implementer (coder) | Write `auth.py` and `test_auth.py` | Temporary sandbox (see below) |
| Reviewer (auditor) | File exists, defines `validate_jwt`, AST parses, path stays in scope | Independent pass over the files |

This run creates a real `git worktree`, writes HS256 `auth.py` and
`test_auth.py` into it, runs pytest there (3 passed), copies the files
back to this module, appends `telemetry.jsonl`, then removes the worktree.

[auth.py](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_08_compound_engineering/auth.py)
is the implementer output from the last run, not a `return True` stub.

## Files

| Path | Role |
| --- | --- |
| [multi_agent_team_simulator.py](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_08_compound_engineering/multi_agent_team_simulator.py) | Planner / implementer / reviewer |
| [auth.py](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_08_compound_engineering/auth.py) | HS256 JWT from the last implementer run |
| [test_auth.py](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_08_compound_engineering/test_auth.py) | Real pytest file from the last implementer run |
| [telemetry.jsonl](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_08_compound_engineering/telemetry.jsonl) | Append-only telemetry |
| [run_evidence.json](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_08_compound_engineering/output/run_evidence.json) | Last worktree path, branch, pytest output |
| [spec-reviewer.md](https://github.com/kenhuangus/packt-harness/blob/main/.claude/agents/spec-reviewer.md) | Real Claude Code subagent definition |
| [RUN_RESULTS.md](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_08_compound_engineering/RUN_RESULTS.md) | Last captured stdout |

## How to run

```powershell
C:\Users\kenhu\AppData\Local\Programs\Python\Python313\python.exe C:\Users\kenhu\packt-harness\course_implementation\module_08_compound_engineering\multi_agent_team_simulator.py
```

## Output file and evidence

- **Stdout** (exit 0).
- **Live telemetry (ephemeral):** `C:\Users\kenhu\AppData\Local\Temp\module_08_team_<random>\telemetry.jsonl`
- **Recorded copy:** [RUN_RESULTS.md](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_08_compound_engineering/RUN_RESULTS.md)

Captured on this machine, 2026-08-17:

```text
[Isolation] git worktree created at ...\Temp\module08-agent-27740-20260817061818385121
[Isolation] branch module08-agent-27740-20260817061818385121
[Planner Subagent (Architect)] Analyzing requirement...
  [PASS] Plan Generated: 2 micro-subtasks allocated.
[Implementer Subagent (Coder)] Writing into the worktree...
  [PASS] Wrote ...\auth.py (2392 bytes).
  [PASS] Wrote ...\test_auth.py (663 bytes).
[Reviewer Subagent (Auditor)] AST + pytest in the worktree...
  [PASS] Review auth.py: {'syntax_ok': True, 'defines_validate_jwt': True, ...}
  [PASS] Review test_auth.py: {'syntax_ok': True, 'defines_validate_jwt': False, ...}
3 passed in 0.22s
  [PASS] pytest passed inside the isolated worktree.
[Self-Improvement Telemetry] Appended to ...\telemetry.jsonl
[Isolation] git worktree removed.
```

## Annotated code

```python
class SubagentPromptIsolator:
    """
    Real Claude Code subagents already start with a clean context window.
    This helper keeps lines that mention the subtask name, allowed scope,
    or non-goals, and drops the rest.
    """

class WorktreeIsolation:
    """
    Runs `git worktree add` on a real branch and removes it in a finally
    block. The implementer never writes into the checked-out repository.
    """

class MultiAgentTeam:
    """
    Each role gets the worktree path, not the repository root, so scope
    violations fail on the filesystem rather than on trust.
    """

    def run_planner(self, spec_text):
        # Two named subtasks: auth_component -> auth.py, test_suite -> test_auth.py

    def run_implementer(self, subtask, master_spec):
        # Write one scoped Python file from a focused spec slice.

    def run_reviewer(self, target_file):
        # ast.parse the file and confirm it defines validate_jwt.
```

`main()` then runs pytest inside the worktree and returns 1 if it does
not exit 0, so a failing suite fails the module instead of printing
`[PASS]`.
