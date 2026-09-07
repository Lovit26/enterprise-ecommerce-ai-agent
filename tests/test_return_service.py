import pytest

from backend.db.session import SessionLocal
from backend.models.user import User
from backend.services.order_service import OrderAccessDeniedError
from backend.services.return_service import ReturnService


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


@pytest.fixture
def return_service():
    return ReturnService()


def test_return_eligible(
    db,
    alice,
    return_service,
):
    result = return_service.check_return_eligibility(
        db,
        "ORD-10001",
        alice.id,
    )

    assert result.eligible is True
    assert result.reason == "Order is eligible for return."


def test_return_window_expired(
    db,
    alice,
    return_service,
):
    result = return_service.check_return_eligibility(
        db,
        "ORD-10002",
        alice.id,
    )

    assert result.eligible is False
    assert result.reason == "Return window has expired."
    assert result.days_since_delivery is not None
    assert result.days_since_delivery > 30


def test_order_not_delivered(
    db,
    alice,
    return_service,
):
    result = return_service.check_return_eligibility(
        db,
        "ORD-10003",
        alice.id,
    )

    assert result.eligible is False
    assert result.reason == "Order has not been delivered."


def test_existing_return_request(
    db,
    alice,
    return_service,
):
    result = return_service.check_return_eligibility(
        db,
        "ORD-10005",
        alice.id,
    )

    assert result.eligible is False
    assert (
        result.reason
        == "An active return request already exists."
    )


def test_cannot_access_another_users_order(
    db,
    alice,
    return_service,
):
    with pytest.raises(OrderAccessDeniedError):
        return_service.check_return_eligibility(
            db,
            "ORD-20001",
            alice.id,
        )