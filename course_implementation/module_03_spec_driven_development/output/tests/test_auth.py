import time

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
