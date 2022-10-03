from tkinter import *
from tests import position

## ROOT

root = Tk()
root.title("MITRA")
root.geometry("500x300+610+153")
root.resizable(width=1, height=1)

## TESTS

root.bind('<Button-1>', position.start_place)
root.bind('<ButtonRelease-1>', lambda arg: position.end_place(arg, root))
root.bind('<Button-3>', lambda arg: position.para_geometry(root))

# GLOBALS

## IMGS

IMG_BG = PhotoImage(file="assets\\MITRA_Login.png")
IMG_BTN = PhotoImage(file="assets\\ENTRAR.png")

lab_bg = Label(root, image=IMG_BG)
lab_bg.pack()

## Entry boxs

inp_login = Entry(root, bd=0, font=("Calibri", 20), justify=LEFT)
inp_login.place(width=434, height=42, x=30, y=119)

inp_pass = Entry(root, bd=0, font=("Calibri", 20), justify=LEFT)
inp_pass.place(width=220, height=42, x=30, y=218)

## Buttons

bt_login = Button(root, bd=0, image=IMG_BTN)
bt_login.place(width=144, height=63, x=320, y=208)

root.mainloop()
