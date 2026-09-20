def user_payload(**overrides):
    payload = {
        "username": "cashier",
        "email": "cashier@example.com",
        "password": "secret123",
        "role": "cashier",
        "is_active": True,
    }

    payload.update(overrides)

    return payload


def login(client, username, password):
    response = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": password,
        },
    )

    assert response.status_code == 200

    client.headers["Authorization"] = (
        f"Bearer {response.json()['access_token']}"
    )


def test_protected_endpoints_require_authentication(client):
    client.headers.pop("Authorization", None)

    protected_endpoints = [
        "/users/",
        "/customers/",
        "/suppliers/",
        "/categories/",
        "/products/",
        "/sales/",
        "/sale-items/",
        "/payments/",
        "/receipts/",
    ]

    for endpoint in protected_endpoints:
        response = client.get(endpoint)

        assert response.status_code == 401
        assert response.json() == {
            "detail": "Not authenticated"
        }

        assert response.headers["www-authenticate"] == "Bearer"


def test_invalid_bearer_token_is_rejected(client):
    client.headers["Authorization"] = "Bearer invalid-token"

    response = client.get("/products/")

    assert response.status_code == 401

    assert response.json() == {
        "detail": "Could not validate credentials"
    }

    assert response.headers["www-authenticate"] == "Bearer"


def test_cashier_can_read_products_but_not_manage_users(client):
    registered = client.post(
        "/auth/register",
        json=user_payload(),
    )

    assert registered.status_code == 201

    login(
        client,
        "cashier",
        "secret123",
    )

    products = client.get("/products/")
    users = client.get("/users/")

    assert products.status_code == 200

    assert users.status_code == 403
    assert users.json() == {
        "detail": "User does not have admin privileges"
    }


def test_inactive_user_cannot_login(client):
    registered = client.post(
        "/auth/register",
        json=user_payload(
            is_active=False,
        ),
    )

    assert registered.status_code == 201

    response = client.post(
        "/auth/login",
        data={
            "username": "cashier",
            "password": "secret123",
        },
    )

    assert response.status_code == 403

    assert response.json() == {
        "detail": "Inactive user"
    }


def test_cashier_cannot_create_catalog_records(client):
    registered = client.post(
        "/auth/register",
        json=user_payload(),
    )

    assert registered.status_code == 201

    login(
        client,
        "cashier",
        "secret123",
    )

    response = client.post(
        "/products/",
        json={
            "product_name": "Silk Scarf",
            "unit_price": "25.00",
            "stock_qty": 1,
        },
    )

    assert response.status_code == 403

    assert response.json() == {
        "detail": "User does not have admin privileges"
    }