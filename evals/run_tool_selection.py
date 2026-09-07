import json
from pathlib import Path

from backend.llm.provider import get_chat_model
from backend.tools.registry import TOOLS


DATASET_PATH = (
    Path(__file__).parent
    / "tool_selection_v1.json"
)


def main():
    with open(
        DATASET_PATH,
        "r",
        encoding="utf-8",
    ) as file:
        dataset = json.load(file)

    model = get_chat_model().bind_tools(TOOLS)

    correct = 0

    for case in dataset:
        response = model.invoke(case["query"])

        if response.tool_calls:
            predicted_tool = response.tool_calls[0]["name"]
        else:
            predicted_tool = None

        expected_tool = case["expected_tool"]

        passed = predicted_tool == expected_tool

        if passed:
            correct += 1

        print("=" * 70)
        print("QUERY:", case["query"])
        print("EXPECTED:", expected_tool)
        print("PREDICTED:", predicted_tool)
        print("RESULT:", "PASS" if passed else "FAIL")

    total = len(dataset)
    accuracy = correct / total

    print("\n" + "=" * 70)
    print("TOOL SELECTION BENCHMARK")
    print("=" * 70)
    print(f"Correct: {correct}/{total}")
    print(f"Accuracy: {accuracy:.2%}")


if __name__ == "__main__":
    main()