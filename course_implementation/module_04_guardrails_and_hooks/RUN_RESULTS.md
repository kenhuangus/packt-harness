============================================================
MODULE 4 DEMO: PRODUCTION GUARDRAILS & HOOKS ENGINE 
============================================================
[LLM Client] Configured aisuite with live model 'openai:nvidia/Qwen3.6-35B-A3B-NVFP4' | Endpoint: 'http://127.0.0.1:8000/v1'

[LLM Client Call] Model='openai:nvidia/Qwen3.6-35B-A3B-NVFP4' | Endpoint='http://127.0.0.1:8000/v1' | Prompt Length=48 chars
  [PASS] LIVE QWEN MODEL RESPONSE RECEIVED (1408 chars)

[Guardrail - Pre-Action Hook] Inspecting shell command: 'pytest tests/unit/'
  [PASS] Pre-Hook Status: Command approved for execution.

[Guardrail - Pre-Action Hook] Inspecting shell command: 'sudo rm -rf /var/config'
  [FAIL] PRE-HOOK SECURITY VIOLATION: Command matches forbidden pattern 'rm\s+-rf'!

[Guardrail - Post-Action Hook] Auditing generated code for 'processor.py'...
  [PASS] AST Parser Status: Valid Python syntax tree generated.
  [PASS] Post-Hook Status: File audit passed cleanly.

[Guardrail - Post-Action Hook] Auditing generated code for 'config.py'...
  [FAIL] POST-HOOK VIOLATION: Hardcoded secret key detected in code!

[Guardrail - Post-Action Hook] Auditing generated code for 'broken.py'...
  [FAIL] POST-HOOK AST VIOLATION: Python syntax error on line 1: invalid syntax

============================================================
MODULE 4 DEMO COMPLETE: All Guardrail Interceptors Active!
============================================================
