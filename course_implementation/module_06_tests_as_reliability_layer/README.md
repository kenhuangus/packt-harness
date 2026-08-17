# Module 6: Tests as the Reliability Layer

## What this module teaches

An agent that cannot see a real traceback cannot repair a real failure.
This module runs **pytest as a subprocess**, captures stdout/stderr, and
feeds that text into a repair loop. Nothing is faked as `[PASS]`.

The Test-Driven Agent (TDA) loop here has three stages:

1. **Prove red.** Write `def divide(a, b): return a / b` and a test that
   asserts `divide(10, 0) == 0`. pytest exits 1 with `ZeroDivisionError`.
2. **Repair and prove green.** Send that captured traceback to the live
   model, write back whatever code it returns, and rerun pytest. A reply
   that is simulated, unparseable, or still red does not count: the loop
   feeds the new failure back and retries, up to three attempts. If none
   pass, the module exits 1 rather than reporting a repair it did not get.
3. **Keep the bug.** Append `test_divide_zero_guard` to the same test
   file and rerun. pytest prints `2 passed`.

That third step is the anti-regression rule: every agent bug becomes a
permanent test.

Scratch files live in a local TemporaryDirectory next to the script
(prefix `tda_reliability_`) and are deleted before the process exits.
They are not committed.

## Files

| Path | Role |
| --- | --- |
| [tda_reliability_pipeline.py](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_06_tests_as_reliability_layer/tda_reliability_pipeline.py) | TDA loop |
| [RUN_RESULTS.md](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_06_tests_as_reliability_layer/RUN_RESULTS.md) | Last captured stdout |

No committed calculator or test file. They exist only inside the temp dir.

## How to run

Run from the repository root, using the project virtualenv
(`python -m venv .venv` then `.venv\Scripts\python.exe -m pip install -e .`
— see the [root README](../../README.md#setup)):

```powershell
python course_implementation/module_06_tests_as_reliability_layer/tda_reliability_pipeline.py
```

Requires pytest on that interpreter. This machine used pytest 9.1.1.
If pytest is missing the script prints `[SKIPPED]` and exits 0.

Stage 2 needs the local model at `http://127.0.0.1:8000/v1`. There is no
offline repair to fall back on: with the model unreachable the run fails
with an actionable error, and with `HARNESS_ALLOW_SIMULATED_LLM=1` the
simulated reply is rejected and the module exits 1.

## Output file and evidence

- **Stdout** (exit 0), including the real pytest traceback.
- **Recorded copy:** [RUN_RESULTS.md](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_06_tests_as_reliability_layer/RUN_RESULTS.md)

Captured on this machine, 2026-08-17:

```text
[PASS] pytest availability check: pytest 9.1.1

[TDA Stage 1] Prove the proposed implementation fails a real test.
[FAIL] pytest exited with return code 1; captured failure output follows:
E   ZeroDivisionError: division by zero
FAILED test_calculator.py::test_divide_by_zero - ZeroDivisionError: division ...
1 failed in 2.88s

[TDA Stage 2] Send the real traceback to the model and rerun pytest, up to 3 attempts.

[Repair Attempt 1/3]
--- REPAIR PROMPT GENERATED ---
System Instruction: Fix the following pytest failure output:
E   ZeroDivisionError: division by zero
[Repair Proposed] 66 chars of model-authored code.
[PASS] pytest summary: 1 passed in 0.88s
[PASS] Model repair verified by pytest on attempt 1.

[TDA Stage 3] Persist the bug as a regression test and rerun pytest.
[PASS] Regression safeguard enforced. pytest summary: 2 passed in 0.92s
[PASS] Temporary pytest scratch directory cleaned up.
```

Stage 1's `[FAIL]` is expected. It is the evidence the loop started from
a real red test.

## Annotated code

```python
class TDAReliabilityPipeline:
    """
    Stage 1 writes a divide() that raises ZeroDivisionError and captures
    the traceback. Stage 2 sends that traceback to the live model and
    reruns pytest against whatever it returns, retrying with each new
    failure until a repair passes or the attempts run out.
    Stage 3 appends a permanent regression test and reruns again.
    """

    def run_test_suite(self, code_under_test):
        # Write calculator.py, run pytest as a subprocess, return
        # pass/fail plus the exact captured output.

    def format_fix_prompt(self, traceback_str):
        # The repair prompt is the real pytest text, not a summary.

    def request_repair(self, traceback_str):
        # Ask the live model. Reject simulated replies, ast.parse the
        # result, and return None on any failure so the caller retries
        # instead of falling back to a canned answer.

    def register_anti_regression_test(self, bug_name, test_code):
        # Append to the live test file, rerun, keep the test only if it passes.
```
