# Module 1 Run Results

Captured 2026-08-14 on this machine from an actual process.

```text
> C:\Users\kenhu\AppData\Local\Programs\Python\Python313\python.exe C:\Users\kenhu\packt-harness\course_implementation\module_01_why_harness_engineering\harness_vs_model_demo.py
cwd = C:\Users\kenhu\packt-harness\course_implementation\module_01_why_harness_engineering
============================================================
MODULE 1 DEMO: WHY HARNESS ENGINEERING IS REQUIRED 
============================================================
[LLM Client] Configured LLM client with model 'default-harness-model' | Endpoint: 'http://127.0.0.1:8000/v1'

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
