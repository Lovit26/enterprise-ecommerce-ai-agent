from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ShipmentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    shipment_id: str
    carrier: str
    tracking_number: str
    status: str
    estimated_delivery: datetime | None
    shipped_at: datetime | None
    delivered_at: datetime | None