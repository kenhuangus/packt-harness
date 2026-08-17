---
name: harness-five-step-sop-pipeline
description: Runs an end-to-end 5-step Standard Operating Procedure (SOP) pipeline
  combining Spec First, Sandbox Execution, Guardrails, Pytest Verification, and Unified
  Diff Review. Trigger when executing end-to-end feature development or auditing workflow
  rigor before PR submission.
version: 1.0.0
author: Harness Engineering Team
allowed-tools: Bash, Read, Write, Grep
---

# Harness Five-Step SOP Pipeline

## Overview
Executes the canonical 5-step Standard Operating Procedure (SOP) pipeline (Spec First ➔ Sandbox ➔ Guardrails ➔ Pytest ➔ Diff Review) for bulletproof enterprise code changes.

## Structure & Progressive Disclosure
- `scripts/`: Executable helper and verification tools.
- `references/`: Detailed specifications, guides, and architectural rules.
- `assets/`: Configuration templates and machine-readable schemas.

## When to Use
- When executing complete end-to-end feature development cycles.
- When verifying code modifications against all 5 architectural gates before opening a pull request.
- When automating CI/CD pull request gate audits.

## Required Inputs
- Specification contract (`SPEC.md`).
- Target code and test files.
- Pipeline configuration (`assets/pipeline_config.json`).

## Instructions
Run all commands from the repository root.
1. Gate 1 (Spec First): Parse `SPEC.md` and validate scope bounds.
2. Gate 2 (Sandbox Execution): Constrain tool writes strictly to `allowed_files`.
3. Gate 3 (Guardrails): Run AST syntax verification and regex secret scanning on all diffs.
4. Gate 4 (Pytest): Run test suite via subprocess asserting returncode == 0.
5. Gate 5 (Human Sign-off): Produce clean unified diff patch for human review.
6. Run `python .claude/skills/harness-five-step-sop-pipeline/scripts/run_sop_pipeline.py` to execute all 5 gates sequentially.
7. Consult `references/five-step-sop-checklist.md` for gate requirements.

## Output Format
Always format output adhering to this structure:
```json
{
  "pipeline": "5-Step Production SOP",
  "gates": {
    "1_spec_first": "PASS",
    "2_sandbox": "PASS",
    "3_guardrails": "PASS",
    "4_pytest": "PASS",
    "5_diff_review": "READY"
  },
  "status": "READY_FOR_MERGE"
}
```

## Examples
### Running 5-Step Pipeline
```python
from scripts.run_sop_pipeline import main

main()  # Evaluates all 5 gates and prints pass/fail matrix
```

## Key Implementation Links (GitHub)
- [https://github.com/kenhuangus/packt-harness/tree/main/.claude/skills/harness-five-step-sop-pipeline/](https://github.com/kenhuangus/packt-harness/tree/main/.claude/skills/harness-five-step-sop-pipeline/)
- [https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-five-step-sop-pipeline/SKILL.md](https://github.com/kenhuangus/packt-harness/blob/main/.claude/skills/harness-five-step-sop-pipeline/SKILL.md)
- [https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_09_practical_workflow_pattern/](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_09_practical_workflow_pattern/)
