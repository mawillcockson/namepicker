from datetime import timezone
from pathlib import Path
from typing import Union

import pytest
from pony.orm import Database

from namepicker.database import (
    enable_debugging,
    in_memory_db_filename,
    initialize_database,
    time_now,
)

SPath = Union[str, Path]


def test_time_now_is_aware() -> None:
    """
    Ensures time_now() returns an aware object, as opposed to a naive one
    https://docs.python.org/3/library/datetime.html#aware-and-naive-objects
    """

    datetime_object = time_now()
    assert isinstance(datetime_object.tzinfo, timezone)


@pytest.mark.parametrize("filename", [int(), bool(), list(), dict()])
@pytest.mark.parametrize("create", [True, False])
def test_database_initialization_filename_type(filename: SPath, create: bool) -> None:
    with pytest.raises(TypeError):
        db = initialize_database(filename=filename, create=create)


@pytest.mark.parametrize(
    "filename", [in_memory_db_filename, Path(in_memory_db_filename)]
)
@pytest.mark.parametrize("create", [True, False])
def test_in_memory_database_initialization(filename: SPath, create: bool) -> None:
    """
    Test if an in-memory database is initialized properly
    """

    db = initialize_database(in_memory_db_filename, create=create)
    assert isinstance(db, Database)
    for name in ["Item", "ItemList", "ItemMetadata"]:
        assert name in db.entities


def test_database_initialization_creates_file(tmp_path: Path) -> None:
    """
    Test if a database can be created on disk
    """

    temp_db_path = tmp_path / "temporary_namepicker.sqlitedb"

    db = initialize_database(temp_db_path, create=True)

    assert temp_db_path.is_file()


def test_database_file_must_not_exist(tmp_path: Path) -> None:
    """
    Test if database initialization will fail if the
    file exists and create was True
    """

    temp_db_path = tmp_path / "temporary_namepicker.sqlitedb"
    temp_db_path.touch()

    with pytest.raises(FileExistsError):
        db = initialize_database(filename=temp_db_path, create=True)


def test_database_file_must_exist(tmp_path: Path) -> None:
    """
    Test if database initialization will fail if the
    file does not exist and create was False
    """

    temp_db_path = tmp_path / "temporary_namepicker.sqlitedb"

    with pytest.raises(FileNotFoundError):
        db = initialize_database(temp_db_path, False)


# NOTE: all xfail tests will be implemented at a later time
@pytest.mark.xfail(raises=NotImplementedError, reason="Haven't setup database logging")
def test_enable_all_debugging() -> None:
    """
    Ensure enabling all debugging works as intended
    """

    enable_debugging(enable=True, enable_sql=True)

    assert False


@pytest.mark.xfail(reason="Don't know how to see if SQL debugging is enabled")
def test_enable_sql_debugging() -> None:
    """
    Ensure enabling just SQL debugging works as intended
    """

    enable_debugging(False, enable_sql=True)

    assert False


@pytest.mark.xfail(raises=NotImplementedError, reason="Haven't setup database logging")
def test_enable_logging_debugging() -> None:
    """
    Ensure enabling only logging debugging works as intended
    """

    enable_debugging(True, False)

    assert False


@pytest.mark.xfail(
    reason="""
Haven't setup database logging
Don't know how to see if SQL debugging is enabled"""
)
def test_disable_debugging() -> None:
    """
    Ensure passing False to everything disables debugging
    """

    enable_debugging(False, False)

    assert False
