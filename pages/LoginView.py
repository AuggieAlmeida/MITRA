from tkinter import *
from lib.functions import set_window_center


class Login(Tk):
    def __init__(self, master=None):
        self.root = master
        self.root.title("MITRA")
        set_window_center(self.root, 500, 300)



# ROOT

root = Tk()

root.resizable(width=1, height=1)

# TESTS


# IMGS

IMG_BG = PhotoImage(file="../data/assets/MITRA_Login.png")
IMG_BTN = PhotoImage(file="../data/assets/ENTRAR.png")

lab_bg = Label(root, image=IMG_BG)
lab_bg.pack()

# Entry boxs

inp_login = Entry(root, bd=0, font=("Calibri", 20), justify=LEFT)
inp_login.place(width=434, height=42, x=30, y=119)

inp_pass = Entry(root, bd=0, font=("Calibri", 20), justify=LEFT)
inp_pass.place(width=220, height=42, x=30, y=218)

# Buttons

bt_login = Button(root, bd=0, image=IMG_BTN)
bt_login.place(width=144, height=63, x=320, y=208)

root.mainloop()
