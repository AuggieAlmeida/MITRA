import sqlite3
import os
from tkinter import *
from tkinter import ttk, messagebox

from components import menubar
from views import ClientesView, ComercialView, ProdutosView, FluxoView

from lib.colours import color
from lib.functions import set_window_center
import lib.global_variable as glv
from database import db


glv.init_global_variable()
glv.set_variable("APP_NAME", "MITRA")
glv.set_variable("APP_PATH", os.path.dirname(__file__))
glv.set_variable("DATA_DIR", "database")

root = Tk()


class GradientFrame(Canvas):
    def __init__(self, parent, color1=color("background"), color2="#e0eaef", **kwargs):
        Canvas.__init__(self, parent, **kwargs)
        self._color1 = color1
        self._color2 = color2
        self.bind("<Configure>", self._drawgradient)

    def _drawgradient(self, event = None):
        self.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()
        limit = width
        (r1, g1, b1) = self.winfo_rgb(self._color1)
        (r2, g2, b2) = self.winfo_rgb(self._color2)
        r_ratio = float(r2-r1)/limit
        g_ratio = float(g1-g2)/limit
        b_ratio = float(b2-b1)/limit

        for i in range(limit):
            nr = int(r1 + (r_ratio * i))
            ng = int(r1 + (g_ratio * i))
            nb = int(r1 + (b_ratio * i))
            color = "#%4.4x%4.4x%4.4x" % (nr, ng, nb)
            self.create_line(i, 0, i, height, tags=("gradient"), fill=color)
        self.lower("gradient")


class App:
    def __init__(self):
        self.root = root
        self.home()
        menubar.init_bar(self.root)
        db.Database().struct_db()
        self.frames()
        self.menu_buttons()
        self.init_home()
        root.mainloop()

    def home(self):
        self.root.title("Sacomã Persianas")
        self.root.configure(background=color("background2"))
        set_window_center(self.root, 1260, 680)
        self.root.resizable(False, False)
        self.root.bind("<B3-Motion>", self.move_app)
        self.root.iconbitmap('assets\icon.ico')

    def move_app(self, e):
        self.root.geometry(f'+{e.x_root - 630}+{e.y_root - 340}')

    def frames(self):
        self.frameupleft = GradientFrame(self.root)
        self.frameupleft.place(relx=0.005, rely=0.1, width=430, height=70)

        self.framedownleft = Frame(self.root, background=color("background"))
        self.framedownleft.place(relx=0.005, rely=0.21, width=430, height=528)

        self.frameright = Frame(self.root, background=color("background"))
        self.frameright.place(relx=0.352, rely=0.1, width=810, height=606)

        self.framebar = Frame(self.root)
        self.framebar.place(relx=0, rely=0, relwidth=1, height=60)

    def init_home(self):
        self.reset_page()
        self.init_layout()
        self.init_reports()
        self.init_lists()

    def init_clientes(self):
        self.reset_page()
        ClientesView.ClientsView(self.framedownleft, self.frameright, self.frameupleft)

    def init_comercial(self):
        self.reset_page()
        ComercialView.ComercialView(self.framedownleft, self.frameright, self.frameupleft)

    def init_produtos(self):
        self.reset_page()
        ProdutosView.ProductsView(self.framedownleft, self.frameright, self.frameupleft)

    def init_fluxo(self):
        self.reset_page()
        FluxoView.FluxoView(self.framedownleft, self.frameright, self.frameupleft)

    def connect_db(self):
        db_path = os.path.join(
            glv.get_variable("APP_PATH"),
            "SPDB.db"
        )
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def disconnect_db(self):
        self.conn.close()

    def reset_page(self):
        for widget in self.frameupleft.winfo_children():
            widget.destroy()
        for widget in self.framedownleft.winfo_children():
            widget.destroy()
        for widget in self.frameright.winfo_children():
            widget.destroy()

    def menu_buttons(self):
        self.barImg = PhotoImage(file=r'assets\BAR.png')
        self.bar = Label(self.framebar, image=self.barImg)
        self.bar.place(relx=0, rely=0, relwidth=1, height=60)

        self.homeImg = PhotoImage(file=r'assets\1.png')
        self.btnHome = Button(self.framebar,image=self.homeImg, relief='flat', command=self.init_home)
        self.btnHome.place(x=740, rely=0, width=70, height=60)

        self.clientsImg = PhotoImage(file=r'assets\2.png')
        self.btnclients = Button(self.framebar,image=self.clientsImg, relief='flat', command=self.init_clientes)
        self.btnclients.place(x=820, rely=0, width=70, height=60)

        self.ordersImg = PhotoImage(file=r'assets\3.png')
        self.btnorders = Button(self.framebar, image=self.ordersImg, relief='flat', command=self.init_comercial)
        self.btnorders.place(x=900, rely=0, width=70, height=60)

        self.productsImg = PhotoImage(file=r'assets\4.png')
        self.btnproducts = Button(self.framebar,image=self.productsImg, relief='flat', command=self.init_produtos)
        self.btnproducts.place(x=980, rely=0, width=70, height=60)

        self.fluxImg = PhotoImage(file=r'assets\5.png')
        self.btnflux = Button(self.framebar,image=self.fluxImg, relief='flat', command=self.init_fluxo)
        self.btnflux.place(x=1060, rely=0, width=70, height=60)

        self.configImg = PhotoImage(file=r'assets\6.png')
        self.btnconfig = Button(self.framebar,image=self.configImg, relief='flat', command=self.root.destroy)
        self.btnconfig.place(x=1180, rely=0, width=70, height=60)

    def init_layout(self):
        self.bgImg = PhotoImage(file=r'assets\CARD.png')
        self.bg = Label(self.framedownleft, image=self.bgImg)
        self.bg.place(relx=0, rely=0, relwidth=1, height=445)

        self.bg2Img = PhotoImage(file=r'assets\CARD2.png')
        self.bg2 = Label(self.frameright, image=self.bg2Img, bg=color("background2"))
        self.bg2.place(relwidth=1, relheight=1)

        self.title = Label(self.framedownleft, text="Home", font="Ivy 18 bold", bg="#CEDCE4")
        self.title.place(relx=0.008, rely=0.005, relwidth=0.20, height= 28)

        self.text = Label(self.frameright, text="Administrativo", font="Ivy 20 bold", bg="#CEDCE4")
        self.text.place(relx=0.01, rely=0.018, relwidth=0.3, relheight=0.05)


        self.logoImg = PhotoImage(file=r'assets\LOGO.PNG')
        self.logo = Label(self.framedownleft, image=self.logoImg, background=color("background"))
        self.logo.place(x=0, y=39, relwidth=1, height=390)


        Label(self.framedownleft, text="                                                 ", font="Ivy 13 bold",
              bg=color("background-bar")). \
            place(relx=0, rely=0.84, relwidth=1, relheight=0.02)

    def init_reports(self):
        self.connect_db()
        self.cursor.execute("SELECT count(*) FROM tb_clientes")
        clients = self.cursor.fetchone()
        self.cursor.execute("SELECT count(*) FROM tb_comercial WHERE tipo = 'orçamento'")
        budgets = self.cursor.fetchone()
        self.cursor.execute("SELECT count(*) FROM tb_comercial WHERE tipo = 'venda'")
        sales = self.cursor.fetchone()
        self.cursor.execute("SELECT count(*) FROM tb_comercial WHERE tipo = 'ordem'")
        orders = self.cursor.fetchone()
        self.cursor.execute("SELECT count(*) FROM tb_produtos")
        prod = self.cursor.fetchone()
        self.disconnect_db()

        self.framereport = LabelFrame(self.frameright, bg=color("background"))
        self.framereport.place(relx=0.02, rely=0.1, relwidth=0.96, relheight=0.3)

        self.lb_bud = Label(self.framereport, text=budgets[0], font=('Arial', 40, 'bold'), bg=color("background"),
                            anchor='center')
        self.lb_bud.place(relx=0, rely=0.3, relwidth=0.3, relheight=0.69)
        self.lb_bud = Label(self.framereport, text='Orçamentos cadastrados', font=('Arial', 13, 'bold'),
                            bg=color("background"), anchor='center')
        self.lb_bud.place(relx=0, rely=0.15, relwidth=0.3, relheight=0.1)

        self.lb_sal = Label(self.framereport, text=sales[0], font=('Arial', 40, 'bold'), bg=color("background"),
                            anchor='center')
        self.lb_sal.place(relx=0.365, rely=0.3, relwidth=0.3, relheight=0.69)
        self.lb_sal = Label(self.framereport, text='Vendas cadastradas', font=('Arial', 13, 'bold'),
                            bg=color("background"), anchor='center')
        self.lb_sal.place(relx=0.365, rely=0.15, relwidth=0.3, relheight=0.1)

        self.lb_ord = Label(self.framereport, text=orders[0], font=('Arial', 40, 'bold'), bg=color("background"),
                            anchor='center')
        self.lb_ord.place(relx=0.7, rely=0.3, relwidth=0.3, relheight=0.69)
        self.lb_ord = Label(self.framereport, text='Ordens de serviço\ncadastradas', font=('Arial', 13, 'bold'),
                            bg=color("background"), anchor='center')
        self.lb_ord.place(relx=0.70, rely=0.15, relwidth=0.3, relheight=0.2)

        self.framereport2 = LabelFrame(self.frameright, bg=color("background"))
        self.framereport2.place(relx=0.02, rely=0.45, relwidth=0.35, relheight=0.5)

        self.lb_clients = Label(self.framereport2, text=clients[0], font=('Arial', 40, 'bold'), bg=color("background"),
                                anchor='center')
        self.lb_clients.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.4)
        self.lb_clients = Label(self.framereport2, text='Clientes cadastrados', font=('Arial', 13, 'bold'),
                                bg=color("background"), anchor='center')
        self.lb_clients.place(relx=0.1, rely=0.03, relwidth=0.8, relheight=0.2)

        self.lb_products = Label(self.framereport2, text=prod[0], font=('Arial', 40, 'bold'), bg=color("background"),
                                 anchor='center')
        self.lb_products.place(relx=0.3, rely=0.6, relwidth=0.4, relheight=0.4)
        self.lb_products = Label(self.framereport2, text='Produtos cadastrados', font=('Arial', 13, 'bold'),
                                 bg=color("background"), anchor='center')
        self.lb_products.place(relx=0.195, rely=0.53, relwidth=0.62, relheight=0.2)

    def init_lists(self):

        self.connect_db()
        self.cursor.execute(""" SELECT * FROM info """)
        row = self.cursor.fetchone()
        self.disconnect_db()

        self.framereport3 = LabelFrame(self.frameright, bg=color("background"))
        self.framereport3.place(relx=0.40, rely=0.45, relwidth=0.58, relheight=0.5)

        self.configure = ttk.Notebook(self.framereport3)

        self.tabAcc = Frame(self.configure, background=color("background"))
        self.tabEnt = Frame(self.configure, background=color("background"))
        self.tabLoc = Frame(self.configure, background=color("background"))
        self.tabPag = Frame(self.configure, background=color("background"))
        self.configure.add(self.tabEnt, text="  Dados da Empresa  ")
        self.configure.add(self.tabAcc, text="  Dados Bancários  ")
        self.configure.add(self.tabLoc, text="  Dados Adicionais  ")
        self.configure.place(x=0, y=0, relheight=1, relwidth=1)

        self.addImg = PhotoImage(file=r'assets\ATUALIZAR.png')

        ## TAB EMPRESA

        self.lb_enter = Label(self.tabEnt, text="Empresa:", font=("Ivy", 14, "bold"), bg=color("background"))
        self.lb_enter.place(relx=0.023, rely=0.15, relwidth=0.2)
        self.enter_entry = Entry(self.tabEnt, font=("Ivy", 14))
        self.enter_entry.place(relx=0.25, rely=0.15, relwidth=0.70, relheight=0.1)
        self.enter_entry.insert(END, row[1])

        self.lb_title = Label(self.tabEnt, text="Título:", font=("Ivy", 14, "bold"), bg=color("background"))
        self.lb_title.place(relx=0.065, rely=0.35, relwidth=0.18)
        self.title_entry = Entry(self.tabEnt, font=("Ivy", 14))
        self.title_entry.place(relx=0.25, rely=0.35, relwidth=0.70, relheight=0.1)
        self.title_entry.insert(END, row[2])

        self.lb_cnpj = Label(self.tabEnt, text="CNPJ:", font=("Ivy", 14, "bold"), bg=color("background"))
        self.lb_cnpj.place(relx=0.054, rely=0.55, relwidth=0.2)
        self.cnpj_entry = Entry(self.tabEnt, font=("Ivy", 14))
        self.cnpj_entry.place(relx=0.25, rely=0.55, relwidth=0.40, relheight=0.1)
        self.cnpj_entry.insert(END, row[3])


        self.lb_ie = Label(self.tabEnt, text="IE:", font=("Ivy", 14, "bold"), bg=color("background"))
        self.lb_ie.place(relx=0.077, rely=0.75, relwidth=0.23)
        self.ie_entry = Entry(self.tabEnt, font=("Ivy", 14))
        self.ie_entry.place(relx=0.25, rely=0.75, relwidth=0.4, relheight=0.1)
        self.ie_entry.insert(END, row[4])

        self.btn_addEnt = Button(self.tabEnt, image=self.addImg, relief='flat',
                                     command=self.addEmpresa)
        self.btn_addEnt.place(relx=0.7, rely=0.68, width=98, height=50)

        ## TAB BANCO

        self.lb_pix = Label(self.tabAcc, text="Pix:", font=("Ivy", 14, "bold"), bg=color("background"))
        self.lb_pix.place(relx=0.079, rely=0.15, relwidth=0.2)
        self.pix_entry = Entry(self.tabAcc, font=("Ivy", 14))
        self.pix_entry.place(relx=0.25, rely=0.15, relwidth=0.70, relheight=0.1)
        self.pix_entry.insert(END, row[5])

        self.lb_bank = Label(self.tabAcc, text="Banco:", font=("Ivy", 14, "bold"), bg=color("background"))
        self.lb_bank.place(relx=0.049, rely=0.35, relwidth=0.2)
        self.bank_entry = Entry(self.tabAcc, font=("Ivy", 14))
        self.bank_entry.place(relx=0.25, rely=0.35, relwidth=0.30, relheight=0.1)
        self.bank_entry.insert(END, row[6])

        self.lb_account = Label(self.tabAcc, text="Conta:", font=("Ivy", 14, "bold"), bg=color("background"))
        self.lb_account.place(relx=0.07, rely=0.55, relwidth=0.18)
        self.account_entry = Entry(self.tabAcc, font=("Ivy", 14))
        self.account_entry.place(relx=0.25, rely=0.55, relwidth=0.30, relheight=0.1)
        self.account_entry.insert(END, row[7])

        self.lb_agency = Label(self.tabAcc, text="Agência:", font=("Ivy", 14, "bold"), bg=color("background"))
        self.lb_agency.place(relx=0.048, rely=0.75, relwidth=0.18)
        self.agency_entry = Entry(self.tabAcc, font=("Ivy", 14))
        self.agency_entry.place(relx=0.25, rely=0.75, relwidth=0.30, relheight=0.1)
        self.agency_entry.insert(END, row[8])

        self.btn_addAccount = Button(self.tabAcc, image=self.addImg, relief='flat',
                                     command=self.addConta)
        self.btn_addAccount.place(relx=0.7, rely=0.68, width=98, height=50)

        ## TAB LOCAL

        self.lb_email = Label(self.tabLoc, text="Email:", font=("Ivy", 13, "bold"), bg=color("background"))
        self.lb_email.place(relx=0.05, rely=0.1, relwidth=0.2)
        self.email_entry = Entry(self.tabLoc, font=("Ivy", 14))
        self.email_entry.place(relx=0.25, rely=0.1, relwidth=0.70, relheight=0.1)
        self.email_entry.insert(END, row[9])

        self.lb_ctt = Label(self.tabLoc, text="Telefone:", font=("Ivy", 13, "bold"), bg=color("background"))
        self.lb_ctt.place(relx=0.07, rely=0.25, relwidth=0.18)
        self.ctt_entry = Entry(self.tabLoc, font=("Ivy", 14))
        self.ctt_entry.place(relx=0.25, rely=0.25, relwidth=0.7, relheight=0.1)
        self.ctt_entry.insert(END, row[10])

        self.lb_end = Label(self.tabLoc, text="Endereço:", font=("Ivy", 13, "bold"), bg=color("background"))
        self.lb_end.place(relx=0.05, rely=0.50, relwidth=0.2)
        self.end_entry = Entry(self.tabLoc, font=("Ivy", 14))
        self.end_entry.place(relx=0.25, rely=0.5, relwidth=0.70, relheight=0.1)
        self.end_entry.insert(END, row[11])

        self.lb_loc = Label(self.tabLoc, text="Localidade:", font=("Ivy", 13, "bold"), bg=color("background"))
        self.lb_loc.place(relx=0.045, rely=0.65, relwidth=0.2)
        self.loc_entry = Entry(self.tabLoc, font=("Ivy", 14))
        self.loc_entry.place(relx=0.25, rely=0.65, relwidth=0.30, relheight=0.1)
        self.loc_entry.insert(END, row[12])

        self.lb_cep = Label(self.tabLoc, text="CEP:", font=("Ivy", 14, "bold"), bg=color("background"))
        self.lb_cep.place(relx=0.045, rely=0.8, relwidth=0.18)
        self.cep_entry = Entry(self.tabLoc, font=("Ivy", 14))
        self.cep_entry.place(relx=0.25, rely=0.8, relwidth=0.30, relheight=0.1)
        self.cep_entry.insert(END, row[13])

        self.btn_addLoc = Button(self.tabLoc, image=self.addImg, relief='flat',
                                     command=self.addDados)
        self.btn_addLoc.place(relx=0.7, rely=0.68, width=98, height=50)

    def addEmpresa(self):
        self.empresa = self.enter_entry.get()
        self.title = self.title_entry.get()
        self.cnpj = self.cnpj_entry.get()
        self.ie = self.ie_entry.get()
        self.connect_db()
        self.cursor.execute(""" UPDATE info SET
                empresa = ?, 
                titulo = ?, 
                cnpj = ?, 
                ie = ?
                WHERE cod = 1""",
                            (self.empresa, self.title, self.cnpj, self.ie))
        self.conn.commit()
        messagebox.showinfo('Empresa', 'Dados da empresa registrados com sucesso.')
        self.disconnect_db()

    def addConta(self):
        self.pix = self.pix_entry.get()
        self.banco = self.bank_entry.get()
        self.conta = self.account_entry.get()
        self.agencia = self.agency_entry.get()
        self.connect_db()
        self.cursor.execute(""" UPDATE info SET
                pix = ?, 
                banco = ?, 
                conta = ?, 
                agencia = ?
                WHERE cod = 1""",
                            (self.pix, self.banco, self.conta, self.agencia))
        self.conn.commit()
        messagebox.showinfo('Empresa', 'Dados da empresa registrados com sucesso.')
        self.disconnect_db()

    def addDados(self):
        self.email = self.email_entry.get()
        self.ctt = self.ctt_entry.get()
        self.end = self.end_entry.get()
        self.loc = self.loc_entry.get()
        self.cep = self.cep_entry.get()
        self.connect_db()
        self.cursor.execute(""" UPDATE info SET
                email = ?, 
                ctt = ?, 
                end = ?, 
                loc = ?,
                cep = ?
                WHERE cod = 1""",
                            (self.email, self.ctt, self.end, self.loc, self.cep))
        self.conn.commit()
        messagebox.showinfo('Empresa', 'Dados da empresa registrados com sucesso.')
        self.disconnect_db()



App()
