# Module 5: Permission Escalation Gateway

## What this module teaches

Not every tool call deserves the same approval friction. A read can be
auto-approved. A `git push` to `main` cannot. This module is the
10-minute Q&A block's working example: a risk matrix that decides
auto-approve, log, or require an explicit confirmation.

| Risk | Tools | Action in this demo |
| --- | --- | --- |
| LOW | `read_file`, `list_dir`, `grep` | Auto-approve |
| MEDIUM | `write_file`, `run_test` | Log and approve |
| HIGH | `pip_install` | Extra logging, still allowed |
| CRITICAL | `git_push`, `db_drop` | Block unless `user_auto_approve=True` |

LOW actually reads `output\src\main.py`. MEDIUM actually overwrites that
file. CRITICAL looks up `request_id` in `output\approvals.json`. Without
a record the push is blocked; after `grant_approval` the gateway writes
`pending_push.json` and does **not** run `git push`.

## Files

| Path | Role |
| --- | --- |
| [permission_escalation_gateway.py](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_05_break_and_qna/permission_escalation_gateway.py) | Risk matrix + four cases |
| [RUN_RESULTS.md](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_05_break_and_qna/RUN_RESULTS.md) | Last captured stdout |

Output files:

- [main.py](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_05_break_and_qna/output/src/main.py)
- [approvals.json](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_05_break_and_qna/output/approvals.json)
- [pending_push.json](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_05_break_and_qna/output/pending_push.json)
- [audit.jsonl](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_05_break_and_qna/output/audit.jsonl)
- [run_evidence.json](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_05_break_and_qna/output/run_evidence.json)

## How to run

Run from the repository root:

```powershell
python course_implementation/module_05_break_and_qna/permission_escalation_gateway.py
```

## Output file and evidence

- **Stdout** (exit 0).
- **Recorded copy:** [RUN_RESULTS.md](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_05_break_and_qna/RUN_RESULTS.md)

Captured on this machine, 2026-08-14:

```text
[Escalation Gateway] Evaluating Request: Tool='read_file' | Risk Level=LOW
  ✓ [AUTO-APPROVED] Low-risk tool call permitted instantly.

[Escalation Gateway] Evaluating Request: Tool='write_file' | Risk Level=MEDIUM
  ✓ [LOGGED & APPROVED] Medium-risk tool call executed and logged to audit trace.

[Escalation Gateway] Evaluating Request: Tool='git_push' | Risk Level=CRITICAL
  ❌ [ESCALATION BLOCKED] Critical action requires explicit developer click approval!

[Escalation Gateway] Evaluating Request: Tool='git_push' | Risk Level=CRITICAL
  ✓ [USER CONFIRMED] Critical action approved by developer modal prompt.
```

## Annotated code

```python
class PermissionEscalationGateway:
    """
    LOW    — read-only tools, auto-approve
    MEDIUM — non-destructive writes/tests, log then approve
    HIGH   — package installs, extra logging, still allowed here
    CRITICAL — git_push / db_drop: blocked unless the caller supplies
               an explicit user confirmation (user_auto_approve=True)
    """

    def evaluate_request(self, tool_name, params, user_auto_approve=False):
        # Unknown tools default to HIGH so they are never silently treated as LOW.
        risk = self.risk_matrix.get(tool_name, "HIGH")
        if risk == "CRITICAL" and not user_auto_approve:
            return False
```
