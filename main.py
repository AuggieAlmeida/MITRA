#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
from tkinter import Tk

import lib.global_variable as glv
from views import Splash
from routes import routes as rt

glv.init_global_variable()
glv.set_variable("APP_NAME", "MITRA")
glv.set_variable("APP_PATH", os.path.dirname(__file__))
glv.set_variable("DATA_DIR", "data")


class Initials(Tk):
    def __init__(self):
        rt.EventHandler("Splash", self)
        Tk.__init__(self)
        Splash.Splash(self)
        self.mainloop()


class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        rt.ClientesView.Clients(self)
        self.mainloop()


if __name__ == "__main__":
    Initials()

