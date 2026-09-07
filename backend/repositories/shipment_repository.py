from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.shipment import Shipment


class ShipmentRepository:

    def get_by_order_id(
        self,
        db: Session,
        order_id: int,
    ) -> Shipment | None:

        statement = select(Shipment).where(
            Shipment.order_id == order_id
        )

        return db.scalar(statement)