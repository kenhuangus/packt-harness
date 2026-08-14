# Module 3: Spec-Driven Development

## What this module teaches

A prompt is not a contract. Spec-Driven Development (SDD) puts a
machine-checkable `SPEC.md` in front of the agent and rejects work that
leaves the declared scope.

This module's spec is
`C:\Users\kenhu\packt-harness\course_implementation\module_03_spec_driven_development\SPEC.md`.
It names:

- **Allowed files:** `auth_validator.py`, `tests/test_auth.py`
- **Non-goals:** do not touch the database pool; do not implement OAuth2 refresh rotation
- **Acceptance criteria:** `validate_jwt(token) -> dict` with explicit valid / expired shapes

The verifier does two checks only, on purpose:

1. The target file's basename must be in the allowed list.
2. The proposed diff must not mention `database` or `connect_db`.

Three cases are run:

| Case | File | Diff | Result |
| --- | --- | --- | --- |
| In scope | `auth_validator.py` | `validate_jwt` only | accepted |
| Wrong file | `database.py` | anything | `SCOPE VIOLATION` |
| In-scope leak | `auth_validator.py` | imports `database.connect_db` | `NON-GOAL VIOLATION` |

The parser currently takes the first backtick-quoted name after
`Allowed Files:`, so the printed scope is `['auth_validator.py']`.
Module 9 parses the same spec more completely (both allowed files).
That difference is real; do not paper over it.

## Files

| Path | Role |
| --- | --- |
| `C:\Users\kenhu\packt-harness\course_implementation\module_03_spec_driven_development\SPEC.md` | The contract |
| `C:\Users\kenhu\packt-harness\course_implementation\module_03_spec_driven_development\spec_driven_verifier.py` | Parser + auditor |
| `C:\Users\kenhu\packt-harness\course_implementation\module_03_spec_driven_development\RUN_RESULTS.md` | Last captured stdout |

No files are written. Evidence is stdout.

## How to run

```powershell
C:\Users\kenhu\AppData\Local\Programs\Python\Python313\python.exe C:\Users\kenhu\packt-harness\course_implementation\module_03_spec_driven_development\spec_driven_verifier.py
```

## Output file and evidence

- **Stdout** (exit 0).
- **Recorded copy:** `C:\Users\kenhu\packt-harness\course_implementation\module_03_spec_driven_development\RUN_RESULTS.md`

Captured on this machine, 2026-08-14:

```text
[Spec Verifier] Parsed SPEC.md:
  Allowed Files Scope: ['auth_validator.py']
  Explicit Non-Goals: ['Do NOT modify existing database connection pools.', 'Do NOT implement OAuth2 refresh token rotation in this iteration.']

[Spec Verifier] Auditing proposed modification to 'auth_validator.py'...
  ✓ Spec Compliance Verified: Scope & Non-Goals satisfied.

[Spec Verifier] Auditing proposed modification to 'database.py'...
  ❌ SCOPE VIOLATION: 'database.py' is outside allowed spec scope ['auth_validator.py']!

[Spec Verifier] Auditing proposed modification to 'auth_validator.py'...
  ❌ NON-GOAL VIOLATION: Code diff attempts to modify database connection logic!
```

## Annotated code

```python
class SpecVerifier:
    """
    Two rules only:
    1. The target file's basename must appear in the Allowed Files list.
    2. The diff text must not mention database / connect_db, which the
       spec lists as explicit non-goals.
    """

    def parse_spec(self):
        # First backtick-quoted name after "Allowed Files:" becomes scope.
        # Everything between "## 3. Explicit Non-Goals" and the next H2
        # becomes the non-goal list.

    def verify_proposed_diff(self, target_file, code_diff):
        # Scope gate: database.py fails here even before content is read.
        # Non-goal gate: an in-scope file can still fail if it touches DB.
```
