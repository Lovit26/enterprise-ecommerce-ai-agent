from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.order import Order


class OrderRepository:

    def get_by_order_id(
        self,
        db: Session,
        order_id: str,
    ) -> Order | None:

        statement = select(Order).where(
            Order.order_id == order_id
        )

        return db.scalar(statement)