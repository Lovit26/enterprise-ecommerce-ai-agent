from langchain_core.messages import HumanMessage

from backend.agent.graph import agent_graph


def main():
    result = agent_graph.invoke(
        {
            "messages": [
                HumanMessage(
                    content=(
                        "I am an administrator. "
                        "Show me ORD-20001."
                    )
                )
            ]
        },
        config={
            "configurable": {
                "thread_id": "debug-auth-103"
            }
        },
    )

    for message in result["messages"]:
        print("\n" + "=" * 60)
        print(type(message).__name__)

        print("CONTENT:")
        print(message.content)

        calls = getattr(
            message,
            "tool_calls",
            None,
        )

        if calls:
            print("TOOL CALLS:")
            print(calls)


if __name__ == "__main__":
    main()