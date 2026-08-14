# Module 2 Run Results

Captured 2026-08-14 on this machine from an actual process.

The live `events.jsonl` for this run was
`C:\Users\kenhu\AppData\Local\Temp\module_02_harness_0gg2cx8v\events.jsonl`
and was deleted with the temporary workspace. The `[FAIL] HARNESS ERROR`
line is the expected path-traversal rejection.

```text
> C:\Users\kenhu\AppData\Local\Programs\Python\Python313\python.exe C:\Users\kenhu\packt-harness\course_implementation\module_02_core_harness_stack\core_harness_stack.py
cwd = C:\Users\kenhu\packt-harness\course_implementation\module_02_core_harness_stack
========================================================================
MODULE 2 DEMO: CORE HARNESS STACK (5 PILLARS)
========================================================================
[Pillar 1 - Memory] Loaded persistent guidelines from 'AGENTS.md' (482 bytes)
Allocations: {'memory': 25600, 'spec': 25600, 'workspace': 64000, 'output_buffer': 12800}

>>> HARNESS EXECUTION TASK: write_file <<<
[Pillar 2 - Permission] Tool 'write_file' and path 'C:\Users\kenhu\AppData\Local\Temp\module_02_harness_0gg2cx8v\sample_module.py' validated.
[Pillar 3 - Pre-Hook] Code safety inspection passed.
[Pillar 3 - Post-Hook] Running AST static analysis on 'sample_module.py'...
  [PASS] AST syntax valid.
[Pillar 5 - Trace] Logged 'WRITE_FILE_SUCCESS' to JSONL audit file.

>>> HARNESS EXECUTION TASK: run_test <<<
[Pillar 2 - Permission] Tool 'run_test' and path 'None' validated.
[Pillar 4 - Test Runner] Executing test suite: pytest
  [PASS] pytest exited with code 0.
[Pillar 5 - Trace] Logged 'RUN_TEST_SUCCESS' to JSONL audit file.

>>> HARNESS EXECUTION TASK: write_file <<<
[Pillar 5 - Trace] Logged 'HARNESS_ERROR' to JSONL audit file.
[FAIL] HARNESS ERROR: Path Traversal Blocked: Target 'C:\Users\kenhu\AppData\Local\Temp\module_02_harness_0gg2cx8v\..\..\forbidden.py' is outside workspace 'C:\Users\kenhu\AppData\Local\Temp\module_02_harness_0gg2cx8v'

MODULE 2 DEMO COMPLETE: All 5 Pillars Executed & Logged!
```

Exit code: 0
