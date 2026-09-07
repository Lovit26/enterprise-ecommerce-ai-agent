from backend.db.session import SessionLocal
from backend.models.user import User
from backend.services.order_service import (
    OrderAccessDeniedError,
    OrderService,
)
from backend.services.return_service import ReturnService
from backend.services.shipping_service import (
    ShipmentNotFoundError,
    ShippingService,
)


def main():
    db = SessionLocal()

    try:
        alice = (
            db.query(User)
            .filter(User.user_id == "USR-10001")
            .first()
        )

        if alice is None:
            raise RuntimeError("Alice not found.")

        order_service = OrderService()
        shipping_service = ShippingService()
        return_service = ReturnService()

        print("\n=== TEST 1: OWN ORDER ===")

        order = order_service.get_order_for_user(
            db,
            "ORD-10001",
            alice.id,
        )

        print(order.order_id, order.status)

        print("\n=== TEST 2: SHIPPING ===")

        shipment = shipping_service.get_shipping_status(
            db,
            "ORD-10003",
            alice.id,
        )

        print(
            shipment.status,
            shipment.tracking_number,
        )

        print("\n=== TEST 3: NOT SHIPPED ===")

        try:
            shipping_service.get_shipping_status(
                db,
                "ORD-10004",
                alice.id,
            )
        except ShipmentNotFoundError as exc:
            print("EXPECTED:", exc)

        print("\n=== TEST 4: RETURN ELIGIBLE ===")

        result = return_service.check_return_eligibility(
            db,
            "ORD-10001",
            alice.id,
        )

        print(result)

        print("\n=== TEST 5: RETURN WINDOW EXPIRED ===")

        result = return_service.check_return_eligibility(
            db,
            "ORD-10002",
            alice.id,
        )

        print(result)

        print("\n=== TEST 6: NOT DELIVERED ===")

        result = return_service.check_return_eligibility(
            db,
            "ORD-10003",
            alice.id,
        )

        print(result)

        print("\n=== TEST 7: EXISTING RETURN ===")

        result = return_service.check_return_eligibility(
            db,
            "ORD-10005",
            alice.id,
        )

        print(result)

        print("\n=== TEST 8: UNAUTHORIZED ORDER ===")

        try:
            order_service.get_order_for_user(
                db,
                "ORD-20001",
                alice.id,
            )
        except OrderAccessDeniedError as exc:
            print("EXPECTED:", exc)

    finally:
        db.close()


if __name__ == "__main__":
    main()