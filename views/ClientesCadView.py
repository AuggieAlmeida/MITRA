import sqlite3
import os
from tkinter import *
from datetime import date

from lib.functions import set_window_sided
from lib.colours import color
import lib.global_variable as glv


class ClientsCadController:
    def connect_db(self):
        db_path = os.path.join(
            glv.get_variable("APP_PATH"),
            glv.get_variable("DATA_DIR"),
            "SPDB.db"
        )
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def disconnect_db(self):
        self.conn.close()

    def insertClients(self):
        self.name = self.name_entry.get()
        self.email = self.email_entry.get()
        self.cp = self.cp_entry.get()
        self.birth= self.birth_entry.get()
        self.occup = self.occup_entry.get()
        self.datecad = date.today().strftime("%d/%m/%Y")
        self.obs = self.obs_entry.get("1.0", END)
        self.connect_db()
        self.cursor.execute(""" INSERT INTO tb_clientes (nome, email, cp, profissao, datacad, nascimento, fiscal)
            VALUES (?, ?, ?, ?, ?, ?, ?)""", (self.name, self.email, self.cp,  self.occup, self.datecad, self.birth,
                                              self.obs))
        self.conn.commit()
        self.disconnect_db()


class ClientsCadView(ClientsCadController):
    def __init__(self):
        super().__init__()
        self.cadwin = Toplevel()
        self.cadwin.title("Clientes")
        self.cadwin.configure(background=color("background-bar"))
        self.cadwin.resizable(False, False)
        set_window_sided(self.cadwin, 370, 490)
        self.cadwin.iconbitmap('assets\icon.ico')
        self.init_window()

    def init_window(self):
        Label(self.cadwin, text="Relatório de clientes", font="Ivy 15", bg="#254465", fg=color("background"))\
            .place(relx=0, rely=0, relwidth=1, relheight=0.07)

        self.reg = Frame(self.cadwin, background=color("background"))
        self.reg.place(relx=0.01, rely=0.08, relwidth=0.98, relheight=0.78)

        self.buttons = Frame(self.cadwin, background=color("background"))
        self.buttons.place(relx=0.01, rely=0.88, relwidth=0.98, relheight=0.11)

        self.bt_leave = Button(self.buttons, text="Voltar", font='Ivy 14', bg=color("background"),
                               command=self.cadwin.destroy)
        self.bt_leave.place(relx=0.03, rely=0.10, relheight=0.80, relwidth=0.22)
        self.bt_clean = Button(self.buttons, text="Relatório", font='Ivy 14', bg=color("background"),
                               command=self.clean)
        self.bt_clean.place(relx=0.75, rely=0.10, relheight=0.80, relwidth=0.22)

    def clean(self):
        self.name_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.cp_entry.delete(0, END)
        self.ctt_entry.delete(0, END)
        self.address_entry.delete(0, END)
        self.birth_entry.delete(0, END)
        self.occup_entry.delete(0, END)
        self.obs_entry.delete("1.0", END)


