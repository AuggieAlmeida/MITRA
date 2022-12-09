import csv
import random
import sqlite3
import os

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import csv

from datetime import date

from lib.colours import color
import lib.global_variable as glv


class ComercialController:
    def __init__(self):
        pass

    def getclientEntry(self):
        self.cod = self.lb_id.cget("text")
        self.name = self.lb_name.get()

    def setclientEntry(self, cod, name):
        self.lb_id.config(text=cod)
        self.lb_name.insert(END, name)

    def getCepEntry(self):
        self.cepcod = self.lb_cepid.cget("text")
        self.cep = self.lb_cep.get()

    def setCepEntry(self, cod, end):
        self.lb_cepid.config(text=cod)
        self.lb_cep.insert(END, f'{end}')

    def getCttEntry(self):
        if self.lb_num.get() == "":
            self.num = ""
        else:
            self.num = self.lb_num.get()

    def setCttEntry(self, end):
        self.lb_num.insert(END, f'{end}')

    def getProdEntry(self):
        self.cod = self.prodcod.cget("text")
        self.prod.get()
        self.vkg = self.valuekg.cget("text")
        self.vm = self.valuem.cget("text")
        self.vm2 = self.valuem2.cget("text")
        self.vuni = self.valueuni.cget("text")

    def setProdEntry(self, cod, name, kg, m, m2, uni):
        self.prodcod.config(text=cod)
        self.prod.insert(END, name)
        self.valuekg.config(text=kg)
        self.valuem.config(text=m)
        self.valuem2.config(text=m2)
        self.valueuni.config(text=uni)

    def clean(self):
        self.lb_name.delete(0, END)

    def cleancep(self):
        self.lb_cepid.config(text="0")
        self.lb_cep.delete(0, END)

    def cleanctt(self):
        self.lb_num.delete(0, END)

    def cleanprod(self):
        self.prod.config(state=NORMAL)
        self.prodcod.config(text=' ')
        self.prod.delete(0, END)
        self.kg.delete(0, END)
        self.m.delete(0, END)
        self.m2.delete(0, END)
        self.uni.delete(0, END)
        self.lblgain.config(text='')

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
        self.getclientEntry()
        auxlist = []
        cod = [self.cod]
        self.connect_db()
        self.cursor.execute(""" SELECT cod, cep, endereco, cid FROM tb_enderecos 
                    WHERE cliente_cod = ?""", (cod))
        self.info = self.cursor.fetchall()
        for i in self.info:
            auxlist.append(i)

        self.disconnect_db()
        return auxlist

    def selectCepbyId(self, idcep):
        self.connect_db()
        idcep = int(idcep)
        self.cursor.execute(""" SELECT cod, cep, endereco, cid FROM tb_enderecos
                WHERE cod = ?""", (idcep,))
        row = self.cursor.fetchall()
        self.disconnect_db()

        return row

    def selectAllCtt(self):
        self.getclientEntry()
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

    def searchClientByName(self):
        self.connect_db()
        self.name_entry.insert(END, '%')
        nome = self.name_entry.get()
        self.cursor.execute(""" SELECT * FROM tb_clientes
            WHERE nome LIKE '%s' ORDER BY nome ASC """ % nome)
        row = self.cursor.fetchall()
        self.disconnect_db()

        return row

    def selectAllProducts(self):
        auxlist = []
        self.connect_db()
        self.cursor.execute(""" SELECT cod, servico, material, kg, m, m2, unit FROM tb_produtos """)
        self.info = self.cursor.fetchall()

        for i in self.info:
            auxlist.append(i)

        self.disconnect_db()
        return auxlist

    def selectAllOrders(self):
        auxlist = []
        self.connect_db()
        self.cursor.execute(""" SELECT cod, cliente, status, pagamento, parcelas, subtotal, discount, total, data, tipo FROM tb_comercial ORDER BY data desc""")
        self.info = self.cursor.fetchall()

        for i in self.info:
            auxlist.append(i)

        self.disconnect_db()
        return auxlist

    def selectProductbyId(self, idprod=int):
        self.connect_db()
        self.cursor.execute(""" SELECT * FROM tb_produtos 
            WHERE cod = ?""", (idprod,))
        row = self.cursor.fetchall()
        self.disconnect_db()

        return row

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

    @staticmethod
    def budgettreeSelect():
        treev_data = productTree.focus()
        treev_dicionario = productTree.item(treev_data)
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

        tree.bind("<ButtonRelease-1>", self.OnDoubleClick)

    def treecepReload(self):
        global ceptree
        listcep = self.selectAllCep()

        self.adress_header = ['id', 'CEP', 'endereço']

        ceptree = ttk.Treeview(self.frameup, selectmode="extended", columns=self.adress_header, show="headings")
        self.vsb2 = ttk.Scrollbar(self.frameup, orient="vertical", command=ceptree.yview)

        ceptree.configure(yscrollcommand=self.vsb2.set)
        ceptree.place(relx=0.02, rely=0.63, relheight=0.19, relwidth=0.62)
        self.vsb2.place(relx=0.64, rely=0.63, relheight=0.19, relwidth=0.03)

        hd = ["nw", "nw", "nw"]
        h = [5, 50, 160]
        n = 0

        for col in self.adress_header:
            ceptree.heading(col, text=col.title(), anchor=CENTER)
            ceptree.column(col, width=h[n], anchor=hd[n])
            n += 1

        for item in listcep:
            ceptree.insert('', END, values=item)

        ceptree.bind("<ButtonRelease-1>", self.OnDoubleClick2)

    def treecttReload(self):
        global ctttree

        listctt = self.selectAllCtt()

        self.ctt_header = ['Numero', 'Tipo']

        ctttree = ttk.Treeview(self.frameup, selectmode="extended", columns=self.ctt_header, show="headings")
        self.vsb3 = ttk.Scrollbar(self.frameup, orient="vertical", command=ctttree.yview)

        ctttree.configure(yscrollcommand=self.vsb3.set)
        ctttree.place(relx=0.02, rely=0.42, relheight=0.19, relwidth=0.62)
        self.vsb3.place(relx=0.64, rely=0.42, relheight=0.19, relwidth=0.03)

        hd = ["nw", "nw", "nw", "nw", "center", "center"]
        h = [100, 50]
        n = 0

        for col in self.ctt_header:
            ctttree.heading(col, text=col.title(), anchor=CENTER)
            ctttree.column(col, width=h[n], anchor=hd[n])
            n += 1

        for item in listctt:
            ctttree.insert('', END, values=item)

        ctttree.bind("<ButtonRelease-1>", self.OnDoubleClick3)

    def OnDoubleClick(self, event):
        try:
            self.lb_name.config(state=NORMAL)
            self.clean()
            self.lb_cep.config(state=NORMAL)
            self.cleancep()
            self.lb_num.config(state=NORMAL)
            self.cleanctt()
            cod = self.treeSelect()
            values = self.selectClientbyId(int(cod[0]))
            self.setclientEntry(values[0][0], values[0][1])
            self.lb_name.config(state=DISABLED)
            self.lb_cep.config(state=DISABLED)
            self.lb_num.config(state=DISABLED)

            self.treecepReload()
            self.treecttReload()
        except:
            self.lb_name.config(state=DISABLED)
            self.lb_cep.config(state=DISABLED)
            self.lb_num.config(state=DISABLED)

    def OnDoubleClick2(self, event):
        try:
            self.lb_cep.config(state = NORMAL)
            self.cleancep()
            cepcod = self.ceptreeSelect()
            values = self.selectCepbyId(cepcod[0])
            self.setCepEntry(values[0][0], values[0][2])
            self.lb_cep.config(state=DISABLED)
        except:
            self.lb_cep.config(state=DISABLED)

    def OnDoubleClick3(self, event):
        try:
            self.lb_num.config(state=NORMAL)
            self.cleanctt()
            ctt = self.ctttreeSelect()
            self.setCttEntry(ctt[0])
            self.lb_num.config(state=DISABLED)
        except:
            self.lb_num.config(state=DISABLED)

    def OnClick(self, event):
        try:
            self.prod.config(state=NORMAL)
            prod = self.budgettreeSelect()
            self.gain = self.selectProductbyId(int(prod[0]))[0][9]
            self.cleanprod()
            self.lblgain.config(text=f'R$ {self.gain} ')
            self.setProdEntry(prod[0], f'{prod[1]} - {prod[2]}', prod[3], prod[4], prod[5], prod[6])
            self.prod.config(state = DISABLED)
            self.kg.insert(END, "0")
            self.m.insert(END, "0")
            self.m2.insert(END, "0")
            self.uni.insert(END, "0")
        except:
            self.prod.config(state=NORMAL)


class ComercialView(ComercialController):
    def __init__(self, frameup, framedown, framebar):
        self.taxChk = StringVar()
        self.subtotalvalue = 0
        self.list_cli = ttk.Treeview
        self.framedown = framedown
        self.frameup = frameup
        self.framebar = framebar
        self.setup()

    def setup(self):
        self.init_Comercial()

    def init_Comercial(self):
        self.clearAll()
        self.init_layout()
        self.init_treecomercial()
        self.init_treecomercial2()
        self.init_comercialPage()

    def init_budget(self):
        self.clearAll()
        self.init_layout()
        self.init_budgets()
        self.init_budgets2()
        self.init_treebudget()
        self.init_treebudget2()
        self.init_budgetButtons()

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

    def init_comercialPage(self):
        self.title = Label(self.frameup, text="Comercial", font="Ivy 18 bold", bg="#CEDCE4")
        self.title.place(relx=0.015, rely=0.005, relwidth=0.30, height= 28)

        self.name = Label(self.frameup, text='Cliente: ', font='Ivy 13', bg=color("background"))
        self.name.place(relx=0.02, y=38, relheight=0.08, relwidth=0.15)
        self.name_entry = Entry(self.frameup, font='Ivy 14')
        self.name_entry.place(relx=0.17, y=45, relwidth=0.6, relheight=0.05)

        self.clientid = Entry(self.frameup)

        self.cmbStatus = ttk.Combobox(self.framedown)
        self.cmbStatus = ttk.Combobox(self.framedown, font=('Ivy', 14))
        self.cmbStatus.place(relx=0.02, rely=0.092, relwidth=0.3, relheight=0.05)
        self.cmbStatus['values'] = ('Status','Novo lead', 'Em contato', 'Orçamento enviado', 'Aguardando Retorno', 'Perdido', 'Fechado', 'Pendente', 'Em produção', 'Entrega finalizada')
        self.cmbStatus.current(0)
        self.cmbStatus['state'] = 'readonly'
        self.cmbStatus.bind('<<ComboboxSelected>>', self.filtercmb)

        self.cmbPagamento = ttk.Combobox(self.framedown)
        self.cmbPagamento = ttk.Combobox(self.framedown, font=('Ivy', 14))
        self.cmbPagamento.place(relx=0.35, rely=0.092, relwidth=0.2, relheight=0.05)
        self.cmbPagamento['values'] = ('Pagamento','À vista', 'Antecipado', 'Parcelado')
        self.cmbPagamento.current(0)
        self.cmbPagamento['state'] = 'readonly'
        self.cmbPagamento.bind('<<ComboboxSelected>>', self.filtercmb)


        self.obs_entry = Text(self.framedown, font=('arial', 10))
        self.obs_entry.place(relx=0.02, rely=0.74, relwidth=0.6, relheight=0.23)

        self.init_comercialButtons()

    def init_comercialButtons(self):
        self.srchImg = PhotoImage(file=r"assets\procurar.png")
        self.bt_srch = Button(self.frameup, image=self.srchImg, relief='flat', background=color("background"),
                              command=self.searchClientComercial)
        self.bt_srch.place(relx=0.80, y=40, relwidth=0.08, relheight=0.06)

        self.clrImg = PhotoImage(file=r"assets\lixo.png")
        self.bt_clr = Button(self.frameup, image=self.clrImg, relief='flat', background=color("background"),
                             command=self.init_Comercial)
        self.bt_clr.place(relx=0.90, y=40, relwidth=0.08, relheight=0.06)

        self.budgetsIMG = PhotoImage(file=r"assets\ORC.png")
        self.btn_budgets = Button(self.frameup, image=self.budgetsIMG, relief='flat',
                                  command=lambda: self.filter('orçamento'))
        self.btn_budgets.place(relx=0.020, rely=0.88, relwidth=0.225, relheight=0.1)

        self.salesIMG = PhotoImage(file=r"assets\VEN.png")
        self.btn_sales = Button(self.frameup, image=self.salesIMG, relief='flat',
                                  command=lambda: self.filter('venda'))
        self.btn_sales.place(relx=0.39, rely=0.88, relwidth=0.225, relheight=0.1)

        self.orderIMG = PhotoImage(file=r"assets\ORD.png")
        self.btn_order = Button(self.frameup, image=self.orderIMG, relief='flat',
                                  command=lambda: self.filter('ordem'))
        self.btn_order.place(relx=0.755, rely=0.88, relwidth=0.225, relheight=0.1)

        self.rprtImg = PhotoImage(file=r'assets\report.png')
        self.bt_report = Button(self.framebar, image=self.rprtImg, relief='flat',
                                command=self.genReport)
        self.bt_report.place(relx=0.8, rely=0.08, width=70, height=60)

        self.newIMG = PhotoImage(file=r'assets\NOVO.png')
        self.bt_new = Button(self.framedown, image=self.newIMG, relief='flat',
                                command=self.init_budget)
        self.bt_new.place(relx=0.81, rely=0.8, width=140, height=100)

        self.attImg = PhotoImage(file=r"assets\add.png")
        self.bt_att = Button(self.framedown, image=self.attImg, relief='flat',
                                command=self.attHist)
        self.bt_att.place(relx=0.63, rely=0.875, width=70, height=60)

    def init_budgets(self):
        self.title = Label(self.frameup, text="Comercial", font="Ivy 18 bold", bg="#CEDCE4")
        self.title.place(relx=0.015, rely=0.005, relwidth=0.30, height= 28)

        self.rtrnImg = PhotoImage(file=r'assets\retornar.png')
        self.bt_return = Button(self.framebar, image=self.rtrnImg, relief='flat',
                                command=self.init_Comercial)
        self.bt_return.place(relx=0.8, rely=0.08, width=70, height=60)

        self.name = Label(self.frameup, text='Cliente: ', font='Ivy 13', bg=color("background"))
        self.name.place(relx=0.02, y=38, relheight=0.08, relwidth=0.15)
        self.name_entry = Entry(self.frameup, font='Ivy 14')
        self.name_entry.place(relx=0.17, y=45, relwidth=0.6, relheight=0.05)

        self.srchImg = PhotoImage(file=r"assets\procurar.png")
        self.bt_srch = Button(self.frameup, image=self.srchImg, relief='flat', background=color("background"),
                              command=self.searchClientBudget)
        self.bt_srch.place(relx=0.80, y=40, relwidth=0.08, relheight=0.06)

        self.clrImg = PhotoImage(file=r"assets\lixo.png")
        self.bt_clr = Button(self.frameup, image=self.clrImg, relief='flat', background=color("background"),
                             command=self.init_budget)
        self.bt_clr.place(relx=0.90, y=40, relwidth=0.08, relheight=0.06)

        self.lb_idref = Label(self.frameup, text="ID: ", font='Ivy 16', background=color("background"))
        self.lb_idref.place(relx=0.70, rely=0.42, relheight=0.06, relwidth=0.1)
        self.lb_id = Label(self.frameup, text="0", font='Ivy 16', background=color("background"),
                           anchor="w", justify=LEFT)
        self.lb_id.place(relx=0.78, rely=0.42, relheight=0.06, relwidth=0.15)


        self.lb_name = Entry(self.frameup, background=color("background"))
        self.lb_name.place(relx=0.73, rely=0.50, relheight=0.06, relwidth=0.25)

        self.lb_cep = Entry(self.frameup, background=color("background"))
        self.lb_cep.place(relx=0.73, rely=0.70, relheight=0.06, relwidth=0.25)

        self.lb_cepid = Label(self.frameup, text="0", font='Ivy 16', background=color("background"),
                           anchor="w", justify=LEFT)


        self.lb_num = Entry(self.frameup, background=color("background"))
        self.lb_num.place(relx=0.73, rely=0.60, relheight=0.06, relwidth=0.25)
        self.lb_name.config(state=DISABLED)
        self.lb_cep.config(state=DISABLED)
        self.lb_num.config(state=DISABLED)

    def init_budgets2(self):

        self.lblv = Label(self.framedown, font=('arial', 13, 'bold'), text="Visita:", bg=color("background"),
                          anchor='w', justify=RIGHT)
        self.lblv.place(relx=0.018, rely=0.72, relwidth=0.7, relheight=0.08)
        self.lblvisita = Label(self.framedown, font=('arial', 13, 'bold'), text="Não será cobrada visita",
                               bg=color("background"), anchor='w', justify=LEFT)
        self.lblvisita.place(relx=0.0835, rely=0.72, relwidth=0.4, relheight=0.08)

        self.lblf = Label(self.framedown, font=('arial', 13, 'bold'), text="Deslocamento:", bg=color("background"),
                          anchor='e', justify=RIGHT)
        self.lblf.place(relx=0.02, rely=0.665, relwidth=0.15, relheight=0.08)
        self.lblfrete = Entry(self.framedown, font=('arial', 13, 'bold'), justify=RIGHT)
        self.lblfrete.place(relx=0.18, rely=0.68, relwidth=0.14, relheight=0.05)

        self.lblfrete.bind('<Return>', self.discountValue)
        self.lblfrete.bind('<FocusOut>', self.discountValue)

        self.lblSubTotal = Label(self.framedown, font=('arial', 14, 'bold'), text="Subtotal", bg=color("background"),
                                 anchor='e', justify=RIGHT)
        self.lblSubTotal.place(relx=0.655, rely=0.68, relwidth=0.13, relheight=0.08)
        self.subTotal = Entry(self.framedown, font=('arial', 14, 'bold'), bg=color("background"))
        self.subTotal.place(relx=0.80, rely=0.69, relwidth=0.17, relheight=0.06)
        self.subTotal.config(state=DISABLED)

        self.lbldiscount = Label(self.framedown, font=('arial', 14, 'bold'),
                                 text="Desconto                              %", bg=color("background"),
                                 anchor='e', justify=RIGHT)
        self.lbldiscount.place(relx=0.65, rely=0.78, relwidth=0.34, relheight=0.08)
        self.discount = Entry(self.framedown, font=('arial', 14, 'bold'), bg=color("background"), justify=RIGHT)
        self.discount.place(relx=0.80, rely=0.79, relwidth=0.13, relheight=0.06)
        self.discount.insert(END, "0")

        self.discount.bind('<Return>', self.discountValue)
        self.discount.bind('<FocusOut>', self.discountValue)

        self.lbltotal = Label(self.framedown, font=('arial', 14, 'bold'), text="Total", bg=color("background"),
                                 anchor='e', justify=RIGHT)
        self.lbltotal.place(relx=0.63, rely=0.88, relwidth=0.16, relheight=0.08)
        self.total = Entry(self.framedown, font=('arial', 14, 'bold'), bg=color("background"))
        self.total.place(relx=0.80, rely=0.89, relwidth=0.17, relheight=0.06)
        self.total.config(state=DISABLED)

        self.cmbPag = ttk.Combobox(self.framedown, font=('Ivy', 14, 'bold'))
        self.cmbPag.place(relx=0.35, rely=0.77, relwidth=0.24, relheight=0.06)
        self.cmbPag['values'] = ('À vista', 'Antecipado', 'Parcelado')
        self.cmbPag.current(0)
        self.cmbPag['state'] = 'readonly'
        self.cmbPag.bind('<<ComboboxSelected>>', self.callback)

        self.lb_taxChk = Checkbutton(self.framedown, text="", font="Ivy 10", bg=color("background"), variable=self.taxChk, command=self.sumTotal)
        self.lb_taxChk.place(relx=0.63, rely=0.90, relwidth=0.03)
        self.taxChk.set(0)

        self.cmbPar = ttk.Combobox(self.framedown, font=('Ivy', 14))
        self.cmbPar.place(relx=0.67, rely=0.89, relwidth=0.05, relheight=0.06)
        self.cmbPar['values'] = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12')
        self.cmbPar.current(0)
        self.cmbPar['state'] = 'disabled'
        self.cmbPar.bind('<<ComboboxSelected>>', self.divTotal)

        self.cmbStts = ttk.Combobox(self.framedown, font=('Ivy', 12, 'bold'))
        self.cmbStts.place(relx=0.35, rely=0.69, relwidth=0.24, relheight=0.06)
        self.cmbStts['values'] = ('Novo lead', 'Em contato', 'Orçamento enviado', 'Aguardando Retorno', 'Perdido', 'Fechado', 'Pendente', 'Em produção', 'Entrega finalizada')
        self.cmbStts.current(0)
        self.cmbStts['state'] = 'readonly'

        self.lblobs = Label(self.framedown, font=('arial', 13), text="Anotações:", bg=color("background"),
                          anchor='e', justify=RIGHT)
        self.lblobs.place(relx=0.060, rely=0.80, relwidth=0.25, relheight=0.08)
        self.obs_entry = Text(self.framedown, font=('arial', 10))
        self.obs_entry.place(relx=0.208, rely=0.86, relwidth=0.38, relheight=0.10)

        self.lblkg = Label(self.framedown, font=('arial', 13, 'bold'), text="kg", bg=color("background"),
                                 anchor='e', justify=RIGHT)
        self.lblkg.place(relx=0.53, rely=0.18, relwidth=0.06, relheight=0.08)
        self.kg = Entry(self.framedown, font=('arial', 13), bg=color("background"), justify=CENTER)
        self.kg.place(relx=0.60, rely=0.19, relwidth=0.07, relheight=0.06)

        self.lblm = Label(self.framedown, font=('arial', 13, 'bold'), text="m", bg=color("background"),
                                 anchor='e', justify=RIGHT)
        self.lblm.place(relx=0.53, rely=0.28, relwidth=0.06, relheight=0.08)
        self.m = Entry(self.framedown, font=('arial', 13), bg=color("background"), justify=CENTER)
        self.m.place(relx=0.60, rely=0.29, relwidth=0.07, relheight=0.06)

        self.lblm2 = Label(self.framedown, font=('arial', 13, 'bold'), text="m²", bg=color("background"),
                                 anchor='e', justify=RIGHT)
        self.lblm2.place(relx=0.67, rely=0.18, relwidth=0.06, relheight=0.08)
        self.m2 = Entry(self.framedown, font=('arial', 13), bg=color("background"), justify=CENTER)
        self.m2.place(relx=0.74, rely=0.19, relwidth=0.07, relheight=0.06)

        self.lbluni = Label(self.framedown, font=('arial', 13, 'bold'), text="unit", bg=color("background"),
                                 anchor='e', justify=RIGHT)
        self.lbluni.place(relx=0.67, rely=0.28, relwidth=0.06, relheight=0.08)
        self.uni = Entry(self.framedown, font=('arial', 13), bg=color("background"), justify=CENTER)
        self.uni.place(relx=0.74, rely=0.29, relwidth=0.07, relheight=0.06)

        self.lblgain = Label(self.framedown, font=('arial', 16, 'bold'), text="", bg=color("background"),
                                 anchor='e', justify=RIGHT)
        self.lblgain.place(relx=0.88, rely=0.20)

        self.prodcod = Label(self.framedown, font=('arial', 1), bg=color("background"), fg=color("background"))
        self.prodcod.place(relx=0.55, rely=0.11, relwidth=0.26, relheight=0.05)
        self.prod = Entry(self.framedown, font=('arial', 11), justify=LEFT)
        self.prod.place(relx=0.55, rely=0.11, relwidth=0.33, relheight=0.05)

        self.mat = Label(self.framedown)
        self.valuekg = Label(self.framedown)
        self.valuem = Label(self.framedown)
        self.valuem2 = Label(self.framedown)
        self.valueuni = Label(self.framedown)

        self.rmvImg = PhotoImage(file=r'assets\rmv.png')
        self.addImg = PhotoImage(file=r'assets\add.png')

        self.bt_clearprod = Button(self.framedown, image=self.srchImg, bg=color("background"), relief='flat',
                                   command=self.searchProdBudgets)
        self.bt_clearprod.place(relx=0.88, rely=0.10, relwidth=0.05, relheight=0.07)

        self.bt_clearprod = Button(self.framedown, image=self.clrImg, bg=color("background"), relief='flat',
                                command=self.cleanprod)
        self.bt_clearprod.place(relx=0.93, rely=0.10, relwidth=0.05, relheight=0.07)

        self.bt_prodadd = Button(self.framedown, image=self.addImg, relief='flat',
                                    command=self.addProd)
        self.bt_prodadd.place(relx=0.83, rely=0.282, relwidth=0.07, relheight=0.08)

        self.bt_prodrmv = Button(self.framedown, image=self.rmvImg, relief='flat',
                                    command=self.rmvProd)
        self.bt_prodrmv.place(relx=0.91, rely=0.282, relwidth=0.07, relheight=0.08)

        self.budid = Label(self.framedown, text="Cod: ", font="Ivy 20", background="#CEDCE4")
        self.budid.place(relx=0.02, rely=0.013)
        self.lb_idbud = Label(self.framedown, text="0", font="Ivy 20", background="#CEDCE4", justify=LEFT)
        self.lb_idbud.place(relx=0.1, rely=0.013)

        self.respons = Entry(self.framedown, font=('arial', 14, 'bold'), bg=color("background"), justify=RIGHT)
        self.respons.place(relx=0.30, rely=0.013, relwidth=0.35, relheight=0.06)
        self.respons.insert(END, "")

        self.lb_typebud = Label(self.framedown, text="", font="Ivy 18", background="#CEDCE4", anchor='e', justify=RIGHT)
        self.lb_typebud.place(relx=0.73, rely=0.013, relwidth=0.25)

    def init_budgetButtons(self):
        self.svbudImg = PhotoImage(file=r"assets\genorc.png")
        self.bt_savebudget = Button(self.frameup, image=self.svbudImg, relief='flat',
                                command=self.saveorc)
        self.bt_savebudget.place(relx=0.75, rely=0.88, relwidth=0.23, relheight=0.1)

        self.gnrtSale = PhotoImage(file=r"assets\genven.png")
        self.bt_genSale = Button(self.frameup, image=self.gnrtSale, relief='flat',
                                command=self.genSale)
        self.bt_genSale.place(relx=0.38, rely=0.88, relwidth=0.23, relheight=0.1)

        self.gnrtServ = PhotoImage(file=r"assets\genods.png")
        self.bt_genService = Button(self.frameup, image=self.gnrtServ, relief='flat',
                                command=self.genOrder)
        self.bt_genService.place(relx=0.020, rely=0.88, relwidth=0.23, relheight=0.1)

        self.prntCsv = PhotoImage(file=r"assets\gencsv.png")
        self.printCsv = Button(self.framedown, image=self.prntCsv, relief='flat',
                                command=self.gencsv)
        self.printCsv.place(relx=0.022, rely=0.8, height=100, width=130)

    def init_treecomercial(self):
        global treecomercial
        list = self.selectAllClients()

        self.list_header = ['ID', 'Nome', 'Email', 'Documento']
        treecomercial = ttk.Treeview(self.frameup, selectmode="extended", columns=self.list_header, show="headings")
        self.vsb2 = ttk.Scrollbar(self.frameup, orient="vertical", command=treecomercial.yview)

        treecomercial.configure(yscrollcommand=self.vsb2.set)
        treecomercial.place(relx=0.02, rely=0.16, relwidth=0.92, relheight=0.65)
        self.vsb2.place(relx=0.94, rely=0.16, relwidth=0.04, relheight=0.65)

        hd = ["nw", "nw", "nw", "nw"]
        h = [10, 120, 120, 90]
        n = 0

        for col in self.list_header:
            treecomercial.heading(col, text=col.title(), anchor=CENTER)
            treecomercial.column(col, width=h[n], anchor=hd[n])
            n += 1

        for item in list:
            treecomercial.insert('', END, values=item)

        treecomercial.bind('<ButtonRelease-1>', self.defclient)

    def init_treecomercial2(self):
        global comercialtree

        list = self.selectAllOrders()

        self.list_header = ['ID', 'Cliente', 'Status', 'Pagamento', 'Parcelas', 'desconto', 'total', 'data']
        comercialtree = ttk.Treeview(self.framedown, selectmode="extended", columns=self.list_header, show="headings")
        self.vsb = ttk.Scrollbar(self.framedown, orient="vertical", command=comercialtree.yview)

        comercialtree.tag_configure('orc', background="yellow")
        comercialtree.tag_configure('sal', background="light green")
        comercialtree.tag_configure('ord', background="light blue")

        comercialtree.configure(yscrollcommand=self.vsb.set)
        comercialtree.place(relx=0.02, rely=0.16, relwidth=0.94, relheight=0.55)
        self.vsb.place(relx=0.96, rely=0.16, relwidth=0.02, relheight=0.55)

        hd = ["nw", "nw", "nw", "nw", "nw", "nw", "nw", "nw", "nw"]
        h = [10, 150, 80, 70, 70, 60, 60, 60, 60]
        n = 0

        for col in self.list_header:
            comercialtree.heading(col, text=col.title(), anchor=CENTER)
            comercialtree.column(col, width=h[n], anchor=hd[n])
            n += 1

        for row in list:
            subtotal = float(row[5][3:])
            disc = row[6]/100 * subtotal
            if row[9] == 'orçamento':
                self.tag = 'orc'
            elif row[9] == 'venda':
                self.tag = 'sal'
            elif row[9] == 'ordem':
                self.tag = 'ord'
            comercialtree.insert('', END, text='1', tags=self.tag ,values=(row[0], row[1], row[2], row[3], f'{row[4]} x {row[7]}',
                                                            f'R$ {disc:.2f}', row[5], row[8]))

        comercialtree.bind('<ButtonRelease-1>', self.showHist)
        comercialtree.bind('<Double-Button-1>', self.OnClickComercial)

    def init_treebudget(self):
        global tree
        list = self.selectAllClients()

        self.list_header = ['ID', 'Nome', 'Email', 'Documento']
        tree = ttk.Treeview(self.frameup, selectmode="extended", columns=self.list_header, show="headings")
        self.vsb = ttk.Scrollbar(self.frameup, orient="vertical", command=tree.yview)

        tree.configure(yscrollcommand=self.vsb.set)
        tree.place(relx=0.02, rely=0.15, relwidth=0.92, relheight=0.25)
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

        tree.bind("<ButtonRelease-1>", self.OnDoubleClick)

        global ctttree

        self.ctt_header = ['Numero', 'Tipo']

        ctttree = ttk.Treeview(self.frameup, selectmode="extended", columns=self.ctt_header, show="headings")
        self.vsb3 = ttk.Scrollbar(self.frameup, orient="vertical", command=ctttree.yview)

        ctttree.configure(yscrollcommand=self.vsb3.set)
        ctttree.place(relx=0.02, rely=0.42, relheight=0.19, relwidth=0.62)
        self.vsb3.place(relx=0.64, rely=0.42, relheight=0.19, relwidth=0.03)

        hd = ["nw", "nw", "nw", "nw", "center", "center"]
        h = [100, 50]
        n = 0

        for col in self.ctt_header:
            ctttree.heading(col, text=col.title(), anchor=CENTER)
            ctttree.column(col, width=h[n], anchor=hd[n])
            n += 1

        global ceptree

        self.adress_header = ['id', 'CEP', 'endereço']

        ceptree = ttk.Treeview(self.frameup, selectmode="extended", columns=self.adress_header, show="headings")
        self.vsb2 = ttk.Scrollbar(self.frameup, orient="vertical", command=ceptree.yview)

        ceptree.configure(yscrollcommand=self.vsb2.set)
        ceptree.place(relx=0.02, rely=0.63, relheight=0.19, relwidth=0.62)
        self.vsb2.place(relx=0.64, rely=0.63, relheight=0.19, relwidth=0.03)

        hd = ["nw", "nw", "nw"]
        h = [5, 50, 160]
        n = 0

        for col in self.adress_header:
            ceptree.heading(col, text=col.title(), anchor=CENTER)
            ceptree.column(col, width=h[n], anchor=hd[n])
            n += 1

    def init_treebudget2(self):
        global productTree
        list = self.selectAllProducts()

        self.list_header = ['ID', 'Nome', 'Material', 'kg', 'm', 'm²', 'uni']
        productTree = ttk.Treeview(self.framedown, selectmode="extended", columns=self.list_header, show="headings")
        self.vsb = ttk.Scrollbar(self.framedown, orient="vertical", command=productTree.yview)

        productTree.configure(yscrollcommand=self.vsb.set)
        self.vsb.place(relx=0.52, rely=0.11, relwidth=0.02, relheight=0.26)
        productTree.place(relx=0.02, rely=0.11, relwidth=0.50, relheight=0.26)

        hd = ["nw", "nw", "nw", "nw", "nw", "nw", "nw"]
        h = [10, 120, 80, 30, 30, 30, 30]
        n = 0

        for col in self.list_header:
            productTree.heading(col, text=col.title(), anchor=CENTER)
            productTree.column(col, width=h[n], anchor=hd[n])
            n += 1

        for item in list:
            productTree.insert('', END, values=item)

        productTree.bind("<ButtonRelease-1>", self.OnClick)

        global budgetTree

        self.list_header = ['ID', 'Serviço', 'kg', 'm', 'm²', 'uni', 'Total']
        budgetTree = ttk.Treeview(self.framedown, selectmode="extended", columns=self.list_header, show="headings")
        self.vsb = ttk.Scrollbar(self.framedown, orient="vertical", command=budgetTree.yview)

        budgetTree.configure(yscrollcommand=self.vsb.set)
        self.vsb.place(relx=0.96, rely=0.39, relwidth=0.02, relheight=0.27)
        budgetTree.place(relx=0.02, rely=0.39, relwidth=0.94, relheight=0.27)

        hd = ["nw", "nw", "center", "center", "center", "center", "ne"]
        h = [1, 180, 30, 30, 30, 30, 60]
        n = 0

        for col in self.list_header:
            budgetTree.heading(col, text=col.title(), anchor=CENTER)
            budgetTree.column(col, width=h[n], anchor=hd[n])
            n += 1

    def clear_frameleft(self):
        for widget in self.frameup.winfo_children():
            widget.destroy()

    def clear_frameright(self):
        for widget in self.framedown.winfo_children():
            widget.destroy()

    def clearAll(self):
        self.clear_frameleft()
        self.clear_frameright()

    def searchProdBudgets(self):
        self.connect_db()
        self.prod.insert(END, '%')
        nome = self.prod.get()
        self.cursor.execute(""" SELECT * FROM tb_produtos
            WHERE servico LIKE ? OR material LIKE ? ORDER BY servico ASC """, (nome, nome,))
        self.info = self.cursor.fetchall()
        self.disconnect_db()
        self.prod.delete(0, END)

        self.list_header = ['ID', 'Nome', 'Material', 'kg', 'm', 'm²', 'uni']
        productTree = ttk.Treeview(self.framedown, selectmode="extended", columns=self.list_header, show="headings")
        self.vsb = ttk.Scrollbar(self.framedown, orient="vertical", command=productTree.yview)

        productTree.configure(yscrollcommand=self.vsb.set)
        self.vsb.place(relx=0.52, rely=0.11, relwidth=0.02, relheight=0.26)
        productTree.place(relx=0.02, rely=0.11, relwidth=0.50, relheight=0.26)

        hd = ["nw", "nw", "nw", "nw", "nw", "nw", "nw"]
        h = [10, 120, 80, 30, 30, 30, 30]
        n = 0

        for col in self.list_header:
            productTree.heading(col, text=col.title(), anchor=CENTER)
            productTree.column(col, width=h[n], anchor=hd[n])
            n += 1

        for item in self.info:
            productTree.insert('', END, values=item)

        productTree.bind("<ButtonRelease-1>", self.OnClick)

    def searchClientComercial(self):
        if self.name_entry.get() == '':
            list = self.selectAllClients()
        else:
            list = self.searchClientByName()

        self.name_entry.delete(0, END)
        global tree

        self.list_header = ['ID', 'Nome', 'Email', 'Documento']
        tree = ttk.Treeview(self.frameup, selectmode="extended", columns=self.list_header, show="headings")
        self.vsb = ttk.Scrollbar(self.frameup, orient="vertical", command=tree.yview)

        tree.configure(yscrollcommand=self.vsb.set)
        tree.place(relx=0.02, rely=0.16, relwidth=0.92, relheight=0.650)
        self.vsb.place(relx=0.94, rely=0.16, relwidth=0.04, relheight=0.650)

        hd = ["nw", "nw", "nw", "nw"]
        h = [10, 120, 120, 90]
        n = 0

        for col in self.list_header:
            tree.heading(col, text=col.title(), anchor=CENTER)
            tree.column(col, width=h[n], anchor=hd[n])
            n += 1

        for item in list:
            tree.insert('', END, values=item)

        tree.bind("<ButtonRelease-1>", self.OnDoubleClick)

    def searchClientBudget(self):
        if self.name_entry.get() == '':
            list = self.selectAllClients()
        else:
            list = self.searchClientByName()

        self.name_entry.delete(0, END)
        self.clean()
        global tree

        self.list_header = ['ID', 'Nome', 'Email', 'Documento']
        tree = ttk.Treeview(self.frameup, selectmode="extended", columns=self.list_header, show="headings")
        self.vsb = ttk.Scrollbar(self.frameup, orient="vertical", command=tree.yview)

        tree.configure(yscrollcommand=self.vsb.set)
        tree.place(relx=0.02, rely=0.15, relwidth=0.92, relheight=0.25)
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

        tree.bind("<ButtonRelease-1>", self.OnDoubleClick)

    def addProd(self):
        if float(self.kg.get().replace(",", ".")) < 0 or float(self.m.get().replace(",", "."))< 0 or float(self.m2.get().replace(",", ".")) < 0 or float(self.uni.get().replace(",", ".")) < 0:
            messagebox.showerror('Erro', 'Permitido apenas valores positivos.')
        else:
            if self.kg.get() != '' or self.m.get() != '' or self.m2.get() != '' or self.uni.get() != '':
                self.getProdEntry()
                if self.kg.get() == "":
                    self.kg.insert(END, "0")
                else:
                    self.kgt = self.kg.get().replace(",", ".")
                    self.totalkg = float(self.vkg) * float(self.kgt)

                if self.m.get() == "":
                    self.m.insert(END, "0")
                else:
                    self.mt = self.m.get().replace(",", ".")
                    self.totalm = float(self.vm) * float(self.mt)

                if self.m2.get() == "":
                    self.m2.insert(END, "0")
                else:
                    self.m2t = self.m2.get().replace(",", ".")
                    self.totalm2 = float(self.vm2) * float(self.m2t)

                if self.uni.get() == "":
                    self.uni.insert(END, "0")
                else:
                    self.unit = self.uni.get().replace(",", ".")
                    self.totaluni = float(self.vuni) * float(self.unit)

                self.totalitem = self.totalkg + self.totalm + self.totalm2 + self.totaluni

                budgetTree.insert("", END, values=(self.prodcod.cget("text"), self.prod.get(), f"{self.totalkg:.2f}", f'{self.totalm:.2f}', f'{self.totalm2:.2f}',
                                                   f'{self.totaluni:.2f}', f'{self.totalitem:.2f}'))
                self.cleanprod()
                self.prod.config(state=NORMAL)
                self.sumTotal()

            else:
                messagebox.showerror('Erro', 'Favor insira valores numéricos.')

    def rmvProd(self):
        selected_item = budgetTree.selection()[0]
        budgetTree.delete(selected_item)
        self.sumTotal()

    def discountValue(self, event):
        try:
            float(self.discount.get())
        except:
            messagebox.showerror('Erro', 'Favor inserir desconto válido.')
            self.discount.delete(0, END)
            self.discount.insert(END, "0")
            self.discountValue(None)
        else:
            if float(self.discount.get()) > 100 or float(self.discount.get()) < 0:
                messagebox.showerror('Erro', 'Favor inserir desconto válido.')
                self.discount.delete(0, END)
                self.discount.insert(END, "0")
            else:
                self.sumTotal()

    def defclient(self, event):
        treev_data = treecomercial.focus()
        treev_dicionario = treecomercial.item(treev_data)
        treev_list = treev_dicionario['values']
        cod = treev_list[0]

        for widget in self.framedown.winfo_children():
            widget_class = widget.__class__.__name__
            if widget_class == 'Treeview' or widget_class == 'Scrollbar':
                widget.destroy()

        self.connect_db()
        self.cursor.execute(
            """ SELECT cod, cliente, status, pagamento, parcelas, total, discount, subtotal, data, tipo FROM tb_comercial
            WHERE cliente_cod = ? ORDER BY data desc """, (cod,))
        row = self.cursor.fetchall()
        self.disconnect_db()

        global comercialtree

        list = row

        self.list_header = ['ID', 'Cliente', 'Status', 'Pagamento', 'Parcelas', 'desconto', 'total', 'data']
        comercialtree = ttk.Treeview(self.framedown, selectmode="extended", columns=self.list_header,
                                     show="headings")
        self.vsb = ttk.Scrollbar(self.framedown, orient="vertical", command=comercialtree.yview)

        comercialtree.tag_configure('orc', background="yellow")
        comercialtree.tag_configure('sal', background="light green")
        comercialtree.tag_configure('ord', background="light blue")

        comercialtree.configure(yscrollcommand=self.vsb.set)
        comercialtree.place(relx=0.02, rely=0.16, relwidth=0.94, relheight=0.55)
        self.vsb.place(relx=0.96, rely=0.16, relwidth=0.02, relheight=0.55)

        hd = ["nw", "nw", "nw", "nw", "nw", "nw", "nw", "nw", "nw"]
        h = [10, 150, 80, 70, 70, 60, 60, 60, 60]
        n = 0

        comercialtree.bind('<ButtonRelease-1>', self.showHist)
        comercialtree.bind('<Double-Button-1>', self.OnClickComercial)

        for col in self.list_header:
            comercialtree.heading(col, text=col.title(), anchor=CENTER)
            comercialtree.column(col, width=h[n], anchor=hd[n])
            n += 1

        for row in list:
            subtotal = float(row[5][3:])
            disc = row[6] / 100 * subtotal
            if row[9] == 'orçamento':
                self.tag = 'orc'
            elif row[9] == 'venda':
                self.tag = 'sal'
            elif row[9] == 'ordem':
                self.tag = 'ord'
            comercialtree.insert('', END, text='1', tags=self.tag,
                                 values=(row[0], row[1], row[2], row[3], f'{row[4]} x {row[5]}',
                                         f'R$ {disc:.2f}', row[7], row[8]))

    def sumTotal(self):
        self.subtotalvalue = 0
        if self.lblfrete.get() == "":
            self.frete = 0
        else:
            self.frete = float(self.lblfrete.get())

        cod = self.cmbPar.get()
        self.connect_db()
        self.cursor.execute(
            """ SELECT taxa FROM tb_tax
            WHERE cod = ? """, (cod,))
        row = self.cursor.fetchone()
        self.disconnect_db()
        print(row[0]/100)

        for child in budgetTree.get_children():
            self.value = float(budgetTree.item(child, "values")[6])
            self.subtotalvalue += self.value
        self.div = int(self.cmbPar.get())
        if self.taxChk.get() == "1":
            self.totalvalue = (( (self.subtotalvalue + self.frete) * (1 - (float(self.discount.get()) / 100) ) / self.div)) * (1 +(float(row[0])/100))
        else:
            self.totalvalue = ((self.subtotalvalue + self.frete) * (1 - (float(self.discount.get()) / 100)))/self.div


        self.subTotal.config(state=NORMAL)
        self.subTotal.delete(0, END)
        self.subTotal.insert(END, str(f'R$ {self.subtotalvalue:.2f}'))
        self.subTotal.config(state=DISABLED)

        self.total.config(state=NORMAL)
        self.total.delete(0, END)
        self.total.insert(END, str(f'R$ {self.totalvalue:.2f}'))
        self.total.config(state=DISABLED)

    def OnClickComercial(self, event):
        comercialtreev_data = comercialtree.focus()
        comercialtreev_dicionario = comercialtree.item(comercialtreev_data)
        comercialtreev_list = comercialtreev_dicionario['values'][0]
        self.connect_db()
        self.cursor.execute(""" SELECT * FROM tb_comercial WHERE cod = ? """, (comercialtreev_list,))
        row = self.cursor.fetchone()
        self.disconnect_db()
        self.init_budget()

        self.id = row[0]#
        self.nome = row[1]#
        self.clienteid = row[2]#
        self.endereco = row[3]#
        self.contato = row[4]#
        self.pagamento = row[5]#
        self.parcela = row[6]#
        self.totaldiv = row[10]#
        self.desconto = row[8]#
        self.sub = row[7]#
        self.anotac = row[11]#
        if row[14] == 'venda':
            self.type = "Venda"
        elif row[14] == 'ordem':
            self.type = 'Ordem de serviço'
        elif row[14] == 'orçamento':
            self.type = 'Orçamento'
        self.status = row[13]#
        self.orcamento = row[15]#

        self.connect_db()
        self.cursor.execute(""" SELECT endereco FROM tb_enderecos WHERE cod = ? """, (self.endereco,))
        rowcep = self.cursor.fetchone()
        self.disconnect_db()

        self.lb_idbud.config(text=self.id)
        self.lb_typebud.config(text=self.type)
        try:
            self.lb_name.config(state=NORMAL)
            self.lb_cep.config(state=NORMAL)
            self.lb_num.config(state=NORMAL)

            self.lb_id.config(text=self.clienteid)
            self.lb_name.insert(END, self.nome)
            self.lb_cepid.config(text=self.endereco)
            self.lb_cep.insert(END, rowcep[0])
            self.lb_num.insert(END, self.contato)

            self.lb_name.config(state=DISABLED)
            self.lb_cep.config(state=DISABLED)
            self.lb_num.config(state=DISABLED)
        except:
            self.lb_name.config(state=DISABLED)
            self.lb_cep.config(state=DISABLED)
            self.lb_num.config(state=DISABLED)

        self.subTotal.config(state=NORMAL)
        self.subTotal.delete(0, END)
        self.subTotal.insert(END, f'{self.sub}')
        self.subTotal.config(state=DISABLED)

        self.total.config(state=NORMAL)
        self.total.delete(0, END)
        self.total.insert(END, f'{self.totaldiv}')
        self.total.config(state=DISABLED)

        self.discount.insert(END, self.desconto)

        self.obs_entry.insert("1.0", self.anotac)

        if self.pagamento == 'À vista':
            self.cmbPag.current(0)
        elif self.pagamento == 'Antecipado':
            self.cmbPag.current(1)
        elif self.pagamento == 'Parcelado':
            self.cmbPag.current(2)
            self.cmbPar['state'] = NORMAL
            self.cmbPar.set(self.parcela)

        self.cmbStts.set(self.status)

        csv_path = os.path.join(
            glv.get_variable("APP_PATH"),
            "orçamentos",
            "Reg",
            f"{self.orcamento}.csv"
        )

        with open(csv_path) as myfile:
            csvread = csv.reader(myfile, delimiter=',')

            for row in csvread:
                budgetTree.insert("", 'end', values=row)

        self.treecttReload()
        self.treecepReload()

    def getAllData(self):
        self.datecad = date.today().strftime("%Y-%m-%d")

        self.zip = random.randint(10000000000, 99999999999)
        self.link = f"{self.cod}_{self.name}_{self.datecad}_{self.zip}"

        csv_path = os.path.join(
            glv.get_variable("APP_PATH"),
            "orçamentos",
            "Reg",
            f"{self.link}.csv"
        )

        data = []
        for row_id in budgetTree.get_children():
            row = budgetTree.item(row_id)['values']
            data.append(row)
        file = open(csv_path, 'w+', newline='')

        with file:
            write = csv.writer(file)
            write.writerows(data)
        self.id = self.lb_idbud.cget("text")
        self.subtotal = self.subTotal.get()
        self.disc = self.discount.get()
        self.tot = self.total.get()
        self.obs = (self.obs_entry.get("1.0", "end-1c")).strip()
        self.status = self.cmbStts.get()
        self.pag = self.cmbPag.get()
        self.par = self.cmbPar.get()
        self.paid = '0'

    def saveorc(self):
        self.sumTotal()
        if self.lb_name.get() == "":
            messagebox.showerror("Erro", "Escolha ao menos um cliente para vincular à esta venda.")
            return
        else:
            self.getclientEntry()

        if self.lb_num.get() != "":
            self.getCttEntry()
        else:
            self.num =""

        self.getCepEntry()
        if self.cepcod == "0":
            messagebox.showerror("Erro", "Escolha ao menos um endereço para vincular à esta venda.")
            return
        self.type = "Orçamento"
        self.lb_typebud.config(text=self.type)

        self.datecad = date.today().strftime("%Y-%m-%d")

        self.zip = random.randint(10000000000, 99999999999)
        self.link = f"{self.cod}_{self.name}_{self.datecad}_{self.zip}"

        csv_path = os.path.join(
            glv.get_variable("APP_PATH"),
            "orçamentos",
            "Reg",
            f"{self.link}.csv"
        )

        data = []
        for row_id in budgetTree.get_children():
            row = budgetTree.item(row_id)['values']
            data.append(row)
        file = open(csv_path, 'w+', newline='')

        with file:
            write = csv.writer(file)
            write.writerows(data)

        self.subtotal = self.subTotal.get()
        self.disc = self.discount.get()
        self.tot = self.total.get()
        self.obs = (self.obs_entry.get("1.0", "end-1c")).strip()
        self.status = self.cmbStts.get()
        self.hist = ""
        self.tipo = "orçamento"
        self.paid = '0'
        self.pag = self.cmbPag.get()
        self.par = self.cmbPar.get()

        if self.cod == "0":
            messagebox.showerror('Erro', 'Escolha um usuário para registrar.')
        else:
            if self.lb_idbud.cget("text") == "0":
                self.connect_db()
                self.cursor.execute(""" INSERT INTO tb_comercial (cliente, cliente_cod, cep_cod, linha, pagamento,
                 parcelas, subtotal, discount, data, total, obs, hist, status, tipo, link, pagas) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) """,
                            (self.name, self.cod, self.cepcod, self.num, self.pag, self.par, self.tot, self.disc,
                             self.datecad, self.subtotal, self.obs, self.hist, self.status, self.tipo, self.link, self.paid))
                self.conn.commit()
                messagebox.showinfo('ORÇAMENTO', 'Dados inseridos com sucesso.')
                id = self.link
                self.cursor.execute(""" SELECT cod FROM tb_comercial 
                        WHERE link = ?""", (id,))
                row = self.cursor.fetchone()
                self.disconnect_db()
                self.lb_idbud.config(text=row[0])
            else:
                self.id = self.lb_idbud.cget("text")
                self.connect_db()
                self.cursor.execute(""" UPDATE tb_comercial SET
                    cliente = ?, 
                    cliente_cod = ?, 
                    cep_cod = ?, 
                    linha = ?,
                    pagamento = ?,
                    parcelas = ?, 
                    subtotal = ?, 
                    discount = ?,
                    data = ?, 
                    total = ?, 
                    obs = ?, 
                    status = ?, 
                    tipo = ?, 
                    link = ?,
                    pagas = ?
                    WHERE cod = ?""",
                        (self.name,
                         self.cod,
                         self.cepcod,
                         self.num,
                         self.pag,
                         self.par,
                         self.subtotal,
                         self.disc,
                         self.datecad,
                         self.tot,
                         self.obs,
                         self.status,
                         self.tipo,
                         self.link,
                         self.paid,
                         self.id))
                self.conn.commit()
                messagebox.showinfo('Sucesso', 'Dados atualizados com sucesso.')
                self.disconnect_db()

    def gencsv(self):
        if self.lb_name.get() == "":
            messagebox.showerror("Erro", "Escolha ao menos um cliente para vincular à esta venda.")
            return
        elif self.lb_cep.get() == "":
            messagebox.showerror("Erro", "Escolha ao menos um endereço para vincular à esta venda.")
            return

        self.sumTotal()
        self.datecad = date.today().strftime("%d-%m-%Y")
        self.subtotal = self.subTotal.get()
        self.disc = self.discount.get()
        self.tot = self.total.get()
        self.obs = (self.obs_entry.get("1.0", "end-1c")).strip()
        self.status = self.cmbStts.get()
        self.hist = ""
        self.tipo = "orçamento"
        self.pag = self.cmbPag.get()
        self.par = self.cmbPar.get()

        self.client = self.selectClientbyId(self.lb_id.cget("text"))
        self.client = self.client[0]

        self.cepcod = int(self.lb_cepid.cget("text"))

        self.cep = self.selectCepbyId(self.cepcod)[0]

        self.connect_db()
        self.cursor.execute(""" SELECT * FROM info""")
        self.info = self.cursor.fetchone()
        self.disconnect_db()

        self.num = self.lb_num.get()

        self.today = [self.datecad]
        self.clientString = [self.client[1], self.client[3], self.client[2], self.num]
        self.endString = [self.cep[1], self.cep[2], self.cep[3]]
        self.sp = [self.info[1], self.info[2], self.info[3], self.info[4]]
        self.bank = [self.info[5], self.info[6], self.info[7], self.info[8]]
        self.ctt = [self.info[9], self.info[10]]
        self.loc = [self.info[13], self.info[11], self.info[12]]
        self.todo = [self.obs_entry.get("1.0", "end-1c").strip()]
        self.orderString = [f'{self.par} x {self.tot}', self.pag, self.subtotal]

        data = []
        for row_id in budgetTree.get_children():
            row = budgetTree.item(row_id)['values']
            data.append(row)

        self.zip = random.randint(10000000000, 99999999999)
        self.archive = f'{self.client[1]}_{self.tipo}{self.datecad}_{self.zip}'

        csv_path = os.path.join(
            glv.get_variable("APP_PATH"),
            "orçamentos",
            f"{self.archive}.csv"
        )

        file = open(csv_path, 'w+', newline='')

        with file:
            write = csv.writer(file)
            write.writerow(self.today)
            write.writerow(self.orderString)
            write.writerow(self.clientString)
            write.writerow(self.endString)
            write.writerow(self.sp)
            write.writerow(self.bank)
            write.writerow(self.ctt)
            write.writerow(self.loc)
            write.writerow(self.todo)
            write.writerows(data)

    def genSale(self):
        if self.lb_idbud.cget("text") == "0":
            self.saveorc()
            if self.lb_name.get() == "":
                return
            elif self.lb_cep.get() == "":
                return
            else:
                self.genSale()
        else:
            if self.lb_name.get() == "":
                messagebox.showerror("Erro", "Escolha ao menos um cliente para vincular à esta venda.")
                return
            else:
                self.getclientEntry()

            if self.lb_num.get() != "":
                self.getCttEntry()
            else:
                self.num = ""

            self.getCepEntry()
            if self.cepcod == "0":
                messagebox.showerror("Erro", "Escolha ao menos um endereço para vincular à esta venda.")
                return
            self.getAllData()
            self.tipo = "venda"
            self.type = "Venda"
            self.lb_typebud.config(text=self.type)
            messagebox.showinfo('VENDA', 'Venda gerada com sucesso.')
            self.connect_db()
            self.cursor.execute(""" UPDATE tb_comercial SET
                    cliente = ?, 
                    cliente_cod = ?, 
                    cep_cod = ?, 
                    linha = ?,
                    pagamento = ?,
                    parcelas = ?, 
                    subtotal = ?, 
                    discount = ?,
                    data = ?, 
                    total = ?, 
                    obs = ?, 
                    status = ?, 
                    tipo = ?, 
                    link = ?,
                    pagas = ?
                    WHERE cod = ?""",
                        (self.name,
                         self.cod,
                         self.cepcod,
                         self.num,
                         self.pag,
                         self.par,
                         self.subtotal,
                         self.disc,
                         self.datecad,
                         self.tot,
                         self.obs,
                         self.status,
                         self.tipo,
                         self.link,
                         self.paid,
                         self.id))
            self.conn.commit()
            self.disconnect_db()

    def genOrder(self):
        if self.lb_idbud.cget("text") == "0":
            self.saveorc()

            if self.lb_name.get() == "":
                return
            elif self.lb_cep.get() == "":
                return
            else:
                self.genOrder()
        else:
            if self.lb_name.get() == "":
                messagebox.showerror("Erro", "Escolha ao menos um cliente para vincular à esta venda.")
                return
            else:
                self.getclientEntry()

            if self.lb_num.get() != "":
                self.getCttEntry()
            else:
                self.num = ""

            self.getCepEntry()
            if self.cepcod == "0":
                messagebox.showerror("Erro", "Escolha ao menos um endereço para vincular à esta venda.")
                return
            self.getAllData()
            self.id = self.lb_idbud.cget("text")
            self.tipo = "ordem"
            self.type = "Ordem de Serviço"
            self.lb_typebud.config(text=self.type)
            messagebox.showinfo('ORDEM DE SERVIÇO', 'Ordem de serviço gerada com sucesso.')
            self.connect_db()
            self.cursor.execute(""" UPDATE tb_comercial SET
                    cliente = ?, 
                    cliente_cod = ?, 
                    cep_cod = ?, 
                    linha = ?,
                    pagamento = ?,
                    parcelas = ?, 
                    subtotal = ?, 
                    discount = ?,
                    data = ?, 
                    total = ?, 
                    obs = ?, 
                    status = ?, 
                    tipo = ?, 
                    link = ?,
                    pagas = ?
                    WHERE cod = ?""",
                        (self.name,
                         self.cod,
                         self.cepcod,
                         self.num,
                         self.pag,
                         self.par,
                         self.subtotal,
                         self.disc,
                         self.datecad,
                         self.tot,
                         self.obs,
                         self.status,
                         self.tipo,
                         self.link,
                         self.paid,
                         self.id))
            self.conn.commit()
            self.disconnect_db()

    def callback(self, event):
        if self.cmbPag.get() == 'À vista':
            self.cmbPar.current(0)
            self.cmbPar['state'] = 'disabled'
        elif self.cmbPag.get() == 'Parcelado':
            self.cmbPar['state'] = 'readonly'
        elif self.cmbPag.get() == 'Antecipado':
            self.cmbPar.current(0)
            self.cmbPar['state'] = 'disabled'

        self.discountValue(event)

    def divTotal(self, event):
        self.discountValue(self)

    def filter(self, type):
        for widget in self.framedown.winfo_children():
            widget_class = widget.__class__.__name__
            if widget_class == 'Treeview' or widget_class == 'Scrollbar':
                widget.destroy()

        self.connect_db()
        self.name_entry.insert(END, '%')
        nome = self.name_entry.get()
        self.cursor.execute(
            """ SELECT cod, cliente, status, pagamento, parcelas, total, discount, subtotal, data, tipo FROM tb_comercial
            WHERE tipo LIKE ? AND cliente LIKE ? ORDER BY data desc """, (type, nome))
        row = self.cursor.fetchall()
        self.disconnect_db()
        self.name_entry.delete(0, END)
        global comercialtree

        list = row

        self.list_header = ['ID', 'Cliente', 'Status', 'Pagamento', 'Parcelas', 'desconto', 'total', 'data']
        comercialtree = ttk.Treeview(self.framedown, selectmode="extended", columns=self.list_header,
                                     show="headings")
        self.vsb = ttk.Scrollbar(self.framedown, orient="vertical", command=comercialtree.yview)

        comercialtree.tag_configure('orc', background="yellow")
        comercialtree.tag_configure('sal', background="light green")
        comercialtree.tag_configure('ord', background="light blue")

        comercialtree.configure(yscrollcommand=self.vsb.set)
        comercialtree.place(relx=0.02, rely=0.16, relwidth=0.94, relheight=0.55)
        self.vsb.place(relx=0.96, rely=0.16, relwidth=0.02, relheight=0.55)

        hd = ["nw", "nw", "nw", "nw", "nw", "nw", "nw", "nw", "nw"]
        h = [10, 150, 80, 70, 70, 60, 60, 60, 60]
        n = 0

        comercialtree.bind('<ButtonRelease-1>', self.showHist)
        comercialtree.bind('<Double-Button-1>', self.OnClickComercial)

        for col in self.list_header:
            comercialtree.heading(col, text=col.title(), anchor=CENTER)
            comercialtree.column(col, width=h[n], anchor=hd[n])
            n += 1

        for row in list:
            subtotal = float(row[5][3:])
            disc = row[6] / 100 * subtotal
            if row[9] == 'orçamento':
                self.tag = 'orc'
            elif row[9] == 'venda':
                self.tag = 'sal'
            elif row[9] == 'ordem':
                self.tag = 'ord'
            comercialtree.insert('', END, text='1', tags=self.tag,
                                 values=(row[0], row[1], row[2], row[3], f'{row[4]} x {row[5]}',
                                         f'R$ {disc:.2f}', row[7], row[8]))

    def genReport(self):
        csv_path = os.path.join(
            glv.get_variable("APP_PATH"),
            glv.get_variable("DATA_DIR"),
            "reports",
            "comercial.csv"
        )

        with open(csv_path, "w", newline='') as myfile:
            csvwriter = csv.writer(myfile, delimiter=',')
            for entry in comercialtree.get_children():
                values = (comercialtree.item(entry, 'values'))
                self.connect_db()
                self.cursor.execute(""" SELECT cliente, cep_cod, linha, pagamento, parcelas, pagas ,subtotal, discount, total, data, obs, hist, status, tipo FROM tb_comercial
                    WHERE cod = ?""", (values[0],))
                row = self.cursor.fetchone()
                self.cursor.execute(""" SELECT cep, endereco, cid FROM tb_enderecos 
                    WHERE cod = ?""", (row[1],))
                rowcep = self.cursor.fetchone()
                self.disconnect_db()

                if row[13] == 'ordem':
                    self.stage = 'Ordem de serviço'
                elif row[13] == 'venda':
                    self.stage = "Venda"
                else:
                    self.stage = "Orçamento"

                self.entrada = row[5] * float(row[8][3:])

                data = [row[0], row[2], rowcep[0], rowcep[1], rowcep[2], row[3], row[4], row[5], row[8], f'R$ {self.entrada}',row[6], row[7],  row[9], row[12], self.stage]
                csvwriter.writerow(data)

        os.startfile(csv_path)

    def filtercmb(self, event):
        for widget in self.framedown.winfo_children():
            widget_class = widget.__class__.__name__
            if widget_class == 'Treeview' or widget_class == 'Scrollbar':
                widget.destroy()
        self.connect_db()

        if self.cmbStatus.get() != "Status" and self.cmbPagamento.get() != 'Pagamento':
            self.cursor.execute(
                """ SELECT cod, cliente, status, pagamento, parcelas, total, discount, subtotal, data, tipo FROM tb_comercial
                WHERE status LIKE ? AND pagamento LIKE ? ORDER BY data desc """,
                (self.cmbStatus.get(), self.cmbPagamento.get(),))
            row = self.cursor.fetchall()

        elif self.cmbStatus.get() != "Status" and self.cmbPagamento.get() == "Pagamento":
            self.cursor.execute(
                """ SELECT cod, cliente, status, pagamento, parcelas, total, discount, subtotal, data, tipo FROM tb_comercial
                WHERE status LIKE ? ORDER BY data desc """,
                (self.cmbStatus.get(),))
            row = self.cursor.fetchall()

        elif self.cmbStatus.get() == "Status" and self.cmbPagamento.get() != "Pagamento":
            self.cursor.execute(
                """ SELECT cod, cliente, status, pagamento, parcelas, total, discount, subtotal, data, tipo FROM tb_comercial
                WHERE pagamento LIKE ? ORDER BY data desc """,
                (self.cmbPagamento.get(),))
            row = self.cursor.fetchall()
        else:
            self.cursor.execute(
                """ SELECT cod, cliente, status, pagamento, parcelas, total, discount, subtotal, data, tipo FROM tb_comercial
                ORDER BY data desc """)
            row = self.cursor.fetchall()
        self.disconnect_db()

        global comercialtree

        list = row

        self.list_header = ['ID', 'Cliente', 'Status', 'Pagamento', 'Parcelas', 'desconto', 'total', 'data']
        comercialtree = ttk.Treeview(self.framedown, selectmode="extended", columns=self.list_header,
                                     show="headings")
        self.vsb = ttk.Scrollbar(self.framedown, orient="vertical", command=comercialtree.yview)

        comercialtree.tag_configure('orc', background="yellow")
        comercialtree.tag_configure('sal', background="light green")
        comercialtree.tag_configure('ord', background="light blue")

        comercialtree.configure(yscrollcommand=self.vsb.set)
        comercialtree.place(relx=0.02, rely=0.16, relwidth=0.94, relheight=0.55)
        self.vsb.place(relx=0.96, rely=0.16, relwidth=0.02, relheight=0.55)

        hd = ["nw", "nw", "nw", "nw", "nw", "nw", "nw", "nw", "nw"]
        h = [10, 150, 80, 70, 70, 60, 60, 60, 60]
        n = 0

        for col in self.list_header:
            comercialtree.heading(col, text=col.title(), anchor=CENTER)
            comercialtree.column(col, width=h[n], anchor=hd[n])
            n += 1

        for row in list:
            subtotal = float(row[5][3:])
            disc = row[6] / 100 * subtotal
            if row[9] == 'orçamento':
                self.tag = 'orc'
            elif row[9] == 'venda':
                self.tag = 'sal'
            elif row[9] == 'ordem':
                self.tag = 'ord'
            comercialtree.insert('', END, text='1', tags=self.tag,
                                 values=(row[0], row[1], row[2], row[3], f'{row[4]} x {row[5]}',
                                         f'R$ {disc:.2f}', row[7], row[8]))

        comercialtree.bind('<ButtonRelease-1>', self.showHist)
        comercialtree.bind('<Double-Button-1>', self.OnClickComercial)

    def showHist(self, event):
        treev_data = comercialtree.focus()
        treev_dicionario = comercialtree.item(treev_data)
        treev_list = treev_dicionario['values']
        cod = treev_list[0]

        self.connect_db()
        self.cursor.execute(
            """ SELECT hist FROM tb_comercial
            WHERE cod = ? ORDER BY data desc """, (cod,))
        row = self.cursor.fetchall()
        self.disconnect_db()

        self.obs_entry.delete("1.0", END)
        self.obs_entry.insert("1.0", row[0][0])

    def attHist(self):
        treev_data = comercialtree.focus()
        treev_dicionario = comercialtree.item(treev_data)
        treev_list = treev_dicionario['values']
        cod = treev_list[0]

        self.hist = self.obs_entry.get("1.0", END).strip()
        self.connect_db()
        self.cursor.execute(""" UPDATE tb_comercial SET
                            hist = ?
                            WHERE cod = ?""",
                            (self.hist,
                             cod))
        self.conn.commit()
        messagebox.showinfo('Sucesso', 'Dados atualizados com sucesso.')
        self.disconnect_db()

    def searchProduct(self):

        for widget in self.framedown.winfo_children():
            widget_class = widget.__class__.__name__
            if widget_class == 'Treeview':
                widget.destroy()

        if self.prod_entry.get() == '':
           list = self.selectAllProducts()
        else:
            if self.prod_entry.get() != '':
                list = self.searchProductbyName()

        self.treeReload(list)