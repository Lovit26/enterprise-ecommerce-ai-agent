import json
from pathlib import Path


BASE_DIR = Path(__file__).parent

REPORT_PATH = (
    BASE_DIR
    / "reports"
    / "agent_eval_v1.json"
)

BADCASE_PATH = (
    BASE_DIR
    / "reports"
    / "badcases_v1.json"
)


def classify_failure(result):
    failures = []

    if not result["tool_pass"]:
        failures.append(
            "tool_selection"
        )

    if not result["args_pass"]:
        failures.append(
            "argument_extraction"
        )

    if not result["facts_pass"]:
        failures.append(
            "answer_correctness"
        )

    if not result["safety_pass"]:
        failures.append(
            "authorization_safety"
        )

    return failures


def main():
    with open(
        REPORT_PATH,
        "r",
        encoding="utf-8",
    ) as file:
        report = json.load(file)

    badcases = []

    for result in report["results"]:

        if result["task_success"]:
            continue

        result["failure_types"] = (
            classify_failure(result)
        )

        badcases.append(result)

    with open(
        BADCASE_PATH,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            badcases,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print(
        f"Badcases: "
        f"{len(badcases)}"
    )

    print(
        f"Saved to: "
        f"{BADCASE_PATH}"
    )


if __name__ == "__main__":
    main()