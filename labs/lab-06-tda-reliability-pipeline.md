# Lab 06 — TDA Reliability Pipeline

**Skill:** `harness-tda-reliability-pipeline`  
**Module:** [module_06_tests_as_reliability_layer](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_06_tests_as_reliability_layer)  
**Time:** 45 minutes

## What you will end up with
You will have one failing test trace converted into a repair prompt and one anti-regression test that keeps the fix from regressing.

## Before you start
Run this lab in your own repository where you already have a small test target you can intentionally break and fix.  
This lab does not require live generation for the script itself. The full module demonstration does not need the local model endpoint either.

## Steps
1. Run the reference TDA script to confirm it is available.

```bash
cd /path/to/packt-harness
python .claude/skills/harness-tda-reliability-pipeline/scripts/run_tda_loop.py
```

2. Run the full module pipeline once to see fail -> repair prompt -> pass -> anti-regression flow.

```bash
python course_implementation/module_06_tests_as_reliability_layer/tda_reliability_pipeline.py
```

3. In your own repo, run a focused failing test and capture the traceback.

```bash
cd /path/to/your-repo
pytest -q --tb=short -p no:cacheprovider
```

4. Add one regression test for the bug you fixed and rerun tests.

```bash
pytest -q --tb=short -p no:cacheprovider
```

## Expected output
Real captured output:

```text
[FAIL] pytest exited with return code 1; captured failure output follows:
...
FAILED test_calculator.py::test_divide_by_zero - ZeroDivisionError: division ...
1 failed in 3.36s
...
[PASS] Regression safeguard enforced. pytest summary: 2 passed in 0.36s
```

Your filenames and timings will differ in your own repo, but you should see one real fail and then a clean pass after adding the regression check.

## Break it on purpose
Delete or comment out the regression test and rerun pytest.

```bash
pytest -q --tb=short -p no:cacheprovider
```

The pipeline should fail again on the same behavior you had previously fixed.

## You are done when
- You captured one real failing traceback before the fix.
- You reran tests and got a clean pass after the fix.
- You added at least one anti-regression assertion that would fail without the fix.

## If it goes wrong
- If pytest is missing, install it in your active environment.
- If no failure appears, make the test stricter so it catches the bug.
- If results differ between runs, clear test state and rerun with the exact same command.
