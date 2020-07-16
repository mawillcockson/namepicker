"""
Wraps Pony to provide a basic interface to the database
Until Pony gains type annotations, this will live in it's own module
"""
import logging
from datetime import datetime
from enum import Enum
from functools import partial
from pathlib import Path
from typing import Dict, Iterator, List, NamedTuple, Optional, Tuple, Union

from pony import orm

SPath = Union[str, Path]

default_database_file = "./namepicker.sqlitedb"
# This is specific to SQLite
# https://www.sqlite.org/inmemorydb.html
in_memory_db_filename = ":memory:"


class ListNotFoundError(Exception):
    pass


def time_now() -> datetime:
    return datetime.now().astimezone()


def initialize_database(
    filename: SPath = default_database_file, create: bool = False
) -> None:
    """
    Find and initialize a database in a file

    if create is True, create the database file if it's not found
    """

    if not isinstance(filename, (str, Path)):
        raise TypeError(f"'filename' must be either a Path or str")

    path = Path(filename)

    if str(filename) == in_memory_db_filename:
        # Have to create the in-memory database, since it doesn't exist
        # already
        create = True
    elif not create and not path.is_file():
        # If we're supposed to find a database, but one isn't found
        raise FileNotFoundError(
            f"'{filename}' must be a file, but is not\nto have the database be created, pass create=True"
        )
    elif create and path.exists():
        raise FileExistsError(
            f"'{filename}' already exists, but create=True was passed"
        )

    db = orm.Database()

    class Item(db.Entity):
        # id = PrimaryKey(int, auto=True)
        text = orm.Required(str, unique=True)
        lists = orm.Set("ItemList")
        item_datas = orm.Set("ItemData")

    class ItemList(db.Entity):
        # id = PrimaryKey(int, auto=True)
        title = orm.Required(str, unique=True)
        items = orm.Set(Item)
        items_datas = orm.Set("ItemData")

    class ItemData(db.Entity):
        # id = PrimaryKey(int, auto=True)
        item = orm.Required(Item)
        list = orm.Required(ItemList)
        date_added = orm.Required(datetime, default=time_now)

    db.bind(provider="sqlite", filename=str(filename), create_db=create)
    db.generate_mapping(check_tables=True, create_tables=create)

    return db


def enable_debugging(enable: bool = True, enable_sql: bool = True) -> None:
    """
    enables Pony's debugging as well as other logging in this module
    """
    if enable:
        pass

    if enable_sql:
        orm.set_sql_debug(debug=True, show_values=True)


# @orm.db_session()
# def select_list(list_title: str) -> Iterator[NameTuple]:
#    if not isinstance(list_title, str):
#        raise TypeError(f"list_title must be a str; got {type(list_title)}")
#    query = NameList.select(name for name in Name if list_title in name.lists)
#    for item in query:
#        yield NameTuple(value=item.value, lists=[l.title for l in item.lists])
