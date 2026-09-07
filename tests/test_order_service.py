import pytest

from backend.db.session import SessionLocal
from backend.models.user import User
from backend.services.order_service import (
    OrderAccessDeniedError,
    OrderNotFoundError,
    OrderService,
)
from backend.services.shipping_service import (
    ShipmentNotFoundError,
    ShippingService,
)


@pytest.fixture
def db():
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def alice(db):
    user = (
        db.query(User)
        .filter(User.user_id == "USR-10001")
        .first()
    )

    assert user is not None

    return user


def test_get_own_order(db, alice):
    service = OrderService()

    order = service.get_order_for_user(
        db,
        "ORD-10001",
        alice.id,
    )

    assert order.order_id == "ORD-10001"
    assert order.status == "delivered"


def test_order_not_found(db, alice):
    service = OrderService()

    with pytest.raises(OrderNotFoundError):
        service.get_order_for_user(
            db,
            "ORD-99999",
            alice.id,
        )


def test_order_access_denied(db, alice):
    service = OrderService()

    with pytest.raises(OrderAccessDeniedError):
        service.get_order_for_user(
            db,
            "ORD-20001",
            alice.id,
        )


def test_shipping_status(db, alice):
    service = ShippingService()

    shipment = service.get_shipping_status(
        db,
        "ORD-10003",
        alice.id,
    )

    assert shipment.status == "in_transit"
    assert shipment.tracking_number == "DHL10003"


def test_order_not_shipped(db, alice):
    service = ShippingService()

    with pytest.raises(ShipmentNotFoundError):
        service.get_shipping_status(
            db,
            "ORD-10004",
            alice.id,
        )