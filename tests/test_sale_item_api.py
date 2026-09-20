import pytest


def product_payload():
    return {
        "barcode": "890000000001",
        "product_name": "Silk Scarf",
        "unit_price": "25.00",
        "stock_qty": 12,
    }


def create_sale_and_product(client):
    sale_id = client.post(
        "/sales/",
        json={
            "total_amount": "25.00",
        },
    ).json()["id"]

    product_id = client.post(
        "/products/",
        json=product_payload(),
    ).json()["id"]

    return sale_id, product_id


def sale_item_payload(
    sale_id,
    product_id,
    **overrides,
):
    payload = {
        "sale_id": sale_id,
        "product_id": product_id,
        "quantity": 2,
        "item_price": "25.00",
    }

    payload.update(overrides)

    return payload


def sale_item_sale_id(body):
    return body.get(
        "sale_id",
        body.get("Sale_id"),
    )


def test_sale_item_crud_lifecycle(client):
    sale_id, product_id = create_sale_and_product(
        client
    )

    assert client.get(
        "/sale-items/"
    ).json() == []

    created = client.post(
        "/sale-items/",
        json=sale_item_payload(
            sale_id,
            product_id,
        ),
    )

    assert created.status_code == 201

    sale_item_id = created.json()["id"]

    assert sale_item_sale_id(
        created.json()
    ) == sale_id

    fetched = client.get(
        f"/sale-items/{sale_item_id}"
    )

    assert fetched.status_code == 200

    updated = client.put(
        f"/sale-items/{sale_item_id}",
        json={
            "quantity": 3,
        },
    )

    assert updated.status_code == 200
    assert updated.json()["quantity"] == 3

    assert sale_item_sale_id(
        updated.json()
    ) == sale_id

    deleted = client.delete(
        f"/sale-items/{sale_item_id}"
    )

    assert deleted.status_code == 204

    assert client.get(
        f"/sale-items/{sale_item_id}"
    ).status_code == 404


def test_sale_item_accepts_legacy_aliases(client):
    sale_id, product_id = create_sale_and_product(
        client
    )

    response = client.post(
        "/sale-items/",
        json={
            "Sale_id": sale_id,
            "Product_id": product_id,
            "quantity": 1,
            "item_price": "25.00",
        },
    )

    assert response.status_code == 201

    assert sale_item_sale_id(
        response.json()
    ) == sale_id


def test_sale_item_rejects_invalid_foreign_keys(client):
    response = client.post(
        "/sale-items/",
        json=sale_item_payload(
            999,
            999,
        ),
    )

    assert response.status_code == 400

    assert response.json() == {
        "detail": (
            "Invalid sale_id or product_id. "
            "Make sure both exist."
        )
    }


@pytest.mark.parametrize(
    "method",
    ["get", "put", "delete"],
)
def test_sale_item_missing_resource_returns_404(
    client,
    method,
):
    if method == "put":
        response = client.put(
            "/sale-items/999",
            json={
                "quantity": 1,
            },
        )
    else:
        response = getattr(
            client,
            method,
        )("/sale-items/999")

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Sale item not found"
    }


def test_sale_item_rejects_non_positive_quantity(client):
    sale_id, product_id = create_sale_and_product(
        client
    )

    response = client.post(
        "/sale-items/",
        json=sale_item_payload(
            sale_id,
            product_id,
            quantity=0,
        ),
    )

    assert response.status_code == 422