from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_id: str
    status: str
    total_amount: Decimal
    created_at: datetime
    updated_at: datetime