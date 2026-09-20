import pytest


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


def test_user_crud_lifecycle(client):
    existing_users = client.get("/users/").json()

    assert len(existing_users) == 1
    assert existing_users[0]["username"] == "test-admin"

    created = client.post(
        "/users/",
        json=user_payload(),
    )

    assert created.status_code == 201

    user_id = created.json()["id"]

    assert created.json()["email"] == "alice@example.com"
    assert "password" not in created.json()

    fetched = client.get(
        f"/users/{user_id}"
    )

    assert fetched.status_code == 200
    assert fetched.json()["username"] == "alice"

    updated = client.put(
        f"/users/{user_id}",
        json={
            "email": "updated@example.com",
        },
    )

    assert updated.status_code == 200
    assert updated.json()["email"] == "updated@example.com"

    deleted = client.delete(
        f"/users/{user_id}"
    )

    assert deleted.status_code == 204
    assert deleted.content == b""

    assert client.get(
        f"/users/{user_id}"
    ).status_code == 404


def test_user_create_hashes_password_for_login(client):
    response = client.post(
        "/users/",
        json=user_payload(),
    )

    assert response.status_code == 201

    login = client.post(
        "/auth/login",
        data={
            "username": "alice",
            "password": "secret123",
        },
    )

    assert login.status_code == 200
    assert login.json()["access_token"]


@pytest.mark.parametrize(
    ("method", "path", "payload"),
    [
        ("get", "/users/999", None),
        (
            "put",
            "/users/999",
            {"email": "new@example.com"},
        ),
        ("delete", "/users/999", None),
    ],
)
def test_user_missing_resource_returns_404(
    client,
    method,
    path,
    payload,
):
    if payload:
        response = getattr(client, method)(
            path,
            json=payload,
        )
    else:
        response = getattr(client, method)(path)

    assert response.status_code == 404

    assert response.json() == {
        "detail": "User not found"
    }


def test_user_rejects_duplicate_username_and_email(client):
    assert client.post(
        "/users/",
        json=user_payload(),
    ).status_code == 201

    duplicate_username = client.post(
        "/users/",
        json=user_payload(
            email="other@example.com",
        ),
    )

    assert duplicate_username.status_code == 400

    duplicate_email = client.post(
        "/users/",
        json=user_payload(
            username="other",
        ),
    )

    assert duplicate_email.status_code == 400


def test_user_rejects_invalid_payload(client):
    response = client.post(
        "/users/",
        json=user_payload(
            username="ab",
            password="short",
            email="invalid",
        ),
    )

    assert response.status_code == 422