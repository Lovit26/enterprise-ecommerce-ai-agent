from backend.agent.checkpoint import (
    setup_checkpoint_database,
)


def main():
    setup_checkpoint_database()

    print(
        "PostgreSQL checkpoint tables created successfully."
    )


if __name__ == "__main__":
    main()