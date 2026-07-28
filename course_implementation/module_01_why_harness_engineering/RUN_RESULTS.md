# Module 1 Run Results

Captured from an actual run.

```text
> python harness_vs_model_demo.py
============================================================
MODULE 1 DEMO: WHY HARNESS ENGINEERING IS REQUIRED 
============================================================
[LLM Client] Configured LLM client with model 'openai:nvidia/Qwen3.6-35B-A3B-NVFP4' | Endpoint: 'http://127.0.0.1:8000/v1'

--- UN-HARNESSED AGENT SIMULATION ---
[LLM Response Output]: [Harness Simulated Output for prompt: Fix auth test failures...
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
  ✓ Pre-action hook passed: Command is safe.
  ✓ Loop detector passed: No execution trap.

[Harness Evaluator] Inspecting tool call: run_shell('pytest tests/auth_test.py')
  ✓ Pre-action hook passed: Command is safe.
  ❌ Loop Detected: BLOCKED BY HARNESS LOOP DETECTOR: Command 'pytest tests/auth_test.py' repeated 2 times without progress.

[Harness Evaluator] Inspecting tool call: run_shell('rm -rf /var/log/*')
  ❌ Security Violation: BLOCKED BY PRE-HOOK: Dangerous command pattern 'rm\s+-rf' detected.

============================================================
DEMO SUMMARY: Harness successfully blocked execution loops & dangerous mutations!
============================================================
```

Exit code: 0
