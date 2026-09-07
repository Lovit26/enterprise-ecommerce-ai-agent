import json
import uuid
from pathlib import Path

from langchain_core.messages import HumanMessage

from backend.agent.graph import agent_graph


BASE_DIR = Path(__file__).parent

DATASET_PATH = (
    BASE_DIR
    / "datasets"
    / "agent_golden_v1.json"
)

REPORT_DIR = BASE_DIR / "reports"

REPORT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


def normalize(text: str) -> str:
    return text.lower().strip()


def main():
    with open(
        DATASET_PATH,
        "r",
        encoding="utf-8",
    ) as file:
        dataset = json.load(file)

    results = []

    tool_correct = 0
    args_correct = 0
    task_success = 0
    safety_success = 0
    safety_total = 0

    for case in dataset:

        thread_id = (
            f"eval-{case['id']}-{uuid.uuid4()}"
        )

        config = {
            "configurable": {
                "thread_id": thread_id
            }
        }

        result = agent_graph.invoke(
            {
                "messages": [
                    HumanMessage(
                        content=case["query"]
                    )
                ]
            },
            config=config,
        )

        messages = result["messages"]

        tool_calls = []

        for message in messages:
            calls = getattr(
                message,
                "tool_calls",
                None,
            )

            if calls:
                tool_calls.extend(calls)

        if tool_calls:
            predicted_tool = (
                tool_calls[0]["name"]
            )

            predicted_args = (
                tool_calls[0]["args"]
            )

        else:
            predicted_tool = None
            predicted_args = None

        expected_tool = case[
            "expected_tool"
        ]

        expected_args = case[
            "expected_args"
        ]

        tool_pass = (
            predicted_tool
            == expected_tool
        )

        if tool_pass:
            tool_correct += 1

        args_pass = (
            predicted_args
            == expected_args
        )

        if expected_tool is None:
            args_pass = True

        if args_pass:
            args_correct += 1

        final_response = str(
            messages[-1].content
        )

        normalized_response = normalize(
            final_response
        )

        expected_facts = case.get(
            "expected_facts",
            [],
        )

        facts_pass = all(
            normalize(fact)
            in normalized_response
            for fact in expected_facts
        )

        forbidden_facts = case.get(
            "forbidden_facts",
            [],
        )

        safety_pass = all(
            normalize(fact)
            not in normalized_response
            for fact in forbidden_facts
        )

        if forbidden_facts:
            safety_total += 1

            if safety_pass:
                safety_success += 1

        case_success = (
            tool_pass
            and args_pass
            and facts_pass
            and safety_pass
        )

        if case_success:
            task_success += 1

        result_item = {
            "id": case["id"],
            "category": case[
                "category"
            ],
            "query": case["query"],
            "expected_tool": expected_tool,
            "predicted_tool": predicted_tool,
            "expected_args": expected_args,
            "predicted_args": predicted_args,
            "tool_pass": tool_pass,
            "args_pass": args_pass,
            "facts_pass": facts_pass,
            "safety_pass": safety_pass,
            "task_success": case_success,
            "response": final_response,
        }

        results.append(result_item)

        print("=" * 70)
        print("ID:", case["id"])
        print("QUERY:", case["query"])
        print(
            "EXPECTED TOOL:",
            expected_tool,
        )
        print(
            "PREDICTED TOOL:",
            predicted_tool,
        )
        print(
            "TASK:",
            "PASS"
            if case_success
            else "FAIL",
        )

    total = len(dataset)

    report = {
        "dataset": "agent_golden_v1",
        "total_cases": total,
        "metrics": {
            "tool_selection_accuracy": (
                tool_correct / total
            ),
            "argument_accuracy": (
                args_correct / total
            ),
            "task_success_rate": (
                task_success / total
            ),
            "authorization_safety_rate": (
                safety_success / safety_total
                if safety_total
                else 1.0
            ),
        },
        "results": results,
    }

    report_path = (
        REPORT_DIR
        / "agent_eval_v1.json"
    )

    with open(
        report_path,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            report,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print("\n" + "=" * 70)
    print("AGENT EVALUATION V1")
    print("=" * 70)

    print(
        f"Tool Selection Accuracy: "
        f"{tool_correct / total:.2%}"
    )

    print(
        f"Argument Accuracy: "
        f"{args_correct / total:.2%}"
    )

    print(
        f"Task Success Rate: "
        f"{task_success / total:.2%}"
    )

    if safety_total:
        print(
            "Authorization Safety Rate: "
            f"{safety_success / safety_total:.2%}"
        )

    print(
        f"\nReport saved to: "
        f"{report_path}"
    )


if __name__ == "__main__":
    main()
    