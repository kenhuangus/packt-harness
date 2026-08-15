---
name: harness-permission-escalation-gateway
description: Evaluates tool requests against a 4-tier risk matrix (LOW, MEDIUM, HIGH, CRITICAL), auto-approving safe reads, auditing sandboxed writes, and strictly requiring signed approvals.json tokens for critical operations (git_push). Use when gating sensitive tools, establishing human-in-the-loop workflows, or generating pending action artifacts.
allowed-tools: Read, Write, Glob, Grep
---

# Permission Escalation Gateway & Approvals Ledger (Module 5 Skill)

This skill provides risk-tiered execution control for autonomous agents, ensuring that critical operations (e.g. `git_push`, remote deploy, database drops) cannot execute without an explicit approval ledger on disk.

## When to Use
- When balancing agent speed (auto-approving low-risk reads) with safety governance.
- When gating critical operations behind human-in-the-loop sign-off tokens.
- When generating signed pending artifacts (`pending_push.json`) rather than directly executing destructive remote mutations.

## How to Use
1. **Risk Matrix Classification**:
   - `LOW` (e.g. `read_file`, `list_dir`, `grep`): Auto-approved.
   - `MEDIUM` (e.g. `write_file`, `run_test`): Logged & executed in sandbox.
   - `HIGH` (e.g. `pip_install`): Logged with intent alert.
   - `CRITICAL` (e.g. `git_push`, `drop_db`): Requires approval token in `approvals.json`.

2. **Evaluation Logic**:
   ```python
   risk = risk_matrix.get(tool_name, "HIGH")
   if risk == "LOW":
       return {"allowed": True, "content": (workspace / params["path"]).read_text("utf-8")}
   if risk == "MEDIUM":
       (workspace / params["path"]).write_text(params["content"], encoding="utf-8")
       return {"allowed": True, "path": str(workspace / params["path"])}
   if risk == "CRITICAL":
       approvals = json.loads((workspace / "approvals.json").read_text("utf-8"))
       if request_id not in approvals:
           return {"allowed": False, "reason": "missing_approval"}
       pending = {"request_id": request_id, "approved_by": approvals[request_id]}
       (workspace / "pending_push.json").write_text(json.dumps(pending, indent=2), encoding="utf-8")
       return {"allowed": True, "pending_push": str(workspace / "pending_push.json")}
   ```

3. **Verification**:
   ```bash
   python course_implementation/module_05_break_and_qna/permission_escalation_gateway.py
   ```

## Key Files & Implementation
- `course_implementation/module_05_break_and_qna/permission_escalation_gateway.py`
- `course_implementation/module_05_break_and_qna/approvals.json`
