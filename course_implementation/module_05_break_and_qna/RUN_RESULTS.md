============================================================
MODULE 5 DEMO: RISK-TIERED PERMISSION ESCALATION GATEWAY 
============================================================
[LLM Client] Configured aisuite with live model 'openai:nvidia/Qwen3.6-35B-A3B-NVFP4' | Endpoint: 'http://127.0.0.1:8000/v1'

[LLM Client Call] Model='openai:nvidia/Qwen3.6-35B-A3B-NVFP4' | Endpoint='http://127.0.0.1:8000/v1' | Prompt Length=42 chars
  [PASS] LIVE QWEN MODEL RESPONSE RECEIVED (1723 chars)

[Escalation Gateway] Evaluating Request: Tool='read_file' | Risk Level=LOW
  [PASS] [AUTO-APPROVED] Low-risk tool call permitted instantly.

[Escalation Gateway] Evaluating Request: Tool='write_file' | Risk Level=MEDIUM
  [PASS] [LOGGED & APPROVED] Medium-risk tool call executed and logged to audit trace.

[Escalation Gateway] Evaluating Request: Tool='git_push' | Risk Level=CRITICAL
  [FAIL] [ESCALATION BLOCKED] Critical action requires explicit developer click approval!

[Escalation Gateway] Evaluating Request: Tool='git_push' | Risk Level=CRITICAL
  [PASS] [USER CONFIRMED] Critical action approved by developer modal prompt.

============================================================
MODULE 5 DEMO COMPLETE: Escalation Gateway Risk Matrix Active!
============================================================
