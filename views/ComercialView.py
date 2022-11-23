import sqlite3
import os

from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from lib.colours import color
import lib.global_variable as glv


class ComercialController:
    def __init__(self):
        pass

    def getEntry(self):
        self.cod = self.lb_id.cget("text")
        self.lb_name.get()

    def setEntry(self, cod, name):
        self.lb_id.config(text=cod)
        self.lb_name.insert(END, name)

    def getCepEntry(self):
        self.lb_cep.get()

    def setCepEntry(self, end):
        self.lb_cep.insert(END, f'{end}')

    def getCttEntry(self):
        self.lb_num.get()

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
        self.cursor.execute(""" SELECT cod, cep, num, endereco FROM tb_enderecos 
                    WHERE cliente_cod = ?""", (cod))
        self.info = self.cursor.fetchall()
        for i in self.info:
            auxlist.append(i)

        self.disconnect_db()
        return auxlist

    def selectCepbyId(self, idcep):
        self.connect_db()
        idcep = int(idcep)
        self.cursor.execute(""" SELECT cod, cep, num, endereco FROM tb_enderecos
                WHERE cod = ?""", (idcep,))
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

        tree.bind("<Double-1>", self.OnDoubleClick)

    def treecepReload(self):
        global ceptree
        listcep = self.selectAllCep()

        self.adress_header = ['id', 'CEP', 'N°', 'end']

        ceptree = ttk.Treeview(self.frameup, selectmode="extended", columns=self.adress_header, show="headings")
        self.vsb2 = ttk.Scrollbar(self.frameup, orient="vertical", command=tree.yview)

        ceptree.configure(yscrollcommand=self.vsb2.set)
        ceptree.place(relx=0.02, rely=0.63, relheight=0.19, relwidth=0.450)
        self.vsb2.place(relx=0.46, rely=0.63, relheight=0.19, relwidth=0.03)

        hd = ["nw", "nw", "nw", "nw", "center", "center"]
        h = [10, 60, 30, 100]
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

        ctttree = ttk.Treeview(self.frameup, selectmode="extended", columns=self.ctt_header, show="headings")
        self.vsb3 = ttk.Scrollbar(self.frameup, orient="vertical", command=tree.yview)

        ctttree.configure(yscrollcommand=self.vsb3.set)
        ctttree.place(relx=0.02, rely=0.42, relheight=0.19, relwidth=0.45)
        self.vsb3.place(relx=0.46, rely=0.42, relheight=0.19, relwidth=0.03)

        hd = ["nw", "nw", "nw", "nw", "center", "center"]
        h = [100, 100]
        n = 0

        for col in self.ctt_header:
            ctttree.heading(col, text=col.title(), anchor=CENTER)
            ctttree.column(col, width=h[n], anchor=hd[n])
            n += 1

        for item in listctt:
            ctttree.insert('', END, values=item)

        ctttree.bind("<Double-1>", self.OnDoubleClick3)

    def OnDoubleClick(self, event):
        self.lb_name.config(state = NORMAL)
        self.clean()
        self.lb_cep.config(state = NORMAL)
        self.cleancep()
        self.lb_num.config(state = NORMAL)
        self.cleanctt()
        cod = self.treeSelect()
        values = self.selectClientbyId(int(cod[0]))
        self.setEntry(values[0][0], values[0][1])
        self.lb_name.config(state = DISABLED)

        self.treecepReload()
        self.treecttReload()

    def OnDoubleClick2(self, event):
        self.lb_cep.config(state = NORMAL)
        self.cleancep()
        cepcod = self.ceptreeSelect()
        values = self.selectCepbyId(cepcod[0])
        self.setCepEntry(values[0][1])
        self.lb_cep.config(state = DISABLED)

    def OnDoubleClick3(self, event):
        self.lb_num.config(state = NORMAL)
        self.cleanctt()
        ctt = self.ctttreeSelect()
        self.setCttEntry(ctt[0])
        self.lb_num.config(state = DISABLED)

    def OnClick(self, event):
        self.prod.config(state=NORMAL)
        self.cleanprod()
        prod = self.budgettreeSelect()
        self.setProdEntry(prod[0], f'{prod[1]} - {prod[2]}', prod[3], prod[4], prod[5], prod[6])
        self.prod.config(state = DISABLED)
        self.kg.insert(END, "0")
        self.m.insert(END, "0")
        self.m2.insert(END, "0")
        self.uni.insert(END, "0")


class ComercialView(ComercialController):
    def __init__(self, frameup, framedown, framebar):
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

    def init_sales(self):
        self.clearAll()
        self.init_layout()

        self.rtrnImg = PhotoImage(file=r'assets\retornar.png')
        self.bt_return = Button(self.framebar, image=self.rtrnImg, relief='flat',
                                command=self.init_Comercial)
        self.bt_return.place(relx=0.8, rely=0.08, width=70, height=60)

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
                                  command=self.init_budget)
        self.btn_budgets.place(relx=0.02, rely=0.6, width=130, height=100)

        self.salesIMG = PhotoImage(file=r"assets\VEN.png")
        self.btn_sales = Button(self.frameup, image=self.salesIMG, relief='flat',
                                  command=self.init_sales)
        self.btn_sales.place(relx=0.349, rely=0.6, width=130, height=100)

        self.orderIMG = PhotoImage(file=r"assets\ORD.png")
        self.btn_order = Button(self.frameup, image=self.orderIMG, relief='flat',
                                  command=self.init_sales)
        self.btn_order.place(relx=0.678, rely=0.6, width=130, height=100)

        self.rprtImg = PhotoImage(file=r'assets\report.png')
        self.bt_report = Button(self.framebar, image=self.rprtImg, relief='flat',
                                command=self.init_Comercial)
        self.bt_report.place(relx=0.8, rely=0.08, width=70, height=60)

    def init_budgets(self):
        self.title = Label(self.frameup, text="Orçamentos", font="Ivy 18 bold", bg="#CEDCE4")
        self.title.place(relx=0.015, rely=0.005, relwidth=0.35, height= 28)

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
        self.lb_idref.place(relx=0.52, rely=0.42, relheight=0.06, relwidth=0.1)
        self.lb_id = Label(self.frameup, text="0", font='Ivy 16', background=color("background"),
                           anchor="w", justify=LEFT)
        self.lb_id.place(relx=0.62, rely=0.42, relheight=0.06, relwidth=0.15)

        self.lb_clientref = Label(self.frameup, text="Nome: ", background=color("background"))
        self.lb_clientref.place(relx=0.52, rely=0.50, relheight=0.06, relwidth=0.1)
        self.lb_name = Entry(self.frameup, background=color("background"))
        self.lb_name.place(relx=0.62, rely=0.50, relheight=0.06, relwidth=0.36)

        self.lb_cepref = Label(self.frameup, text="End: ", background=color("background"))
        self.lb_cepref.place(relx=0.535, rely=0.70, relheight=0.06, relwidth=0.1)
        self.lb_cep = Entry(self.frameup, background=color("background"))
        self.lb_cep.place(relx=0.62, rely=0.70, relheight=0.06, relwidth=0.36)

        self.lb_numref = Label(self.frameup, text="Num: ", background=color("background"))
        self.lb_numref.place(relx=0.525, rely=0.60, relheight=0.06, relwidth=0.1)
        self.lb_num = Entry(self.frameup, background=color("background"))
        self.lb_num.place(relx=0.62, rely=0.60, relheight=0.06, relwidth=0.36)

    def init_budgets2(self):
        self.lblf = Label(self.framedown, font=('arial', 13, 'bold'), text="Frete:", bg=color("background"),
                          anchor='e', justify=RIGHT)
        self.lblf.place(relx=0.25, rely=0.68, relwidth=0.1, relheight=0.08)
        self.lblfrete = Label(self.framedown, font=('arial', 13, 'bold'), text="Não será cobrado frete",
                              bg=color("background"), anchor='w', justify=LEFT)
        self.lblfrete.place(relx=0.35, rely=0.68, relwidth=0.6, relheight=0.08)

        self.lblv = Label(self.framedown, font=('arial', 13, 'bold'), text="Visita:", bg=color("background"),
                          anchor='e', justify=RIGHT)
        self.lblv.place(relx=0.25, rely=0.78, relwidth=0.1, relheight=0.08)
        self.lblvisita = Label(self.framedown, font=('arial', 13, 'bold'), text="Não será cobrada visita",
                               bg=color("background"), anchor='w', justify=LEFT)
        self.lblvisita.place(relx=0.35, rely=0.78, relwidth=0.4, relheight=0.08)

        self.lblSubTotal = Label(self.framedown, font=('arial', 14, 'bold'), text="Subtotal", bg=color("background"),
                                 anchor='e', justify=RIGHT)
        self.lblSubTotal.place(relx=0.63, rely=0.68, relwidth=0.13, relheight=0.08)
        self.subTotal = Entry(self.framedown, font=('arial', 14, 'bold'), bg=color("background"))
        self.subTotal.place(relx=0.780, rely=0.69, relwidth=0.19, relheight=0.06)
        self.subTotal.config(state=DISABLED)

        self.lbldiscount = Label(self.framedown, font=('arial', 14, 'bold'), text="Desconto                               %", bg=color("background"),
                                 anchor='e', justify=RIGHT)
        self.lbldiscount.place(relx=0.63, rely=0.78, relwidth=0.34, relheight=0.08)
        self.discount = Entry(self.framedown, font=('arial', 14, 'bold'), bg=color("background"), justify=RIGHT)
        self.discount.place(relx=0.780, rely=0.79, relwidth=0.15, relheight=0.06)
        self.discount.insert(END, "0")

        self.discount.bind('<Return>', self.discountValue)
        self.discount.bind('<FocusOut>', self.discountValue)

        self.lbltotal = Label(self.framedown, font=('arial', 14, 'bold'), text="total", bg=color("background"),
                                 anchor='e', justify=RIGHT)
        self.lbltotal.place(relx=0.60, rely=0.88, relwidth=0.16, relheight=0.08)
        self.total = Entry(self.framedown, font=('arial', 14, 'bold'), bg=color("background"))
        self.total.place(relx=0.780, rely=0.89, relwidth=0.19, relheight=0.06)
        self.total.config(state=DISABLED)

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

        self.prodcod = Label(self.framedown, font=('arial', 1), bg=color("background"), fg=color("background"))
        self.prodcod.place(relx=0.55, rely=0.11, relwidth=0.26, relheight=0.05)
        self.prod = Entry(self.framedown, font=('arial', 11), justify=LEFT)
        self.prod.place(relx=0.55, rely=0.11, relwidth=0.38, relheight=0.05)
        self.prod.config(state=DISABLED)

        self.mat = Label(self.framedown)
        self.valuekg = Label(self.framedown)
        self.valuem = Label(self.framedown)
        self.valuem2 = Label(self.framedown)
        self.valueuni = Label(self.framedown)

        self.rmvImg = PhotoImage(file=r'assets\rmv.png')
        self.addImg = PhotoImage(file=r'assets\add.png')

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
        self.lb_idbud = Label(self.framedown, text="", font="Ivy 20", background="#CEDCE4", justify=LEFT)
        self.lb_idbud.place(relx=0.1, rely=0.013)

    def init_budgetButtons(self):
        self.svbudImg = PhotoImage(file=r"assets\salvarorc.png")
        self.bt_savebudget = Button(self.framedown, image=self.svbudImg, relief='flat',
                                command=self)
        self.bt_savebudget.place(relx=0.022, rely=0.7, height=100, width=130)

        self.gnrtSale = PhotoImage(file=r"assets\genven.png")
        self.bt_genSale = Button(self.frameup, image=self.gnrtSale, relief='flat',
                                command=self)
        self.bt_genSale.place(relx=0.020, rely=0.88, relwidth=0.225, relheight=0.1)

        self.gnrtServ = PhotoImage(file=r"assets\genods.png")
        self.bt_genService = Button(self.frameup, image=self.gnrtServ, relief='flat',
                                command=self)
        self.bt_genService.place(relx=0.38, rely=0.88, relwidth=0.225, relheight=0.1)

        self.prntCsv = PhotoImage(file=r"assets\printcsv.png")
        self.printCsv = Button(self.frameup, image=self.prntCsv, relief='flat',
                                command=self)
        self.printCsv.place(relx=0.75, rely=0.88, relwidth=0.225, relheight=0.1)

    def init_treecomercial(self):
        global tree

        self.list_header = ['ID', 'Nome', 'Email', 'Documento']
        tree = ttk.Treeview(self.frameup, selectmode="extended", columns=self.list_header, show="headings")
        self.vsb = ttk.Scrollbar(self.frameup, orient="vertical", command=tree.yview)

        tree.configure(yscrollcommand=self.vsb.set)
        tree.place(relx=0.02, rely=0.16, relwidth=0.92, relheight=0.41)
        self.vsb.place(relx=0.94, rely=0.16, relwidth=0.04, relheight=0.41)

        hd = ["nw", "nw", "nw", "nw"]
        h = [10, 120, 120, 90]
        n = 0

        for col in self.list_header:
            tree.heading(col, text=col.title(), anchor=CENTER)
            tree.column(col, width=h[n], anchor=hd[n])
            n += 1


        tree.bind("<Double-1>", self.OnDoubleClick)

    def init_treecomercial2(self):
        global comercialtree

        self.list_header = ['ID', 'Cliente', 'subtotal', 'desconto', 'total', 'data']
        comercialtree = ttk.Treeview(self.framedown, selectmode="extended", columns=self.list_header, show="headings")
        self.vsb = ttk.Scrollbar(self.framedown, orient="vertical", command=comercialtree.yview)

        comercialtree.configure(yscrollcommand=self.vsb.set)
        comercialtree.place(relx=0.02, rely=0.15, relwidth=0.94, relheight=0.60)
        self.vsb.place(relx=0.96, rely=0.15, relwidth=0.02, relheight=0.60)

        hd = ["nw", "nw", "nw", "nw", "nw", "nw"]
        h = [10, 230, 60, 60, 60, 60]
        n = 0

        for col in self.list_header:
            comercialtree.heading(col, text=col.title(), anchor=CENTER)
            comercialtree.column(col, width=h[n], anchor=hd[n])
            n += 1

        tree.bind("<Double-1>", self.OnDoubleClick)

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

        self.ctt_header = ['Numero', 'Tipo']

        ctttree = ttk.Treeview(self.frameup, selectmode="extended", columns=self.ctt_header, show="headings")
        self.vsb3 = ttk.Scrollbar(self.frameup, orient="vertical", command=tree.yview)

        ctttree.configure(yscrollcommand=self.vsb3.set)
        ctttree.place(relx=0.02, rely=0.42, relheight=0.19, relwidth=0.45)
        self.vsb3.place(relx=0.46, rely=0.42, relheight=0.19, relwidth=0.03)

        hd = ["nw", "nw", "nw", "nw", "center", "center"]
        h = [100, 100]
        n = 0

        for col in self.ctt_header:
            ctttree.heading(col, text=col.title(), anchor=CENTER)
            ctttree.column(col, width=h[n], anchor=hd[n])
            n += 1

        global ceptree

        self.adress_header = ['id', 'CEP', 'N°', 'end']

        ceptree = ttk.Treeview(self.frameup, selectmode="extended", columns=self.adress_header, show="headings")
        self.vsb2 = ttk.Scrollbar(self.frameup, orient="vertical", command=tree.yview)

        ceptree.configure(yscrollcommand=self.vsb2.set)
        ceptree.place(relx=0.02, rely=0.63, relheight=0.19, relwidth=0.450)
        self.vsb2.place(relx=0.46, rely=0.63, relheight=0.19, relwidth=0.03)

        hd = ["nw", "nw", "nw", "nw", "center", "center"]
        h = [10, 60, 30, 100]
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
        tree.place(relx=0.02, rely=0.16, relwidth=0.93, relheight=0.41)
        self.vsb.place(relx=0.94, rely=0.16, relwidth=0.04, relheight=0.41)

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

    def addProd(self):
        if float(self.kg.get()) < 0 or float(self.m.get() )< 0 or float(self.m2.get()) < 0 or float(self.uni.get()) < 0:
            messagebox.showerror('Erro', 'Permitido apenas valores positivos')
        else:
            if self.kg.get() != '' or self.m.get() != '' or self.m2.get() != '' or self.uni.get() != '':
                self.getProdEntry()
                if self.kg.get() == "":
                    self.kg.insert(END, "0")
                else:
                    self.totalkg = float(self.vkg) * float(self.kg.get())

                if self.m.get() == "":
                    self.m.insert(END, "0")
                else:
                    self.totalm = float(self.vm) * float(self.m.get())

                if self.m2.get() == "":
                    self.m2.insert(END, "0")
                else:
                    self.totalm2 = float(self.vm2) * float(self.m2.get())

                if self.uni.get() == "":
                    self.uni.insert(END, "0")
                else:
                    self.totaluni = float(self.vuni) * float(self.uni.get())

                self.totalitem = self.totalkg + self.totalm + self.totalm2 + self.totaluni

                budgetTree.insert("", END, values=(self.prodcod.cget("text"), self.prod.get(), self.totalkg, self.totalm, self.totalm2,
                                                   self.totaluni, self.totalitem))
                self.sumTotal()

            else:
                messagebox.showerror('Erro', 'Favor insira valores numéricos')

    def rmvProd(self):
        selected_item = budgetTree.selection()[0]
        budgetTree.delete(selected_item)
        self.sumTotal()

    def discountValue(self, event):
        if float(self.discount.get()) > 100 or float(self.discount.get()) < 0:
            messagebox.showerror('Erro', 'Favor inserir desconto válido')
            self.discount.delete(0, END)
            self.discount.insert(END, "0")
        else:
            self.sumTotal()

    def sumTotal(self):
        self.subtotalvalue = 0
        for child in budgetTree.get_children():
            self.value = float(budgetTree.item(child, "values")[6])
            self.subtotalvalue += self.value

        self.totalvalue = self.subtotalvalue * (1 - (float(self.discount.get()) / 100))

        self.subTotal.config(state=NORMAL)
        self.subTotal.delete(0, END)
        self.subTotal.insert(END, str(f'R$ {self.subtotalvalue:.2f}'))
        self.subTotal.config(state=DISABLED)

        self.total.config(state=NORMAL)
        self.total.delete(0, END)
        self.total.insert(END, str(f'R$ {self.totalvalue:.2f}'))
        self.total.config(state=DISABLED)

