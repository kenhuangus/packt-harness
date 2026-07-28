============================================================
MODULE 2 DEMO: CORE HARNESS STACK (5 PILLARS )
============================================================
[LLM Client] Configured aisuite with live model 'openai:nvidia/Qwen3.6-35B-A3B-NVFP4' | Endpoint: 'http://127.0.0.1:8000/v1'
[Pillar 1 - Memory] Loaded persistent guidelines from 'AGENTS.md' (467 bytes)

[LLM Client Call] Model='openai:nvidia/Qwen3.6-35B-A3B-NVFP4' | Endpoint='http://127.0.0.1:8000/v1' | Prompt Length=31 chars
  [PASS] LIVE QWEN MODEL RESPONSE RECEIVED (5095 chars)

>>> HARNESS EXECUTION TASK: write_file <<<
[Pillar 2 - Permission] Tool 'write_file' and path 'C:\Users\kenhu\packt\harness\course_implementation\module_02_core_harness_stack\sample_module.py' validated.
[Pillar 3 - Pre-Hook] Code safety inspection passed.
[Pillar 3 - Post-Hook] Running AST static analysis on 'sample_module.py'...
[Pillar 5 - Trace] Logged 'WRITE_FILE_SUCCESS' to JSONL audit file.

>>> HARNESS EXECUTION TASK: run_test <<<
[Pillar 2 - Permission] Tool 'run_test' and path 'None' validated.
[Pillar 4 - Test Runner] Executing test suite: pytest
[Pillar 5 - Trace] Logged 'RUN_TEST_SUCCESS' to JSONL audit file.

>>> HARNESS EXECUTION TASK: write_file <<<
[Pillar 5 - Trace] Logged 'HARNESS_ERROR' to JSONL audit file.
[FAIL] HARNESS ERROR: Path Traversal Blocked: Target '../../forbidden.py' is outside workspace 'C:\Users\kenhu\packt\harness\course_implementation\module_02_core_harness_stack'.

============================================================
MODULE 2 DEMO COMPLETE: All 5 Pillars Executed & Logged!
============================================================
