import pytest
from pathlib import Path
from namepicker.database import initialize_database, in_memory_db_filename
from pony.orm import Database


@pytest.mark.parametrize("create", [(True,), (False,),])
def test_in_memory_database_initialization(create: bool) -> None:
    """
    Test if an in-memory database is initialized properly
    """

    db = initialize_database(in_memory_db_filename, create=create)
    assert isinstance(db, Database)
    for name in ["Item", "ItemList", "ItemData"]:
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
