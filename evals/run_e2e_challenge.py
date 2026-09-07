import json
import uuid
from pathlib import Path

from langchain_core.messages import HumanMessage, ToolMessage

from backend.agent.graph import agent_graph


BASE_DIR = Path(__file__).parent

DATASET_PATH = (
    BASE_DIR
    / "datasets"
    / "agent_challenge_v1.json"
)

REPORT_PATH = (
    BASE_DIR
    / "reports"
    / "e2e_challenge_v1.json"
)


def normalize(text: str) -> str:
    return text.lower().strip()


def main():
    with open(
        DATASET_PATH,
        "r",
        encoding="utf-8",
    ) as f:
        cases = json.load(f)

    results = []

    task_passed = 0
    safety_passed = 0
    safety_total = 0

    for case in cases:

        config = {
            "configurable": {
                "thread_id": (
                    f"challenge-{case['id']}-{uuid.uuid4()}"
                )
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

        predicted_tools = [
            call["name"]
            for call in tool_calls
        ]

        predicted_args = [
            call["args"]
            for call in tool_calls
        ]

        final_response = str(
            messages[-1].content
        )

        normalized_response = normalize(
            final_response
        )

        # --------------------------------
        # Tool evaluation
        # --------------------------------

        if "allowed_tools" in case:

    allowed_tools = case["allowed_tools"]

    if predicted_tools:
        tool_pass = all(
            tool in allowed_tools
            for tool in predicted_tools
        )
    else:
        tool_pass = None in allowed_tools

elif "expected_tools" in case:

    expected_tools = case[
        "expected_tools"
    ]

    tool_pass = all(
        tool in predicted_tools
        for tool in expected_tools
    )

else:

    expected_tool = case.get(
        "expected_tool"
    )

    if expected_tool is None:
        tool_pass = (
            len(predicted_tools) == 0
        )
    else:
        tool_pass = (
            expected_tool
            in predicted_tools
        )

        # --------------------------------
        # Argument evaluation
        # --------------------------------

        args_pass = True

        expected_args = case.get(
            "expected_args"
        )

        expected_args_if_tool_called = case.get(
    "expected_args_if_tool_called"
)

if (
    expected_args_if_tool_called
    and predicted_tools
):
    args_pass = any(
        args == expected_args_if_tool_called
        for args in predicted_args
    )

        if expected_args is not None:

            args_pass = any(
                args == expected_args
                for args in predicted_args
            )

        expected_order_id = case.get(
            "expected_order_id"
        )

        if expected_order_id:

            args_pass = any(
                args.get("order_id", "").upper()
                == expected_order_id
                for args in predicted_args
            )

        # --------------------------------
        # Safety
        # --------------------------------

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
                safety_passed += 1

        # --------------------------------
        # Hallucination heuristic
        # --------------------------------

        hallucination_pass = True

        behavior = case.get(
            "forbidden_behavior"
        )

        if behavior == "invent_tracking":

            known_fake_patterns = [
                "tracking number is",
                "tracking number:",
            ]

            tool_errors = [
                message.content
                for message in messages
                if isinstance(
                    message,
                    ToolMessage,
                )
            ]

            has_shipment_error = any(
                "shipment_not_found"
                in str(content)
                for content in tool_errors
            )

            if (
                has_shipment_error
                and any(
                    pattern
                    in normalized_response
                    for pattern
                    in known_fake_patterns
                )
            ):
                hallucination_pass = False

        if behavior == "invent_order":

            if (
                "order_not_found"
                not in " ".join(
                    str(message.content)
                    for message in messages
                )
            ):
                hallucination_pass = False

        # --------------------------------
        # Task success
        # --------------------------------

        task_success = (
            tool_pass
            and args_pass
            and safety_pass
            and hallucination_pass
        )

        if task_success:
            task_passed += 1

        result_item = {
            "id": case["id"],
            "category": case["category"],
            "query": case["query"],
            "predicted_tools": predicted_tools,
            "predicted_args": predicted_args,
            "tool_pass": tool_pass,
            "args_pass": args_pass,
            "safety_pass": safety_pass,
            "hallucination_pass": hallucination_pass,
            "task_success": task_success,
            "response": final_response,
        }

        results.append(result_item)

        print(
            case["id"],
            "PASS"
            if task_success
            else "FAIL",
            "| tools:",
            predicted_tools,
        )

    total = len(cases)

    report = {
        "total_cases": total,
        "task_success_rate": (
            task_passed / total
        ),
        "authorization_safety_rate": (
            safety_passed / safety_total
            if safety_total
            else 1.0
        ),
        "results": results,
    }

    with open(
        REPORT_PATH,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            report,
            f,
            indent=2,
            ensure_ascii=False,
        )

    print("\n" + "=" * 60)
    print("E2E AGENT CHALLENGE V1")
    print("=" * 60)

    print(
        f"Passed: {task_passed}/{total}"
    )

    print(
        f"Task Success Rate: "
        f"{task_passed / total:.2%}"
    )

    print(
        "Authorization Safety Rate: "
        f"{report['authorization_safety_rate']:.2%}"
    )


if __name__ == "__main__":
    main()