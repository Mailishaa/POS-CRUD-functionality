import pytest


def category_payload():
    return {
        "category_name": "Accessories",
        "tax_rate": "8.25",
    }


def supplier_payload():
    return {
        "supplier_name": "Urban Fashion Wholesale",
        "contact_name": "Sam Supplier",
        "phone": "+15551234567",
    }


def product_payload(**overrides):
    payload = {
        "barcode": "890000000001",
        "product_name": "Silk Scarf",
        "unit_price": "25.00",
        "stock_qty": 12,
    }

    payload.update(overrides)

    return payload


def test_product_crud_lifecycle_and_optional_relationships(client):
    category_id = client.post(
        "/categories/",
        json=category_payload(),
    ).json()["id"]

    supplier_id = client.post(
        "/suppliers/",
        json=supplier_payload(),
    ).json()["id"]

    payload = product_payload(
        category_id=category_id,
        supplier_id=supplier_id,
    )

    assert client.get("/products/").json() == []

    created = client.post(
        "/products/",
        json=payload,
    )

    assert created.status_code == 201

    product_id = created.json()["id"]

    assert created.json()["is_active"] is True
    assert created.json()["category_id"] == category_id
    assert created.json()["supplier_id"] == supplier_id

    fetched = client.get(
        f"/products/{product_id}"
    )

    assert fetched.status_code == 200
    assert fetched.json()["product_name"] == "Silk Scarf"

    updated = client.put(
        f"/products/{product_id}",
        json={
            "product_name": "Printed Silk Scarf",
            "stock_qty": 10,
        },
    )

    assert updated.status_code == 200

    assert updated.json()["product_name"] == (
        "Printed Silk Scarf"
    )

    assert updated.json()["stock_qty"] == 10
    assert updated.json()["category_id"] == category_id

    deleted = client.delete(
        f"/products/{product_id}"
    )

    assert deleted.status_code == 204

    assert client.get(
        f"/products/{product_id}"
    ).status_code == 404


def test_product_allows_missing_optional_relationships(client):
    response = client.post(
        "/products/",
        json=product_payload(
            barcode=None,
        ),
    )

    assert response.status_code == 201
    assert response.json()["category_id"] is None
    assert response.json()["supplier_id"] is None


def test_product_rejects_duplicate_barcode(client):
    assert client.post(
        "/products/",
        json=product_payload(),
    ).status_code == 201

    response = client.post(
        "/products/",
        json=product_payload(
            product_name="Leather Belt",
        ),
    )

    assert response.status_code == 400


@pytest.mark.parametrize(
    "method",
    ["get", "put", "delete"],
)
def test_product_missing_resource_returns_404(
    client,
    method,
):
    if method == "put":
        response = client.put(
            "/products/999",
            json={
                "product_name": "Missing",
            },
        )
    else:
        response = getattr(
            client,
            method,
        )("/products/999")

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Product not found"
    }


def test_product_rejects_negative_values(client):
    response = client.post(
        "/products/",
        json=product_payload(
            unit_price="-1",
            stock_qty=-1,
        ),
    )

    assert response.status_code == 422