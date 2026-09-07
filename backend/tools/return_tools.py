from langchain_core.tools import tool

from backend.db.session import SessionLocal
from backend.models.user import User
from backend.services.order_service import (
    OrderAccessDeniedError,
    OrderNotFoundError,
)
from backend.services.return_service import ReturnService


return_service = ReturnService()


def get_demo_user(db):
    user = (
        db.query(User)
        .filter(User.user_id == "USR-10001")
        .first()
    )

    if user is None:
        raise RuntimeError("Demo user not found.")

    return user


@tool
def check_return_eligibility(order_id: str) -> dict:
    """Check whether a specific order belonging to the current user
    is eligible for return.
    """

    db = SessionLocal()

    try:
        user = get_demo_user(db)

        result = return_service.check_return_eligibility(
            db,
            order_id,
            user.id,
        )

        return {
            "success": True,
            "eligible": result.eligible,
            "reason": result.reason,
            "days_since_delivery": result.days_since_delivery,
        }

    except OrderNotFoundError:
        return {
            "success": False,
            "error": "order_not_found",
        }

    except OrderAccessDeniedError:
        return {
            "success": False,
            "error": "access_denied",
        }

    finally:
        db.close()