# Module 9: Practical Workflow SOP

## What this module teaches

The earlier modules are pieces. This one runs them in order as a five-step
standard operating procedure for one feature: User Auth Token Validator.

| Step | Name | What actually runs |
| --- | --- | --- |
| 1 | Spec first | Parse [SPEC.md](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_03_spec_driven_development/SPEC.md) |
| 2 | Constrained execution | Write `auth_validator.py`; reject `database.py` |
| 3 | Deterministic checks | Reuse module 4's `GuardrailsEngine` (AST, secret scan, `rm -rf`) |
| 4 | Test verification | Real pytest: 3 tests, 3 passed |
| 5 | Human review | Print a unified diff. No PR is created or merged. |

The SOP writes a real HS256 JWT module (same implementation as module 3),
not the old `"valid-token"` string table. The temp workspace is copied to
[course_implementation/module_09_practical_workflow_pattern/output/](https://github.com/kenhuangus/packt-harness/tree/main/course_implementation/module_09_practical_workflow_pattern/output/)
before it is deleted.

This pipeline imports
[guardrails_engine.py](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_04_guardrails_and_hooks/guardrails_engine.py)
by inserting that directory on `sys.path`. It does not copy the engine.

## Files

| Path | Role |
| --- | --- |
| [five_step_sop_pipeline.py](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_09_practical_workflow_pattern/five_step_sop_pipeline.py) | The SOP |
| [SPEC.md](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_03_spec_driven_development/SPEC.md) | Spec consumed in step 1 |
| [guardrails_engine.py](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_04_guardrails_and_hooks/guardrails_engine.py) | Engine reused in step 3 |
| [RUN_RESULTS.md](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_09_practical_workflow_pattern/RUN_RESULTS.md) | Last captured stdout |

## How to run

Run from the repository root:

```powershell
python course_implementation/module_09_practical_workflow_pattern/five_step_sop_pipeline.py
```

Requires pytest on that interpreter.

## Output file and evidence

- **Stdout** (exit 0), including the 8-line review diff.
- **Recorded copy:** [RUN_RESULTS.md](https://github.com/kenhuangus/packt-harness/blob/main/course_implementation/module_09_practical_workflow_pattern/RUN_RESULTS.md)

Captured on this machine, 2026-08-14:

```text
[STEP 1: SPEC FIRST] Parsing SPEC.md requirements...
  [PASS] SPEC.md parsed: read C:\Users\kenhu\packt-harness\course_implementation\module_03_spec_driven_development\SPEC.md
  Allowed file scope: ['auth_validator.py', 'tests/test_auth.py']

[STEP 2: CONSTRAINED EXECUTION] Enforcing the parsed allowed-file scope...
  [PASS] In-scope edit: Wrote allowed file 'auth_validator.py'.
  [PASS] Out-of-scope edit rejected: 'database.py' is not in the allowed file scope. File created: False.

[STEP 3: DETERMINISTIC CHECKS] Running module 4 guardrails...
  [PASS] AST syntax and generated-code secret scan: AST syntax valid. Zero secret leaks detected.
  [PASS] Secret-bearing code rejected: SECURITY CRITICAL: Hardcoded API secret key detected!
  [PASS] Dangerous shell command intercepted: CRITICAL SECURITY BLOCK: Command matches dangerous pattern 'rm\s+-rf'

[STEP 4: TEST VERIFICATION] Running a real temporary pytest suite...
    3 passed in 0.49s
  [PASS] Pytest suite: return code 0; 3 passed, 0 failed.

[STEP 5: HUMAN REVIEW] Showing the implementation actually produced...
  --- /dev/null
  +++ auth_validator.py
  +def validate_jwt(token: str) -> dict:
  ...
  [PASS] Review diff generated: 8 implementation lines shown from the temporary workspace.
  Human approval and any PR merge are out-of-band; this pipeline did not create or merge a PR.
```

## Annotated code

```python
def parse_spec(spec_path):
    """
    Step 1: Allowed files are the backtick-quoted names on the Allowed
    Files line. Non-goals are the dash list under heading 3. Either
    field empty is a hard error.
    """

class ScopeEnforcer:
    """
    Step 2: allow writes only to the exact relative paths in the spec.
    database.py is rejected even though the workspace is writable.
    """

class FiveStepSOPPipeline:
    """
    Temporary files are always deleted. Human PR merge is printed as
    out-of-band so the demo does not claim it opened a pull request.
    """

    def run_pipeline(self, feature_name):
        # Step 3 calls GuardrailsEngine from module 4.
        # Step 4 runs: python -m pytest tests/test_auth.py -q
        # Step 5 prints difflib.unified_diff of the produced file.
```
