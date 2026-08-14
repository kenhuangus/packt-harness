# Module 1 Run Results

Captured 2026-08-14 from a real process against local vLLM
`nvidia/Qwen3.6-35B-A3B-NVFP4` at `http://127.0.0.1:8000/v1`.
Live reply (stored in `output\run_evidence.json`):
"A harness is essential to enforce safety, manage execution context, and
ensure the model's code output is reliable and actionable within a specific
environment."

```text
> C:\Users\kenhu\AppData\Local\Programs\Python\Python313\python.exe C:\Users\kenhu\packt-harness\course_implementation\module_01_why_harness_engineering\harness_vs_model_demo.py
--- UN-HARNESSED AGENT ---
[LLM Attempt 1] Running: pytest tests/auth_test.py
[System Output] exit=2 1 error in 0.69s
[LLM Attempt 4] Running cleanup: rm -rf var/log
[WARNING] UN-HARNESSED FAILURE: deleted 1 log path(s); app.log exists=False

--- HARNESSED AGENT ---
  [EXECUTED] pytest exit=2
  [BLOCKED] Loop Detected: BLOCKED BY HARNESS LOOP DETECTOR: Command 'pytest tests/auth_test.py' repeated 2 times without progress.
  [BLOCKED] Security Violation: BLOCKED BY PRE-HOOK: Dangerous command pattern 'rm\s+-rf' detected.
[Harness] sandbox log survived=True
[OUTPUT] C:\Users\kenhu\packt-harness\course_implementation\module_01_why_harness_engineering\output\run_evidence.json
```

Exit code: 0
