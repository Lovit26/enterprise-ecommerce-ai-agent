import json
from pathlib import Path


BASE_DIR = Path(__file__).parent
REPORT_DIR = BASE_DIR / "reports"


def load_json(filename):
    path = REPORT_DIR / filename

    with open(
        path,
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def main():
    golden = load_json(
        "agent_eval_v1.json"
    )

    challenge = load_json(
        "e2e_challenge_v1.json"
    )

    multiturn = load_json(
        "multiturn_eval_v1.json"
    )

    root_causes = load_json(
        "root_cause_v1.json"
    )

    summary = {
        "version": "V1",
        "evaluation_summary": {
            "golden_set": {
                "cases": golden[
                    "total_cases"
                ],
                "tool_selection_accuracy":
                    golden["metrics"][
                        "tool_selection_accuracy"
                    ],
                "argument_accuracy":
                    golden["metrics"][
                        "argument_accuracy"
                    ],
                "task_success_rate":
                    golden["metrics"][
                        "task_success_rate"
                    ],
                "authorization_safety_rate":
                    golden["metrics"][
                        "authorization_safety_rate"
                    ],
            },

            "challenge_set": {
                "cases": challenge[
                    "total_cases"
                ],
                "task_success_rate":
                    challenge[
                        "task_success_rate"
                    ],
                "authorization_safety_rate":
                    challenge[
                        "authorization_safety_rate"
                    ],
            },

            "multiturn_set": {
                "cases": multiturn[
                    "total_cases"
                ],
                "task_success_rate":
                    multiturn[
                        "task_success_rate"
                    ],
            },
        },

        "root_cause_reviews":
            root_causes,
    }

    output = (
        REPORT_DIR
        / "v1_summary.json"
    )

    with open(
        output,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            summary,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print("=" * 60)
    print("V1 FINAL EVALUATION")
    print("=" * 60)

    print(
        "Golden cases:",
        golden["total_cases"],
    )

    print(
        "Golden task success:",
        f"{golden['metrics']['task_success_rate']:.2%}",
    )

    print(
        "Challenge cases:",
        challenge["total_cases"],
    )

    print(
        "Challenge task success:",
        f"{challenge['task_success_rate']:.2%}",
    )

    print(
        "Challenge safety:",
        f"{challenge['authorization_safety_rate']:.2%}",
    )

    print(
        "Multi-turn cases:",
        multiturn["total_cases"],
    )

    print(
        "Multi-turn task success:",
        f"{multiturn['task_success_rate']:.2%}",
    )

    print(
        "Root-cause reviews:",
        len(root_causes),
    )

    print(
        "\nSaved:",
        output,
    )


if __name__ == "__main__":
    main()