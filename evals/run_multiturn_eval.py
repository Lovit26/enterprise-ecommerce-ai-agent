import json
import uuid
from pathlib import Path

from langchain_core.messages import HumanMessage

from backend.agent.graph import agent_graph


BASE_DIR = Path(__file__).parent

DATASET_PATH = (
    BASE_DIR
    / "datasets"
    / "multiturn_v1.json"
)

REPORT_PATH = (
    BASE_DIR
    / "reports"
    / "multiturn_eval_v1.json"
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
    passed = 0

    for case in dataset:

        thread_id = (
            f"mt-{case['id']}-{uuid.uuid4()}"
        )

        config = {
            "configurable": {
                "thread_id": thread_id
            }
        }

        previous_message_count = 0
        final_turn_tools = []
        final_turn_args = []
        final_response = ""

        for turn in case["turns"]:

            result = agent_graph.invoke(
                {
                    "messages": [
                        HumanMessage(content=turn)
                    ]
                },
                config=config,
            )

            messages = result["messages"]

            new_messages = messages[
                previous_message_count:
            ]

            previous_message_count = len(messages)

            final_turn_tools = []
            final_turn_args = []

            for message in new_messages:
                calls = getattr(
                    message,
                    "tool_calls",
                    None,
                )

                if calls:
                    for call in calls:
                        final_turn_tools.append(
                            call["name"]
                        )
                        final_turn_args.append(
                            call["args"]
                        )

            final_response = str(
                messages[-1].content
            )

        # -----------------------------
        # Tool check
        # -----------------------------

        tool_pass = True

        allowed_tools = case.get(
            "allowed_final_tools"
        )

        expected_tool = case.get(
            "expected_final_tool"
        )

        if allowed_tools is not None:
            if final_turn_tools:
                tool_pass = all(
                    tool in allowed_tools
                    for tool in final_turn_tools
                )
            else:
                tool_pass = None in allowed_tools

        elif expected_tool:
            tool_pass = (
                expected_tool
                in final_turn_tools
            )

        elif case.get("expected_no_tool"):
            tool_pass = (
                len(final_turn_tools) == 0
            )

        # -----------------------------
        # Argument check
        # -----------------------------

        args_pass = True

        expected_order_id_if_tool_called = case.get(
        "expected_final_order_id_if_tool_called"
    )

    if (
        expected_order_id_if_tool_called
        and final_turn_tools
    ):
        args_pass = any(
            args.get(
                "order_id",
                ""
            ).upper()
            == expected_order_id_if_tool_called
            for args in final_turn_args
        )

        # -----------------------------
        # Final facts
        # -----------------------------

        normalized_response = normalize(
            final_response
        )

        expected_facts = case.get(
            "expected_final_facts",
            [],
        )

        facts_pass = all(
            normalize(fact)
            in normalized_response
            for fact in expected_facts
        )

        # -----------------------------
        # Safety
        # -----------------------------

        forbidden_facts = case.get(
            "forbidden_final_facts",
            [],
        )

        safety_pass = all(
            normalize(fact)
            not in normalized_response
            for fact in forbidden_facts
        )

        success = (
            tool_pass
            and args_pass
            and facts_pass
            and safety_pass
        )

        if success:
            passed += 1

        item = {
            "id": case["id"],
            "category": case["category"],
            "turns": case["turns"],
            "final_tools": final_turn_tools,
            "final_args": final_turn_args,
            "final_response": final_response,
            "tool_pass": tool_pass,
            "args_pass": args_pass,
            "facts_pass": facts_pass,
            "safety_pass": safety_pass,
            "task_success": success,
        }

        results.append(item)

        print(
            case["id"],
            "PASS" if success else "FAIL",
            "| tools:",
            final_turn_tools,
            "| args:",
            final_turn_args,
        )

    total = len(dataset)

    report = {
        "dataset": "multiturn_v1",
        "total_cases": total,
        "passed": passed,
        "task_success_rate": (
            passed / total
        ),
        "results": results,
    }

    with open(
        REPORT_PATH,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            report,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print("\n" + "=" * 60)
    print("MULTI-TURN AGENT EVALUATION V1")
    print("=" * 60)

    print(
        f"Passed: {passed}/{total}"
    )

    print(
        f"Task Success Rate: "
        f"{passed / total:.2%}"
    )


if __name__ == "__main__":
    main()