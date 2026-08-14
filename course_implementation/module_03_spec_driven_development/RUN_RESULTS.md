# Module 3 Run Results

Captured 2026-08-14 from a real process. A real HS256 JWT module was
written, `database.py` was not created, pytest reported 3 passed, and
`validate_jwt` was called on live tokens.

```text
> C:\Users\kenhu\AppData\Local\Programs\Python\Python313\python.exe C:\Users\kenhu\packt-harness\course_implementation\module_03_spec_driven_development\spec_driven_verifier.py
[Spec Verifier] Parsed SPEC.md:
  Allowed Files Scope: ['auth_validator.py', 'tests/test_auth.py']
  [PASS] Wrote ...\output\auth_validator.py (2201 bytes).
  [BLOCKED] SCOPE VIOLATION: 'database.py'
  [BLOCKED] NON-GOAL VIOLATION: diff mentions database or OAuth2 refresh logic.
  [PASS] Wrote ...\output\tests\test_auth.py (673 bytes).
3 passed in 0.23s
[Live call] valid token -> {'valid': True, 'user_id': '123', 'roles': ['user']}
[Live call] expired token -> {'valid': False, 'error': 'EXPIRED'}
[OUTPUT] C:\Users\kenhu\packt-harness\course_implementation\module_03_spec_driven_development\output\run_evidence.json
```

Exit code: 0
