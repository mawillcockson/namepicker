import tkinter
from tkinter import ttk
from typing import List, Dict
from dataclasses import dataclass

root = tkinter.Tk()
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

container = ttk.Frame(root)
container.grid(column=0, row=0, sticky="N E S W")
container.rowconfigure(0, weight=1)
container.columnconfigure(0, weight=1)

label1 = ttk.Label(container, text="Label 1")
label1.grid(column=0, row=1, pady=5, sticky="N W")

canvas_frame = ttk.Frame(container)
canvas_frame.grid(column=0, row=0, pady=(5, 0), sticky="N S E W")
canvas_frame.grid_rowconfigure(0, weight=1)
canvas_frame.grid_columnconfigure(0, weight=1)
canvas_frame.grid_propagate(False)

canvas = tkinter.Canvas(canvas_frame, bg="yellow")
canvas.grid(column=0, row=0, sticky="N E S W")
canvas.columnconfigure(0, weight=1)
canvas.rowconfigure(0, weight=1)

scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
scrollbar.grid(row=0, column=1, sticky="N S")
canvas.configure(yscrollcommand=scrollbar.set)

scrollable_frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
scrollable_frame.grid(column=0, row=0, sticky="N S E W")
scrollable_frame.columnconfigure(0, weight=1)
scrollable_frame.rowconfigure(0, weight=1)

string_vars = [tkinter.StringVar(value=f"Item {i} of 100") for i in range(1, 100 + 1)]
entries = [
    ttk.Entry(scrollable_frame, textvariable=string_var) for string_var in string_vars
]
for i, entry in enumerate(entries):
    entry.grid(column=0, row=i, sticky="E W")

scrollable_frame.update_idletasks()

# 10% of the screen's smallest dimension
sidelength = (min(root.winfo_screenwidth(), root.winfo_screenheight()) * 30) // 100

canvas_frame.config(width=sidelength, height=sidelength)
canvas.config(scrollregion=canvas.bbox("all"))


def update_canvas(event) -> None:
    scrollable_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))


scrollable_frame.bind("<<Configure>>", update_canvas)

root.bind("<KeyPress-Escape>", lambda e: root.destroy())
root.mainloop()
