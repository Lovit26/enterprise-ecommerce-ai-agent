from langchain_core.tools import tool

from backend.db.session import SessionLocal
from backend.models.user import User
from backend.services.order_service import (
    OrderAccessDeniedError,
    OrderNotFoundError,
    OrderService,
)


order_service = OrderService()


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
def get_order(order_id: str) -> dict:
    """
    Get an order that belongs to the current user.

    Use this tool when the user asks about a specific order,
    including its status or basic order information.
    """

    db = SessionLocal()

    try:
        user = get_demo_user(db)

        order = order_service.get_order_for_user(
            db,
            order_id,
            user.id,
        )

        return {
            "success": True,
            "order_id": order.order_id,
            "status": order.status,
            "total_amount": str(order.total_amount),
            "created_at": order.created_at.isoformat(),
        }

    except OrderNotFoundError:
        return {
            "success": False,
            "error": "order_not_found",
            "message": f"Order {order_id} was not found.",
        }

    except OrderAccessDeniedError:
        return {
            "success": False,
            "error": "access_denied",
            "message": "The current user cannot access this order.",
        }

    finally:
        db.close()