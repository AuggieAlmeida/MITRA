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


class HomeController:
    def __init__(self):
        pass

class HomePage(HomeController):

    def __init__(self, frameup, framedown, framebar):
        self.framedown = framedown
        self.frameup = frameup
        self.framebar = framebar
        self.setup()

    def setup(self):
        self.init_Home()

    def init_Home(self):
        self.init_layout()
        self.init_buttons()

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

    def init_buttons(self):

        self.clrImg = PhotoImage(file=r"assets\lixo.png")
        self.bt_limpar = Button(self.frameup, image=self.clrImg, bg=color("background"), relief='flat')
        self.bt_limpar.place(relx=0.88, rely=0.07, relwidth=0.08, relheight=0.07)

        self.rprtImg = PhotoImage(file=r'assets\report.png')
        self.bt_report = Button(self.framebar,image=self.rprtImg, relief='flat')
        self.bt_report.place(relx=0.8, rely=0.08, width=70, height=60)

        self.insrtImg = PhotoImage(file=r"assets\INSERIR.png")
        self.bt_insert = Button(self.frameup, image=self.insrtImg, relief='flat')
        self.bt_insert.place(relx=0.020, rely=0.88, relwidth=0.225, relheight=0.1)

        self.attImg = PhotoImage(file=r"assets\ATUALIZAR.png")
        self.bt_update = Button(self.frameup, image=self.attImg, relief='flat')
        self.bt_update.place(relx=0.265, rely=0.88, relwidth=0.225, relheight=0.1)

        self.dltImg = PhotoImage(file=r"assets\DELETAR.png")
        self.bt_delete = Button(self.frameup, image=self.dltImg, relief='flat')
        self.bt_delete.place(relx=0.51, rely=0.88, relwidth=0.225, relheight=0.1)

        self.imprtImg = PhotoImage(file=r"assets\IMPORTAR.png")
        self.bt_import = Button(self.frameup, image=self.imprtImg, relief='flat')
        self.bt_import.place(relx=0.755, rely=0.88, relwidth=0.225, relheight=0.1)

    def init_lists(self):
        pass

