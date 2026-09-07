from langchain_core.messages import HumanMessage

from backend.agent.graph import agent_graph


def chat(thread_id: str, message: str):
    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    result = agent_graph.invoke(
        {
            "messages": [
                HumanMessage(content=message)
            ]
        },
        config=config,
    )

    final_message = result["messages"][-1]

    print("\nUSER:")
    print(message)

    print("\nASSISTANT:")
    print(final_message.content)

    return result


def main():
    thread_id = "test-conversation-001"

    chat(
        thread_id,
        "Where is order ORD-10003?",
    )

    chat(
        thread_id,
        "Can I return it?",
    )

    chat(
    "test-conversation-002",
    "Can I return it?",
)


if __name__ == "__main__":
    main()

