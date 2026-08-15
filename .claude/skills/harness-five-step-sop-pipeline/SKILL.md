---
name: harness-five-step-sop-pipeline
description: Runs an end-to-end 5-step Standard Operating Procedure (SOP) pipeline combining Spec First (1), Constrained Sandbox Execution (2), Deterministic AST/Secret Guardrails (3), Subprocess Pytest Verification (4), and Unified Diff Human Review (5). Use when executing end-to-end feature pipelines or auditing workflow rigor before PR submission.
allowed-tools: Bash, Read, Write, Glob, Grep
---

# Five-Step Production SOP Pipeline (Module 9 Skill)

This skill executes the canonical end-to-end harness development workflow: Spec First ➔ Sandbox Execution ➔ Guardrails ➔ Test Verification ➔ Human Review.

## When to Use
- When developing any complete feature or bug fix with full verification.
- When orchestrating all 5 harness control gates in a single automated pipeline.
- When generating standard unified diffs for engineer review before pull request creation.

## How to Use
1. **Pipeline Execution Sequence**:
   ```python
   # Step 1: Spec First
   allowed_files, non_goals = parse_spec("SPEC.md")

   with tempfile.TemporaryDirectory() as temp:
       workspace = Path(temp)

       # Step 2: Constrained Execution
       enforcer = ScopeEnforcer(workspace, allowed_files)
       enforcer.attempt_write("auth_validator.py", code)

       # Step 3: Deterministic Checks
       engine = GuardrailsEngine(workspace)
       engine.audit_ast_and_secrets("auth_validator.py", code)

       # Step 4: Test Verification
       subprocess.run([sys.executable, "-m", "pytest", "tests/test_auth.py", "-q"], cwd=workspace, check=True)

       # Step 5: Human Review & Diff
       diff = difflib.unified_diff(original.splitlines(), code.splitlines())
   ```

2. **Verification**:
   ```bash
   python course_implementation/module_09_practical_workflow_pattern/five_step_sop_pipeline.py
   ```

## Key Files & Implementation
- `course_implementation/module_09_practical_workflow_pattern/five_step_sop_pipeline.py`
- `course_implementation/module_09_practical_workflow_pattern/SPEC.md`
