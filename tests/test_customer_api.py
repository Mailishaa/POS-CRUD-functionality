import pytest


def customer_payload(**overrides):
    payload = {
        "first_name": "Amina",
        "last_name": "Kamau",
        "email": "amina@example.com",
        "phone_number": "+15551234567",
    }

    payload.update(overrides)

    return payload


def test_customer_crud_lifecycle(client):
    assert client.get("/customers/").json() == []

    created = client.post(
        "/customers/",
        json=customer_payload(),
    )

    assert created.status_code == 201

    customer_id = created.json()["id"]

    fetched = client.get(
        f"/customers/{customer_id}"
    )

    assert fetched.status_code == 200
    assert fetched.json()["first_name"] == "Amina"

    updated = client.put(
        f"/customers/{customer_id}",
        json={
            "phone_number": "+15557654321",
        },
    )

    assert updated.status_code == 200
    assert updated.json()["phone_number"] == "+15557654321"
    assert updated.json()["first_name"] == "Amina"

    deleted = client.delete(
        f"/customers/{customer_id}"
    )

    assert deleted.status_code == 204

    assert client.get(
        f"/customers/{customer_id}"
    ).status_code == 404


@pytest.mark.parametrize(
    "method",
    ["get", "put", "delete"],
)
def test_customer_missing_resource_returns_404(
    client,
    method,
):
    if method == "put":
        response = client.put(
            "/customers/999",
            json={"first_name": "Missing"},
        )
    else:
        response = getattr(
            client,
            method,
        )("/customers/999")

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Customer not found"
    }


def test_customer_requires_names(client):
    response = client.post(
        "/customers/",
        json={
            "email": "missing@example.com",
        },
    )

    assert response.status_code == 422