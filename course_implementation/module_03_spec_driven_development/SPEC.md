# FEATURE SPECIFICATION: User Auth Token Validator

## 1. Objective
Implement a lightweight JWT token validation module for user authentication.

## 2. Allowed Modification Scope
- Allowed Files: `auth_validator.py`, `tests/test_auth.py`
- Forbidden Files: `database.py`, `config/settings.py`

## 3. Explicit Non-Goals
- Do NOT modify existing database connection pools.
- Do NOT implement OAuth2 refresh token rotation in this iteration.

## 4. Input / Output Data Schemas
```json
{
  "token": "string (JWT format)",
  "return": {
    "valid": "boolean",
    "user_id": "string",
    "roles": "array of strings"
  }
}
```

## 5. Acceptance Criteria
- [ ] AC-01: `auth_validator.py` exports `validate_jwt(token: str) -> dict`.
- [ ] AC-02: Returns `{"valid": True, "user_id": "123"}` for valid tokens.
- [ ] AC-03: Returns `{"valid": False, "error": "EXPIRED"}` for expired tokens.
- [ ] AC-04: Test coverage must be 100% in `tests/test_auth.py`.
