import tkinter
from tkinter import ttk
from typing import List, Dict
from dataclasses import dataclass

country_names = [
    "Argentina",
    "Australia",
    "Belgium",
    "Brazil",
    "Canada",
    "China",
    "Denmark",
    "Finland",
    "France",
    "Greece",
    "India",
    "Italy",
    "Japan",
    "Mexico",
    "Netherlands",
    "Norway",
    "Spain",
    "Sweden",
    "Switzerland",
]

country_pops = {
    "ar": 41000000,
    "au": 21179211,
    "be": 10584534,
    "br": 185971537,
    "ca": 33148682,
    "cn": 1323128240,
    "dk": 5457415,
    "fi": 5302000,
    "fr": 64102140,
    "gr": 11147000,
    "in": 1131043000,
    "it": 59206382,
    "jp": 127718000,
    "mx": 106535000,
    "nl": 16402414,
    "no": 4738085,
    "es": 45116894,
    "se": 9174082,
    "ch": 7508700,
}

@dataclass
class Country:
    name: str
    code: str
    population: str
    index: int

    def __str__(self) -> str:
        return f"The population of {self.name} ({self.code}) is {self.population}"

countries: List[Country] = list()
for i, (code, pop) in enumerate(country_pops.items()):
    countries.append(Country(name=country_names[i], code=code, population=pop, index=i))

root = tkinter.Tk()

content = ttk.Frame(root)
info_line = ttk.Frame(root)

list_items = tkinter.StringVar(value=country_names)
info_text = tkinter.StringVar()
gift = tkinter.StringVar()
gift_result = tkinter.StringVar()

listbox = tkinter.Listbox(content, listvariable=list_items)
message = ttk.Label(content, text="Send to country's leader:")
info_label = ttk.Label(info_line, textvariable=info_text)
greeting = ttk.Radiobutton(content, text="Greeting card", variable=gift, value="Greeting card")
flowers = ttk.Radiobutton(content, text="Flowers", variable=gift, value="Flowers")
nastygram = ttk.Radiobutton(content, text="Nastygram", variable=gift, value="Nastygram")
initiate_gift = ttk.Button(content, default="active", text="Send Gift", command=lambda : gift_result.set(f"Sent {gift.get()} to leader of {countries[listbox.curselection()[0]].name}"))
gift_message = ttk.Label(content, textvariable=gift_result)

content.grid(column=0, row=0, sticky="N E S W")
info_line.grid(column=0, row=1, sticky="N E S W")
listbox.grid(column=0, row=0, rowspan=6, sticky="N E S W")
message.grid(column=1, row=0, padx=12, pady=12)
info_label.grid(column=0, row=0, padx=5, pady=5, sticky="N E S W")
greeting.grid(column=1, row=1, padx=5, pady=2, sticky="W")
flowers.grid(column=1, row=2, padx=5, pady=2, sticky="W")
nastygram.grid(column=1, row=3, padx=5, pady=2, sticky="W")
initiate_gift.grid(column=2, row=4, padx=9, pady=9, sticky="E")
gift_message.grid(column=1, row=5, columnspan=2, padx=5, pady=5, sticky="N W")

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
content.columnconfigure(0, weight=1)
content.columnconfigure(1, weight=1)
content.columnconfigure(2, weight=1)
content.rowconfigure(0, weight=1)
content.rowconfigure(1, weight=1)
content.rowconfigure(2, weight=1)
content.rowconfigure(3, weight=1)
content.rowconfigure(4, weight=1)
content.rowconfigure(5, weight=1)
info_line.columnconfigure(0, weight=1)

listbox.bind("<<ListboxSelect>>", lambda e: info_text.set(str(countries[listbox.curselection()[0]])))
listbox.bind("<Double-1>", lambda e: initiate_gift.invoke())
root.bind("<KeyPress-Return>", lambda e: initiate_gift.invoke())

root.bind("<KeyPress-Escape>", lambda e: root.destroy())
root.mainloop()
