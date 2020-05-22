#!/usr/bin/env python
import json
import sys
import typing
from collections import Counter, deque
from csv import DictReader
from itertools import accumulate, islice
from pathlib import Path
from random import choices, randint
from re import compile as re_compile
from string import ascii_lowercase
from typing import (
    Any,
    Callable,
    Deque,
    Dict,
    Iterator,
    List,
    Optional,
    TypedDict,
    TypeVar,
    Union,
)

assert sys.version_info >= (
    3,
    8,
), f"Python 3.8 or higher required\ndetected version: {sys.version}"


default_config_file = "./generate_config.json"
SPath = Union[str, Path]


class Config(TypedDict):
    min_length: int
    max_length: int
    letter_weights: Dict[str, float]


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
default_config: Config = {
    "max_length": 8,
    "min_length": 3,
    "letter_weights": default_weights,
}


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


def rand_name(length: int, weights: Dict[str, float]) -> str:
    sample_of_letters = choices(
        list(weights.keys()), weights=list(weights.values()), k=length
    )
    return "".join(sample_of_letters).capitalize()


def rand_names(
    min_length: int = 3,
    max_length: int = 8,
    weights: Dict[str, float] = default_weights,
) -> Iterator[str]:
    while True:
        yield rand_name(length=randint(min_length, max_length), weights=weights)


def rand_list(
    count: int, min_length: int, max_length: int, weights: Dict[str, float]
) -> List[str]:
    return list(
        islice(
            rand_names(min_length=min_length, max_length=max_length, weights=weights),
            count,
        )
    )


def printlist(names: List[str]) -> None:
    print(*names, sep="\n")


def find_unique_prefixes(options: List[str]) -> Dict[str, str]:
    if len(set(options)) != len(options):
        duplicates = ", ".join(filter(lambda s: options.count(s) > 1, options))
        raise ValueError(f"Can't have duplicate items!\n{duplicates}")

    # Create an unlinked copy for this destructive algorithm
    options_duplicate = list(options)
    unique_prefixes: Dict[str, str] = dict()
    options_duplicate.sort()
    while options_duplicate:
        for i, option in enumerate(options_duplicate):
            options_copy = list(options_duplicate)
            del options_copy[i]
            for prefix in accumulate(option):
                if not list(filter(lambda s: s.startswith(prefix), options_copy)):
                    if option in unique_prefixes:
                        raise ValueError(
                            f"""Somehow found duplicate prefix:
options:
{options}
options_duplicate:
{options_duplicate}
option: {option}
prefix: {prefix}
unique_prefixes:
{unique_prefixes}"""
                        )
                    unique_prefixes[option] = prefix
                    break

        for option in unique_prefixes:
            if option in options_duplicate:
                index = options_duplicate.index(option)
                del options_duplicate[index]

    # Recreate dictionary to ensure order of options
    return {option: unique_prefixes[option] for option in options}


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
            print(f"'{option}' too ambiguous for '{option_string}'")
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


def input_type(
    prompt: str = "", convert: Callable[[str], Any] = str, default: Optional[Any] = None
) -> Any:
    resolved: Any = None
    for i in range(default_tries):
        typed = input(prompt)
        if not typed and default is None:
            raise ValueError("No value given; no default given")
        elif not typed:
            return default

        try:
            resolved = convert(typed)
        except ValueError:
            print(f"'{typed}' is not an '{convert.__name__}'")
            continue
        break
    if resolved is None:
        raise ValueError("No value given; no default given")

    return resolved


def valid_config(config: Config) -> Config:
    """Returns unmodified config if it's valid
    if it's invalid, raises ValueError"""
    extra_keys = set(config.keys()) - set(default_config.keys())
    if extra_keys:
        extra_keys_string = ", ".join(f"'{key}'" for key in extra_keys)
        raise ValueError(f"These keys are not necessary: {extra_keys_string}")
    for key in default_config:
        if key not in config:
            raise ValueError(f"Missing config key: '{key}'")
        if not isinstance(config[key], type(default_config[key])):
            raise ValueError(
                f"Type of value for '{key}' does not match: {type(config[key])} =/= {type(default_config[key])}"
            )
        # NOTE: Does not recurse into dictionaries
        # if isinstance(config[key], dict):

    return config


def ask_for_config(defaults: Config = default_config) -> Config:
    config: Config = dict()
    print(
        f"""For each value that needs to be configured, the name of the key will be shown wrapped in quotes,
then the default value in brackets.
For example:
"example_key" ["example_value"] >>
The response must look like the default value; in this case, it must be an 'str'

"""
    )
    needed_keys: Deque[List[str]] = deque([key] for key in defaults.keys())
    while needed_keys:
        keys = needed_keys.pop()
        if not keys:
            raise ValueError(
                f"""Somehow got an empty list for a key:
needed_keys:
{needed_keys}
defaults:
{defaults}
"""
            )
        sub_dict = defaults
        for key in keys[:-1]:
            sub_dict = sub_dict[key]
        key = keys[-1]
        default_value = sub_dict[key]

        if isinstance(default_value, dict):
            for key in default_value:
                new_keys = list(keys)
                new_keys.append(key)
                needed_keys.append(new_keys)
            continue

        keys_string = ".".join(keys)
        typed = input_type(
            f'"{keys_string}" [{default_value}] >> ',
            type(default_value),
            default=default_value,
        )
        sub_dict = config
        for key in keys[:-1]:
            if key not in sub_dict:
                sub_dict[key] = dict()
            sub_dict = sub_dict[key]
        sub_dict[keys[-1]] = typed

    return config


def create_config(path: SPath = default_config_file) -> Config:
    we_want_to_configure = (
        input_options("Do you want to change the configuration?", ["yes", "no"])
        == "yes"
    )
    config_file = Path(path).resolve()
    if not we_want_to_configure and config_file.exists():
        return valid_config(read_config(config_file))
    elif not we_want_to_configure:
        return valid_config(default_config)
    else:
        config = valid_config(ask_for_config(defaults=default_config))

    config_string = json.dumps(config, sort_keys=True, indent=4)
    print(config_string)
    write_config = input_options(
        f"""
        Write above to '{default_config_file}' for future runs?
        If 'no', configuration will be forgotten when program ends
    """.lstrip(),
        ["yes", "no"],
    )
    if write_config == "yes":
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

    return valid_config(config)


def main() -> None:
    config = create_config(default_config_file)

    num = 1
    print("Type anything except a number to quit")
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
                weights=config["letter_weights"],
            )
        )


if __name__ == "__main__":
    main()
