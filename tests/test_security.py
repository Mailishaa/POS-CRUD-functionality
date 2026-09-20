from datetime import timedelta

import jwt
import pytest

from fastapi import HTTPException

from core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
    SECRET_KEY,
    ALGORITHM,
)


def test_hash_password():

    password = "testpassword"

    hashed = hash_password(password)

    assert hashed != password

    assert verify_password(
        password,
        hashed,
    ) is True

    assert verify_password(
        "wrongpassword",
        hashed,
    ) is False


def test_hash_password_is_randomized():

    password = "testpassword"

    hashed1 = hash_password(password)
    hashed2 = hash_password(password)

    assert hashed1 != hashed2

    assert verify_password(password, hashed1)
    assert verify_password(password, hashed2)


def test_verify_password_with_empty_hash():

    assert verify_password(
        "anypassword",
        "",
    ) is False

    assert verify_password(
        "anypassword",
        None,
    ) is False


def test_hash_empty_password():

    hashed = hash_password("")

    assert verify_password(
        "",
        hashed,
    ) is True

    assert verify_password(
        "notempty",
        hashed,
    ) is False


def test_verify_password_with_invalid_hash():

    assert verify_password(
        "testpassword",
        "not-a-valid-hash",
    ) is False


def test_create_access_token():

    data = {
        "user_id": 1,
        "username": "test_user",
    }

    token = create_access_token(data)

    decoded = decode_access_token(token)

    assert decoded["user_id"] == 1
    assert decoded["username"] == "test_user"
    assert "exp" in decoded


def test_create_access_token_with_custom_expiry():

    data = {"user_id": 2}

    token = create_access_token(
        data,
        expires_delta=timedelta(minutes=30),
    )

    decoded = decode_access_token(token)

    assert decoded["user_id"] == 2


def test_decode_expired_token():

    token = create_access_token(
        {"user_id": 3},
        expires_delta=timedelta(seconds=-1),
    )

    with pytest.raises(HTTPException) as exc:

        decode_access_token(token)

    assert exc.value.status_code == 401
    assert exc.value.detail == "Token has expired"


def test_decode_invalid_token():

    with pytest.raises(HTTPException) as exc:

        decode_access_token(
            "not-a-valid-jwt-token"
        )

    assert exc.value.status_code == 401
    assert exc.value.detail == "Invalid token"


def test_decode_empty_token():

    with pytest.raises(HTTPException) as exc:

        decode_access_token("")

    assert exc.value.status_code == 401


def test_decode_tampered_token():

    data = {"user_id": 4}

    token = create_access_token(data)

    parts = token.split(".")

    import base64
    import json

    def decode_part(part):

        padding = "=" * (-len(part) % 4)

        return json.loads(
            base64.urlsafe_b64decode(
                part + padding
            ).decode()
        )

    def encode_part(payload):

        return base64.urlsafe_b64encode(
            json.dumps(payload).encode()
        ).rstrip(b"=").decode()

    header = decode_part(parts[0])
    payload = decode_part(parts[1])

    payload["user_id"] = 999

    tampered = (
        f"{encode_part(header)}."
        f"{encode_part(payload)}."
        f"{parts[2]}"
    )

    with pytest.raises(HTTPException) as exc:

        decode_access_token(tampered)

    assert exc.value.status_code == 401
    assert exc.value.detail == "Invalid token"


def test_decode_token_with_wrong_algorithm():

    token = jwt.encode(
        {"user_id": 5},
        SECRET_KEY,
        algorithm="HS512",
    )

    with pytest.raises(HTTPException) as exc:

        decode_access_token(token)

    assert exc.value.status_code == 401
    assert exc.value.detail == "Invalid token"


def test_secret_key_length_is_secure():

    assert len(
        SECRET_KEY.encode()
    ) >= 32


def test_token_contains_expected_claims():

    data = {
        "user_id": 10,
        "role": "admin",
        "custom": "value",
    }

    token = create_access_token(data)

    decoded = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
    )

    assert decoded["role"] == "admin"
    assert decoded["custom"] == "value"
    assert "exp" in decoded