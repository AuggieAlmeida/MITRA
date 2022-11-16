import sqlite3
import os
import csv
import requests

from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox

from datetime import date

from views import ClientesCadView

from lib.colours import color
import lib.global_variable as glv


class ComercialController:
    def __init__(self):
        pass

    def getEntry(self):
        self.lb_name.get("text")

    def setEntry(self, cod, name):
        self.lb_name.insert(END, name)

    def getCepEntry(self):
        self.lb_cep.get()

    def setCepEntry(self, end):
        self.lb_cep.insert(END, f'{end}')

    def clean(self):
        self.lb_name.delete(0, END)

    def cleancep(self):
        pass

    def connect_db(self):
        db_path = os.path.join(
            glv.get_variable("APP_PATH"),
            "SPDB.db"
        )
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def disconnect_db(self):
        self.conn.close()

    def selectAllClients(self):
        auxlist = []
        self.connect_db()
        self.cursor.execute(""" SELECT * FROM tb_clientes""")
        self.info = self.cursor.fetchall()

        for i in self.info:
            auxlist.append(i)

        self.disconnect_db()
        return auxlist

    def selectClientbyId(self, idclient=int):
        self.connect_db()
        self.cursor.execute(""" SELECT * FROM tb_clientes 
            WHERE cod = ?""", (idclient,))
        row = self.cursor.fetchall()
        self.disconnect_db()

        return row

    def selectAllCep(self):
        self.getEntry()
        auxlist = []
        cod = [self.cod]
        self.connect_db()
        self.cursor.execute(""" SELECT cep, num, compl FROM tb_enderecos 
                    WHERE cliente_cod = ?""", (cod))
        self.info = self.cursor.fetchall()
        for i in self.info:
            auxlist.append(i)

        self.disconnect_db()
        return auxlist

    def searchClientByName(self):
        self.connect_db()
        self.name_entry.insert(END, '%')
        nome = self.name_entry.get()
        self.cursor.execute(""" SELECT * FROM tb_clientes
            WHERE nome LIKE '%s' ORDER BY nome ASC """ % nome)
        row = self.cursor.fetchall()
        self.disconnect_db()
        self.clean()

        return row

    @staticmethod
    def treeSelect():
        treev_data = tree.focus()
        treev_dicionario = tree.item(treev_data)
        treev_list = treev_dicionario['values']

        return treev_list

    def treeReload(self, list):

        global tree

        listClient = list

        self.list_header = ['ID', 'Nome', 'Email', 'Documento']
        tree = ttk.Treeview(self.frameup, selectmode="extended", columns=self.list_header, show="headings")
        self.vsb = ttk.Scrollbar(self.frameup, orient="vertical", command=tree.yview)

        tree.configure(yscrollcommand=self.vsb.set)
        tree.place(relx=0.02, rely=0.15, relwidth=0.93, relheight=0.25)
        self.vsb.place(relx=0.94, rely=0.15, relwidth=0.04, relheight=0.25)

        hd = ["nw", "nw", "nw", "nw"]
        h = [10, 120, 120, 90]
        n = 0

        for col in self.list_header:
            tree.heading(col, text=col.title(), anchor=CENTER)
            tree.column(col, width=h[n], anchor=hd[n])
            n += 1

        for item in listClient:
            tree.insert('', END, values=item)

        self.treecepReload()
        self.treecttReload()

        tree.bind("<Double-1>", self.OnDoubleClick)

    def treecepReload(self):
        global ceptree
        listcep = self.selectAllCep()

        self.adress_header = ['id', 'CEP', 'Num', 'Compl.', 'endereço']

        ceptree = ttk.Treeview(self.frameup, selectmode="extended", columns=self.adress_header, show="headings")
        self.vsb2 = ttk.Scrollbar(self.frameup, orient="vertical", command=tree.yview)

        ceptree.configure(yscrollcommand=self.vsb2.set)
        ceptree.place(relx=0.02, rely=0.62, relheight=0.17, relwidth=0.450)
        self.vsb2.place(relx=0.46, rely=0.62, relheight=0.17, relwidth=0.03)

        hd = ["nw", "nw", "nw", "nw", "center", "center"]
        h = [10, 75, 60, 60, 100]
        n = 0

        for col in self.adress_header:
            ceptree.heading(col, text=col.title(), anchor=CENTER)
            ceptree.column(col, width=h[n], anchor=hd[n])
            n += 1

        for item in listcep:
            ceptree.insert('', END, values=item)

        ceptree.bind("<Double-1>", self.OnDoubleClick2)

    def treecttReload(self):
        global ctttree
        listctt = self.selectAllCtt()

        self.ctt_header = ['', 'Numero', 'Tipo']

        ctttree = ttk.Treeview(self.frameup, selectmode="extended", columns=self.ctt_header, show="headings")
        self.vsb3 = ttk.Scrollbar(self.frameup, orient="vertical", command=tree.yview)

        ctttree.configure(yscrollcommand=self.vsb3.set)
        ctttree.place(relx=0.02, rely=0.42, relheight=0.17, relwidth=0.45)
        self.vsb3.place(relx=0.46, rely=0.42, relheight=0.17, relwidth=0.03)

        hd = ["nw", "nw", "nw", "nw", "center", "center"]
        h = [10, 100, 50]
        n = 0

        for col in self.ctt_header:
            ctttree.heading(col, text=col.title(), anchor=CENTER)
            ctttree.column(col, width=h[n], anchor=hd[n])
            n += 1

        for item in listctt:
            ctttree.insert('', END, values=item)

        ctttree.bind("<Double-1>", self.OnDoubleClick3)

    def OnDoubleClick(self, event):
        self.clean()
        cod = self.treeSelect()
        values = self.selectClientbyId(int(cod[0]))
        self.setEntry(values[0][0], values[0][1])



class ComercialView(ComercialController):
    def __init__(self, frameup, framedown, framebar):
        self.list_cli = ttk.Treeview
        self.framedown = framedown
        self.frameup = frameup
        self.framebar = framebar
        self.setup()

    def setup(self):
        self.init_budget()
        self.init_lists()

    def init_Comercial(self):
        self.init_layout()

    def init_budget(self):
        self.init_layout()
        self.init_budgets()
        self.init_treebudget()

    def init_layout(self):
        self.bgImg = PhotoImage(file=r'assets\CARD.png')
        self.bg = Label(self.frameup, image=self.bgImg)
        self.bg.place(relx=0, rely=0, relwidth=1, height=445)

        self.bg2Img = PhotoImage(file=r'assets\CARD2.png')
        self.bg2 = Label(self.framedown, image=self.bg2Img, bg=color("background2"))
        self.bg2.place(relwidth=1, relheight=1)

        Label(self.frameup, text="                                                 ", font="Ivy 13 bold",
              bg=color("background-bar")). \
            place(relx=0, rely=0.84, relwidth=1, relheight=0.02)

    def init_budgets(self):
        self.rprtImg = PhotoImage(file=r'assets\retornar.png')
        self.bt_return = Button(self.framebar,image=self.rprtImg, relief='flat',
                                command=ClientesCadView.ClientsCadView)
        self.bt_return.place(relx=0.8, rely=0.08, width=70, height=60)

        self.name = Label(self.frameup, text='Cliente: ', font='Ivy 13', bg=color("background"))
        self.name.place(relx=0.02, y=40, relheight=0.08, relwidth=0.15)
        self.name_entry = Entry(self.frameup, font='Ivy 14')
        self.name_entry.place(relx=0.17, y=45, relwidth=0.6, relheight=0.05)

        self.srchImg = PhotoImage(file=r"assets\procurar.png")
        self.bt_srch = Button(self.frameup, image=self.srchImg, relief='flat', background=color("background"),
                              command=self)
        self.bt_srch.place(relx=0.80, y=40, relwidth=0.08, relheight=0.06)

        self.clrImg = PhotoImage(file=r"assets\lixo.png")
        self.bt_clr = Button(self.frameup, image=self.clrImg, relief='flat', background=color("background"),
                             command=self)
        self.bt_clr.place(relx=0.90, y=40, relwidth=0.08, relheight=0.06)

        self.lb_idref = Label(self.frameup, text="ID: ", font='Ivy 16', background=color("background"))
        self.lb_idref.place(relx=0.52, rely=0.42, relheight=0.06, relwidth=0.1)
        self.cod = Label(self.frameup, text="0", font='Ivy 16', background=color("background"), justify=LEFT)
        self.cod.place(relx=0.60, rely=0.42, relheight=0.06, relwidth=0.20)

        self.lb_clientref = Label(self.frameup, text="Nome: ", background=color("background"))
        self.lb_clientref.place(relx=0.52, rely=0.50, relheight=0.06, relwidth=0.1)
        self.lb_name = Entry(self.frameup, background=color("background"))
        self.lb_name.place(relx=0.62, rely=0.50, relheight=0.06, relwidth=0.36)

        self.lb_cepref = Label(self.frameup, text="End: ", background=color("background"))
        self.lb_cepref.place(relx=0.52, rely=0.60, relheight=0.06, relwidth=0.1)
        self.lb_cep = Entry(self.frameup, background=color("background"))
        self.lb_cep.place(relx=0.62, rely=0.60, relheight=0.06, relwidth=0.36)

        self.lb_numref = Label(self.frameup, text="Num: ", background=color("background"))
        self.lb_numref.place(relx=0.52, rely=0.70, relheight=0.06, relwidth=0.1)
        self.lb_num = Entry(self.frameup, background=color("background"))
        self.lb_num.place(relx=0.62, rely=0.70, relheight=0.06, relwidth=0.36)

    def init_treebudget(self):
        global tree
        list = self.selectAllClients()

        self.list_header = ['ID', 'Nome', 'Email', 'Documento']
        tree = ttk.Treeview(self.frameup, selectmode="extended", columns=self.list_header, show="headings")
        self.vsb = ttk.Scrollbar(self.frameup, orient="vertical", command=tree.yview)

        tree.configure(yscrollcommand=self.vsb.set)
        tree.place(relx=0.02, rely=0.15, relwidth=0.93, relheight=0.25)
        self.vsb.place(relx=0.94, rely=0.15, relwidth=0.04, relheight=0.25)

        hd = ["nw", "nw", "nw", "nw"]
        h = [10, 120, 120, 90]
        n = 0

        for col in self.list_header:
            tree.heading(col, text=col.title(), anchor=CENTER)
            tree.column(col, width=h[n], anchor=hd[n])
            n += 1

        for item in list:
            tree.insert('', END, values=item)

        tree.bind("<Double-1>", self.OnDoubleClick)

        global ctttree

        self.ctt_header = ['', 'Numero', 'Tipo']

        ctttree = ttk.Treeview(self.frameup, selectmode="extended", columns=self.ctt_header, show="headings")
        self.vsb3 = ttk.Scrollbar(self.frameup, orient="vertical", command=tree.yview)

        ctttree.configure(yscrollcommand=self.vsb3.set)
        ctttree.place(relx=0.02, rely=0.42, relheight=0.17, relwidth=0.45)
        self.vsb3.place(relx=0.46, rely=0.42, relheight=0.17, relwidth=0.03)

        hd = ["nw", "nw", "nw", "nw", "center", "center"]
        h = [10, 100, 50]
        n = 0

        for col in self.ctt_header:
            ctttree.heading(col, text=col.title(), anchor=CENTER)
            ctttree.column(col, width=h[n], anchor=hd[n])
            n += 1

        global ceptree

        self.adress_header = ['id', 'CEP', 'Num', 'Compl.', 'endereço']

        ceptree = ttk.Treeview(self.frameup, selectmode="extended", columns=self.adress_header, show="headings")
        self.vsb2 = ttk.Scrollbar(self.frameup, orient="vertical", command=tree.yview)

        ceptree.configure(yscrollcommand=self.vsb2.set)
        ceptree.place(relx=0.02, rely=0.62, relheight=0.17, relwidth=0.450)
        self.vsb2.place(relx=0.46, rely=0.62, relheight=0.17, relwidth=0.03)

        hd = ["nw", "nw", "nw", "nw", "center", "center"]
        h = [10, 75, 60, 60, 100]
        n = 0

        for col in self.adress_header:
            ceptree.heading(col, text=col.title(), anchor=CENTER)
            ceptree.column(col, width=h[n], anchor=hd[n])
            n += 1

    def init_lists(self):
        self.rmvImg = PhotoImage(file=r'assets\rmv.png')
        self.addImg = PhotoImage(file=r'assets\add.png')

        self.cadctt = Label(self.framedown, text="Telefone/Celular:", font='Ivy 13', bg=color("background"))
        self.cadctt.place(relx=0.030, rely=0.59, relwidth=0.18, relheight=0.08)

        self.cadctt = Label(self.framedown, text="Número :", font='Ivy 12', bg=color("background"))
        self.cadctt.place(relx=0.02, rely=0.645, relwidth=0.10, relheight=0.08)
        self.ctt_entry = Entry(self.framedown)
        self.ctt_entry.place(relx=0.12, rely=0.66, relwidth=0.15, relheight=0.05)

        self.cmbctt = ttk.Combobox(self.framedown, font='Ivy 13')
        self.cmbctt.place(relx=0.03, rely=0.738, relwidth=0.24, relheight=0.05)
        self.cmbctt['values'] = ['Celular', 'Telefone']

        self.rmvImg = PhotoImage(file=r'assets\rmv.png')
        self.bt_cttrmv = Button(self.framedown, image=self.rmvImg, relief='flat')
        self.bt_cttrmv.place(relx=0.30, rely=0.72, relwidth=0.07, relheight=0.08)

        self.addImg = PhotoImage(file=r'assets\add.png')
        self.bt_cttadd = Button(self.framedown, image=self.addImg, relief='flat')
        self.bt_cttadd.place(relx=0.39, rely=0.72, relwidth=0.07, relheight=0.08)

    def clear_frameleft(self):
        for widget in self.frameup.winfo_children():
            widget.destroy()

    def clear_frameright(self):
        for widget in self.framedown.winfo_children():
            widget.destroy()