"""
Defines most of the graphical functionality
"""

from tkinter import *
from typing import Callable, List

root = Tk()
root


def gen_on_click() -> Callable[[], None]:
    clicks: int = 0
    labels: List[Label] = list()

    def on_click() -> None:
        nonlocal clicks
        clicks += 1
        labels.append(Label(root, text="Button clicked"))
        if clicks > 5:
            for label in labels:
                label.pack()

    return on_click

button = Button(root, text="Add Text", command=gen_on_click())
button.pack()

root.mainloop()
