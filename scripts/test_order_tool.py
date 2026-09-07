from backend.tools.order_tools import get_order


def main():
    print("\n=== TEST 1: OWN ORDER ===")

    result = get_order.invoke(
        {"order_id": "ORD-10001"}
    )

    print(result)

    print("\n=== TEST 2: NOT FOUND ===")

    result = get_order.invoke(
        {"order_id": "ORD-99999"}
    )

    print(result)

    print("\n=== TEST 3: ACCESS DENIED ===")

    result = get_order.invoke(
        {"order_id": "ORD-20001"}
    )

    print(result)


if __name__ == "__main__":
    main()