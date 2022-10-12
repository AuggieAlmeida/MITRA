#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
from tkinter import Tk

import lib.global_variable as glv
from pages import ClientesView, Splash

glv.init_global_variable()
glv.set_variable("APP_NAME", "MITRA")
glv.set_variable("APP_PATH", os.path.dirname(__file__))
glv.set_variable("DATA_DIR", "data")


class App(Tk):

    def __init__(self):
        Splash.Splah()
        Tk.__init__(self)

        ClientesView.Clients()

        self.mainloop()


if __name__ == "__main__":
    App()
