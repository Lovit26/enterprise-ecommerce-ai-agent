from backend.llm.provider import get_chat_model
from backend.tools.order_tools import get_order


def main():
    model = get_chat_model()

    model_with_tools = model.bind_tools(
        [get_order]
    )

    response = model_with_tools.invoke(
        "What is the status of order ORD-10001?"
    )

    print("Content:")
    print(response.content)

    print("\nTool calls:")
    print(response.tool_calls)


if __name__ == "__main__":
    main()