import json
from pathlib import Path

from backend.llm.provider import get_chat_model
from backend.tools.registry import TOOLS


DATASET = (
    Path(__file__).parent
    / "datasets"
    / "agent_challenge_v1.json"
)


def main():
    with open(DATASET, encoding="utf-8") as f:
        cases = json.load(f)

    model = get_chat_model().bind_tools(TOOLS)

    total = 0
    passed = 0
    badcases = []

    for case in cases:
        if "expected_tools" in case:
            continue

        if "expected_tool" not in case:
            continue

        total += 1

        response = model.invoke(case["query"])

        predicted = (
            response.tool_calls[0]["name"]
            if response.tool_calls
            else None
        )

        if "allowed_tools" in case:
            allowed_tools = case["allowed_tools"]
            ok = predicted in allowed_tools
            expected = allowed_tools
        else:
            expected = case["expected_tool"]
            ok = predicted == expected

        if ok:
            passed += 1
        else:
            badcases.append(
                {
                    "id": case["id"],
                    "query": case["query"],
                    "expected": expected,
                    "predicted": predicted,
                    "failure_type": "tool_selection"
                }
            )

        print(
            case["id"],
            "PASS" if ok else "FAIL",
            "| expected:",
            expected,
            "| predicted:",
            predicted,
        )

    accuracy = passed / total

    print("\n" + "=" * 60)
    print("CHALLENGE ROUTING")
    print("=" * 60)
    print(f"Passed: {passed}/{total}")
    print(f"Accuracy: {accuracy:.2%}")
    print(f"Badcases: {len(badcases)}")

    output = (
        Path(__file__).parent
        / "reports"
        / "challenge_routing_badcases.json"
    )

    with open(
        output,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            badcases,
            f,
            indent=2,
            ensure_ascii=False,
        )


if __name__ == "__main__":
    main()