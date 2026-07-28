# Module 6 Run Results

Captured from an actual run.

```text
> python tda_reliability_pipeline.py
============================================================
MODULE 6 DEMO: TEST-DRIVEN AGENT (TDA) & ANTI-REGRESSION PIPELINE
============================================================
[PASS] pytest availability check: pytest 9.1.1

[TDA Stage 1] Prove the proposed implementation fails a real test.

[TDA Pipeline] Running real pytest suite against proposed code...
[FAIL] pytest exited with return code 1; captured failure output follows:
F                                                                        [100%]
================================== FAILURES ===================================
_____________________________ test_divide_by_zero _____________________________
test_calculator.py:5: in test_divide_by_zero
    assert divide(10, 0) == 0
           ^^^^^^^^^^^^^
calculator.py:2: in divide
    return a / b
           ^^^^^
E   ZeroDivisionError: division by zero
=========================== short test summary info ===========================
FAILED test_calculator.py::test_divide_by_zero - ZeroDivisionError: division ...
1 failed in 1.55s

[TDA Pipeline] Formatting real pytest failure into repair prompt:
--- REPAIR PROMPT GENERATED ---
System Instruction: Fix the following pytest failure output:
```
F                                                                        [100%]
================================== FAILURES ===================================
_____________________________ test_divide_by_zero _____________________________
test_calculator.py:5: in test_divide_by_zero
    assert divide(10, 0) == 0
           ^^^^^^^^^^^^^
calculator.py:2: in divide
    return a / b
           ^^^^^
E   ZeroDivisionError: division by zero
=========================== short test summary info ===========================
FAILED test_calculator.py::test_divide_by_zero - ZeroDivisionError: division ...
1 failed in 1.55s

```

[TDA Stage 2] Apply the known-good offline repair and rerun pytest.

[TDA Pipeline] Running real pytest suite against proposed code...
[PASS] pytest summary: 1 passed in 0.37s

[TDA Stage 3] Persist the bug as a regression test and rerun pytest.

[Anti-Regression Pipeline] Writing regression safeguard 'test_divide_zero_guard' to the real pytest file...
[PASS] Regression safeguard enforced. pytest summary: 2 passed in 0.47s
[Anti-Regression Pipeline] Total enforced safeguards: 1
[PASS] Temporary pytest scratch directory cleaned up.

============================================================
MODULE 6 DEMO COMPLETE: REAL TDA FEEDBACK LOOP VERIFIED!
============================================================
```

Exit code: 0
