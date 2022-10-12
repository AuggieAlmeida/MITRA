import tkinter.messagebox
from tkinter import Button, Label, Tk

from lib.functions import set_window_center
from main import App


class InitWindow(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.title("MITRA")
        set_window_center(self, 300, 180)
        self.resizable(False, False)
        self.win_success = None
        self.init_page()


if __name__ == "__main__":
    APP_INIT = InitWindow()
    APP_INIT.mainloop()
