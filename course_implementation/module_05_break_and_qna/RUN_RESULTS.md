# Module 5 Run Results

Captured from an actual run.

```text
> python permission_escalation_gateway.py
============================================================
MODULE 5 DEMO: RISK-TIERED PERMISSION ESCALATION GATEWAY 
============================================================
[LLM Client] Configured LLM client with model 'openai:nvidia/Qwen3.6-35B-A3B-NVFP4' | Endpoint: 'http://127.0.0.1:8000/v1'

[Escalation Gateway] Evaluating Request: Tool='read_file' | Risk Level=LOW
  ✓ [AUTO-APPROVED] Low-risk tool call permitted instantly.

[Escalation Gateway] Evaluating Request: Tool='write_file' | Risk Level=MEDIUM
  ✓ [LOGGED & APPROVED] Medium-risk tool call executed and logged to audit trace.

[Escalation Gateway] Evaluating Request: Tool='git_push' | Risk Level=CRITICAL
  ❌ [ESCALATION BLOCKED] Critical action requires explicit developer click approval!

[Escalation Gateway] Evaluating Request: Tool='git_push' | Risk Level=CRITICAL
  ✓ [USER CONFIRMED] Critical action approved by developer modal prompt.

============================================================
MODULE 5 DEMO COMPLETE: Escalation Gateway Risk Matrix Active!
============================================================
```

Exit code: 0
