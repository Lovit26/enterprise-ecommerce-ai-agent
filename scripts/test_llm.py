from backend.llm.provider import get_chat_model


def main():
    model = get_chat_model()

    response = model.invoke(
        "Reply with exactly: LLM connection successful"
    )

    print("Model response:")
    print(response.content)


if __name__ == "__main__":
    main()