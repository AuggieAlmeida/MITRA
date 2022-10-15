import tkinter
from tkinter import Label, Button, Frame, StringVar, Entry, Scrollbar, Listbox, Tk, Menu, Canvas
from lib.functions import set_window_center


class Clients(Tk):
    def __init__(self, master=None):
        self.page = None
        self.root = master
        self.root.title("MITRA - Clientes")
        self.x_pad = 5
        self.y_pad = 3
        self.w = 980
        self.h = 630
        self.width_entry = 30
        set_window_center(self.root, self.w, self. h)
        self.root.resizable(False, False)
        self.root.config(bg="#213563")

        # text variables
        self.txt_name = StringVar()
        self.txt_email = StringVar()
        self.txt_cp = StringVar()
        self.txt_ctt = StringVar()
        self.setup()

    def setup(self):
        self.init_menu()
        self.init_page()

    def init_menu(self):
        menubar = Menu(self.root)
        homemenu = Menu(menubar, tearoff=0)
        homemenu.add_command(label="Configurações", )
        homemenu.add_separator()
        homemenu.add_command(label="Sair", command=self.root.quit)
        climenu = Menu(menubar, tearoff=0, bg="#213563")

        menubar.add_cascade(label="Home", menu=homemenu)
        menubar.add_cascade(label="Clientes", menu=climenu)
        self.root.config(menu=menubar)

    def init_page(self):
        self.page = Frame(self.root)
        self.page.pack()
        self.page.config(bg="#eef7fc")

        canvas = Canvas(self.page, width=self.w, height=60, bg="#56b0e6")
        canvas.grid(row=0, columnspan=6)
        canvas.create_text(88, 30, text="MITRA", font="time 40", tags="string")





        # Window Objects
        Label(self.page, text="Nome", bg="#eef7fc").grid(row=2, column=0)
        Label(self.page, text="Cel/Tel", bg="#eef7fc").grid(row=3, column=0)
        Label(self.page, text="Email", bg="#eef7fc").grid(row=4, column=0)
        Label(self.page, text="CPF/CNPJ", bg="#eef7fc").grid(row=5, column=0)

        name = Entry(self.page, textvariable=self.txt_name, width=self.width_entry)
        ctt = Entry(self.page, textvariable=self.txt_ctt, width=self.width_entry)
        email = Entry(self.page, textvariable=self.txt_email, width=self.width_entry)
        cp = Entry(self.page, textvariable=self.txt_cp, width=self.width_entry)

        list_clients = Listbox(self.page, width=100)
        scroll_clients = Scrollbar(self.page)

        button_view_all = Button(self.page, text="Ver todos", bg="#eef7fc")
        button_search = Button(self.page, text="Buscar", bg="#eef7fc")
        button_insert = Button(self.page, text="Inserir", bg="#eef7fc")
        button_update = Button(self.page, text="Atualizar Selecionados", bg="#eef7fc")
        button_del = Button(self.page, text="Deletar Selecionados", bg="#eef7fc")
        button_close = Button(self.page, text="Fechar", bg="#eef7fc")

        # Grid association
        name.grid(row=2, column=1, padx=50, pady=50)
        ctt.grid(row=3, column=1)
        email.grid(row=4, column=1)
        cp.grid(row=5, column=1)
        list_clients.grid(row=2, column=2, rowspan=10)
        scroll_clients.grid(row=2, column=6, rowspan=10)
        button_view_all.grid(row=6, column=0, columnspan=2)
        button_search.grid(row=7, column=0, columnspan=2)
        button_insert.grid(row=8, column=0, columnspan=2)
        button_update.grid(row=9, column=0, columnspan=2)
        button_del.grid(row=10, column=0, columnspan=2)
        button_close.grid(row=11, column=0, columnspan=2)

        # Scrollbar connection to listbox
        list_clients.configure(yscrollcommand=scroll_clients.set)
        scroll_clients.configure(command=list_clients.yview)

        # Drip
        for child in self.page.winfo_children():
            widget_class = child.__class__.__name__
            if widget_class == "Button":
                child.grid_configure(sticky='WE', padx=self.x_pad, pady=self.y_pad)
            elif widget_class == "Listbox":
                child.grid_configure(padx=0, pady=0, sticky='NS')
            elif widget_class == "Scrollbar":
                child.grid_configure(padx=0, pady=0, sticky='NS')
            elif widget_class == "Canvas":
                child.grid_configure(padx=0, pady=0, sticky='NS')
            else:
                child.grid_configure(padx=self.x_pad, pady=self.y_pad, sticky='N')
