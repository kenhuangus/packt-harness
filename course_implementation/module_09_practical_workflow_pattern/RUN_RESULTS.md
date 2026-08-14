# Module 9 Run Results

Captured 2026-08-14 from a real process. The SOP wrote a real HS256 JWT
module, rejected `database.py`, ran pytest (3 passed), and copied the
workspace to `output\`.

```text
> C:\Users\kenhu\AppData\Local\Programs\Python\Python313\python.exe C:\Users\kenhu\packt-harness\course_implementation\module_09_practical_workflow_pattern\five_step_sop_pipeline.py
  [PASS] SPEC.md parsed: read C:\Users\kenhu\packt-harness\course_implementation\module_03_spec_driven_development\SPEC.md
  [PASS] In-scope edit: Wrote allowed file 'auth_validator.py'.
  [PASS] Out-of-scope edit rejected: 'database.py' is not in the allowed file scope. File created: False.
    3 passed in 0.20s
  [PASS] Pytest suite: return code 0; 3 passed, 0 failed.
  [PASS] Review diff generated: 58 implementation lines shown from the temporary workspace.
  [OUTPUT] copied workspace to C:\Users\kenhu\packt-harness\course_implementation\module_09_practical_workflow_pattern\output
```

Exit code: 0
