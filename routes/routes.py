from views import ClientesView
from controller import LoginController, SplashController


def EventHandler(view, root):
    if view == "Clientes":
        ClientesView.Clients(root)
    if view == "Login":
        LoginController.Login(root)
    if view == "Splash":
        SplashController.Splash(root)


