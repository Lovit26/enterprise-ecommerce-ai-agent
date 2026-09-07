from datetime import datetime, timedelta, timezone
from decimal import Decimal

from backend.db.session import SessionLocal
from backend.models.order import Order
from backend.models.order_item import OrderItem
from backend.models.product import Product
from backend.models.return_request import ReturnRequest
from backend.models.shipment import Shipment
from backend.models.user import User


def seed_database():
    db = SessionLocal()

    try:
        existing_user = db.query(User).first()

        if existing_user:
            print("Database already contains seed data. Skipping.")
            return

        now = datetime.now(timezone.utc)

        # -------------------------------------------------
        # 1. Users
        # -------------------------------------------------

        alice = User(
            user_id="USR-10001",
            email="alice@example.com",
            name="Alice",
        )

        bob = User(
            user_id="USR-20001",
            email="bob@example.com",
            name="Bob",
        )

        db.add_all([alice, bob])
        db.flush()

        # -------------------------------------------------
        # 2. Products
        # -------------------------------------------------

        headphones = Product(
            product_id="PRD-10001",
            name="Sony Noise Cancelling Headphones",
            category="Electronics",
            description="Wireless over-ear noise cancelling headphones.",
            price=Decimal("129.00"),
            stock=50,
            is_active=True,
        )

        keyboard = Product(
            product_id="PRD-10002",
            name="Mechanical Keyboard",
            category="Electronics",
            description="Compact mechanical keyboard with tactile switches.",
            price=Decimal("89.00"),
            stock=35,
            is_active=True,
        )

        mouse = Product(
            product_id="PRD-10003",
            name="Wireless Mouse",
            category="Electronics",
            description="Ergonomic wireless mouse.",
            price=Decimal("39.00"),
            stock=100,
            is_active=True,
        )

        db.add_all([headphones, keyboard, mouse])
        db.flush()

        # -------------------------------------------------
        # 3. Orders for Alice
        # -------------------------------------------------

        order_1 = Order(
            order_id="ORD-10001",
            user_id=alice.id,
            status="delivered",
            total_amount=Decimal("129.00"),
            created_at=now - timedelta(days=10),
        )

        order_2 = Order(
            order_id="ORD-10002",
            user_id=alice.id,
            status="delivered",
            total_amount=Decimal("89.00"),
            created_at=now - timedelta(days=50),
        )

        order_3 = Order(
            order_id="ORD-10003",
            user_id=alice.id,
            status="shipped",
            total_amount=Decimal("39.00"),
            created_at=now - timedelta(days=3),
        )

        order_4 = Order(
            order_id="ORD-10004",
            user_id=alice.id,
            status="processing",
            total_amount=Decimal("129.00"),
            created_at=now - timedelta(days=1),
        )

        order_5 = Order(
            order_id="ORD-10005",
            user_id=alice.id,
            status="delivered",
            total_amount=Decimal("39.00"),
            created_at=now - timedelta(days=8),
        )

        order_6 = Order(
            order_id="ORD-10006",
            user_id=alice.id,
            status="cancelled",
            total_amount=Decimal("89.00"),
            created_at=now - timedelta(days=2),
        )

        # -------------------------------------------------
        # 4. Orders for Bob
        # -------------------------------------------------

        order_7 = Order(
            order_id="ORD-20001",
            user_id=bob.id,
            status="shipped",
            total_amount=Decimal("129.00"),
            created_at=now - timedelta(days=2),
        )

        order_8 = Order(
            order_id="ORD-20002",
            user_id=bob.id,
            status="delivered",
            total_amount=Decimal("89.00"),
            created_at=now - timedelta(days=7),
        )

        orders = [
            order_1,
            order_2,
            order_3,
            order_4,
            order_5,
            order_6,
            order_7,
            order_8,
        ]

        db.add_all(orders)
        db.flush()

        # -------------------------------------------------
        # 5. Order Items
        # -------------------------------------------------

        order_items = [
            OrderItem(
                order_id=order_1.id,
                product_id=headphones.id,
                quantity=1,
                unit_price=Decimal("129.00"),
            ),
            OrderItem(
                order_id=order_2.id,
                product_id=keyboard.id,
                quantity=1,
                unit_price=Decimal("89.00"),
            ),
            OrderItem(
                order_id=order_3.id,
                product_id=mouse.id,
                quantity=1,
                unit_price=Decimal("39.00"),
            ),
            OrderItem(
                order_id=order_4.id,
                product_id=headphones.id,
                quantity=1,
                unit_price=Decimal("129.00"),
            ),
            OrderItem(
                order_id=order_5.id,
                product_id=mouse.id,
                quantity=1,
                unit_price=Decimal("39.00"),
            ),
            OrderItem(
                order_id=order_6.id,
                product_id=keyboard.id,
                quantity=1,
                unit_price=Decimal("89.00"),
            ),
            OrderItem(
                order_id=order_7.id,
                product_id=headphones.id,
                quantity=1,
                unit_price=Decimal("129.00"),
            ),
            OrderItem(
                order_id=order_8.id,
                product_id=keyboard.id,
                quantity=1,
                unit_price=Decimal("89.00"),
            ),
        ]

        db.add_all(order_items)

        # -------------------------------------------------
        # 6. Shipments
        # -------------------------------------------------

        shipments = [
            Shipment(
                shipment_id="SHP-10001",
                order_id=order_1.id,
                carrier="DHL",
                tracking_number="DHL10001",
                status="delivered",
                estimated_delivery=now - timedelta(days=5),
                shipped_at=now - timedelta(days=8),
                delivered_at=now - timedelta(days=5),
            ),
            Shipment(
                shipment_id="SHP-10002",
                order_id=order_2.id,
                carrier="FedEx",
                tracking_number="FDX10002",
                status="delivered",
                estimated_delivery=now - timedelta(days=45),
                shipped_at=now - timedelta(days=48),
                delivered_at=now - timedelta(days=45),
            ),
            Shipment(
                shipment_id="SHP-10003",
                order_id=order_3.id,
                carrier="DHL",
                tracking_number="DHL10003",
                status="in_transit",
                estimated_delivery=now + timedelta(days=2),
                shipped_at=now - timedelta(days=2),
                delivered_at=None,
            ),
            Shipment(
                shipment_id="SHP-10005",
                order_id=order_5.id,
                carrier="UPS",
                tracking_number="UPS10005",
                status="delivered",
                estimated_delivery=now - timedelta(days=4),
                shipped_at=now - timedelta(days=6),
                delivered_at=now - timedelta(days=4),
            ),
            Shipment(
                shipment_id="SHP-20001",
                order_id=order_7.id,
                carrier="DHL",
                tracking_number="DHL20001",
                status="in_transit",
                estimated_delivery=now + timedelta(days=1),
                shipped_at=now - timedelta(days=1),
                delivered_at=None,
            ),
            Shipment(
                shipment_id="SHP-20002",
                order_id=order_8.id,
                carrier="FedEx",
                tracking_number="FDX20002",
                status="delivered",
                estimated_delivery=now - timedelta(days=3),
                shipped_at=now - timedelta(days=5),
                delivered_at=now - timedelta(days=3),
            ),
        ]

        db.add_all(shipments)

        # -------------------------------------------------
        # 7. Existing Return Request
        # -------------------------------------------------

        existing_return = ReturnRequest(
            return_id="RET-10001",
            order_id=order_5.id,
            reason="Product defective",
            status="processing",
            refund_amount=Decimal("39.00"),
        )

        db.add(existing_return)

        db.commit()

        print("Seed data inserted successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()