from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.db.dependencies import get_db
from backend.models.user import User
from backend.schemas.order import OrderResponse
from backend.schemas.return_request import ReturnEligibilityResponse
from backend.schemas.shipment import ShipmentResponse
from backend.services.order_service import (
    OrderAccessDeniedError,
    OrderNotFoundError,
    OrderService,
)
from backend.services.return_service import ReturnService
from backend.services.shipping_service import (
    ShipmentNotFoundError,
    ShippingService,
)


router = APIRouter(
    prefix="/api/v1/orders",
    tags=["orders"],
)

order_service = OrderService()
shipping_service = ShippingService()
return_service = ReturnService()


def get_demo_user(db: Session) -> User:
    user = (
        db.query(User)
        .filter(User.user_id == "USR-10001")
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Demo user not found.",
        )

    return user


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
)
def get_order(
    order_id: str,
    db: Session = Depends(get_db),
):
    user = get_demo_user(db)

    try:
        return order_service.get_order_for_user(
            db,
            order_id,
            user.id,
        )

    except OrderNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except OrderAccessDeniedError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc


@router.get(
    "/{order_id}/shipment",
    response_model=ShipmentResponse,
)
def get_shipment(
    order_id: str,
    db: Session = Depends(get_db),
):
    user = get_demo_user(db)

    try:
        return shipping_service.get_shipping_status(
            db,
            order_id,
            user.id,
        )

    except OrderNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except OrderAccessDeniedError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc

    except ShipmentNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/{order_id}/return-eligibility",
    response_model=ReturnEligibilityResponse,
)
def check_return_eligibility(
    order_id: str,
    db: Session = Depends(get_db),
):
    user = get_demo_user(db)

    try:
        result = return_service.check_return_eligibility(
            db,
            order_id,
            user.id,
        )

        return ReturnEligibilityResponse(
            eligible=result.eligible,
            reason=result.reason,
            days_since_delivery=result.days_since_delivery,
        )

    except OrderNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except OrderAccessDeniedError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc