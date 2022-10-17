from tkinter import Tk
from views import Splash

from lib.functions import set_window_center


class Splash:
    def __init__(self, master):
        self.view = Splash.Splash(master)
        self.w = 300
        self.h = 300
        set_window_center(self.root, self.w, self.h)
        self.root.title("MITRA")
        self.root.resizable(False, False)
