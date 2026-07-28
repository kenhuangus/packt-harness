# Module 9 Run Results

Captured from an actual run.

```text
> python five_step_sop_pipeline.py
============================================================
MODULE 9 DEMO: 5-STEP SOP PIPELINE FOR 'User Auth Token Validator'
============================================================

[STEP 1: SPEC FIRST] Parsing SPEC.md requirements...
  [PASS] SPEC.md parsed: read C:\Users\kenhu\packt\harness\course_implementation\module_03_spec_driven_development\SPEC.md
  Allowed file scope: ['auth_validator.py', 'tests/test_auth.py']
  Explicit non-goals: ['Do NOT modify existing database connection pools.', 'Do NOT implement OAuth2 refresh token rotation in this iteration.']

[STEP 2: CONSTRAINED EXECUTION] Enforcing the parsed allowed-file scope...
  [PASS] In-scope edit: Wrote allowed file 'auth_validator.py'.
  [PASS] Out-of-scope edit rejected: 'database.py' is not in the allowed file scope. File created: False.

[STEP 3: DETERMINISTIC CHECKS] Running module 4 guardrails...
  [PASS] AST syntax and generated-code secret scan: AST syntax valid. Zero secret leaks detected.
  [PASS] Secret-bearing code rejected: SECURITY CRITICAL: Hardcoded API secret key detected!
  [PASS] Dangerous shell command intercepted: CRITICAL SECURITY BLOCK: Command matches dangerous pattern 'rm\s+-rf'

[STEP 4: TEST VERIFICATION] Running a real temporary pytest suite...
    ...                                                                      [100%]
    3 passed in 0.41s
  [PASS] Pytest suite: return code 0; 3 passed, 0 failed.

[STEP 5: HUMAN REVIEW] Showing the implementation actually produced...
  --- /dev/null
  +++ auth_validator.py
  @@ -0,0 +1,8 @@
  +"""Token validation constrained by the feature specification."""
  +
  +def validate_jwt(token: str) -> dict:
  +    if token == "valid-token":
  +        return {"valid": True, "user_id": "123"}
  +    if token == "expired-token":
  +        return {"valid": False, "error": "EXPIRED"}
  +    return {"valid": False, "error": "INVALID"}
  [PASS] Review diff generated: 8 implementation lines shown from the temporary workspace.
  Human approval and any PR merge are out-of-band; this pipeline did not create or merge a PR.

============================================================
PIPELINE COMPLETE: ALL REPORTED CHECKS EXECUTED AND PASSED
============================================================
```

Exit code: 0
