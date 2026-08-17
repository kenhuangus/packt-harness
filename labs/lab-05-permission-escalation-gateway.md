# Lab 05 — Permission Escalation Gateway

**Skill:** `harness-permission-escalation-gateway`  
**Module:** [module_05_break_and_qna](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_05_break_and_qna)  
**Time:** 40 minutes

## What you will end up with
You will have a repeatable risk-tier check where low-risk requests auto-approve and critical requests block until a ledger approval exists.

## Before you start
Run this against your own repository policy decisions, but use the reference script in this repo.  
If you run the full module demo, it needs generation and may require `HARNESS_ALLOW_SIMULATED_LLM=1`.

## Steps
1. Evaluate a low-risk request.

```bash
cd /path/to/packt-harness
python -c 'from pathlib import Path; import importlib.util; p=Path(".claude/skills/harness-permission-escalation-gateway/scripts/evaluate_gateway.py"); spec=importlib.util.spec_from_file_location("gw", p); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); print(m.evaluate("read_file","req_read_001","approvals.json"))'
```

2. Evaluate a critical request with no ledger entry.

```bash
python -c 'from pathlib import Path; import importlib.util; p=Path(".claude/skills/harness-permission-escalation-gateway/scripts/evaluate_gateway.py"); spec=importlib.util.spec_from_file_location("gw", p); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); print(m.evaluate("git_push","req_push_001","approvals.json"))'
```

3. Run the full module gateway demo with simulated generation fallback enabled.

```bash
export HARNESS_ALLOW_SIMULATED_LLM=1
python course_implementation/module_05_break_and_qna/permission_escalation_gateway.py
```

4. In your own repo, define which tool names map to LOW, MEDIUM, HIGH, and CRITICAL.

```bash
cd /path/to/your-repo
printf "lab05_risk_matrix_drafted: yes\n" >> harness-lab-notes.txt
```

## Expected output
Real captured output:

```text
{'status': 'AUTO_APPROVED', 'risk': 'LOW'}
{'status': 'BLOCKED', 'reason': 'Requires human approval token in approvals.json'}
```

## Break it on purpose
Attempt a critical action without creating `approvals.json`.

```bash
python -c 'from pathlib import Path; import importlib.util; p=Path("/path/to/packt-harness/.claude/skills/harness-permission-escalation-gateway/scripts/evaluate_gateway.py"); spec=importlib.util.spec_from_file_location("gw", p); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); print(m.evaluate("git_push","req_push_break","approvals.json"))'
```

The skill should block and state that a human approval token is required.

## You are done when
- `read_file` is auto-approved.
- `git_push` is blocked without an approval ledger token.
- You can point to your drafted risk-tier mapping notes.

## If it goes wrong
- If import loading fails, verify the absolute script path in the command.
- If `git_push` is unexpectedly approved, check whether `approvals.json` already has that request ID.
- If the full module demo cannot reach a local model, keep `HARNESS_ALLOW_SIMULATED_LLM=1`.
