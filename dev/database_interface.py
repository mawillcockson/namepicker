"""
Uses database.py to provide a (mostly) typed interface to the database
"""
from typing import Iterable, Iterator, Union, Optional
from pathlib import Path
from .database import ListNotFoundError, select_list

# def save_names()
# 
# def save_lists
# 
# def select_names
# 
# def select_lists

SPath = Union[str, Path]

class FileError(Exception):
    """
    Generic file error
    """
    pass


# mypy does not like circular type definitions
# class NameTuple(NamedTuple):
#     value: str
#     lists: Dict[str, "NameListTuple"]]
#     name_datas: Dict[str, "NameDataTuple"]
# 
# 
# class NameListTuple(NamedTuple):
#     title: str
#     names: Dict[str, NameTuple]
#     name_datas: Dict[str, "NameDataTuple"]
# 
# 
# class NameDataTuple(NamedTuple):
#     name: NameTuple
#     list: NameListTuple
#     date_added: datetime


class NameList:
    def __contains__(self, list_title: str) -> bool:
        if not isinstance(list_title, str):
            return False
        try:
            select_list(title=list_title)
        except ListNotFoundError as err:
            return False
        
        return True
    
    def __getitem__
    def __iter__
    def __len__
    def keys
    def items
    def values
    def get
    def __eq__
    def __ne__

def lines_in_file(filename: SPath) -> Iterator[str]:
    path = Path(filename)
    if not path.is_file():
        message = f"'{path}' does not exist, or is not a file"
        raise FileError(message) from FileNotFoundError(message)
    
    try:
        with path.open() as f:
            f.read(0)
    except OSError as err:
        raise FileError(f"Can't read the contents of {path}") from err

    with path.open(mode="r") as f:
        for line in f:
            yield line

def import_file(filename: SPath, title: Optional[str] = None) -> NameList:
    path = Path(filename)
    
    if not (title or path.name):
        raise ValueError("No title specified, and can't use filename as title of list")

    if title is not None:
        list_title = title
    else:
        list_title = path.name
    
    for name in lines_in_file(path):
        add_names(name=name, list_title=list_title)
    
    return NameList[list_title]
