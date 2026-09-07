from sqlalchemy.orm import Session

from backend.models.shipment import Shipment
from backend.repositories.shipment_repository import ShipmentRepository
from backend.services.order_service import OrderService


class ShipmentNotFoundError(Exception):
    pass


class ShippingService:

    def __init__(self):
        self.order_service = OrderService()
        self.shipment_repository = ShipmentRepository()

    def get_shipping_status(
        self,
        db: Session,
        order_id: str,
        user_db_id: int,
    ) -> Shipment:

        order = self.order_service.get_order_for_user(
            db,
            order_id,
            user_db_id,
        )

        shipment = self.shipment_repository.get_by_order_id(
            db,
            order.id,
        )

        if shipment is None:
            raise ShipmentNotFoundError(
                "This order has not been shipped yet."
            )

        return shipment