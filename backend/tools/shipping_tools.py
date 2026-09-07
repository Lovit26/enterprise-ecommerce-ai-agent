from langchain_core.tools import tool

from backend.db.session import SessionLocal
from backend.models.user import User
from backend.services.order_service import (
    OrderAccessDeniedError,
    OrderNotFoundError,
)
from backend.services.shipping_service import (
    ShipmentNotFoundError,
    ShippingService,
)


shipping_service = ShippingService()


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
def get_shipping_status(order_id: str) -> dict:
    """Get shipping and tracking information for a specific order
    belonging to the current user.
    """

    db = SessionLocal()

    try:
        user = get_demo_user(db)

        shipment = shipping_service.get_shipping_status(
            db,
            order_id,
            user.id,
        )

        return {
            "success": True,
            "shipment_id": shipment.shipment_id,
            "carrier": shipment.carrier,
            "tracking_number": shipment.tracking_number,
            "status": shipment.status,
            "estimated_delivery": (
                shipment.estimated_delivery.isoformat()
                if shipment.estimated_delivery
                else None
            ),
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

    except ShipmentNotFoundError:
        return {
            "success": False,
            "error": "shipment_not_found",
        }

    finally:
        db.close()