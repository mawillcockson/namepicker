import json
import sys
import typing
from collections import Counter
from csv import DictReader
from itertools import islice
from pathlib import Path
from random import choices, randint
from re import compile as re_compile
from string import ascii_lowercase
from typing import Callable, Dict, Iterator, List, Optional, TypeVar, Union

default_config_file = "./generate_config.json"
SPath = Union[str, Path]
default_weights = {
    "s": 0.05800358317132825,
    "m": 0.03276713552844685,
    "i": 0.06886568071833632,
    "t": 0.046164579438341,
    "h": 0.03519344426803398,
    "j": 0.003906738259174453,
    "o": 0.06485788319854333,
    "n": 0.07019629431648038,
    "w": 0.01231504603958509,
    "l": 0.06380385283998684,
    "a": 0.10270900872389635,
    "b": 0.026101656751334825,
    "r": 0.08029246904616902,
    "e": 0.11029909108719375,
    "g": 0.026668120501643987,
    "c": 0.036400836487002805,
    "d": 0.03011920560329276,
    "v": 0.011086378186801837,
    "u": 0.030633366753808115,
    "z": 0.01296483935566743,
    "p": 0.016939836939996507,
    "y": 0.015048078499996898,
    "k": 0.02940203944679806,
    "f": 0.012995866321646805,
    "x": 0.000983111579175055,
    "q": 0.0012800839678347876,
    " ": 1.7729694845357168e-06,
}
default_tries: int = 3


def name_list() -> Iterator[str]:
    """Parses names out of file linked from:
    https://www.census.gov/topics/population/genealogy/data/2010_surnames.html"""

    path = Path("Names_2010Census.csv").resolve()

    if not path.is_file():
        raise FileNotFoundError(f"'{path}' is not a file")

    with path.open() as f:
        dreader = DictReader(f)
        for row in dreader:
            yield row["name"].lower()


def letter_weights() -> Dict[str, float]:
    letter_counts: typing.Counter[str] = Counter()
    for name in name_list():
        letter_counts.update(name)

    total_num_letters = sum(letter_counts[letter] for letter in letter_counts)
    return {
        letter: (letter_counts[letter] / total_num_letters) for letter in letter_counts
    }


def rand_name(length: int) -> str:
    weights = default_weights
    sample_of_letters = choices(
        list(weights.keys()), weights=list(weights.values()), k=length
    )
    return "".join(sample_of_letters).capitalize()


def rand_names(min_length: int = 3, max_length: int = 8) -> Iterator[str]:
    while True:
        yield rand_name(randint(min_length, max_length))


def rand_list(count: int, min_length: int, max_length: int) -> List[str]:
    return list(islice(rand_names(min_length=min_length, max_length=max_length), count))


def printlist(names: List[str]) -> None:
    print(*names, sep="\n")


def find_unique_prefixes(options: List[str]) -> Dict[str, str]:
    pass


def input_options(
    prompt: str = "", options: Optional[List[str]] = None, default: Optional[str] = None
) -> str:
    """Case-insensitive input() helper function"""
    if not options:
        return input(prompt)

    if default and (default not in options):
        raise ValueError(f"'{default}' missing from options: {options}")
    if not all(options):
        raise ValueError("Empty string cannot be used as an option")

    option_prefixes = find_unique_prefixes(options)
    option_string = " ".join(
        f"[{ option_prefixes[option].upper() }]{ option.replace(option_prefixes[option], '') }"
        for option in option_prefixes
    )

    def find_matching_option(option: str) -> str:
        matching_options = list(
            filter(lambda s: s.startswith(option), option_prefixes.keys())
        )
        if len(matching_options) < 1:
            print(f"'{option}' does not match any of '{option_string}'")
            return ""
        elif len(matching_options) == 1:
            return matching_options[0]
        else:
            print(f"'{option} too ambiguous for '{option_string}'")
            return ""

    typed = ""
    for i in range(default_tries):
        typed = input(f"{prompt} {option_string} >> ").lower()
        matching_option = find_matching_option(typed)
        if not matching_option:
            typed = ""
            continue
        else:
            typed = matching_option
            break

    if not typed:
        sys.exit(f"Number of tries exceeded")

    return typed


T = TypeVar("T")
ValueParser = Union[float, int, str, Callable[[str], T]]


def input_type(prompt: str = "", type: ValueParser = str) -> T:
    pass


Config = Dict[str, int]


def valid_config(config: Config) -> bool:
    pass

def ask_for_config() -> Config:
    min_length = input_type(f"How long is the shortest name? [3] >> ", int)
    max_length = input_type(f"How long is the longest name?  [8] >> ", int)
    return {
        "min_length": min_length,
        "max_length": max_length,
    }



def create_config(path: SPath = default_config_file) -> Config:
    config_file = Path(path).resolve()
    if config_file.exists():
        overwrite = input_options(
            f"'{config_file.resolve()}' already exists. Overwrite?", ["yes", "no"]
        ).lower()
        if overwrite == "no":
            return read_config(config_file)

    config = ask_for_config()

    config_string = json.dumps(config, sort_keys=True, indent=4)
    print(config_string)
    write_config = input_options(
        f"""
        Write above to '{default_config_file}' for future runs?
        If 'no', configuration will be forgotten when program ends
    """.lstrip(),
        ["yes", "no"],
    )
    if write_config:
        for parent in config_file.parents:
            if parent.exists() and not parent.is_dir():
                raise FileExistsError(
                    f"'{parent}' is not a folder, but is used as a folder in '{config_file}'"
                )
            if not parent.exists():
                parent.mkdir()

        config_file.write_text(config_string)

    return config


def read_config(path: SPath = default_config_file) -> Config:
    config_file = Path(path).resolve()

    if not config_file.exists():
        return create_config(config_file)

    if not config_file.is_file():
        raise FileNotFoundError(f"'{config_file}' is not a file")

    try:
        contents = config_file.read_text()
    except UnicodeError as err:
        raise UnicodeError(f"Can't read file: '{config_file}'") from err

    config = json.loads(contents)

    if not valid_config(config):
        raise ValueError(
            f"Problem with configuration:\nInterpreted\n{config}\n\nFile Contents\n{contents}"
        )

    return config


def main() -> None:
    config = read_config(default_config_file)

    num = 1
    while True:
        typed = input(f"Number of names? [{num}] >> ")
        if typed.isdecimal():
            try:
                num = int(typed)
            except ValueError:
                pass
        elif typed != "":
            sys.exit(0)

        printlist(
            names=rand_list(
                count=num,
                min_length=config["min_length"],
                max_length=config["max_length"],
            )
        )


if __name__ == "__main__":
    main()
