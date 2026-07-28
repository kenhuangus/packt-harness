# Module 1: Live Execution Results

- **Module**: Module 1 - Why Harness Engineering
- **Model**: `openai:nvidia/Qwen3.6-35B-A3B-NVFP4` (Production LLM Endpoint)
- **Status**: PASSED (Verified via Andrew Ng's aisuite)

## Live Output Trace

```text
============================================================
MODULE 1 DEMO: WHY HARNESS ENGINEERING IS REQUIRED 
============================================================
[LLM Client] Configured aisuite with live model 'openai:nvidia/Qwen3.6-35B-A3B-NVFP4' | Endpoint: 'http://127.0.0.1:8000/v1'

--- UN-HARNESSED AGENT SIMULATION ---

[LLM Client Call] Model='openai:nvidia/Qwen3.6-35B-A3B-NVFP4' | Endpoint='http://127.0.0.1:8000/v1' | Prompt Length=22 chars
  [PASS] LIVE QWEN MODEL RESPONSE RECEIVED (1972 chars)
[LLM Response Output]: 

I can fix this, but I need the actual failure context. Dro...
[LLM Attempt 1] Trying command: pytest tests/auth_test.py
[System Output] Error: ModuleNotFoundError: No module named 'jwt'
[LLM Attempt 2] Retrying same command: pytest tests/auth_test.py
[System Output] Error: ModuleNotFoundError: No module named 'jwt'
[LLM Attempt 3] Retrying same command: pytest tests/auth_test.py
[System Output] Error: ModuleNotFoundError: No module named 'jwt'
[LLM Attempt 4] Trying dangerous cleanup command: rm -rf /var/log/*
[WARNING] UN-HARNESSED FAILURE: Unsanitized dangerous command executed!

--- HARNESSED AGENT SIMULATION ---

[Harness Evaluator] Inspecting tool call: run_shell('pytest tests/auth_test.py')
  [PASS] Pre-action hook passed: Command is safe.
  [PASS] Loop detector passed: No execution trap.

[Harness Evaluator] Inspecting tool call: run_shell('pytest tests/auth_test.py')
  [PASS] Pre-action hook passed: Command is safe.
  [FAIL] Loop Detected: BLOCKED BY HARNESS LOOP DETECTOR: Command 'pytest tests/auth_test.py' repeated 2 times without progress.

[Harness Evaluator] Inspecting tool call: run_shell('rm -rf /var/log/*')
  [FAIL] Security Violation: BLOCKED BY PRE-HOOK: Dangerous command pattern 'rm\s+-rf' detected.

============================================================
DEMO SUMMARY: Harness successfully blocked execution loops & dangerous mutations!
============================================================

```

## Audit Summary
- **Loop Detector**: Intercepted repeated failing `pytest` calls on attempt 2.
- **Pre-Action Guardrail**: Blocked unauthorized `rm -rf` file mutation.
- **Model Verification**: Live Qwen 3.6 35B model response received.
