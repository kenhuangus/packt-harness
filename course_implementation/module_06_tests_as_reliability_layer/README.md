# Module 6: Tests as the Reliability Layer

## What this module teaches

An agent that cannot see a real traceback cannot repair a real failure.
This module runs **pytest as a subprocess**, captures stdout/stderr, and
feeds that text into a repair loop. Nothing is faked as `[PASS]`.

The Test-Driven Agent (TDA) loop here has three stages:

1. **Prove red.** Write `def divide(a, b): return a / b` and a test that
   asserts `divide(10, 0) == 0`. pytest exits 1 with `ZeroDivisionError`.
2. **Repair and prove green.** Write the zero-guard and rerun. pytest
   prints `1 passed`.
3. **Keep the bug.** Append `test_divide_zero_guard` to the same test
   file and rerun. pytest prints `2 passed`.

That third step is the anti-regression rule: every agent bug becomes a
permanent test.

Scratch files live under
`C:\Users\kenhu\packt-harness\course_implementation\module_06_tests_as_reliability_layer\tda_reliability_*`
and are deleted before the process exits. If cleanup fails, the leftover
directory is visible next to the script.

## Files

| Path | Role |
| --- | --- |
| `C:\Users\kenhu\packt-harness\course_implementation\module_06_tests_as_reliability_layer\tda_reliability_pipeline.py` | TDA loop |
| `C:\Users\kenhu\packt-harness\course_implementation\module_06_tests_as_reliability_layer\RUN_RESULTS.md` | Last captured stdout |

No committed calculator or test file. They exist only inside the temp dir.

## How to run

```powershell
C:\Users\kenhu\AppData\Local\Programs\Python\Python313\python.exe C:\Users\kenhu\packt-harness\course_implementation\module_06_tests_as_reliability_layer\tda_reliability_pipeline.py
```

Requires pytest on that interpreter. This machine used pytest 9.1.1.
If pytest is missing the script prints `[SKIPPED]` and exits 0.

## Output file and evidence

- **Stdout** (exit 0), including the real pytest traceback.
- **Recorded copy:** `C:\Users\kenhu\packt-harness\course_implementation\module_06_tests_as_reliability_layer\RUN_RESULTS.md`

Captured on this machine, 2026-08-14:

```text
[PASS] pytest availability check: pytest 9.1.1

[TDA Stage 1] Prove the proposed implementation fails a real test.
[FAIL] pytest exited with return code 1; captured failure output follows:
E   ZeroDivisionError: division by zero
FAILED test_calculator.py::test_divide_by_zero
1 failed in 0.60s

[TDA Stage 2] Apply the known-good offline repair and rerun pytest.
[PASS] pytest summary: 1 passed in 0.35s

[TDA Stage 3] Persist the bug as a regression test and rerun pytest.
[PASS] Regression safeguard enforced. pytest summary: 2 passed in 0.28s
[PASS] Temporary pytest scratch directory cleaned up.
```

Stage 1's `[FAIL]` is expected. It is the evidence the loop started from
a real red test.

## Annotated code

```python
class TDAReliabilityPipeline:
    """
    Stage 1 writes a divide() that raises ZeroDivisionError and captures
    the traceback. Stage 2 writes the known-good repair and reruns.
    Stage 3 appends a permanent regression test and reruns again.
    """

    def run_test_suite(self, code_under_test):
        # Write calculator.py, run pytest as a subprocess, return
        # pass/fail plus the exact captured output.

    def format_fix_prompt(self, traceback_str):
        # The repair prompt is the real pytest text, not a summary.

    def register_anti_regression_test(self, bug_name, test_code):
        # Append to the live test file, rerun, keep the test only if it passes.
```
