import sqlite3
import os
import csv

from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import  Calendar
from datetime import date


from lib.colours import color
import lib.global_variable as glv


class FluxoController:
    def __init__(self):
        pass

    def getEntry(self):
        self.id = self.lb_id.cget("text")
        self.sup = self.supplier_entry.get()
        self.pag = self.pag_entry.get()
        self.val = float(self.val_entry.get().replace(",", "."))
        self.par = int(self.par_entry.get())
        self.date = self.date_entry.get()

    def setEntry(self, id ,sup, pag, val, par, date):
        self.lb_id.config(text=id)
        self.supplier_entry.insert(END, sup)
        self.pag_entry.insert(END, pag)
        self.val_entry.insert(END, val)
        self.par_entry.insert(END, par)
        self.date_entry.insert(END, date)

    def clean(self):
        self.supplier_entry.delete(0, END)
        self.pag_entry.delete(0, END)
        self.val_entry.delete(0, END)
        self.par_entry.delete(0, END)
        self.date_entry.delete(0, END)

    def connect_db(self):
        db_path = os.path.join(
            glv.get_variable("APP_PATH"),
            "SPDB.db"
        )
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def disconnect_db(self):
        self.conn.close()

    def selectAllPaidBud(self):
        self.connect_db()
        self.cursor.execute(""" SELECT cod, cliente, pagamento, parcelas, total, subtotal, data, status FROM tb_comercial 
            WHERE status = 'Entrega finalizada' ORDER BY data desc""")
        self.info = self.cursor.fetchall()

        self.disconnect_db()
        return self.info

    def selectAllOutflow(self):

        self.connect_db()
        self.cursor.execute(""" SELECT cod, fornecedor, pagamento, parcelas, valor, total, data, status FROM tb_saidas 
            ORDER BY data desc""")
        self.info = self.cursor.fetchall()

        self.disconnect_db()
        return self.info

    def treeReload(self, list):
        global tree
        list = self.treeAllEntry()

        self.list_header = ['ID', 'Nome', 'Pagamento', 'Parcelas', 'Pago', 'total', 'data']
        tree = ttk.Treeview(self.framedown, selectmode="extended", columns=self.list_header, show="headings")
        self.vsb = ttk.Scrollbar(self.framedown, orient="vertical", command=tree.yview)

        tree.tag_configure('entrada', background="light green")
        tree.tag_configure('saida', background="red")
        tree.tag_configure('pagando', background="light yellow")

        tree.configure(yscrollcommand=self.vsb.set)
        tree.place(relx=0.01, rely=0.10, relwidth=0.96, relheight=0.70)
        self.vsb.place(relx=0.97, rely=0.10, relwidth=0.02, relheight=0.70)

        hd = ["nw", "nw", "nw", "nw", "nw", "nw", "nw", "nw", "nw"]
        h = [10, 150, 80, 70, 70, 60, 60, 60, 60]
        n = 0

        for col in self.list_header:
            tree.heading(col, text=col.title(), anchor=CENTER)
            tree.column(col, width=h[n], anchor=hd[n])
            n += 1

        for item in list:
            if item[7] == 'Entrega finalizada':
                self.tag = 'entrada'
            elif item[7] == 'saida':
                self.tag = 'saida'
            tree.insert('', END, values=item, tags=self.tag)

        self.lucroBruto = 0
        self.lucroLiquido = 0
        for row_id in tree.get_children():
            row = tree.item(row_id)['values']
            print(row[5])
            if row[6] <= date.today().strftime("%d-%m-%Y"):
                if row[7] == 'Entrega finalizada':
                    self.lucroBruto += float(row[5][3:])
                    self.lucroLiquido += float(row[5][3:])
                elif row[7] == 'saida':
                    self.lucroLiquido -= float(row[5])

        self.lucrobru.config(text=f'R$ {self.lucroBruto}')
        self.lucroliq.config(text=f'R$ {self.lucroLiquido}')

        tree.bind("<Double-Button-1>", self.OnDoubleClick)

    def insertOutflow(self):
        try:
            self.getEntry()
            self.value = self.val / self.par
            self.connect_db()
            self.cursor.execute(f""" INSERT INTO tb_saidas (fornecedor, pagamento, valor, parcelas, total, data, status) 
                                                    VALUES (?, ?, ?, ?, ?, ?, ?)""",
                                (self.sup, self.pag, f'{self.value:.2f}', self.par, f'{self.val:.2f}', self.date, "saida"))
            self.conn.commit()
            messagebox.showinfo('Sucesso', 'Dados inseridos com sucesso.')
            self.disconnect_db()
        except sqlite3.Error as err:
            print(err)
            messagebox.showinfo('Erro', 'Não foi possível inserir dados no banco.')

    def updateOutflow(self):
        try:
            self.getEntry()
            self.value = self.val / self.par
            self.connect_db()
            self.cursor.execute(""" UPDATE tb_saidas SET
                fornecedor = ?,
                pagamento = ?,
                valor = ?,
                parcelas = ?,
                total = ?,
                data = ?
                WHERE cod = ?""", (self.sup, self.pag, f'{self.value:.2f}', self.par, f'{self.val:.2f}', self.date, self.id))
            self.conn.commit()
            self.disconnect_db()
        except sqlite3.Error as err:
            print(err)
            messagebox.showinfo('Erro', 'Não foi possível inserir dados no banco.')

    @staticmethod
    def treeSelect():
        treev_data = tree.focus()
        treev_dicionario = tree.item(treev_data)
        treev_list = treev_dicionario['values']

        return treev_list

    def OnDoubleClick(self, event):
        row = self.treeSelect()
        self.clean()
        if row[7] == 'saida':
            self.setEntry(row[0], row[1], row[2], row[4], row[3], row[6])


class FluxoView(FluxoController):
    def __init__(self, frameup, framedown, framebar):
        self.list_cli = ttk.Treeview
        self.framedown = framedown
        self.frameup = frameup
        self.framebar = framebar
        self.setup()

    def setup(self):
        self.init_Fluxo()
        self.init_tree()

    def init_Fluxo(self):
        self.init_layout()
        self.init_layoutcad()
        self.init_buttons()
        self.init_DRE()

    def init_layout(self):
        self.bgImg = PhotoImage(file=r'assets\CARD.png')
        self.bg = Label(self.frameup, image=self.bgImg)
        self.bg.place(relx=0, rely=0, relwidth=1, height=445)

        self.bg2Img = PhotoImage(file=r'assets\CARD2.png')
        self.bg2 = Label(self.framedown, image=self.bg2Img, bg=color("background2"))
        self.bg2.place(relwidth=1, relheight=1)

        self.title = Label(self.frameup, text="Fluxo de Caixa", font="Ivy 18 bold", bg="#CEDCE4")
        self.title.place(relx=0.02, rely=0.005, relwidth=0.4, height= 28)

        Label(self.frameup, text="                                                 ", font="Ivy 13 bold",
              bg=color("background-bar")). \
            place(relx=0, rely=0.84, relwidth=1, relheight=0.02)

    def init_layoutcad(self):
        self.lb_id = Label(self.frameup)

        self.supplier = Label(self.frameup, text="Destino:", font="Ivy 12", bg=color("background"))
        self.supplier.place(relx=0.052, rely=0.07, relwidth=0.2, relheight=0.1)
        self.supplier_entry = Entry(self.frameup, font="Ivy 11")
        self.supplier_entry.place(relx=0.245, rely=0.1, relwidth=0.65, relheight=0.05)

        self.srchImg = PhotoImage(file=r"assets\procurar.png")
        self.bt_srch = Button(self.frameup, image=self.srchImg, relief='flat', background=color("background"),
                              command=self.searchProduct)
        self.bt_srch.place(relx=0.90, rely=0.1, relwidth=0.08, relheight=0.06)

        self.clrImg = PhotoImage(file=r"assets\lixo.png")
        self.bt_clr = Button(self.frameup, image=self.clrImg, relief='flat', background=color("background"),
                             command=self.clean)
        self.bt_clr.place(relx=0.90, rely=0.18, relwidth=0.08, relheight=0.06)

        self.pag = Label(self.frameup, text="Pagamento:", font="Ivy 12", bg=color("background"))
        self.pag.place(relx=0.02, rely=0.16, relwidth=0.2, relheight=0.1)
        self.pag_entry = Entry(self.frameup, font="Ivy 11")
        self.pag_entry.place(relx=0.245, rely=0.19, relwidth=0.65, relheight=0.05)

        self.val = Label(self.frameup, text="Valor:", font="Ivy 12", bg=color("background"))
        self.val.place(relx=0.075, rely=0.28, relwidth=0.2, relheight=0.1)
        self.val_entry = Entry(self.frameup, font="Ivy 11")
        self.val_entry.place(relx=0.245, rely=0.31, relwidth=0.30, relheight=0.05)

        self.par = Label(self.frameup, text="Parcelas:", font="Ivy 12", bg=color("background"))
        self.par.place(relx=0.59, rely=0.28, relwidth=0.2, relheight=0.1)
        self.par_entry = Entry(self.frameup, font="Ivy 11")
        self.par_entry.place(relx=0.785, rely=0.31, relwidth=0.11, relheight=0.05)

        self.date = Label(self.frameup, text="Data:", font="Ivy 12", bg=color("background"))
        self.date.place(relx=0.08, rely=0.39, relwidth=0.2, relheight=0.1)
        self.date_entry = Entry(self.frameup, font="Ivy 11")
        self.date_entry.place(relx=0.25, rely=0.41, relwidth=0.2, relheight=0.06)
        self.date_btn = Button(self.frameup, font="Ivy 11", text="Selecionar Data", command=self.calendar)
        self.date_btn.place(relx=0.62, rely=0.41, relwidth=0.28, relheight=0.06)
        self.date_entry.insert(0, date.today().strftime("%d-%m-%Y"))

    def init_buttons(self):

        self.insrtImg = PhotoImage(file=r"assets\INSERIR.png")
        self.bt_insert = Button(self.frameup, image=self.insrtImg, relief='flat',
                                command=self.addOutflow)
        self.bt_insert.place(relx=0.020, rely=0.88, relwidth=0.225, relheight=0.1)

        self.attImg = PhotoImage(file=r"assets\ATUALIZAR.png")
        self.bt_update = Button(self.frameup, image=self.attImg, relief='flat',
                                command=self.attOutflow)
        self.bt_update.place(relx=0.75, rely=0.88, relwidth=0.225, relheight=0.1)

        self.rprtImg = PhotoImage(file=r'assets\report.png')
        self.bt_report = Button(self.framebar,image=self.rprtImg, relief='flat',
                               command=self.genReport)
        self.bt_report.place(relx=0.8, rely=0.08, width=70, height=60)

    def init_DRE(self):
        self.lucrobru = Label(self.framedown, text=" ", font="Ivy 14", bg=color("background"), anchor='e', justify=RIGHT)
        self.lucrobru.place(relx=0.80, rely=0.80, relwidth=0.18, relheight=0.08)
        self.lb1 = Label(self.framedown, text="Receita Bruta: ", font="Ivy 14", bg=color("background"), anchor='e', justify=RIGHT)
        self.lb1.place(relx=0.65, rely=0.80, relwidth=0.18, relheight=0.08)

        self.lucroliq = Label(self.framedown, text=" ", font="Ivy 14", bg=color("background"), anchor='e', justify=RIGHT)
        self.lucroliq.place(relx=0.80, rely=0.89, relwidth=0.18, relheight=0.08)
        self.lb2 = Label(self.framedown, text="Receita Líquida: ", font="Ivy 14", bg=color("background"), anchor='e', justify=RIGHT)
        self.lb2.place(relx=0.65, rely=0.89, relwidth=0.18, relheight=0.08)


    def init_tree(self):
        global tree
        list = self.treeAllEntry()

        self.list_header = ['ID', 'Nome', 'Pagamento', 'Parcelas', 'Pago', 'total', 'data']
        tree = ttk.Treeview(self.framedown, selectmode="extended", columns=self.list_header, show="headings")
        self.vsb = ttk.Scrollbar(self.framedown, orient="vertical", command=tree.yview)

        tree.tag_configure('entrada', background="light green")
        tree.tag_configure('saida', background="red")
        tree.tag_configure('pagando', background="light yellow")

        tree.configure(yscrollcommand=self.vsb.set)
        tree.place(relx=0.01, rely=0.10, relwidth=0.96, relheight=0.70)
        self.vsb.place(relx=0.97, rely=0.10, relwidth=0.02, relheight=0.70)

        hd = ["nw", "nw", "nw", "nw", "nw", "nw", "nw", "nw", "nw"]
        h = [10, 150, 80, 70, 70, 60, 60, 60, 60]
        n = 0

        for col in self.list_header:
            tree.heading(col, text=col.title(), anchor=CENTER)
            tree.column(col, width=h[n], anchor=hd[n])
            n += 1

        for item in list:
            if item[7] == 'Entrega finalizada':
                self.tag = 'entrada'
            elif item[7] == 'saida':
                self.tag = 'saida'
            tree.insert('', END, values=item, tags=self.tag)

        self.lucroBruto = 0
        self.lucroLiquido = 0
        for row_id in tree.get_children():
            row = tree.item(row_id)['values']
            if row[6] <= date.today().strftime("%d-%m-%Y"):
                if row[7] == 'Entrega finalizada':
                    self.lucroBruto += float(row[5][3:])
                    self.lucroLiquido += float(row[5][3:])
                elif row[7] == 'saida':
                    self.lucroLiquido -= float(row[5])

        self.lucrobru.config(text=f'R$ {self.lucroBruto}')
        self.lucroliq.config(text=f'R$ {self.lucroLiquido}')

        tree.bind("<Double-Button-1>", self.OnDoubleClick)

    def calendar(self):
        self.calendar = Calendar(self.frameup, bg=color("background"), font=("Times", 10, 'bold'), locale='pt_br')
        self.calendar.place(relx=0.316, rely=0.47)
        self.date_btn = Button(self.frameup, font="Ivy 11", text="Inserir Data", command=self.printCal)
        self.date_btn.place(relx=0.62, rely=0.41, relwidth=0.28, relheight=0.06)

    def printCal(self):
        dataIni = self.calendar.get_date().replace("/", "-")
        self.calendar.destroy()
        self.date_entry.delete(0, END)
        self.date_entry.insert(END, dataIni)
        self.date_btn.destroy()

    def addOutflow(self):
        self.insertOutflow()
        self.clean()

        self.treeReload(self.treeAllEntry())

    def attOutflow(self):
        self.updateOutflow()
        self.clean()
        self.treeReload(self.treeAllEntry())

    def searchProduct(self):
        for widget in self.framedown.winfo_children():
            widget_class = widget.__class__.__name__
            if widget_class == 'Treeview':
                widget.destroy()

        if self.supplier_entry.get() == '':
            list = []
        else:
            list = []

        self.treeReload(list)

    def treeAllEntry(self):
        rowOutflow = self.selectAllOutflow()

        rowEntry = self.selectAllPaidBud()

        list = rowOutflow + rowEntry

        return list

    def genReport(self):
        csv_path = os.path.join(
            glv.get_variable("APP_PATH"),
            glv.get_variable("DATA_DIR"),
            "reports",
            "fluxo.csv"
        )

        data = []

        for row_id in tree.get_children():
            row = tree.item(row_id)['values']
            if row[7] == 'Entrega finalizada':
                self.tipo = 'Entrada'
            elif row[7] == 'saida':
                self.tipo = 'Saída'

            self.str = [row[1], row[2], row[3], row[4], row[5], row[6], self.tipo]
            data.append(self.str)

        file = open(csv_path, 'w+', newline='')

        with file:
            write = csv.writer(file)
            write.writerows(data)

        os.startfile(csv_path)

        self.setup()
