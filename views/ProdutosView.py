import sqlite3
import os
import csv

from tkinter import *
from tkinter import ttk
from tkinter import messagebox


from lib.colours import color
import lib.global_variable as glv


class ProductsController:
    def __init__(self):
        pass

    def getEntry(self):
        self.cod = int(self.lb_id.cget("text"))
        self.prod = self.prod_entry.get()
        self.mat = self.mat_entry.get()
        self.kg = self.kg_entry.get()
        self.m = self.m_entry.get()
        self.m2 = self.m2_entry.get()
        self.qtd = self.qtd_entry.get()
        self.liq = self.liq_entry.get()
        self.bru = self.bru_entry.get()
        self.obs = (self.obs_entry.get("1.0", "end-1c")).strip()

    def setEntry(self, cod, name, mat, kg, m, m2, qtd, liq, bru,obs):
        self.lb_id.config(text=cod)
        self.prod_entry.insert(END, name)
        self.mat_entry.insert(END, mat)
        self.kg_entry.insert(END, kg)
        self.m_entry.insert(END, m)
        self.m2_entry.insert(END, m2)
        self.qtd_entry.insert(END, qtd)
        self.liq_entry.insert(END, liq)
        self.bru_entry.insert(END, bru)
        self.obs_entry.insert("1.0", obs)

    def clean(self):
        self.prod_entry.delete(0, END)
        self.mat_entry.delete(0, END)
        self.kg_entry.delete(0, END)
        self.m_entry.delete(0, END)
        self.m2_entry.delete(0, END)
        self.qtd_entry.delete(0, END)
        self.liq_entry.delete(0, END)
        self.bru_entry.delete(0, END)
        self.obs_entry.delete("1.0", END)

    def connect_db(self):
        db_path = os.path.join(
            glv.get_variable("APP_PATH"),
            "SPDB.db"
        )
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def disconnect_db(self):
        self.conn.close()

    def insertProduct(self):
        self.getEntry()
        try:
            if self.kg == "" and float(self.kg) >= 0:
                self.kg = 0
            else:
                self.kg = float(self.kg.replace(",", "."))

            if self.m == "" and float(self.m) >= 0:
                self.m = 0
            else:
                self.m = float(self.m.replace(",", "."))

            if self.m2 == "" and float(self.m2) >= 0:
                self.m2 = 0
            else:
                self.m2 = float(self.m2.replace(",", "."))

            if self.qtd == "" and float(self.qtd) >= 0:
                self.qtd = 0
            else:
                self.qtd = float(self.qtd.replace(",", "."))

            if self.liq == "" and float(self.liq) >= 0:
                self.liq = 0
            else:
                self.liq = float(self.liq.replace(",", "."))

            if self.bru == "" and float(self.bru) >= 0:
                self.bru = 0
            else:
                self.bru = float(self.bru.replace(",", "."))

            if float(self.kg) < 0 or float(self.m) < 0 or float(self.m2) < 0 or float(self.qtd) < 0 or float(self.liq) < 0 or float(self.bru) < 0:
                messagebox.showerror('Erro', 'Preço inválido.')
                return
        except:
            messagebox.showerror('Erro', 'Preço inválido.')
        else:
            if self.prod == '':
                messagebox.showerror('Erro', 'Preencha os dados obrigatórios.')
            else:

                self.clean()
                self.connect_db()
                self.cursor.execute(""" INSERT INTO tb_produtos (servico, material, kg, m, m2, unit, liq, bru, descricao)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                    (self.prod, self.mat,f'{self.kg:.2f}', f'{self.m:.2f}', f'{self.m2:.2f}', f'{self.qtd:.2f}',f'{self.liq:.2f}', f'{self.bru:.2f}', self.obs))
                self.conn.commit()
                messagebox.showinfo('Sucesso', 'Dados inseridos com sucesso.')
                self.disconnect_db()
                row = self.selectAllProducts()
                self.treeReload(row)

    def selectAllProducts(self):
        auxlist = []
        self.connect_db()
        self.cursor.execute(""" SELECT * FROM tb_produtos """)
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

    def updateProduct(self):
        self.getEntry()
        self.connect_db()
        try:
            if self.kg == "":
                self.kg = 0
            else:
                self.kg = float(self.kg.replace(",", "."))
            if self.m == "":
                self.m = 0
            else:
                self.m = float(self.m.replace(",", "."))
            if self.m2 == "":
                self.m2 = 0
            else:
                self.m2 = float(self.m2.replace(",", "."))
            if self.qtd == "":
                self.qtd = 0
            else:
                self.qtd = float(self.qtd.replace(",", "."))

            if self.liq == "" and float(self.liq) >= 0:
                self.liq = 0
            else:
                self.liq = float(self.liq.replace(",", "."))

            if self.bru == "" and float(self.bru) >= 0:
                self.bru = 0
            else:
                self.bru = float(self.bru.replace(",", "."))

            if float(self.kg) < 0 or float(self.m) < 0 or float(self.m2) < 0 or float(self.qtd) < 0 or float(self.liq) < 0 or float(self.bru) < 0:
                messagebox.showerror('Erro', 'Preço inválido.')
                return
        except:
            messagebox.showerror('Erro', 'Preço inválido.')
        else:
            if self.prod == '':
                messagebox.showerror('Erro', 'Preencha os dados obrigatórios.')
            else:
                self.cursor.execute(""" UPDATE tb_produtos SET
                    servico = ?,
                    material = ?,
                    kg = ?,
                    m = ?,
                    m2 = ?,
                    unit = ?,
                    liq = ?,
                    bru = ?,
                    descricao = ?
                    WHERE cod = ?""", (self.prod, self.mat, f'{self.kg:.2f}', f'{self.m:.2f}', f'{self.m2:.2f}', f'{self.qtd:.2f}', f'{self.liq:.2f}', f'{self.bru:.2f}', self.obs, self.cod))
                self.conn.commit()
                self.disconnect_db()
                self.clean()
            row = self.selectAllProducts()
            self.treeReload(row)

    def deleteProduct(self):
        self.getEntry()
        self.msg_box = messagebox.askquestion('Deletar Produto/Serviço',
                                              'Tem certeza que deseja deletar o produto/serviço  ' + self.prod + ".")
        if self.msg_box == 'yes':
            self.connect_db()
            self.cursor.execute(""" DELETE FROM tb_produtos 
                WHERE cod = ? """, (self.cod,))
            self.conn.commit()
            self.disconnect_db()
            self.clean()
            row = self.selectAllProducts()
            self.treeReload(row)

    def searchProductbyName(self):
        self.connect_db()
        self.prod_entry.insert(END, '%')
        self.mat_entry.insert(END, '%')
        nome = self.prod_entry.get()
        mat = self.mat_entry.get
        self.cursor.execute(""" SELECT * FROM tb_produtos
            WHERE servico LIKE ? ORDER BY servico ASC """, (nome,))
        row = self.cursor.fetchall()
        self.disconnect_db()
        self.clean()

        return row

    def treeReload(self, list):
        global tree

        self.list_header = ['ID', 'Serviço', 'Material', 'R$/Kg', 'R$/M', 'R$/M²', 'R$ Unit', 'Valor Líquido', 'Valor Bruto']
        tree = ttk.Treeview(self.framedown, selectmode="extended", columns=self.list_header, show="headings")
        self.vsb = ttk.Scrollbar(self.framedown, orient="vertical", command=tree.yview)

        tree.configure(yscrollcommand=self.vsb.set)
        tree.place(relx=0.01, rely=0.10, relwidth=0.96, relheight=0.87)
        self.vsb.place(relx=0.97, rely=0.10, relwidth=0.02, relheight=0.87)

        hd = ["nw", "nw", "nw", "center", "center", "center", "center", "center", "center"]
        h = [10, 200, 150, 50, 50, 50, 50, 80, 80]
        n = 0

        for col in self.list_header:
            tree.heading(col, text=col.title(), anchor=CENTER)
            tree.column(col, width=h[n], anchor=hd[n])
            n += 1

        for item in list:
            tree.insert('', END, values=item)

        tree.bind("<ButtonRelease-1>", self.OnDoubleClick)

    @staticmethod
    def treeSelect():
        treev_data = tree.focus()
        treev_dicionario = tree.item(treev_data)
        treev_list = treev_dicionario['values']

        return treev_list

    def OnDoubleClick(self, event):
        self.clean()
        cod = self.treeSelect()
        values = self.selectProductbyId(cod[0])
        self.setEntry(values[0][0], values[0][1], values[0][2], values[0][3], values[0][4], values[0][5],
                      values[0][6], values[0][7], values[0][8], values[0][9])


class ProductsView(ProductsController):
    def __init__(self, frameup, framedown, framebar):
        self.list_cli = ttk.Treeview
        self.framedown = framedown
        self.frameup = frameup
        self.framebar = framebar
        self.setup()

    def setup(self):
        self.init_Produtos()
        self.init_tree()

    def init_Produtos(self):
        self.init_layout()
        self.init_layoutcad()
        self.init_buttons()

    def init_layout(self):
        self.bgImg = PhotoImage(file=r'assets\CARD.png')
        self.bg = Label(self.frameup, image=self.bgImg)
        self.bg.place(relx=0, rely=0, relwidth=1, height=445)

        self.bg2Img = PhotoImage(file=r'assets\CARD2.png')
        self.bg2 = Label(self.framedown, image=self.bg2Img, bg=color("background2"))
        self.bg2.place(relwidth=1, relheight=1)

        self.title = Label(self.frameup, text="Produtos", font="Ivy 18 bold", bg="#CEDCE4")
        self.title.place(relx=0.02, rely=0.005, relwidth=0.26, height= 28)

        Label(self.frameup, text="                                                 ", font="Ivy 13 bold",
              bg=color("background-bar")). \
            place(relx=0, rely=0.84, relwidth=1, relheight=0.02)

    def init_layoutcad(self):
        self.srchImg = PhotoImage(file=r"assets\procurar.png")
        self.bt_srch = Button(self.frameup, image=self.srchImg, relief='flat', background=color("background"),
                              command=self.searchProduct)
        self.bt_srch.place(relx=0.90, rely=0.1, relwidth=0.08, relheight=0.06)

        self.clrImg = PhotoImage(file=r"assets\lixo.png")
        self.bt_clr = Button(self.frameup, image=self.clrImg, relief='flat', background=color("background"),
                             command=self.clean)

        self.bt_clr.place(relx=0.90, rely=0.18, relwidth=0.08, relheight=0.06)
        self.prod = Label(self.frameup, text="Serviço:", font="Ivy 12", bg=color("background"))
        self.prod.place(relx=0.05, rely=0.08, relwidth=0.15, relheight=0.1)
        self.prod_entry = Entry(self.frameup, font="Ivy 11")
        self.prod_entry.place(relx=0.215, rely=0.1, relwidth=0.68, relheight=0.05)

        self.mat = Label(self.frameup, text="Material:", font="Ivy 12", bg=color("background"))
        self.mat.place(relx=0.05, rely=0.17, relwidth=0.15, relheight=0.1)

        self.mat_entry = Entry(self.frameup, font="Ivy 11")
        self.mat_entry.place(relx=0.215, rely=0.19, relwidth=0.68, relheight=0.05)

        self.precFrame = LabelFrame(self.frameup, text="  Precificação  ", bg=color("background"), font='Ivy 12')
        self.precFrame.place(relx=0.02, relwidth=0.96, rely=0.27, relheight=0.23)

        self.lb_Kg = Label(self.frameup, text='R$', font='Ivy 11', bg=color("background"))
        self.lb_Kg.place(relx=0.07, rely=0.34)

        self.kg_entry = Entry(self.frameup, font="Ivy 11", justify=RIGHT)
        self.kg_entry.place(relx=0.13, rely=0.34, relwidth=0.15, relheight=0.05)

        self.ckb_Kg = Label(self.frameup, text='Kg', font='Ivy 11', bg=color("background"))
        self.ckb_Kg.place(relx=0.29, rely=0.34)

        self.lb_m = Label(self.frameup, text='R$', font='Ivy 11', bg=color("background"))
        self.lb_m.place(relx=0.07, rely=0.42)

        self.m_entry = Entry(self.frameup, font="Ivy 11", justify=RIGHT)
        self.m_entry.place(relx=0.13, rely=0.42, relwidth=0.15, relheight=0.05)

        self.ckb_M = Label(self.frameup, text='M', font='Ivy 11', bg=color("background"))
        self.ckb_M.place(relx=0.29, rely=0.42)


        self.lb_qtd = Label(self.frameup, text='R$', font='Ivy 11', bg=color("background"))
        self.lb_qtd.place(relx=0.38, rely=0.34)

        self.qtd_entry = Entry(self.frameup, font="Ivy 11", justify=RIGHT)
        self.qtd_entry.place(relx=0.44, rely=0.34, relwidth=0.15, relheight=0.05)

        self.ckb_Qtd = Label(self.frameup, text='Qtd', font='Ivy 11', bg=color("background"))
        self.ckb_Qtd.place(relx=0.60, rely=0.34)

        self.lb_qtd = Label(self.frameup, text='R$', font='Ivy 11', bg=color("background"))
        self.lb_qtd.place(relx=0.38, rely=0.42)

        self.m2_entry = Entry(self.frameup, font="Ivy 11", justify=RIGHT)
        self.m2_entry.place(relx=0.44, rely=0.42, relwidth=0.15, relheight=0.05)

        self.ckb_m2 = Label(self.frameup, text='M²', font='Ivy 11', bg=color("background"))
        self.ckb_m2.place(relx=0.60, rely=0.42)


        self.lb_liq = Label(self.frameup, text='Liq:', font='Ivy 11', bg=color("background"))
        self.lb_liq.place(relx=0.70, rely=0.34)

        self.liq_entry = Entry(self.frameup, font="Ivy 11", justify=RIGHT)
        self.liq_entry.place(relx=0.78, rely=0.34, relwidth=0.12, relheight=0.05)

        self.lb_bru = Label(self.frameup, text='Bru:', font='Ivy 11', bg=color("background"))
        self.lb_bru.place(relx=0.70, rely=0.42)

        self.bru_entry = Entry(self.frameup, font="Ivy 11", justify=RIGHT)
        self.bru_entry.place(relx=0.78, rely=0.42, relwidth=0.12, relheight=0.05)

        self.lb_liq = Label(self.frameup, text='R$', font='Ivy 11', bg=color("background"))
        self.lb_liq.place(relx=0.90, rely=0.34)
        self.lb_bru = Label(self.frameup, text='R$', font='Ivy 11', bg=color("background"))
        self.lb_bru.place(relx=0.90, rely=0.42)


        self.cadobs = Label(self.frameup, text="Descrição:", font="Ivy 13", background=color("background"))
        self.cadobs.place(relx=0.02, rely=0.51)
        self.obs_entry = Text(self.frameup, font='Ivy 14')
        self.obs_entry.place(relx=0.03, rely=0.57, relwidth=0.94, relheight=0.23)

        self.cadid = Label(self.framedown, text="ID: ", font="Ivy 20", background="#CEDCE4")
        self.cadid.place(relx=0.02, rely=0.013)
        self.lb_id = Label(self.framedown, text="0", font="Ivy 20", background="#CEDCE4", justify=LEFT)
        self.lb_id.place(relx=0.07, rely=0.013)

        self.kg_entry.insert(END, "0")
        self.m_entry.insert(END, "0")
        self.m2_entry.insert(END, "0")
        self.qtd_entry.insert(END, "0")
        self.liq_entry.insert(END, "0")
        self.bru_entry.insert(END, "0")


    def init_buttons(self):

        self.insrtImg = PhotoImage(file=r"assets\INSERIR.png")
        self.bt_insert = Button(self.frameup, image=self.insrtImg, relief='flat',
                                command=self.insertProduct)
        self.bt_insert.place(relx=0.020, rely=0.88, relwidth=0.225, relheight=0.1)

        self.attImg = PhotoImage(file=r"assets\ATUALIZAR.png")
        self.bt_update = Button(self.frameup, image=self.attImg, relief='flat',
                                command=self.updateProduct)
        self.bt_update.place(relx=0.265, rely=0.88, relwidth=0.225, relheight=0.1)

        self.dltImg = PhotoImage(file=r"assets\DELETAR.png")
        self.bt_delete = Button(self.frameup, image=self.dltImg, relief='flat',
                                command=self.deleteProduct)
        self.bt_delete.place(relx=0.51, rely=0.88, relwidth=0.225, relheight=0.1)

        self.rprtImg = PhotoImage(file=r'assets\report.png')
        self.bt_report = Button(self.framebar,image=self.rprtImg, relief='flat',
                                command=self.genReport)
        self.bt_report.place(relx=0.8, rely=0.08, width=70, height=60)

        self.imprtImg = PhotoImage(file=r"assets\IMPORTAR.png")
        self.bt_import = Button(self.frameup, image=self.imprtImg, relief='flat',
                                command=self.open_csv)
        self.bt_import.place(relx=0.755, rely=0.88, relwidth=0.225, relheight=0.1)

    def init_tree(self):
        global tree
        list = self.selectAllProducts()

        self.list_header = ['ID', 'Serviço', 'Material', 'R$/Kg', 'R$/M', 'R$/M²', 'R$ Unit', 'Valor Líquido', 'Valor Bruto']
        tree = ttk.Treeview(self.framedown, selectmode="extended", columns=self.list_header, show="headings")
        self.vsb = ttk.Scrollbar(self.framedown, orient="vertical", command=tree.yview)

        tree.configure(yscrollcommand=self.vsb.set)
        tree.place(relx=0.01, rely=0.10, relwidth=0.96, relheight=0.87)
        self.vsb.place(relx=0.97, rely=0.10, relwidth=0.02, relheight=0.87)

        hd = ["nw", "nw", "nw", "center", "center", "center", "center", "center", "center"]
        h = [10, 200, 150, 50, 50, 50, 50, 80, 80]
        n = 0

        for col in self.list_header:
            tree.heading(col, text=col.title(), anchor=CENTER)
            tree.column(col, width=h[n], anchor=hd[n])
            n += 1

        for item in list:
            tree.insert('', END, values=item)

        tree.bind("<ButtonRelease-1>", self.OnDoubleClick)


    def genReport(self):
        csv_path = os.path.join(
            glv.get_variable("APP_PATH"),
            glv.get_variable("DATA_DIR"),
            "reports",
            "produtos.csv"
        )

        with open(csv_path, "w", newline='') as myfile:
            csvwriter = csv.writer(myfile, delimiter=',')
            for row in tree.get_children():
                values = (tree.item(row, 'values'))
                self.connect_db()
                self.cursor.execute(""" SELECT * FROM tb_produtos 
                    WHERE cod = ?""", (values[0],))
                row = self.cursor.fetchone()
                self.disconnect_db()
                csvwriter.writerow(row)

        os.startfile(csv_path)

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

    def open_csv(self):
        csv_path = os.path.join(
            glv.get_variable("APP_PATH"),
            glv.get_variable("DATA_DIR"),
            "catálago.csv"
        )
        self.clean()

        with open(csv_path, "rt") as f:
            reader = csv.reader(f)
            for row in reader:
                entry = row
                self.prod_entry.insert(END, entry[0])
                self.mat_entry.insert(END, entry[1])
                self.kg_entry.insert(END, entry[2])
                self.m_entry.insert(END, entry[4])
                self.m2_entry.insert(END, entry[3])
                self.qtd_entry.insert(END, entry[5])
                self.qtd_entry.insert(END, entry[6])
                self.qtd_entry.insert(END, entry[7])
                self.obs_entry.insert("1.0", entry[8])

                self.getEntry()

                self.connect_db()
                self.cursor.execute(""" INSERT INTO tb_produtos (servico, material, kg, m, m2, unit, liq, bru, descricao)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                    (self.prod, self.mat, f'{self.kg:.2f}', f'{self.m:.2f}', f'{self.m2:.2f}', f'{self.qtd:.2f}', f'{self.liq:.2f}', f'{self.bru:.2f}', self.obs))
                self.conn.commit()
                self.disconnect_db()
