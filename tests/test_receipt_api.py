import pytest


def create_sale(client):
    response = client.post(
        "/sales/",
        json={
            "total_amount": "100.00",
        },
    )

    return response.json()["id"]


def receipt_payload(
    sale_id,
    **overrides,
):
    payload = {
        "sale_id": sale_id,
        "receipt_number": "R-0001",
    }

    payload.update(overrides)

    return payload


def receipt_sale_id(body):
    return body.get(
        "sale_id",
        body.get("Sale_id"),
    )


def test_receipt_crud_lifecycle(client):
    sale_id = create_sale(client)

    assert client.get(
        "/receipts/"
    ).json() == []

    created = client.post(
        "/receipts/",
        json=receipt_payload(sale_id),
    )

    assert created.status_code == 201

    receipt_id = created.json()["id"]

    assert receipt_sale_id(
        created.json()
    ) == sale_id

    assert "created_at" in created.json()

    fetched = client.get(
        f"/receipts/{receipt_id}"
    )

    assert fetched.status_code == 200

    updated = client.put(
        f"/receipts/{receipt_id}",
        json={
            "receipt_number": "R-0002",
        },
    )

    assert updated.status_code == 200

    assert updated.json()["receipt_number"] == "R-0002"

    assert receipt_sale_id(
        updated.json()
    ) == sale_id

    deleted = client.delete(
        f"/receipts/{receipt_id}"
    )

    assert deleted.status_code == 204

    assert client.get(
        f"/receipts/{receipt_id}"
    ).status_code == 404


def test_receipt_accepts_legacy_sale_id_alias(client):
    sale_id = create_sale(client)

    response = client.post(
        "/receipts/",
        json={
            "Sale_id": sale_id,
            "receipt_number": "R-0001",
        },
    )

    assert response.status_code == 201

    assert receipt_sale_id(
        response.json()
    ) == sale_id


def test_receipt_rejects_invalid_sale(client):
    response = client.post(
        "/receipts/",
        json=receipt_payload(999),
    )

    assert response.status_code == 400


def test_receipt_rejects_duplicate_number(client):
    sale_id = create_sale(client)

    first = client.post(
        "/receipts/",
        json=receipt_payload(sale_id),
    )

    assert first.status_code == 201

    second_sale_id = client.post(
        "/sales/",
        json={
            "total_amount": "200.00",
        },
    ).json()["id"]

    response = client.post(
        "/receipts/",
        json=receipt_payload(
            second_sale_id,
        ),
    )

    assert response.status_code == 400


@pytest.mark.parametrize(
    "method",
    ["get", "put", "delete"],
)
def test_receipt_missing_resource_returns_404(
    client,
    method,
):
    if method == "put":
        response = client.put(
            "/receipts/999",
            json={
                "receipt_number": "missing",
            },
        )
    else:
        response = getattr(
            client,
            method,
        )("/receipts/999")

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Receipt not found"
    }