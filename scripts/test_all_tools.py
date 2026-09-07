from backend.tools.registry import TOOLS_BY_NAME


def main():
    tests = [
        (
            "get_order",
            {"order_id": "ORD-10001"},
        ),
        (
            "get_shipping_status",
            {"order_id": "ORD-10003"},
        ),
        (
            "check_return_eligibility",
            {"order_id": "ORD-10001"},
        ),
    ]

    for tool_name, args in tests:
        print(f"\n=== {tool_name} ===")

        result = TOOLS_BY_NAME[tool_name].invoke(args)

        print(result)


if __name__ == "__main__":
    main()