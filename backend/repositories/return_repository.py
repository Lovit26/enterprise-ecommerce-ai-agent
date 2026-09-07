from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.return_request import ReturnRequest


class ReturnRepository:

    def get_active_by_order_id(
        self,
        db: Session,
        order_id: int,
    ) -> ReturnRequest | None:

        statement = select(ReturnRequest).where(
            ReturnRequest.order_id == order_id,
            ReturnRequest.status.in_(
                ["pending", "processing", "approved"]
            ),
        )

        return db.scalar(statement)

    def create(
        self,
        db: Session,
        return_request: ReturnRequest,
    ) -> ReturnRequest:

        db.add(return_request)
        db.flush()

        return return_request