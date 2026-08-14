"""
Minimal HS256 JWT encode/validate using only the Python standard library.

Used by modules 3, 8, and 9 so the course validates real tokens, not
magic strings like "valid-token". The algorithm is the JWT HS256
profile: base64url(header).base64url(payload).HMAC-SHA256.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time
from typing import Any


DEMO_SECRET = "packt-harness-demo-secret"


def b64url_encode(data: bytes) -> str:
    """JWT requires URL-safe base64 without padding."""
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def b64url_decode(data: str) -> bytes:
    """Restore the padding that JWT strips, then decode."""
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def encode_jwt(payload: dict[str, Any], secret: str = DEMO_SECRET) -> str:
    """Sign a payload and return a compact HS256 JWT string."""
    header = {"alg": "HS256", "typ": "JWT"}
    header_part = b64url_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    body_part = b64url_encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    signing_input = f"{header_part}.{body_part}".encode("ascii")
    signature = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha256).digest()
    return f"{header_part}.{body_part}.{b64url_encode(signature)}"


def validate_jwt(token: str, secret: str = DEMO_SECRET) -> dict[str, Any]:
    """
    Verify signature and expiry.

    Return shape matches SPEC.md:
    - valid token: {"valid": True, "user_id": "...", "roles": [...]}
    - expired:     {"valid": False, "error": "EXPIRED"}
    - anything else: {"valid": False, "error": "INVALID"}
    """
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return {"valid": False, "error": "INVALID"}
        header_part, body_part, sig_part = parts
        expected = hmac.new(
            secret.encode("utf-8"),
            f"{header_part}.{body_part}".encode("ascii"),
            hashlib.sha256,
        ).digest()
        actual = b64url_decode(sig_part)
        if not hmac.compare_digest(expected, actual):
            return {"valid": False, "error": "INVALID"}
        payload = json.loads(b64url_decode(body_part))
        if not isinstance(payload, dict):
            return {"valid": False, "error": "INVALID"}
        exp = payload.get("exp")
        if isinstance(exp, (int, float)) and exp < time.time():
            return {"valid": False, "error": "EXPIRED"}
        return {
            "valid": True,
            "user_id": str(payload.get("user_id", "")),
            "roles": list(payload.get("roles", [])),
        }
    except (ValueError, json.JSONDecodeError, UnicodeDecodeError):
        return {"valid": False, "error": "INVALID"}


def auth_validator_source() -> str:
    """Self-contained auth_validator.py text that modules can write to disk."""
    return '''"""HS256 JWT validator. Standard library only."""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time
from typing import Any

DEMO_SECRET = "packt-harness-demo-secret"


def b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def encode_jwt(payload: dict[str, Any], secret: str = DEMO_SECRET) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    header_part = b64url_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    body_part = b64url_encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    signing_input = f"{header_part}.{body_part}".encode("ascii")
    signature = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha256).digest()
    return f"{header_part}.{body_part}.{b64url_encode(signature)}"


def validate_jwt(token: str, secret: str = DEMO_SECRET) -> dict[str, Any]:
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return {"valid": False, "error": "INVALID"}
        header_part, body_part, sig_part = parts
        expected = hmac.new(
            secret.encode("utf-8"),
            f"{header_part}.{body_part}".encode("ascii"),
            hashlib.sha256,
        ).digest()
        actual = b64url_decode(sig_part)
        if not hmac.compare_digest(expected, actual):
            return {"valid": False, "error": "INVALID"}
        payload = json.loads(b64url_decode(body_part))
        if not isinstance(payload, dict):
            return {"valid": False, "error": "INVALID"}
        exp = payload.get("exp")
        if isinstance(exp, (int, float)) and exp < time.time():
            return {"valid": False, "error": "EXPIRED"}
        return {
            "valid": True,
            "user_id": str(payload.get("user_id", "")),
            "roles": list(payload.get("roles", [])),
        }
    except (ValueError, json.JSONDecodeError, UnicodeDecodeError):
        return {"valid": False, "error": "INVALID"}
'''


def test_auth_source() -> str:
    """pytest file that encodes real JWTs and checks the SPEC.md criteria."""
    return '''import time

from auth_validator import encode_jwt, validate_jwt


def test_valid_token():
    token = encode_jwt(
        {"user_id": "123", "roles": ["user"], "exp": time.time() + 3600}
    )
    result = validate_jwt(token)
    assert result["valid"] is True
    assert result["user_id"] == "123"


def test_expired_token():
    token = encode_jwt({"user_id": "123", "exp": time.time() - 30})
    result = validate_jwt(token)
    assert result["valid"] is False
    assert result["error"] == "EXPIRED"


def test_invalid_token():
    result = validate_jwt("not-a-jwt")
    assert result["valid"] is False
    assert result["error"] == "INVALID"
'''
