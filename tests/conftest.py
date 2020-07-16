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

    from namepicker.database import initialize_database, in_memory_db_filename

    return initialize_database(in_memory_db_filename)
