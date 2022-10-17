from tkinter import messagebox

from views import LoginView
from model import LoginModel
from lib.functions import set_window_center


class Login:
    def __init__(self, master):
        self.root = master
        self.view = LoginView.Login(self.root, self)

        self.root.title("MITRA - Login")
        self.root.resizable(False, False)
        self.w = 300
        self.h = 210
        set_window_center(self.root, self.w, self.h)

    @staticmethod
    def login(user, password):
        login_model = LoginModel.LoginModel()
        if user == login_model.txt_login and password == login_model.txt_pass:
            messagebox.showinfo('Login', 'Login efetuado com sucesso!')
            return True
        else:
            messagebox.showwarning('Erro', 'Usuário ou senha incorretos!')
            return False