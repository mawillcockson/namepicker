"""
Main file to run the program
"""

from typing import Tuple, Dict, NamedTuple, Union
from datetime import datetime, timedelta
from .database_interface import select_names, select_lists, save_names, save_lists
import logging
from argparse import ArgumentParser, ArgumentTypeError, Namespace
import sys
from warnings import warn
from pathlib import Path
from enum import IntEnum

# mypy doesn't believe the type declaration Dict[str, int]
# log_attr = partial(getattr, logging)
# log_levels = {
#     name: log_attr(name)
#     for name in dir(logging)
#     if isinstance(log_attr(name), int) and not isinstance(log_attr(name), bool)
# }
log_levels: Dict[str, int] = dict()
for name in dir(logging):
    value = getattr(logging, name)
    if isinstance(value, int) and not isinstance(value, bool):
        log_levels[name] = value

reverse_log_levels = {log_levels[name]:name for name in log_levels}
log_levels["WARN"] = log_levels["WARNING"]

# NOTE: mypy appears to only be satisfied with a static value here;
# it reports an error on any variable
LogLevel = IntEnum("LogLevel", log_levels)

def setup_logging(level: Union[str, int, LogLevel] = LogLevel.INFO) -> logging.Logger:
    if isinstance(level, LogLevel):
        log_level = int(level)
    elif isinstance(level, int) and level in reverse_log_levels:
        log_level = level
    elif isinstance(level, str) and level in log_levels:
        log_level = log_levels[level.upper()]
    else:
        warn(f"'{level}' is not one of {', '.join(log_levels)}\nUsing INFO")
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
    parser = ArgumentParser(prog=prog_name, description="Manages lists of names and selects random names from them", epilog=f"Try: {prog_name} gui")
    parser.add_argument("--list", action="append", type=ExistingPath, help="Path to a file containing a name on each line; list name will be the file name")
    parser.add_argument("--log", type=to_LogLevel, default=LogLevel.INFO, help=f"verbosity of debug messages; one of: {', '.join(log_levels)}")
    
    return parser.parse_args()

def main() -> None:
    args = arguments()
    setup_logging(level=args.log)
    for path in args.list:
        with path.open() as f:
            add_list(title=path.name, names=(name for name in f))

if __name__ == "__main__":
    main()