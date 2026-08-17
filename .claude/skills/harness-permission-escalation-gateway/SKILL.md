---
name: harness-permission-escalation-gateway
description: Evaluates tool requests against a 4-tier risk matrix (LOW, MEDIUM, HIGH,
  CRITICAL), auto-approving safe reads, auditing sandboxed writes, and requiring signed
  approvals.json tokens for critical operations like git_push. Trigger when gating
  sensitive operations, configuring human-in-the-loop approvals, or creating pending
  action ledgers.
version: 1.0.0
author: Harness Engineering Team
allowed-tools: Read, Write, Grep, Bash
---

# Harness Permission Escalation Gateway

## Overview
4-Tier Risk Escalation Gateway that automatically approves read actions while strictly gating high-risk actions behind cryptographic or human-signed approval tokens in `approvals.json`.

## Structure & Progressive Disclosure
- `scripts/`: Executable helper and verification tools.
- `references/`: Detailed specifications, guides, and architectural rules.
- `assets/`: Configuration templates and machine-readable schemas.

## When to Use
- When gating sensitive tools (`git push`, deployments, database modifications).
- When generating pending request artifacts for human-in-the-loop review.
- When validating signed approval tokens against `approvals.json`.

## Required Inputs
- Tool invocation name and parameters.
- Unique request ID.
- Path to signed approval ledger (`approvals.json`).

## Instructions
Run all commands from the repository root.
1. Map requested tool to risk tier in `assets/risk_matrix.json` (LOW, MEDIUM, HIGH, CRITICAL).
2. Auto-approve `LOW` risk operations (`read_file`, `list_dir`, `grep_search`).
3. Log `MEDIUM` risk operations (`write_file`, `run_test`) and proceed inside sandbox.
4. For `CRITICAL` operations (`git_push`), execute `python .claude/skills/harness-permission-escalation-gateway/scripts/evaluate_gateway.py` to check `approvals.json`.
5. If token is missing, generate pending action artifact and block execution.
6. Consult `references/risk-tier-matrix.md` for policy mapping.

## Output Format
Always format output adhering to this structure:
```json
{
  "request_id": "req_push_001",
  "risk_tier": "CRITICAL",
  "decision": "APPROVED_BY_LEDGER | PENDING_HUMAN_APPROVAL",
  "signed_by": "security_officer@enterprise.com"
}
```

## Examples
### Evaluating Critical Operation Permission
```python
from scripts.evaluate_gateway import evaluate

result = evaluate("git_push", "req_push_001", "approvals.json")
print(result["status"])  # BLOCKED (requires signed token in approvals.json)
```

## Key Implementation Links (GitHub)
- [https://github.com/kenhuangus/packt-harness/tree/main/.claude/skills/harness-permission-escalation-gateway/](https://github.com/kenhuangus/packt-harness/tree/main/.claude/skills/harness-permission-escalation-gateway/)
- [https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-permission-escalation-gateway/SKILL.md](https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-permission-escalation-gateway/SKILL.md)
- [https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_05_break_and_qna/](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_05_break_and_qna/)
