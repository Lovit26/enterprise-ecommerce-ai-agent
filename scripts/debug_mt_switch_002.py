from langchain_core.messages import HumanMessage

from backend.agent.graph import agent_graph


THREAD_ID = "debug-mt-switch-002"

CONFIG = {
    "configurable": {
        "thread_id": THREAD_ID
    }
}


def run_turn(message: str):
    result = agent_graph.invoke(
        {
            "messages": [
                HumanMessage(content=message)
            ]
        },
        config=CONFIG,
    )

    print("\n" + "=" * 70)
    print("USER:")
    print(message)

    print("\nNEW MESSAGES:")

    for msg in result["messages"]:
        print(
            f"\n{type(msg).__name__}:"
        )

        if getattr(msg, "content", None):
            print(msg.content)

        calls = getattr(
            msg,
            "tool_calls",
            None,
        )

        if calls:
            print("TOOL CALLS:")
            print(calls)

    return result


def main():

    run_turn(
        "Where is ORD-10003?"
    )

    run_turn(
        "Check ORD-10001 too."
    )

    run_turn(
        "What was the tracking number for the first one?"
    )


if __name__ == "__main__":
    main()