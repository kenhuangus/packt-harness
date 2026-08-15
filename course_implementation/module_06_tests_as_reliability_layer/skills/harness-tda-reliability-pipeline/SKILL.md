---
name: harness-tda-reliability-pipeline
description: Executes deterministic test-driven agent (TDA) feedback loops via isolated pytest subprocesses, captures exact failure tracebacks into repair prompts, and appends anti-regression tests to prevent feature breakage. Use when running automated code repair, verifying test assertions, or preventing regressions.
allowed-tools: Bash, Read, Write, Glob, Grep
---

# Test-Driven Agent (TDA) & Anti-Regression Pipeline (Module 6 Skill)

This skill replaces unverified agent claims with deterministic `pytest` subprocess execution, capturing exact traceback evidence directly into repair prompts and appending regression tests to lock in fixes.

## When to Use
- When generating code to satisfy failing unit/integration tests.
- When capturing real compiler and test failure tracebacks (`ZeroDivisionError`, `AssertionError`) for repair prompt feedback.
- When permanently persisting every discovered bug as an anti-regression test in the test suite.

## How to Use
1. **Execute Pytest Subprocess**:
   ```python
   result = subprocess.run(
       [sys.executable, "-m", "pytest", test_file, "-q", "--tb=short", "-p", "no:cacheprovider"],
       cwd=scratch_dir, capture_output=True, text=True, encoding="utf-8"
   )
   if result.returncode != 0:
       traceback_feedback = result.stdout + (result.stderr or "")
       prompt = f"System Instruction: Fix the following pytest failure:\n```\n{traceback_feedback}\n```"
   ```

2. **Append Anti-Regression Safeguards**:
   ```python
   with open(test_file, "a", encoding="utf-8") as handle:
       handle.write(f"\n\ndef test_{bug_name}_regression():\n    assert ...\n")
   ```

3. **Verification**:
   ```bash
   python course_implementation/module_06_tests_as_reliability_layer/tda_reliability_pipeline.py
   ```

## Key Files & Implementation (GitHub Links)
- [https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_06_tests_as_reliability_layer/tda_reliability_pipeline.py](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_06_tests_as_reliability_layer/tda_reliability_pipeline.py)
- [https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-tda-reliability-pipeline/SKILL.md](https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-tda-reliability-pipeline/SKILL.md)
