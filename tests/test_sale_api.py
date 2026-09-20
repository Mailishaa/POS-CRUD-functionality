import pytest


def sale_payload(**overrides):
    payload = {
        "total_amount": "125.75",
    }

    payload.update(overrides)

    return payload


def test_sale_crud_lifecycle(client):
    assert client.get("/sales/").json() == []

    created = client.post(
        "/sales/",
        json=sale_payload(),
    )

    assert created.status_code == 201

    sale_id = created.json()["id"]

    assert float(
        created.json()["total_amount"]
    ) == 125.75

    fetched = client.get(
        f"/sales/{sale_id}"
    )

    assert fetched.status_code == 200

    updated = client.put(
        f"/sales/{sale_id}",
        json={
            "total_amount": "150.25",
        },
    )

    assert updated.status_code == 200

    assert float(
        updated.json()["total_amount"]
    ) == 150.25

    deleted = client.delete(
        f"/sales/{sale_id}"
    )

    assert deleted.status_code == 204

    assert client.get(
        f"/sales/{sale_id}"
    ).status_code == 404


def test_sale_rejects_invalid_foreign_keys(client):
    response = client.post(
        "/sales/",
        json=sale_payload(
            user_id=999,
            customer_id=999,
        ),
    )

    assert response.status_code == 400

    assert response.json() == {
        "detail": (
            "Invalid user_id or customer_id. "
            "Make sure both exist."
        )
    }


@pytest.mark.parametrize(
    "method",
    ["get", "put", "delete"],
)
def test_sale_missing_resource_returns_404(
    client,
    method,
):
    if method == "put":
        response = client.put(
            "/sales/999",
            json={
                "total_amount": "1",
            },
        )
    else:
        response = getattr(
            client,
            method,
        )("/sales/999")

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Sale not found"
    }


def test_sale_rejects_negative_total(client):
    response = client.post(
        "/sales/",
        json=sale_payload(
            total_amount="-1",
        ),
    )

    assert response.status_code == 422