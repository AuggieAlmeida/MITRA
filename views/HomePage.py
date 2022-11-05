import sqlite3
import os
import csv
import requests

from tkinter import *
from tkinter import ttk

from PIL import ImageTk
from tkinter import messagebox

from datetime import date

from views import ClientesCadView

from lib.colours import color
import lib.global_variable as glv


class HomeController:
    def __init__(self):
        pass

    def getEntry(self):
        self.cod = int(self.lb_id.cget("text"))
        self.name = self.name_entry.get()
        self.email = self.email_entry.get()
        self.cp = self.cod_entry.get()
        self.occup = self.occup_entry.get()
        self.birthday = self.birth.get()
        self.datecad = date.today().strftime("%d/%m/%Y")
        self.obs = self.obs_entry.get("1.0", END)

    def setEntry(self, cod, name, email, cp, occup, birth, datecad, obs):
        self.lb_id.config(text=cod)
        self.name_entry.insert(END, name)
        self.email_entry.insert(END, email)
        self.cod_entry.insert(END, cp)
        self.birth.insert(END, birth)
        self.occup_entry.insert(END, occup)
        self.lb_date.config(text=datecad)
        self.obs_entry.insert("1.0", obs)

    def getCepEntry(self):
        self.cep = self.cep_entry.get()
        self.n = self.n_entry.get()
        self.compl = self.compl_entry.get()

    def setCepEntry(self, cep, n, compl):
        self.cep.insert(END, cep)
        self.n.insert(END, n)
        self.compl.insert(END, compl)

    def clean(self):
        self.cod_entry.delete(0, END)
        self.name_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.occup_entry.delete(0, END)
        self.birth.delete(0, END)
        self.obs_entry.delete("1.0", END)

    def cleancep(self):
        self.cep_entry.delete(0, END)
        self.n_entry.delete(0, END)
        self.compl_entry.delete(0, END)

    def connect_db(self):
        db_path = os.path.join(
            glv.get_variable("APP_PATH"),
            "SPDB.db"
        )
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def disconnect_db(self):
        self.conn.close()

    def insertClient(self):
        self.getEntry()
        if self.name == '':
            messagebox.showerror('Erro', 'Preencha os dados obrigatórios')
        else:
            self.getEntry()
            self.clean()
            self.connect_db()
            self.cursor.execute(""" INSERT INTO tb_clientes (nome, email, cp, profissao, datacad, nascimento, fiscal)
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                                (self.name, self.email, self.cp, self.occup, self.datecad, self.birthday,
                                 self.obs))
            self.conn.commit()
            messagebox.showinfo('Sucesso', 'Dados inseridos com sucesso')
            self.disconnect_db()

    def insertCep(self):
        self.getEntry()
        self.getCepEntry()
        if self.cep == '' or self.n == '':
            messagebox.showerror('Erro', 'Preencha os dados obrigatórios')
        else:
            self.getEntry()
            self.cleancep()
            self.connect_db()
            self.cursor.execute(""" INSERT INTO tb_enderecos (cliente_cod, cep, num, compl)
                VALUES (?, ?, ?, ?)""",
                                (self.cod, self.cep, self.n, self.compl))
            self.conn.commit()
            messagebox.showinfo('Sucesso', 'Dados inseridos com sucesso')
            self.disconnect_db()
            self.treecepReload()

    def selectAllClients(self):
        auxlist = []
        self.connect_db()
        self.cursor.execute(""" SELECT * FROM tb_clientes """)
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

    def updateClient(self):
        self.getEntry()
        self.connect_db()
        self.cursor.execute(""" UPDATE tb_clientes SET
            nome = ?,
            email = ?,
            cp = ?,
            profissao = ?,
            nascimento = ?,
            fiscal = ?
            WHERE cod = ?""", (self.name, self.email, self.cp, self.occup, self.birthday, self.obs, self.cod))
        self.conn.commit()
        self.disconnect_db()

    def deleteClient(self):
        self.getEntry()
        self.msg_box = messagebox.askquestion('Deletar cliente',
                                              'Tem certeza que deseja deletar o cliente ' + self.name)
        self.connect_db()
        self.cursor.execute(""" DELETE FROM tb_clientes 
            WHERE cod = ? """, (self.cod,))
        self.conn.commit()
        self.disconnect_db()
        self.clean()

    def read_csv(self, filename):
        self.getEntry()
        with open(filename, "rt") as f:
            reader = csv.reader(f)
            next(csv.reader(f), None)

            for entry in reader:
                try:
                    self.connect_db()
                    self.cursor.execute(""" INSERT INTO tb_clientes (nome, email, cp, profissao, datacad, nascimento, fiscal)
                VALUES (?, ?, ?, ?, ?, ?, ?)""", (entry[0], entry[1], entry[2], entry[3], self.datecad, entry[4], entry[5]))
                    self.conn.commit()
                    self.disconnect_db()

                except csv.Error as e:
                    print(f'Line: {reader.line_num}, Record: {entry[0], entry[1], entry[2], entry[3], self.datecad, entry[4], entry[5]}')

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

    def searchClientByEmail(self):
        self.connect_db()
        self.email_entry.insert(END, '%')
        email = self.email_entry.get()
        self.cursor.execute(""" SELECT * FROM tb_clientes
            WHERE email LIKE '%s' ORDER BY nome ASC """ % email)
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

    def treecepReload(self):
        global treecep
        listcep = self.selectAllCep()

        self.adress_header = ['CEP', 'Num', 'Complemento']

        ceptree = ttk.Treeview(self.framedown, selectmode="extended", columns=self.adress_header, show="headings")
        self.vsb2 = ttk.Scrollbar(self.framedown, orient="vertical", command=tree.yview)

        ceptree.configure(yscrollcommand=self.vsb2.set)
        ceptree.place(relx=0.53, rely=0.81, relheight=0.17, relwidth=0.40)
        self.vsb2.place(relx=0.93, rely=0.81, relheight=0.17, relwidth=0.03)

        hd = ["nw", "nw", "nw"]
        h = [100, 100, 100]
        n = 0

        for col in self.adress_header:
            ceptree.heading(col, text=col.title(), anchor=CENTER)
            ceptree.column(col, width=h[n], anchor=hd[n])
            n += 1

        for item in listcep:
            ceptree.insert('', END, values=item)

    def treecttReload(self):
        global ctttree
        listcep = self.selectAllCep()

        self.ctt_header = ['', 'Numero', 'Tipo']

        ctttree = ttk.Treeview(self.framedown, selectmode="extended", columns=self.ctt_header, show="headings")
        self.vsb3 = ttk.Scrollbar(self.framedown, orient="vertical", command=tree.yview)

        ctttree.configure(yscrollcommand=self.vsb3.set)
        ctttree.place(relx=0.03, rely=0.795, relheight=0.17, relwidth=0.40)
        self.vsb3.place(relx=0.43, rely=0.795, relheight=0.17, relwidth=0.03)

        hd = ["nw", "nw", "nw", "nw", "center", "center"]
        h = [10, 100, 100]
        n = 0

        for col in self.ctt_header:
            ctttree.heading(col, text=col.title(), anchor=CENTER)
            ctttree.column(col, width=h[n], anchor=hd[n])
            n += 1

    def OnDoubleClick(self, event):
        self.clean()
        cod = self.treeSelect()
        values = self.selectClientbyId(int(cod[0]))
        self.setEntry(values[0][0], values[0][1], values[0][2], values[0][3], values[0][4], values[0][5],
                      values[0][6], values[0][7])
        self.treecepReload()


class HomePage(HomeController):

    def __init__(self, frameup, framedown, framebar):
        self.list_header = ['ID', 'Nome', 'Email', 'Documento', 'Nascimento', 'Profissão']
        self.list_cli = ttk.Treeview
        self.framedown = framedown
        self.frameup = frameup
        self.framebar = framebar
        self.setup()
        self.selectAllClients()

    def setup(self):
        self.init_Home()

    def init_Home(self):
        self.init_layout()

    def init_layout(self):
        self.bgImg = PhotoImage(file=r'assets\CARD.png')
        self.bg = Label(self.frameup, image=self.bgImg)
        self.bg.place(relx=0, rely=0, relwidth=1, height=445)

        self.bg2Img = PhotoImage(file=r'assets\CARD2.png')
        self.bg2 = Label(self.framedown, image=self.bg2Img, bg=color("background2"))
        self.bg2.place(relwidth=1, relheight=1)

        self.title = Label(self.frameup, text="Home", font="Ivy 18 bold", bg="#CEDCE4")
        self.title.place(relx=0.008, rely=0.005, relwidth=0.20, height= 28)

        self.text = Label(self.framedown, text="Administrativo", font="Ivy 20 bold", bg="#CEDCE4")
        self.text.place(relx=0.01, rely=0.018, relwidth=0.3, relheight=0.05)


        self.logoImg = PhotoImage(file=r'assets\LOGO.PNG')
        self.logo = Label(self.frameup, image=self.logoImg, background=color("background"))
        self.logo.place(x=0, y=39, relwidth=1, height=390)


        Label(self.frameup, text="                                                 ", font="Ivy 13 bold",
              bg=color("background-bar")). \
            place(relx=0, rely=0.84, relwidth=1, relheight=0.02)

    def init_tree(self):
        pass

    def init_lists(self):
        pass

    def crtClient(self):
        self.insertClient()

        for widget in self.framedown.winfo_children():
            widget_class = widget.__class__.__name__
            if widget_class == 'Treeview':
                widget.destroy()

        self.init_tree()

    def crtCep(self):
        self.insertCep()

        for widget in self.framedown.winfo_children():
            widget_class = widget.__class__.__name__
            if widget_class == 'Listbox':
                widget.destroy()

    def rmvClient(self):
        self.deleteClient()

        for widget in self.framedown.winfo_children():
            widget_class = widget.__class__.__name__
            if widget_class == 'Treeview':
                widget.destroy()

        self.init_tree()

    def updtClient(self):
        self.updateClient()

        for widget in self.framedown.winfo_children():
            widget_class = widget.__class__.__name__
            if widget_class == 'Treeview':
                widget.destroy()

        self.init_tree()

    def open_csv(self):
        csv_path = os.path.join(
            glv.get_variable("APP_PATH"),
            glv.get_variable("DATA_DIR"),
            "base.csv"
        )
        self.read_csv(csv_path)

        for widget in self.framedown.winfo_children():
            widget_class = widget.__class__.__name__
            if widget_class == 'Treeview':
                widget.destroy()

        self.init_tree()

    def searchClient(self):
        for widget in self.framedown.winfo_children():
            widget_class = widget.__class__.__name__
            if widget_class == 'Treeview':
                widget.destroy()
        global tree

        list = self.searchClientByName()


        self.list_header = ['ID', 'Nome', 'Email', 'Documento', 'Profissão', 'Data de nascimento']
        tree = ttk.Treeview(self.framedown, selectmode="extended", columns=self.list_header, show="headings")
        self.vsb = ttk.Scrollbar(self.framedown, orient="vertical", command=tree.yview)

        tree.configure(yscrollcommand=self.vsb.set)
        tree.place(relx=0.01, rely=0.10, relwidth=0.96, relheight=0.490)
        self.vsb.place(relx=0.97, rely=0.10, relwidth=0.02, relheight=0.490)

        hd = ["nw", "nw", "nw", "nw", "center", "center"]
        h = [10, 170, 190, 90, 120, 100]
        n = 0

        for col in self.list_header:
            tree.heading(col, text=col.title(), anchor=CENTER)
            tree.column(col, width=h[n], anchor=hd[n])
            n += 1

        for item in list:
            tree.insert('', END, values=item)

        tree.bind("<Double-1>", self.OnDoubleClick)

    def verifyCep(self):
        self.cep = self.cep_entry.get()
        if len(self.cep) == 8:
            self.cep = self.cep.replace("-", "").replace(".", "").replace(" ", "")
            self.link = f'https://viacep.com.br/ws/{self.cep}/json'

            request = requests.get(self.link)
            self.dic = request.json()

            self.log = self.dic['logradouro']
            self.bai = self.dic['bairro']
            self.loc = self.dic['localidade']
            self.uf = self.dic['uf']

            self.cadaddress_entry.insert(END, f'{self.log}, {self.bai} - {self.loc}, {self.uf}')
        else:
            messagebox.showinfo("ERRO", "Cep inválido")