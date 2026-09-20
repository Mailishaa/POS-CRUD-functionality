def user_payload(**overrides):
    payload = {
        "username": "alice",
        "email": "alice@example.com",
        "password": "secret123",
        "role": "cashier",
        "is_active": True,
    }
    payload.update(overrides)
    return payload


def test_register_user_returns_public_profile(client):
    response = client.post(
        "/auth/register",
        json=user_payload(),
    )

    assert response.status_code == 201

    body = response.json()

    assert body["username"] == "alice"
    assert body["email"] == "alice@example.com"
    assert body["role"] == "cashier"
    assert body["is_active"] is True
    assert isinstance(body["id"], int)

    assert "created_at" in body
    assert "password" not in body
    assert "password_hash" not in body


def test_register_rejects_duplicate_username(client):
    client.post(
        "/auth/register",
        json=user_payload(),
    )

    response = client.post(
        "/auth/register",
        json=user_payload(
            email="different@example.com"
        ),
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Username already registered"
    }


def test_register_rejects_duplicate_email(client):
    client.post(
        "/auth/register",
        json=user_payload(),
    )

    response = client.post(
        "/auth/register",
        json=user_payload(
            username="different",
        ),
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Email already registered"
    }


def test_register_validates_email_and_password(client):
    response = client.post(
        "/auth/register",
        json=user_payload(
            email="not-an-email",
            password="short",
        ),
    )

    assert response.status_code == 422
    assert len(response.json()["detail"]) >= 2


def test_public_registration_cannot_create_admin(client):
    response = client.post(
        "/auth/register",
        json=user_payload(
            role="admin",
        ),
    )

    assert response.status_code == 403
    assert response.json() == {
        "detail": "Public registration is limited to cashier accounts"
    }


def test_login_returns_bearer_token(client):
    client.post(
        "/auth/register",
        json=user_payload(),
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "alice",
            "password": "secret123",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["token_type"] == "bearer"
    assert isinstance(body["access_token"], str)
    assert body["access_token"]


def test_login_rejects_invalid_credentials(client):
    client.post(
        "/auth/register",
        json=user_payload(),
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "alice",
            "password": "wrong-password",
        },
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Incorrect username or password"
    }