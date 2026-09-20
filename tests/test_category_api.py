import pytest


def category_payload(**overrides):
    payload = {
        "category_name": "Accessories",
        "tax_rate": "8.25",
    }

    payload.update(overrides)

    return payload


def test_category_crud_lifecycle(client):
    assert client.get("/categories/").json() == []

    created = client.post(
        "/categories/",
        json=category_payload(),
    )

    assert created.status_code == 201

    category_id = created.json()["id"]

    assert float(
        created.json()["tax_rate"]
    ) == 8.25

    fetched = client.get(
        f"/categories/{category_id}"
    )

    assert fetched.status_code == 200
    assert fetched.json()["category_name"] == "Accessories"

    updated = client.put(
        f"/categories/{category_id}",
        json={
            "tax_rate": "9.00",
        },
    )

    assert updated.status_code == 200
    assert float(
        updated.json()["tax_rate"]
    ) == 9.0

    assert updated.json()["category_name"] == "Accessories"

    deleted = client.delete(
        f"/categories/{category_id}"
    )

    assert deleted.status_code == 204

    assert client.get(
        f"/categories/{category_id}"
    ).status_code == 404


@pytest.mark.parametrize(
    "method",
    ["get", "put", "delete"],
)
def test_category_missing_resource_returns_404(
    client,
    method,
):
    if method == "put":
        response = client.put(
            "/categories/999",
            json={"tax_rate": "5"},
        )
    else:
        response = getattr(
            client,
            method,
        )("/categories/999")

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Category not found"
    }


def test_category_rejects_out_of_range_tax_rate(client):
    response = client.post(
        "/categories/",
        json=category_payload(
            tax_rate="101",
        ),
    )

    assert response.status_code == 422