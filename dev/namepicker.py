"""
Main file to run the program
"""

from typing import Tuple, Dict, NamedTuple
from datetime import datetime, timedelta

class NameList(NamedTuple):
    name: str
    date: datetime
    items: 

Lists = Dict[str, NameList]

def list_setter_and_getter() -> Tuple[ , ]:
    """
    List Name
    ---------
    Alice
    Bob
    Carol
    David
    """
    lists: NameList = dict()
