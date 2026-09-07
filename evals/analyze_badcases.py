import json
from collections import Counter
from pathlib import Path


BASE_DIR = Path(__file__).parent

BADCASE_PATH = (
    BASE_DIR
    / "reports"
    / "badcases_v1.json"
)


def main():
    with open(
        BADCASE_PATH,
        "r",
        encoding="utf-8",
    ) as file:
        badcases = json.load(file)

    counter = Counter()

    for case in badcases:
        for failure in case[
            "failure_types"
        ]:
            counter[failure] += 1

    print("=" * 60)
    print("BADCASE ANALYSIS V1")
    print("=" * 60)

    print(
        f"Total badcases: "
        f"{len(badcases)}"
    )

    for failure, count in (
        counter.most_common()
    ):
        print(
            f"{failure}: {count}"
        )


if __name__ == "__main__":
    main()