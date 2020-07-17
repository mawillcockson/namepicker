"""
Main file to run the program
"""

import atexit
import logging
import sys
from argparse import ArgumentParser, ArgumentTypeError, Namespace
from datetime import datetime, timedelta
from enum import IntEnum
from pathlib import Path
from typing import Dict, NamedTuple, Tuple, Union
from warnings import warn

# from database_interface import save_lists, save_names, select_lists, select_names


# Record loglevel name in the logging module (e.g. WARNING, INFO, etc)
# mypy doesn't believe the type declaration Dict[str, int]
# log_attr = partial(getattr, logging)
# log_levels = {
#     name: log_attr(name)
#     for name in dir(logging)
#     if isinstance(log_attr(name), int) and not isinstance(log_attr(name), bool)
# }
def map_logging_level_names_to_values() -> Dict[str, int]:
    """
    Record the name and value of log levels from the logging module
    """
    log_levels: Dict[str, int] = dict()
    for name in dir(logging):
        value = getattr(logging, name)
        if isinstance(value, int) and not isinstance(value, bool):
            log_levels[name] = value

    return log_levels


# NOTE: Need to make sure the whole logging situation is only configured once,
# even if this file is imported multiple times in the same program
log_levels = map_logging_level_names_to_values()
# Map level name -> level value
reverse_log_levels = {log_levels[name]: name for name in log_levels}
# Add alias for WARN
log_levels["WARN"] = log_levels["WARNING"]

# # NOTe: mypy appears to only be satisfied with a static value here;
# # it reports an error on any dynamic assignment of Enum content
# LogLevel = IntEnum("LogLevel", log_levels)
#
# NOTe: Cannot set IntEnums dynamically
# In general, type instances should be statically defined; I was just looking
# for a way to specify the logging levels without having to maintain a list and
# keep it up to date with the logging module
#
# On Python 3.7, the above code generates:
# {
#     "CRITICAL": 50,
#     "DEBUG": 10,
#     "ERROR": 40,
#     "FATAL": 50,
#     "INFO": 20,
#     "NOTSET": 0,
#     "WARN": 30,
#     "WARNING": 30,
# }
class LogLevel(IntEnum):
    """
    Logging levels defined in logging, and their values
    """

    CRITICAL = 50
    DEBUG = 10
    ERROR = 40
    FATAL = 50
    INFO = 20
    NOTSET = 0
    WARN = 30
    WARNING = 30


def check_LogLevel(log_levels: Dict[str, int] = log_levels) -> bool:
    """
    Validate that the statically defined LogLevels matches what's currently
    defined in the logging module
    """
    for name in log_levels:
        # Does the name match?
        if not name in LogLevel.__members__:
            return False

        # Are the values the same?
        if not log_levels[name] == getattr(LogLevel, name):
            return False

    return True


nl = "\n"
assert check_LogLevel(), f"""
Python's built-in 'logging' module has changed logging levels; LogLevel needs updating:
LogLevel:
{nl.join(f'{name} = {value}' for name, value in LogLevel.__members__.items())}

logging:
{nl.join(f'{name} = {value}' for name, value in log_levels.items())}
"""


def setup_logging(level: Union[str, int, LogLevel] = LogLevel.INFO) -> logging.Logger:
    """
    Set's up very, very simple logging
    """
    if isinstance(level, LogLevel):
        log_level = int(level)
    elif isinstance(level, int) and level in reverse_log_levels:
        log_level = level
    elif isinstance(level, str) and level in log_levels:
        log_level = log_levels[level.upper()]
    else:
        warn(f"'{level}' is not one of {', '.join(log_levels)}\nUsing 'INFO'")
        log_level = LogLevel.INFO

    logging.basicConfig(level=log_level)

    return logging.getLogger("namepicker")


def to_LogLevel(level: str) -> LogLevel:
    log_level = log_levels.get(level.upper(), None)
    if log_level is None:
        raise ArgumentTypeError(f"'{level}' is not one of {', '.join(log_levels)}")

    return LogLevel[level]


def ExistingPath(filename: str) -> Path:
    path = Path(filename)
    if not path.is_file():
        message = f"Cannot find, or is not a file: {path}"
        raise ArgumentTypeError(message) from FileNotFoundError(message)

    return path.resolve(strict=True)


def arguments() -> Namespace:
    prog_name = __name__ if __name__ != "__main__" else sys.argv[0]
    parser = ArgumentParser(
        prog=prog_name,
        description="Manages lists of names and selects random names from them",
        epilog=f"Try: {prog_name} gui",
    )
    parser.add_argument(
        "--list",
        action="append",
        type=ExistingPath,
        help="Path to a file containing a name on each line; list name will be the file name",
    )
    parser.add_argument(
        "--log",
        type=to_LogLevel,
        default=LogLevel.INFO,
        help=f"verbosity of debug messages; one of: {', '.join(log_levels)}",
    )

    return parser.parse_args()


def main() -> None:
    args = arguments()
    setup_logging(level=args.log)


if __name__ == "__main__":
    main()
