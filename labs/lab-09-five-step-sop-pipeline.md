# Lab 09 — Five-Step SOP Pipeline

**Skill:** `harness-five-step-sop-pipeline`  
**Module:** [module_09_practical_workflow_pattern](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_09_practical_workflow_pattern)  
**Time:** 45 minutes

## What you will end up with
You will have one full run of the five-gate pipeline and a checklist you can reuse before every PR in your own repository.

## Before you start
Have one small feature branch in your own repo ready for evaluation.  
This module script does not require live generation in this environment.

## Steps
1. Run the five-step wrapper script from this repo.

```bash
cd /path/to/packt-harness
python .claude/skills/harness-five-step-sop-pipeline/scripts/run_sop_pipeline.py
```

2. Read the five gate outcomes in the output and copy them to your notes.

```bash
printf "lab09_gates_recorded: yes\n" >> labs/lab-notes.txt
```

3. In your own repo, create a pre-PR checklist file with the same five gates.

```bash
cd /path/to/your-repo
cat > SOP_CHECKLIST.md <<'EOF'
1. Spec First
2. Sandbox Execution
3. Guardrails
4. Pytest
5. Human Diff Review
EOF
```

4. Run your project tests as gate 4.

```bash
pytest -q --tb=short
```

## Expected output
Real captured output:

```text
[STEP 1: SPEC FIRST] Parsing SPEC.md requirements...
[STEP 2: CONSTRAINED EXECUTION] Enforcing the parsed allowed-file scope...
[STEP 3: DETERMINISTIC CHECKS] Running module 4 guardrails...
[STEP 4: TEST VERIFICATION] Running a real temporary pytest suite...
[PASS] Pytest suite: return code 0; 3 passed, 0 failed.
[STEP 5: HUMAN REVIEW] Showing the implementation actually produced...
PIPELINE COMPLETE: ALL REPORTED CHECKS EXECUTED AND PASSED
```

## Break it on purpose
Intentionally change a file outside the allowed spec scope and rerun your gates.

```bash
printf "# out of scope change\n" >> database.py
```

The SOP process should fail at scope or guardrail checks before merge.

## You are done when
- You ran all five gates at least once.
- You recorded each gate outcome in notes.
- You can show a failing out-of-scope case that blocks completion.

## If it goes wrong
- If wrapper script path fails, run it from `/path/to/packt-harness`.
- If your own repo has no pytest suite, run the equivalent project test command and document it.
- If gates are skipped, enforce them in your PR template before continuing.
