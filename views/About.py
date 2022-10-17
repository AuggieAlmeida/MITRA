from tkinter import Tk, Label, Message

from lib.functions import set_window_center
from lib.global_variable import get_variable


class About(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Sobre")
        self.app_name = get_variable("APP_NAME")
        self.app_version = "0.1.1"
        self.app_url = ""
        self.resizable(False, False)
        self.init_page()

    def init_page(self):
        Label(self, text="MITRA").pack(fill="both")
        Label(self, text=self.app_name).pack()
        Label(self, text=self.app_version).pack()
        Label(self,)
