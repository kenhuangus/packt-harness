"""HS256 JWT validator. Standard library only."""
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
