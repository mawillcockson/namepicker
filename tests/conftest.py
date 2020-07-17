"""
pytest test fixtures
https://docs.pytest.org/en/stable/fixture.html#conftest-py
"""
import pytest
from pony.orm import Database


@pytest.fixture
def namepicker_database() -> Database:
    """
    Builds an in-memeory database
    """

    from namepicker.database import in_memory_db_filename, initialize_database

    return initialize_database(in_memory_db_filename)
