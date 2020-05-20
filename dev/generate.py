from random import choices
from pathlib import Path
from csv import DictReader
from typing import Iterator


def name_list() -> Iterator[dict]:
    path = Path("Names_2010Census.csv")

    if not path.is_file():
        raise FileNotFoundError(f"'{path}' is not a file")

    with path.open() as f:
        dreader = DictReader(f)
        for row in dreader:
            yield row


def main() -> None:
    names, proportions = [(row["name"], row["prop100k"]/100_000) for row in name_list()]


if __name__ == "__main__":
    main()
