from tkinter import *

from lib.colours import color


class Login:
    def __init__(self, master, controller):
        self.bar = None
        self.page = None
        self.root = master
        self.controller = controller

        self.width_entry = 31

        self.entry_login = StringVar()
        self.entry_pass = StringVar()
        self.setup()

    def setup(self):
        self.init_menu()
        self.init_page()

    def init_menu(self):
        menubar = Menu(self.root)
        homemenu = Menu(menubar, tearoff=0)
        homemenu.add_command(label="Sobre")
        homemenu.add_command(label="Sair", command=self.root.quit)

        menubar.add_cascade(label="Opções", menu=homemenu)
        self.root.config(menu=menubar)
        pass

    def init_page(self):
        self.bar = Frame(self.root, width=300, height=50, bg=color("background"), relief='flat')
        self.bar.grid(row=0, column=0, pady=1, padx=0, sticky="NSWE")

        # Title
        Label(self.bar,
              text="LOGIN",
              anchor=NE,
              font='BOLD 25',
              bg=color("background"),
              fg="black").place(x=5, y=5)
        Label(self.bar, text="",
              width=275,
              anchor=NW,
              font='Ivy 1',
              bg=color("background-bar"),
              fg="black").place(x=9, y=47)

        self.page = Frame(self.root,
                          width=300,
                          height=160,
                          bg=color("background"),
                          relief='flat')
        self.page.grid(row=1,
                       column=0,
                       pady=1,
                       padx=0,
                       sticky="NSWE")

        # User
        Label(self.page, text="Usuário *",
              anchor=NE, font='Ivy 14',
              bg=color("background"),
              fg=color("background-bar")).place(x=9, y=10)
        entry_user = Entry(self.page,
                           textvariable=self.entry_login,
                           width=self.width_entry,
                           justify='left',
                           font='Ivy 12',
                           relief='solid')
        entry_user.place(x=10, y=40)

        # Password
        Label(self.page, text="Senha *",
              anchor=NE, font='Ivy 14',
              bg=color("background"),
              fg=color("background-bar")).place(x=10, y=70)
        entry_pass = Entry(self.page,
                           textvariable=self.entry_pass,
                           width=self.width_entry - 8,
                           justify='left',
                           font='Ivy 12', show="*",
                           relief='solid')
        entry_pass.place(x=10, y=100)

        button_login = Button(self.page,
                              text="Entrar",
                              width=6, height=2,
                              font='Ivy 11 bold', relief='flat',
                              bg=color("background-bar"), fg=color("background"), activebackground=color("background"),
                              command=self.login_clicked)
        button_login.place(x=230, y=88)

    def login_clicked(self):
        e_user = self.entry_login.get()
        e_pass = self.entry_pass.get()

        if self.controller.login(e_user, e_pass):
            self.root.destroy()


