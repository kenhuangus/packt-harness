# Module 4 Run Results

Captured 2026-08-14 from a real process. `bash_guard.py` was invoked as
a subprocess with JSON on stdin.

```text
> C:\Users\kenhu\AppData\Local\Programs\Python\Python313\python.exe C:\Users\kenhu\packt-harness\course_implementation\module_04_guardrails_and_hooks\guardrails_engine.py
[Live Claude Code hook subprocess]
  [PASS] bash_guard.py safe pytest: exit=0 decision=defer
  [PASS] bash_guard.py dangerous rm: exit=0 decision=deny
  [OUTPUT] C:\Users\kenhu\packt-harness\course_implementation\module_04_guardrails_and_hooks\output\hook_results.json
MODULE 4 DEMO COMPLETE: ALL EXPECTED CONTROLS VERIFIED!
```

Exit code: 0
