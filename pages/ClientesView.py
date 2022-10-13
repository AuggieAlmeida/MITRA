import tkinter
from tkinter import NONE, Label, Button, Frame, StringVar, Entry, Scrollbar, Listbox
from lib.functions import set_window_center


class Clients:
    def __init__(self, master=NONE):
        self.page = Frame(master)
        master.title("MITRA - Clientes")
        self.x_pad = 5
        self.y_pad = 3
        self.width_entry = 30
        set_window_center(master, 980, 630)
        master.resizable(False, False)

        # text variables
        self.txt_name = StringVar()
        self.txt_email = StringVar()
        self.txt_cp = StringVar()
        self.txt_ctt = StringVar()
        self.setup()

    def setup(self):
        self.init_page()

    def init_page(self):
        self.page.pack()

        # Window Objects
        Label(self.page, text="Nome").grid(row=0, column=0)
        Label(self.page, text="Cel/Tel").grid(row=1, column=0)
        Label(self.page, text="Email").grid(row=2, column=0)
        Label(self.page, text="CPF/CNPJ").grid(row=3, column=0)

        name = Entry(self.page, textvariable=self.txt_name, width=self.width_entry)
        ctt = Entry(self.page, textvariable=self.txt_ctt, width=self.width_entry)
        email = Entry(self.page, textvariable=self.txt_email, width=self.width_entry)
        cp = Entry(self.page, textvariable=self.txt_cp, width=self.width_entry)

        list_clients = Listbox(self.page, width=100)
        scroll_clients = Scrollbar(self.page)

        button_view_all = Button(self.page, text="Ver todos")
        button_search = Button(self.page, text="Buscar")
        button_insert = Button(self.page, text="Inserir")
        button_update = Button(self.page, text="Atualizar Selecionados")
        button_del = Button(self.page, text="Deletar Selecionados")
        button_close = Button(self.page, text="Fechar")

        # Grid association
        name.grid(row=0, column=1, padx=50, pady=50)
        ctt.grid(row=1, column=1)
        email.grid(row=2, column=1)
        cp.grid(row=3, column=1)
        list_clients.grid(row=0, column=2, rowspan=10)
        scroll_clients.grid(row=0, column=6, rowspan=10)
        button_view_all.grid(row=4, column=0, columnspan=2)
        button_search.grid(row=5, column=0, columnspan=2)
        button_insert.grid(row=6, column=0, columnspan=2)
        button_update.grid(row=7, column=0, columnspan=2)
        button_del.grid(row=8, column=0, columnspan=2)
        button_close.grid(row=9, column=0, columnspan=2)

        # Scrollbar connection to listbox
        list_clients.configure(yscrollcommand=scroll_clients.set)
        scroll_clients.configure(command=list_clients.yview)
        for child in self.page.winfo_children():
            widget_class = child.__class__.__name__
            if widget_class == "Button":
                child.grid_configure(sticky='WE', padx=self.x_pad, pady=self.y_pad)
            elif widget_class == "Listbox":
                child.grid_configure(padx=0, pady=0, sticky='NS')
            elif widget_class == "Scrollbar":
                child.grid_configure(padx=0, pady=0, sticky='NS')
            else:
                child.grid_configure(padx=self.x_pad, pady=self.y_pad, sticky='N')
