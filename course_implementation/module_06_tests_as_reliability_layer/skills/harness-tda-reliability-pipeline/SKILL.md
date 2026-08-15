---
name: harness-tda-reliability-pipeline
description: Executes Test-Driven Agent (TDA) feedback loops via isolated pytest subprocesses,
  extracts exact failure tracebacks into repair prompts, and appends anti-regression
  tests to prevent recurring bugs. Trigger when running automated code repair, running
  test assertions, or preventing regression failures.
version: 1.0.0
author: Harness Engineering Team
allowed-tools: Bash, Read, Write, Glob, Grep
---

# Harness TDA Reliability Pipeline

## Overview
Executes deterministic pytest feedback loops in isolated subprocesses, extracting exact failure tracebacks into repair context and locking fixes with anti-regression test suites.

## Structure & Progressive Disclosure
- `scripts/`: Executable helper and verification tools.
- `references/`: Detailed specifications, guides, and architectural rules.
- `assets/`: Configuration templates and machine-readable schemas.

## When to Use
- When implementing code using Test-Driven Agent workflows (Red ➔ Green ➔ Refactor).
- When executing real `pytest` test suites and asserting returncode == 0.
- When capturing concise tracebacks to guide model repair without token bloat.
- When locking in bugfixes with anti-regression test cases.

## Required Inputs
- Test file path (e.g. `tests/test_feature.py`).
- Target implementation source file.
- Maximum test-and-repair iterations (default: 3).

## Instructions
1. Execute `python scripts/run_tda_loop.py` running `pytest -q --tb=short -p no:cacheprovider`.
2. Capture stdout and stderr; evaluate process exit code.
3. If exit code == 0, mark test loop as SUCCESS.
4. If exit code != 0, extract the concise failure traceback and supply it to the model for targeted repair.
5. Lock the passing assertion into `tests/test_regression.py` to prevent regressions.
6. Consult `references/tda-feedback-guide.md` for prompt formatting guidance.

## Output Format
Always format output adhering to this structure:
```json
{
  "exit_code": 0,
  "passed": true,
  "tests_run": 8,
  "failures": 0,
  "traceback": null
}
```

## Examples
### Running Pytest Subprocess
```python
import subprocess
import sys

res = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-q", "--tb=short"], capture_output=True, text=True)
print(f"Pytest Exit Code: {res.returncode}")
```

## Key Implementation Links (GitHub)
- [https://github.com/kenhuangus/packt-harness/tree/main/.claude/skills/harness-tda-reliability-pipeline/](https://github.com/kenhuangus/packt-harness/tree/main/.claude/skills/harness-tda-reliability-pipeline/)
- [https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-tda-reliability-pipeline/SKILL.md](https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-tda-reliability-pipeline/SKILL.md)
- [https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_06_tests_as_reliability_layer/](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_06_tests_as_reliability_layer/)
