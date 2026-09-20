import pytest


def supplier_payload(**overrides):
    payload = {
        "supplier_name": "Urban Fashion Wholesale",
        "contact_name": "Sam Supplier",
        "phone": "+15551234567",
    }

    payload.update(overrides)

    return payload


def test_supplier_crud_lifecycle(client):
    assert client.get("/suppliers/").json() == []

    created = client.post(
        "/suppliers/",
        json=supplier_payload(),
    )

    assert created.status_code == 201

    supplier_id = created.json()["id"]

    assert "created_at" in created.json()

    fetched = client.get(
        f"/suppliers/{supplier_id}"
    )

    assert fetched.status_code == 200
    assert fetched.json()["supplier_name"] == (
        "Urban Fashion Wholesale"
    )

    updated = client.put(
        f"/suppliers/{supplier_id}",
        json={
            "phone": "+15557654321",
        },
    )

    assert updated.status_code == 200
    assert updated.json()["phone"] == "+15557654321"

    deleted = client.delete(
        f"/suppliers/{supplier_id}"
    )

    assert deleted.status_code == 204

    assert client.get(
        f"/suppliers/{supplier_id}"
    ).status_code == 404


@pytest.mark.parametrize(
    "method",
    ["get", "put", "delete"],
)
def test_supplier_missing_resource_returns_404(
    client,
    method,
):
    if method == "put":
        response = client.put(
            "/suppliers/999",
            json={"phone": "555"},
        )
    else:
        response = getattr(
            client,
            method,
        )("/suppliers/999")

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Supplier not found"
    }


def test_supplier_requires_name_and_phone(client):
    response = client.post(
        "/suppliers/",
        json={
            "supplier_name": "Missing phone",
        },
    )

    assert response.status_code == 422