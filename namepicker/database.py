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

db = orm.Database()


class ListNotFoundError(Exception):
    pass


class Name(db.Entity):
    # id = PrimaryKey(int, auto=True)
    value = orm.Required(str, unique=True)
    lists = orm.Set("NameList")
    name_datas = orm.Set("NameData")


class NameList(db.Entity):
    # id = PrimaryKey(int, auto=True)
    title = orm.Required(str, unique=True)
    names = orm.Set(Name)
    name_datas = orm.Set("NameData")


def time_now() -> datetime:
    return datetime.now().astimezone()


class NameData(db.Entity):
    # id = PrimaryKey(int, auto=True)
    name = orm.Required(Name)
    list = orm.Required(NameList)
    date_added = orm.Required(datetime, default=time_now)


def initialize_database(filename: SPath = default_database_file) -> None:
    db.bind(provider="sqlite", filename=str(filename), create_db=True)
    db.generate_mapping(check_tables=True, create_tables=True)


def enable_debugging(enable: bool = True, enable_sql: bool = True) -> None:
    """
    enables Pony's debugging as well as other logging in this module
    """
    if enable:
        pass

    if enable_sql:
        orm.set_sql_debug(debug=True, show_values=True)


#@orm.db_session()
#def select_list(list_title: str) -> Iterator[NameTuple]:
#    if not isinstance(list_title, str):
#        raise TypeError(f"list_title must be a str; got {type(list_title)}")
#    query = NameList.select(name for name in Name if list_title in name.lists)
#    for item in query:
#        yield NameTuple(value=item.value, lists=[l.title for l in item.lists])


