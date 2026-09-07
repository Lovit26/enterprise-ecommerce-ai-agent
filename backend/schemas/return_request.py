from pydantic import BaseModel


class ReturnEligibilityResponse(BaseModel):
    eligible: bool
    reason: str
    days_since_delivery: int | None = None