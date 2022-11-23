import sqlite3
import os
import csv

import requests

from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from datetime import date

from lib.colours import color
import lib.global_variable as glv


class ClientsController:
    def __init__(self):
        pass

    def getEntry(self):
        self.cod = self.lb_id.cget("text")
        self.name = self.name_entry.get()
        self.email = self.email_entry.get()
        self.cp = self.cod_entry.get()
        self.occup = self.occup_entry.get()
        self.birthday = self.birth.get()
        self.datecad = date.today().strftime("%d/%m/%Y")
        self.obs = (self.obs_entry.get("1.0", "end-1c")).strip()
        self.lead = self.lead_entry.get()

    def setEntry(self, cod, name, email, cp, occup, birth, datecad, obs, lead):
        self.lb_id.config(text=cod)
        self.name_entry.insert(END, name)
        self.email_entry.insert(END, email)
        self.cod_entry.insert(END, cp)
        self.birth.insert(END, birth)
        self.occup_entry.insert(END, occup)
        self.lb_date.config(text=datecad)
        self.obs_entry.insert("1.0", obs)
        try:
            self.lead_entry.insert(END, lead)
        except:
            pass

    def getCepEntry(self):
        self.cepcod = self.cepid.cget("text")
        self.cep = self.cep_entry.get()
        self.n = self.n_entry.get()
        self.compl = self.compl_entry.get()

    def setCepEntry(self, cod, cep, n, compl):
        self.cepid.config(text=cod)
        self.cep_entry.insert(END, cep)
        self.n_entry.insert(END, n)
        self.compl_entry.insert(END, compl)

    def getCttEntry(self):
        self.ctt = self.ctt_entry.get()
        self.typectt = self.cmbctt.get()

    def setCttEntry(self, num, mbl):
        self.ctt_entry.insert(END, num)
        if mbl == 'Celular':
            self.cmbctt.current(0)
        elif mbl == 'Telefone':
            self.cmbctt.current(1)

    def clean(self):
        self.lb_id.config(text='0')
        self.cod_entry.delete(0, END)
        self.name_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.occup_entry.delete(0, END)
        self.birth.delete(0, END)
        self.lb_date.config(text="")
        self.lead_entry.delete(0, END)
        self.obs_entry.delete("1.0", END)

    def cleancep(self):
        self.cepid.config(text=' ')
        self.cep_entry.delete(0, END)
        self.n_entry.delete(0, END)
        self.compl_entry.delete(0, END)
        self.cadaddress_entry.delete(0, END)

    def cleanctt(self):
        self.cttid.config(text=' ')
        self.ctt_entry.delete(0, END)
        self.cmbctt.current(0)

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
            self.cursor.execute(""" INSERT INTO tb_clientes (nome, email, cp, profissao, datacad, nascimento, fiscal, lead)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                                (self.name, self.email, self.cp, self.occup, self.datecad, self.birthday,
                                 self.obs, self.lead))
            self.conn.commit()
            messagebox.showinfo('Sucesso', 'Dados inseridos com sucesso')
            self.disconnect_db()

    def insertCep(self):
        self.getEntry()
        self.getCepEntry()
        if self.cod == "0":
            messagebox.showerror('Erro', 'Escolha um usuário para cadastrar um cep.')
        else:
            self.link = f'https://viacep.com.br/ws/{self.cep}/json'

            request = requests.get(self.link)
            self.dic = request.json()
            self.log = self.dic['logradouro']
            self.bai = self.dic['bairro']
            self.loc = self.dic['localidade']
            self.uf = self.dic['uf']

            self.end = f'{self.log} - {self.bai}. {self.loc} - {self.uf}'
            self.cleancep()
            self.connect_db()
            self.cursor.execute(""" INSERT INTO tb_enderecos (cliente_cod, cep, num, compl, endereco)
                    VALUES (?, ?, ?, ?, ?)""",
                                (self.cod, self.cep, self.n, self.compl, self.end))
            self.conn.commit()
            messagebox.showinfo('Sucesso', 'Dados inseridos com sucesso')
            self.disconnect_db()
            self.treecepReload()

    def insertCtt(self):
        self.getEntry()
        self.getCttEntry()
        if self.cod == "0":
            messagebox.showerror('Erro', 'Escolha um usuário para cadastrar um número.')
        else:
            self.cleanctt()
            self.connect_db()
            self.cursor.execute(""" INSERT INTO tb_contatos (linha, tipo, cliente_cod) 
                    VALUES (?, ?, ?)""",
                                (self.ctt, self.typectt, self.cod))
            self.conn.commit()
            messagebox.showinfo('Sucesso', 'Dados inseridos com sucesso')
            self.disconnect_db()
            self.treecttReload()

    def selectAllClients(self):
        auxlist = []
        self.connect_db()
        self.cursor.execute(""" SELECT * FROM tb_clientes """)
        self.info = self.cursor.fetchall()

        for i in self.info:
            auxlist.append(i)

        self.disconnect_db()
        return auxlist

    def selectReportClients(self):
        auxlist = []
        self.connect_db()
        self.cursor.execute(""" SELECT cod, nome, email, cp, profissao, nascimento, fiscal FROM tb_clientes """)
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
        self.cursor.execute(""" SELECT cod, cep, num, compl, endereco FROM tb_enderecos 
                    WHERE cliente_cod = ?""", (cod))
        self.info = self.cursor.fetchall()
        for i in self.info:
            auxlist.append(i)

        self.disconnect_db()
        return auxlist

    def selectCepbyId(self, idcep):
        self.connect_db()
        idcep = int(idcep)
        self.cursor.execute(""" SELECT cod, cep, num, compl, endereco FROM tb_enderecos
                WHERE cod = ?""", (idcep,))
        row = self.cursor.fetchall()
        self.disconnect_db()

        return row

    def selectCttbyId(self, num):
        self.connect_db()
        idctt = num
        self.cursor.execute(""" SELECT * FROM tb_contatos 
                WHERE linha = ?""", (idctt))
        row = self.cursor.fetchall()
        self.disconnect_db()

        return row

    def selectAllCtt(self):
        self.getEntry()
        auxlist = []
        cod = [self.cod]
        self.connect_db()
        self.cursor.execute(""" SELECT linha, tipo FROM tb_contatos 
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
            fiscal = ?,
            lead = ?
            WHERE cod = ?""", (self.name, self.email, self.cp, self.occup, self.birthday, self.obs, self.lead, self.cod))
        self.conn.commit()
        self.disconnect_db()

    def deleteClient(self):
        self.getEntry()
        self.msg_box = messagebox.askquestion('Deletar cliente',
                                              'Tem certeza que deseja deletar o cliente ' + self.name)
        if self.msg_box == 'yes':
            self.connect_db()
            self.cursor.execute(""" DELETE FROM tb_clientes 
                WHERE cod = ? """, (self.cod,))
            self.conn.commit()
            self.disconnect_db()
            self.clean()

    def deleteCep(self):
        self.getEntry()
        self.getCepEntry()
        self.msg_boxcep = messagebox.askquestion('Deletar endereço',
                                                 f'Tem certeza que deseja deletar o endereço {self.cep} \ndo cliente {self.name}')
        if self.msg_boxcep == 'yes':
            self.connect_db()
            self.cursor.execute(""" DELETE FROM tb_enderecos 
                WHERE cod = ? """, (self.cepcod,))
            self.conn.commit()
            self.disconnect_db()
            self.cleancep()
            self.treecepReload()

    def deleteCtt(self):
        self.getEntry()
        self.getCttEntry()
        self.msg_boxctt = messagebox.askquestion('Deletar número',
                                                 f'Tem certeza que deseja deletar o número {self.ctt} \ndo cliente {self.name}')
        if self.msg_boxctt == 'yes':
            self.connect_db()
            self.cursor.execute(""" DELETE FROM tb_contatos 
                WHERE linha = ? """, (self.ctt,))
            self.conn.commit()
            self.disconnect_db()
            self.cleanctt()
            self.treecttReload()

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
            WHERE email LIKE '%s' ORDER BY email ASC """ % email)
        row = self.cursor.fetchall()
        self.disconnect_db()
        self.clean()

        return row

    def treeReload(self, list):

        global tree

        listClient = list

        self.list_header = ['ID', 'Nome', 'Email', 'Documento', 'Profissão', 'Data de nascimento']
        tree = ttk.Treeview(self.framedown, selectmode="extended", columns=self.list_header, show="headings")
        self.vsb = ttk.Scrollbar(self.framedown, orient="vertical", command=tree.yview)

        tree.configure(yscrollcommand=self.vsb.set)
        tree.place(relx=0.01, rely=0.10, relwidth=0.96, relheight=0.490)
        self.vsb.place(relx=0.97, rely=0.10, relwidth=0.02, relheight=0.490)

        hd = ["nw", "nw", "nw", "nw", "center", "center"]
        h = [30, 190, 190, 90, 100, 100]
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

        ceptree = ttk.Treeview(self.framedown, selectmode="extended", columns=self.adress_header, show="headings")
        self.vsb2 = ttk.Scrollbar(self.framedown, orient="vertical", command=tree.yview)

        ceptree.configure(yscrollcommand=self.vsb2.set)
        ceptree.place(relx=0.53, rely=0.81, relheight=0.17, relwidth=0.40)
        self.vsb2.place(relx=0.93, rely=0.81, relheight=0.17, relwidth=0.03)

        hd = ["nw", "nw", "nw", "nw", "center", "center"]
        h = [10, 75, 40, 40, 100]
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

        self.ctt_header = ['Numero', 'Tipo']

        ctttree = ttk.Treeview(self.framedown, selectmode="extended", columns=self.ctt_header, show="headings")
        self.vsb3 = ttk.Scrollbar(self.framedown, orient="vertical", command=tree.yview)

        ctttree.configure(yscrollcommand=self.vsb3.set)
        ctttree.place(relx=0.03, rely=0.81, relheight=0.17, relwidth=0.40)
        self.vsb3.place(relx=0.43, rely=0.81, relheight=0.17, relwidth=0.03)

        hd = ["nw", "nw", "nw", "nw", "center", "center"]
        h = [120, 120]
        n = 0

        for col in self.ctt_header:
            ctttree.heading(col, text=col.title(), anchor=CENTER)
            ctttree.column(col, width=h[n], anchor=hd[n])
            n += 1

        for item in listctt:
            ctttree.insert('', END, values=item)

        ctttree.bind("<Double-1>", self.OnDoubleClick3)

    @staticmethod
    def treeSelect():
        treev_data = tree.focus()
        treev_dicionario = tree.item(treev_data)
        treev_list = treev_dicionario['values']

        return treev_list

    @staticmethod
    def ceptreeSelect():
        ceptreev_data = ceptree.focus()
        ceptreev_dicionario = ceptree.item(ceptreev_data)
        ceptreev_list = ceptreev_dicionario['values']

        return ceptreev_list

    @staticmethod
    def ctttreeSelect():
        ctttreev_data = ctttree.focus()
        ctttreev_dicionario = ctttree.item(ctttreev_data)
        ctttreev_list = ctttreev_dicionario['values']

        return ctttreev_list

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

    def OnDoubleClick(self, event):
        self.clean()
        cod = self.treeSelect()
        values = self.selectClientbyId(int(cod[0]))
        self.setEntry(values[0][0], values[0][1], values[0][2], values[0][3], values[0][4], values[0][5],
                      values[0][6], values[0][7], values[0][8])
        self.treecepReload()
        self.treecttReload()
        self.cleanctt()
        self.cleancep()

    def OnDoubleClick2(self, event):
        self.cleancep()
        cepcod = self.ceptreeSelect()
        values = self.selectCepbyId(cepcod[0])
        self.setCepEntry(values[0][0], values[0][1], values[0][2], values[0][3])
        self.verifyCep()

    def OnDoubleClick3(self, event):
        self.cleanctt()
        ctt = self.ctttreeSelect()
        self.setCttEntry(ctt[0], ctt[1])

class ClientsView(ClientsController):
    def __init__(self, frameup, framedown, framebar):
        self.list_cli = ttk.Treeview
        self.framedown = framedown
        self.frameup = frameup
        self.framebar = framebar
        self.setup()

    def setup(self):
        self.init_Clients()
        self.init_tree()
        self.init_lists()

    def init_Clients(self):
        self.init_layout()
        self.init_buttons()

    def init_layout(self):
        self.srchImg = PhotoImage(file=r"assets\procurar.png")
        self.bgImg = PhotoImage(file=r'assets\CARD.png')
        self.bg = Label(self.frameup, image=self.bgImg)
        self.bg.place(relx=0, rely=0, relwidth=1, height=445)

        self.bg2Img = PhotoImage(file=r'assets\CARD2.png')
        self.bg2 = Label(self.framedown, image=self.bg2Img, bg=color("background2"))
        self.bg2.place(relwidth=1, relheight=1)

        self.title = Label(self.frameup, text="Clientes", font="Ivy 18 bold", bg="#CEDCE4")
        self.title.place(relx=0.015, rely=0.005, relwidth=0.24, height= 28)

        self.lb_cod = Label(self.frameup, text="CPF/CNPJ:", font="Ivy 10", bg=color("background"))
        self.lb_cod.place(relx=0.002, rely=0.08, relwidth=0.2)
        self.cod_entry = Entry(self.frameup, font="Ivy 11")
        self.cod_entry.place(relx=0.20, rely=0.08, relwidth=0.30, relheight=0.05)

        self.lb_name = Label(self.frameup, text="Nome:", font="Ivy 11", bg=color("background"))
        self.lb_name.place(relx=0.075, rely=0.15, relwidth=0.1)
        self.name_entry = Entry(self.frameup, font="Ivy 11")
        self.name_entry.place(relx=0.20, rely=0.15, relwidth=0.75, relheight=0.05)

        self.lb_email = Label(self.frameup, text="Email:", font="Ivy 11", bg=color("background"))
        self.lb_email.place(relx=0.08, rely=0.22, relwidth=0.1)
        self.email_entry = Entry(self.frameup, font="Ivy 11")
        self.email_entry.place(relx=0.20, rely=0.22, relwidth=0.75, relheight=0.05)

        Label(self.frameup, text="________________________________________________", font="Ivy 13",
              bg=color("background")). \
            place(relx=0, rely=0.27, relwidth=1, relheight=0.04)

        self.lb_occup = Label(self.frameup, text="Profissão:", font="Ivy 11", bg=color("background"))
        self.lb_occup.place(relx=0.02, rely=0.32, relwidth=0.16)
        self.occup_entry = Entry(self.frameup, font="Ivy 11")
        self.occup_entry.place(relx=0.02, rely=0.37, relwidth=0.58, relheight=0.05)

        self.lb_birth = Label(self.frameup, text="Data de Nasc.:", font="Ivy 11", bg=color("background"))
        self.lb_birth.place(relx=0.65, rely=0.32, relwidth=0.24)
        self.birth = Entry(self.frameup)
        self.birth.place(relx=0.65, rely=0.37, relwidth=0.30, relheight=0.05)

        Label(self.frameup, text="________________________________________________", font="Ivy 13",
              bg=color("background")). \
            place(relx=0, rely=0.42, relwidth=1, relheight=0.04)

        Label(self.frameup, text="                                                 ", font="Ivy 13 bold",
              bg=color("background-bar")). \
            place(relx=0, rely=0.84, relwidth=1, relheight=0.02)


        self.cadlead = Label(self.frameup, text="Como nos conheceu:", font="Ivy 13", background=color("background"))
        self.cadlead.place(relx=0.02, rely=0.49)
        self.lead_entry = Entry(self.frameup, font='Ivy 13')
        self.lead_entry.place(relx=0.40, rely=0.49, relwidth=0.57, relheight=0.05)

        self.cadobs = Label(self.frameup, text="Observação:", font="Ivy 13", background=color("background"))
        self.cadobs.place(relx=0.02, rely=0.56)
        self.obs_entry = Text(self.frameup, font='Ivy 14')
        self.obs_entry.place(relx=0.03, rely=0.62, relwidth=0.94, relheight=0.20)

        self.cadid = Label(self.framedown, text="ID: ", font="Ivy 20", background="#CEDCE4")
        self.cadid.place(relx=0.02, rely=0.013)
        self.lb_id = Label(self.framedown, text="0", font="Ivy 20", background="#CEDCE4", justify=LEFT)
        self.lb_id.place(relx=0.07, rely=0.013)

        self.caddate = Label(self.framedown, text="Registrado em: ", font="Ivy 20", background="#CEDCE4")
        self.caddate.place(relx=0.56, rely=0.013)
        self.lb_date = Label(self.framedown, text="", font="Ivy 20", background="#CEDCE4")
        self.lb_date.place(relx=0.80, rely=0.013)

    def init_buttons(self):

        self.bt_pesquisar = Button(self.frameup, image=self.srchImg, bg=color("background"), relief='flat',
                                   command=self.searchClient)
        self.bt_pesquisar.place(relx=0.79, rely=0.07, relwidth=0.08, relheight=0.07)

        self.clrImg = PhotoImage(file=r"assets\lixo.png")
        self.bt_limpar = Button(self.frameup, image=self.clrImg, bg=color("background"), relief='flat',
                                command=self.clean)
        self.bt_limpar.place(relx=0.88, rely=0.07, relwidth=0.08, relheight=0.07)

        self.rprtImg = PhotoImage(file=r'assets\report.png')
        self.bt_report = Button(self.framebar,image=self.rprtImg, relief='flat',
                                command=self.genReport)
        self.bt_report.place(relx=0.8, rely=0.08, width=70, height=60)

        self.insrtImg = PhotoImage(file=r"assets\INSERIR.png")
        self.bt_insert = Button(self.frameup, image=self.insrtImg, relief='flat',
                                command=self.crtClient)
        self.bt_insert.place(relx=0.020, rely=0.88, relwidth=0.225, relheight=0.1)

        self.attImg = PhotoImage(file=r"assets\ATUALIZAR.png")
        self.bt_update = Button(self.frameup, image=self.attImg, relief='flat',
                                command=self.updtClient)
        self.bt_update.place(relx=0.265, rely=0.88, relwidth=0.225, relheight=0.1)

        self.dltImg = PhotoImage(file=r"assets\DELETAR.png")
        self.bt_delete = Button(self.frameup, image=self.dltImg, relief='flat',
                                command=self.rmvClient)
        self.bt_delete.place(relx=0.51, rely=0.88, relwidth=0.225, relheight=0.1)

        self.imprtImg = PhotoImage(file=r"assets\IMPORTAR.png")
        self.bt_import = Button(self.frameup, image=self.imprtImg, relief='flat',
                                command=self.open_csv)
        self.bt_import.place(relx=0.755, rely=0.88, relwidth=0.225, relheight=0.1)

    def init_tree(self):
        global tree
        list = self.selectAllClients()

        self.list_header = ['ID', 'Nome', 'Email', 'Documento', 'Profissão', 'Data de nascimento']
        tree = ttk.Treeview(self.framedown, selectmode="extended", columns=self.list_header, show="headings")
        self.vsb = ttk.Scrollbar(self.framedown, orient="vertical", command=tree.yview)

        tree.configure(yscrollcommand=self.vsb.set)
        tree.place(relx=0.01, rely=0.10, relwidth=0.96, relheight=0.490)
        self.vsb.place(relx=0.97, rely=0.10, relwidth=0.02, relheight=0.490)

        hd = ["nw", "nw", "nw", "nw", "center", "center"]
        h = [30, 190, 190, 90, 100, 100]
        n = 0

        for col in self.list_header:
            tree.heading(col, text=col.title(), anchor=CENTER)
            tree.column(col, width=h[n], anchor=hd[n])
            n += 1

        for item in list:
            tree.insert('', END, values=item)

        tree.bind("<Double-1>", self.OnDoubleClick)

        global ceptree

        self.adress_header = ['id', 'CEP', 'Num', 'Compl.', 'endereço']

        ceptree = ttk.Treeview(self.framedown, selectmode="extended", columns=self.adress_header, show="headings")
        self.vsb2 = ttk.Scrollbar(self.framedown, orient="vertical", command=tree.yview)

        ceptree.configure(yscrollcommand=self.vsb2.set)
        ceptree.place(relx=0.53, rely=0.81, relheight=0.17, relwidth=0.40)
        self.vsb2.place(relx=0.93, rely=0.81, relheight=0.17, relwidth=0.03)

        hd = ["nw", "nw", "nw", "nw", "center", "center"]
        h = [10, 75, 40, 40, 100]
        n = 0

        for col in self.adress_header:
            ceptree.heading(col, text=col.title(), anchor=CENTER)
            ceptree.column(col, width=h[n], anchor=hd[n])
            n += 1

        ceptree.bind("<Double-1>", self.OnDoubleClick2)

        global ctttree

        self.ctt_header = ['Numero', 'Tipo']

        ctttree = ttk.Treeview(self.framedown, selectmode="extended", columns=self.ctt_header, show="headings")
        self.vsb3 = ttk.Scrollbar(self.framedown, orient="vertical", command=tree.yview)

        ctttree.configure(yscrollcommand=self.vsb3.set)
        ctttree.place(relx=0.03, rely=0.81, relheight=0.17, relwidth=0.40)
        self.vsb3.place(relx=0.43, rely=0.81, relheight=0.17, relwidth=0.03)

        hd = ["nw", "nw", "nw", "nw", "center", "center"]
        h = [120, 120]
        n = 0

        for col in self.ctt_header:
            ctttree.heading(col, text=col.title(), anchor=CENTER)
            ctttree.column(col, width=h[n], anchor=hd[n])
            n += 1

        ctttree.bind("<Double-1>", self.OnDoubleClick3)

    def init_lists(self):
        self.rmvImg = PhotoImage(file=r'assets\rmv.png')
        self.addImg = PhotoImage(file=r'assets\add.png')

        self.cttid = Label(self.framedown, text=' ', fg=color("background"), bg=color("background"))
        self.cttid.place(relx=0.03, rely=0.6, relheight=0.01, relwidth=0.01)

        self.cadctt = Label(self.framedown, text="Telefone/Celular:", font='Ivy 14', bg=color("background"))
        self.cadctt.place(relx=0.020, rely=0.595, relwidth=0.18, relheight=0.05)

        self.cadctt = Label(self.framedown, text="Número :", font='Ivy 13', bg=color("background"))
        self.cadctt.place(relx=0.02, rely=0.645, relwidth=0.10, relheight=0.08)
        self.ctt_entry = Entry(self.framedown)
        self.ctt_entry.place(relx=0.12, rely=0.66, relwidth=0.15, relheight=0.05)

        self.cmbctt = ttk.Combobox(self.framedown, font='Ivy 13')
        self.cmbctt.place(relx=0.03, rely=0.738, relwidth=0.24, relheight=0.05)
        self.cmbctt['values'] = ['Celular', 'Telefone']
        self.cmbctt.current(0)

        self.bt_cttrmv = Button(self.framedown, image=self.rmvImg, relief='flat',
                                command=self.rmvCtt)
        self.bt_cttrmv.place(relx=0.30, rely=0.72, relwidth=0.07, relheight=0.08)

        self.bt_cttadd = Button(self.framedown, image=self.addImg, relief='flat',
                                command=self.crtCtt)
        self.bt_cttadd.place(relx=0.39, rely=0.72, relwidth=0.07, relheight=0.08)


        self.cepid = Label(self.framedown, text=' ', fg=color("background"), bg=color("background"))
        self.cepid.place(relx=0.5, rely=0.6, relheight=0.01, relwidth=0.01)

        self.cadaddress = Label(self.framedown, text="Endereço:", font='Ivy 14', bg=color("background"))
        self.cadaddress.place(relx=0.48, rely=0.595, relwidth=0.18, relheight=0.05)

        self.cadcep= Label(self.framedown, text="CEP :", font='Ivy 12', bg=color("background"))
        self.cadcep.place(relx=0.46, rely=0.645, relwidth=0.18, relheight=0.08)
        self.cep_entry = Entry(self.framedown)
        self.cep_entry.place(relx=0.58, rely=0.66, relwidth=0.08, relheight=0.05)

        self.bt_srch = Button(self.framedown, image=self.srchImg, relief='flat', background=color("background"),
                                command=self.verifyCep)
        self.bt_srch.place(relx=0.66, rely=0.66, relwidth=0.035, relheight=0.05)

        self.cadn = Label(self.framedown, text="N° :", font='Ivy 12', bg=color("background"))
        self.cadn.place(relx=0.70, rely=0.645, relwidth=0.04, relheight=0.08)
        self.n_entry = Entry(self.framedown)
        self.n_entry.place(relx=0.74, rely=0.66, relwidth=0.05, relheight=0.05)

        self.cadcompl = Label(self.framedown, text="Compl.:", font='Ivy 12', bg=color("background"))
        self.cadcompl.place(relx=0.80, rely=0.645, relwidth=0.07, relheight=0.08)
        self.compl_entry = Entry(self.framedown)
        self.compl_entry.place(relx=0.88, rely=0.66, relwidth=0.08, relheight=0.05)

        self.cadaddress_entry = Entry(self.framedown, font='Ivy 13', bg=color("background"), justify=LEFT)
        self.cadaddress_entry.place(relx=0.53, rely=0.73, relwidth=0.25, relheight=0.06)


        self.bt_addressrmv = Button(self.framedown, image=self.rmvImg, relief='flat',
                                    command=self.deleteCep)
        self.bt_addressrmv.place(relx=0.80, rely=0.72, relwidth=0.07, relheight=0.08)

        self.bt_addressadd = Button(self.framedown, image=self.addImg, relief='flat',
                                    command=self.crtCep)
        self.bt_addressadd.place(relx=0.89, rely=0.72, relwidth=0.07, relheight=0.08)

    def crtClient(self):
        self.insertClient()

        for widget in self.framedown.winfo_children():
            widget_class = widget.__class__.__name__
            if widget_class == 'Treeview':
                widget.destroy()

        self.init_tree()

    def crtCep(self):
        if self.cep_entry.get() == '' or self.n_entry.get() == '':
            messagebox.showerror('Erro', 'Preencha os dados obrigatórios')
        else:
            self.insertCep()

    def crtCtt(self):
        if self.ctt_entry.get() == '':
            messagebox.showerror('Erro', 'Preencha os dados obrigatórios')
        else:
            self.insertCtt()

    def rmvClient(self):
        self.deleteClient()

        for widget in self.framedown.winfo_children():
            widget_class = widget.__class__.__name__
            if widget_class == 'Treeview':
                widget.destroy()

        self.init_tree()

    def rmvCep(self):
        self.deleteCep()

    def rmvCtt(self):
        self.deleteCtt()

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
        self.clean()
        self.datecad = date.today().strftime("%d/%m/%Y")
        with open(csv_path, "rt") as f:
            reader = csv.reader(f)
            for row in reader:
                entry = row
                self.name_entry.insert(END, entry[0])
                self.email_entry.insert(END, entry[1])
                self.cod_entry.insert(END, entry[2])
                self.birth.insert(END, entry[4])
                self.occup_entry.insert(END, entry[3])
                self.lead_entry.insert(END, entry[5])
                self.obs_entry.insert("1.0", entry[6])

                self.getEntry()
                self.cp = self.cp.replace(".", "").replace("/", "").replace("-", "")
                self.connect_db()
                self.cursor.execute(""" INSERT INTO tb_clientes (nome, email, cp, profissao, datacad, nascimento, fiscal, lead)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                                    (self.name, self.email, self.cp, self.occup, self.datecad, self.birthday,
                                     self.obs, self.lead))
                self.conn.commit()
                self.disconnect_db()

                self.connect_db()
                self.cursor.execute(""" SELECT cod FROM tb_clientes 
                    WHERE cp = ?""", (self.cp,))
                cod = self.cursor.fetchall()[0][0]
                self.disconnect_db()
                self.lb_id.config(text=str(cod))

                for index, element in enumerate(row):
                    if index > 6:
                        self.num = element.replace(" ", "").replace("(", "").replace(")", "").replace("-", "")
                        if len(self.num) == 11:
                            self.type = 'Celular'
                        elif len(self.num) == 10:
                            self.type = 'Telefone'
                        try:
                            self.connect_db()
                            self.cursor.execute(f""" INSERT INTO tb_contatos (linha, tipo, cliente_cod) 
                                        VALUES (?, ?, ?)""",
                                                    (int(self.num), self.type, int(self.lb_id.cget("text"))))
                            self.conn.commit()
                            self.disconnect_db()
                        except:
                            pass

                self.clean()

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

        if self.name_entry.get() == '' and self.email_entry.get() == '':
           list = self.selectAllClients()
        else:
            if self.name_entry.get() != '':
                list = self.searchClientByName()
            if self.email_entry.get() != '':
                list = self.searchClientByEmail()

        self.treeReload(list)

    def genReport(self):
        csv_path = os.path.join(
            glv.get_variable("APP_PATH"),
            glv.get_variable("DATA_DIR"),
            "clientes.csv"
        )

        data = []
        for row in tree.get_children():
            self.clean()
            self.cleanctt()
            dataline = []
            values = self.selectClientbyId(int(tree.item(row, 'values')[0]))
            self.setEntry(values[0][0], values[0][1], values[0][2], values[0][3], values[0][5], values[0][4],
                          values[0][6], values[0][7], values[0][8])
            self.getEntry()
            dataline.append(self.name)
            dataline.append(self.email)
            dataline.append(self.cp)
            dataline.append(self.occup)
            dataline.append(self.birthday)
            dataline.append(self.lead)
            dataline.append(self.obs)

            datactt = self.selectAllCtt()
            for rowctt in datactt:

                dataline.append(rowctt[0])

            data.append(dataline)
        print(csv_path)

        file = open(csv_path, 'w+', newline='')

        with file:
            write = csv.writer(file)
            write.writerows(data)

        self.setup()