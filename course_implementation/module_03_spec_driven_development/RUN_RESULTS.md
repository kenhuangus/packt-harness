# Module 3 Run Results

Captured from an actual run.

```text
> python spec_driven_verifier.py
============================================================
MODULE 3 DEMO: SPEC-DRIVEN DEVELOPMENT VERIFIER 
============================================================
[LLM Client] Configured LLM client with model 'openai:nvidia/Qwen3.6-35B-A3B-NVFP4' | Endpoint: 'http://127.0.0.1:8000/v1'
[Spec Verifier] Parsed SPEC.md:
  Allowed Files Scope: ['auth_validator.py']
  Explicit Non-Goals: ['Do NOT modify existing database connection pools.', 'Do NOT implement OAuth2 refresh token rotation in this iteration.']

[Spec Verifier] Auditing proposed modification to 'auth_validator.py'...
  ✓ Spec Compliance Verified: Scope & Non-Goals satisfied.

[Spec Verifier] Auditing proposed modification to 'database.py'...
  ❌ SCOPE VIOLATION: 'database.py' is outside allowed spec scope ['auth_validator.py']!

[Spec Verifier] Auditing proposed modification to 'auth_validator.py'...
  ❌ NON-GOAL VIOLATION: Code diff attempts to modify database connection logic!

============================================================
MODULE 3 DEMO COMPLETE: Spec Verifier Enforced Target Boundaries!
============================================================
```

Exit code: 0
