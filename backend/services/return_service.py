from dataclasses import dataclass
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from backend.repositories.return_repository import ReturnRepository
from backend.repositories.shipment_repository import ShipmentRepository
from backend.services.order_service import OrderService


RETURN_WINDOW_DAYS = 30


@dataclass
class ReturnEligibilityResult:
    eligible: bool
    reason: str
    days_since_delivery: int | None = None


class ReturnService:

    def __init__(self):
        self.order_service = OrderService()
        self.shipment_repository = ShipmentRepository()
        self.return_repository = ReturnRepository()

    def check_return_eligibility(
        self,
        db: Session,
        order_id: str,
        user_db_id: int,
    ) -> ReturnEligibilityResult:

        # 1. Order exists + authorization
        order = self.order_service.get_order_for_user(
            db,
            order_id,
            user_db_id,
        )

        # 2. Order must be delivered
        if order.status != "delivered":
            return ReturnEligibilityResult(
                eligible=False,
                reason="Order has not been delivered.",
            )

        # 3. Shipment must exist
        shipment = self.shipment_repository.get_by_order_id(
            db,
            order.id,
        )

        if shipment is None or shipment.delivered_at is None:
            return ReturnEligibilityResult(
                eligible=False,
                reason="Delivery information is unavailable.",
            )

        # 4. Calculate return window
        now = datetime.now(timezone.utc)

        delivered_at = shipment.delivered_at

        if delivered_at.tzinfo is None:
            delivered_at = delivered_at.replace(
                tzinfo=timezone.utc
            )

        days_since_delivery = (
            now - delivered_at
        ).days

        if days_since_delivery > RETURN_WINDOW_DAYS:
            return ReturnEligibilityResult(
                eligible=False,
                reason="Return window has expired.",
                days_since_delivery=days_since_delivery,
            )

        # 5. Existing return request
        existing_return = (
            self.return_repository.get_active_by_order_id(
                db,
                order.id,
            )
        )

        if existing_return is not None:
            return ReturnEligibilityResult(
                eligible=False,
                reason="An active return request already exists.",
                days_since_delivery=days_since_delivery,
            )

        return ReturnEligibilityResult(
            eligible=True,
            reason="Order is eligible for return.",
            days_since_delivery=days_since_delivery,
        )