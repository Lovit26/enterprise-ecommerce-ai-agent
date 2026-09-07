from sqlalchemy.orm import Session

from backend.models.order import Order
from backend.repositories.order_repository import OrderRepository


class OrderNotFoundError(Exception):
    pass


class OrderAccessDeniedError(Exception):
    pass


class OrderService:

    def __init__(self):
        self.order_repository = OrderRepository()

    def get_order_for_user(
        self,
        db: Session,
        order_id: str,
        user_db_id: int,
    ) -> Order:

        order = self.order_repository.get_by_order_id(
            db,
            order_id,
        )

        if order is None:
            raise OrderNotFoundError(
                f"Order {order_id} not found."
            )

        if order.user_id != user_db_id:
            raise OrderAccessDeniedError(
                "You do not have access to this order."
            )

        return order