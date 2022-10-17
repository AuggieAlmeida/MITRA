from tkinter import Frame, Label, Button
from lib.colours import color


def init_bar(master):
    bar = Frame(master, width=980, height=60)
    bar.config(bg=color("background-bar"))
    bar.pack(fill="both")

    Label(bar, text="MITRA", font="time 40").grid(row=0, column=1)
    Label(bar, text="                  ", font="time 40").grid(row=0, column=2)
    button_home = Button(bar, text="Home", font="time 16", relief="flat")
    button_home.grid(row=0, column=3)
    button_home = Button(bar, text="Comercial", font="time 16", relief="flat")
    button_home.grid(row=0, column=4)
    button_home = Button(bar, text="Clientes", font="time 16", relief="flat")
    button_home.grid(row=0, column=5)
    button_home = Button(bar, text="Produtos", font="time 16", relief="flat")
    button_home.grid(row=0, column=6)

    for child in bar.winfo_children():
        widget_class = child.__class__.__name__
        if widget_class == "Button":
            child.configure(bg=color("background-bar"), activebackground=color("background-bar"))
            child.grid_configure(sticky='WE', padx=5, pady=3)
        elif widget_class == "Label":
            child.grid_configure(pady=0, padx=15, sticky="W")
            child.configure(bg=color("background-bar"))
        elif widget_class == "Frame":
            child.grid_configure(pady=0, padx=0, sticky="NSWE")
        else:
            child.grid_configure(padx=5, pady=3, sticky='N')
