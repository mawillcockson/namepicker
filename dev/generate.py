from random import choices, randint
from pathlib import Path
from csv import DictReader
from typing import Iterator
from re import compile as re_compile
from string import ascii_lowercase
from collections import Counter


def name_list() -> Iterator[dict]:
    path = Path("Names_2010Census.csv")

    if not path.is_file():
        raise FileNotFoundError(f"'{path}' is not a file")

    with path.open() as f:
        dreader = DictReader(f)
        for row in dreader:
            yield row


def main() -> None:
    letter_counts = Counter("".join([row["name"].lower() for row in name_list()]))
    total_count = sum(letter_counts[letter] for letter in letter_counts)
    weights = [letter_counts[letter]/total_count for letter in letter_counts]
    name = lambda x: "".join(choices(list(letter_counts.keys()), weights=weights, k=x)).capitalize()
    rand20 = lambda:print(*(name(randint(3, 8)) for i in range(20)), sep="\n")
    rand20()
    breakpoint()


if __name__ == "__main__":
    main()
