from random import choices, randint
from pathlib import Path
from csv import DictReader
from typing import Iterator, List, Callable
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


def rand_names() -> Callable[[int], List[str]]:
    letter_counts = Counter("".join([row["name"].lower() for row in name_list()]))
    total_count = sum(letter_counts[letter] for letter in letter_counts)
    weights = [letter_counts[letter] / total_count for letter in letter_counts]
    name = lambda x: "".join(
        choices(list(letter_counts.keys()), weights=weights, k=x)
    ).capitalize()

    def randlist(count: int) -> List[str]:
        return list(name(randint(3, 8)) for i in range(count))

    return randlist


randlist = rand_names()
printlist = lambda x: print(*randlist(x), sep="\n")


def main() -> None:
    printlist(100)


if __name__ == "__main__":
    main()
