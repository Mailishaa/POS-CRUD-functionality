import pytest


def create_sale(client):
    response = client.post(
        "/sales/",
        json={
            "total_amount": "100.00",
        },
    )

    return response.json()["id"]


def payment_payload(
    sale_id,
    **overrides,
):
    payload = {
        "sale_id": sale_id,
        "payment_method": "card",
        "amount_paid": "100.00",
    }

    payload.update(overrides)

    return payload


def test_payment_crud_lifecycle(client):
    sale_id = create_sale(client)

    assert client.get(
        "/payments/"
    ).json() == []

    created = client.post(
        "/payments/",
        json=payment_payload(sale_id),
    )

    assert created.status_code == 201

    payment_id = created.json()["id"]

    assert "created_at" in created.json()

    fetched = client.get(
        f"/payments/{payment_id}"
    )

    assert fetched.status_code == 200
    assert fetched.json()["sale_id"] == sale_id

    updated = client.put(
        f"/payments/{payment_id}",
        json={
            "amount_paid": "95.50",
        },
    )

    assert updated.status_code == 200

    assert float(
        updated.json()["amount_paid"]
    ) == 95.5

    deleted = client.delete(
        f"/payments/{payment_id}"
    )

    assert deleted.status_code == 204

    assert client.get(
        f"/payments/{payment_id}"
    ).status_code == 404


def test_payment_rejects_invalid_sale(client):
    response = client.post(
        "/payments/",
        json=payment_payload(999),
    )

    assert response.status_code == 400


@pytest.mark.parametrize(
    "method",
    ["get", "put", "delete"],
)
def test_payment_missing_resource_returns_404(
    client,
    method,
):
    if method == "put":
        response = client.put(
            "/payments/999",
            json={
                "amount_paid": "1",
            },
        )
    else:
        response = getattr(
            client,
            method,
        )("/payments/999")

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Payment not found"
    }


def test_payment_rejects_negative_amount(client):
    sale_id = create_sale(client)

    response = client.post(
        "/payments/",
        json=payment_payload(
            sale_id,
            amount_paid="-1",
        ),
    )

    assert response.status_code == 422