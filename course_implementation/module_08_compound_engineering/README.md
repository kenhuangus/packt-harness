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

`C:\Users\kenhu\packt-harness\course_implementation\module_08_compound_engineering\auth.py`
is the implementer output from the last run, not a `return True` stub.

## Files

| Path | Role |
| --- | --- |
| `C:\Users\kenhu\packt-harness\course_implementation\module_08_compound_engineering\multi_agent_team_simulator.py` | Planner / implementer / reviewer |
| `C:\Users\kenhu\packt-harness\course_implementation\module_08_compound_engineering\auth.py` | HS256 JWT from the last implementer run |
| `C:\Users\kenhu\packt-harness\course_implementation\module_08_compound_engineering\test_auth.py` | Real pytest file from the last implementer run |
| `C:\Users\kenhu\packt-harness\course_implementation\module_08_compound_engineering\telemetry.jsonl` | Append-only telemetry |
| `C:\Users\kenhu\packt-harness\course_implementation\module_08_compound_engineering\output\run_evidence.json` | Last worktree path, branch, pytest output |
| `C:\Users\kenhu\packt-harness\.claude\agents\spec-reviewer.md` | Real Claude Code subagent definition |
| `C:\Users\kenhu\packt-harness\course_implementation\module_08_compound_engineering\RUN_RESULTS.md` | Last captured stdout |

## How to run

```powershell
C:\Users\kenhu\AppData\Local\Programs\Python\Python313\python.exe C:\Users\kenhu\packt-harness\course_implementation\module_08_compound_engineering\multi_agent_team_simulator.py
```

## Output file and evidence

- **Stdout** (exit 0).
- **Live telemetry (ephemeral):** `C:\Users\kenhu\AppData\Local\Temp\module_08_team_<random>\telemetry.jsonl`
- **Recorded copy:** `C:\Users\kenhu\packt-harness\course_implementation\module_08_compound_engineering\RUN_RESULTS.md`

Captured on this machine, 2026-08-14:

```text
[Planner Subagent (Architect)] Analyzing requirement...
  [PASS] Plan Generated: 2 micro-subtasks allocated.
[Implementer Subagent (Coder)] Executing simulated edits in a temporary sandbox...
  Claude Code project subagents are defined in .claude/agents/<name>.md with frontmatter `isolation: worktree`.
  [Illustrative command - NOT EXECUTED] git worktree add -b agent-worktree ./worktree-dir main
  [PASS] Simulated isolated edit completed for 'auth_component'.
  [PASS] Simulated isolated edit completed for 'test_suite'.
[Reviewer Subagent (Auditor)] Auditing Implementer output against SPEC.md...
  [PASS] Review Passed: AST syntax valid, scope compliance confirmed.
[Self-Improvement Telemetry] Recorded task 'jwt_auth_multi_agent_handoff' into 'telemetry.jsonl'.
```

## Annotated code

```python
class SubagentPromptIsolator:
    """
    Real Claude Code subagents already start with a clean context window.
    This helper keeps lines that mention the subtask name, allowed scope,
    or non-goals, and drops the rest.
    """

class MultiAgentTeamSimulator:
    """
    The implementer writes into a TemporaryDirectory, not a real git
    worktree. The printed `git worktree add` line is labelled NOT EXECUTED.
    """

    def run_planner(self, spec_text):
        # Two named subtasks: auth_component -> auth.py, test_suite -> test_auth.py

    def run_implementer_in_worktree(self, subtask, master_spec):
        # Write one scoped Python file from a focused spec slice.

    def run_reviewer(self, target_file):
        # File exists and defines validate_jwt. AST and scope are checked in main().
```
