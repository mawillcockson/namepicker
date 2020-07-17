import tkinter
from dataclasses import dataclass
from tkinter import ttk
from typing import Dict, List

root = tkinter.Tk()
root.grid_rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

container = ttk.Frame(root)
container.grid(sticky="N E S W")

label1 = ttk.Label(container, text="Label 1")
label1.grid(column=0, row=1, pady=5, sticky="N W")

canvas_frame = ttk.Frame(container)
canvas_frame.grid(column=0, row=0, pady=(5, 0), sticky="N W")
canvas_frame.grid_rowconfigure(0, weight=1)
canvas_frame.grid_columnconfigure(0, weight=1)
canvas_frame.grid_propagate(False)

canvas = tkinter.Canvas(canvas_frame, bg="yellow")
canvas.grid(column=0, row=0, sticky="N E S W")

scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
scrollbar.grid(row=0, column=1, sticky="N S")
canvas.configure(yscrollcommand=scrollbar.set)

scrollable_frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

rows = 9
columns = 5
buttons = [[tkinter.Button() for j in range(columns)] for i in range(rows)]
for i in range(0, rows):
    for j in range(0, columns):
        buttons[i][j] = tkinter.Button(
            scrollable_frame, text=("%d,%d" % (i + 1, j + 1))
        )
        buttons[i][j].grid(row=i, column=j, sticky="news")

# Update buttons frames idle tasks to let tkinter calculate buttons sizes
scrollable_frame.update_idletasks()

first5columns_width = sum([buttons[0][j].winfo_width() for j in range(0, 5)])
first5rows_height = sum([buttons[i][0].winfo_height() for i in range(0, 5)])
canvas_frame.config(
    width=first5columns_width + scrollbar.winfo_width(), height=first5rows_height
)

canvas.config(scrollregion=canvas.bbox("all"))

# def update_canvas(event) -> None:
#    print(f"{event}\n{dir(event)}")
#    print(canvas.bbox("all"))
#    scrollable_frame.update_idletasks()
#    canvas.config(scrollregion=canvas.bbox("all"))
#
# scrollable_frame.bind("<<Configure>>", update_canvas)

root.bind("<KeyPress-Escape>", lambda e: root.destroy())
root.mainloop()
