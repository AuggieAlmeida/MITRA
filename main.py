import os
from tkinter import *

from components import menubar
from views import HomePage, ClientesView, ComercialView, ProdutosView

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
        self.init_clientes()
        root.mainloop()

    def home(self):
        self.root.title("Sacomã Persianas")
        self.root.configure(background=color("background2"))
        set_window_center(self.root, 1260, 680)
        self.root.resizable(False, False)

        self.root.iconbitmap('assets\icon.ico')

    def frames(self):
        self.frameupleft = GradientFrame(self.root)
        self.frameupleft.place(relx=0.005, rely=0.1, width=430, height=70)

        self.framedownleft = Frame(self.root, background=color("background"))
        self.framedownleft.place(relx=0.005, rely=0.21, width=430, height=528)

        self.frameright = Frame(self.root, background=color("background"))
        self.frameright.place(relx=0.352, rely=0.1, width=810, height=606)

        self.framebar = Frame(self.root)
        self.framebar.place(relx=0, rely=0, relwidth=1, height=60)

    def init_clientes(self):
        self.reset_page()
        ClientesView.ClientsView(self.framedownleft, self.frameright, self.frameupleft)

    def init_home(self):
        self.reset_page()
        HomePage.HomePage(self.framedownleft, self.frameright, self.frameupleft)

    def init_comercial(self):
        self.reset_page()
        ComercialView.ComercialView(self.framedownleft, self.frameright, self.frameupleft)

    def init_produtos(self):
        self.reset_page()
        ProdutosView.ProductsView(self.framedownleft, self.frameright, self.frameupleft)

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
        self.btnflux = Button(self.framebar,image=self.fluxImg, relief='flat', command=self.reset_page)
        self.btnflux.place(x=1060, rely=0, width=70, height=60)

        self.configImg = PhotoImage(file=r'assets\6.png')
        self.btnconfig = Button(self.framebar,image=self.configImg, relief='flat', command=self.root.destroy)
        self.btnconfig.place(x=1180, rely=0, width=70, height=60)


App()
