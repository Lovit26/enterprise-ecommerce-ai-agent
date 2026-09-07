from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_database_health():
    response = client.get("/health/db")

    assert response.status_code == 200
    assert response.json()["database"] == "connected"


def test_get_order():
    response = client.get(
        "/api/v1/orders/ORD-10001"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["order_id"] == "ORD-10001"
    assert data["status"] == "delivered"


def test_order_not_found():
    response = client.get(
        "/api/v1/orders/ORD-99999"
    )

    assert response.status_code == 404


def test_order_access_denied():
    response = client.get(
        "/api/v1/orders/ORD-20001"
    )

    assert response.status_code == 403


def test_shipping():
    response = client.get(
        "/api/v1/orders/ORD-10003/shipment"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "in_transit"
    assert data["tracking_number"] == "DHL10003"


def test_not_shipped():
    response = client.get(
        "/api/v1/orders/ORD-10004/shipment"
    )

    assert response.status_code == 404


def test_return_eligible():
    response = client.get(
        "/api/v1/orders/ORD-10001/return-eligibility"
    )

    assert response.status_code == 200
    assert response.json()["eligible"] is True


def test_return_expired():
    response = client.get(
        "/api/v1/orders/ORD-10002/return-eligibility"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["eligible"] is False
    assert data["reason"] == "Return window has expired."


def test_existing_return():
    response = client.get(
        "/api/v1/orders/ORD-10005/return-eligibility"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["eligible"] is False
    assert (
        data["reason"]
        == "An active return request already exists."
    )