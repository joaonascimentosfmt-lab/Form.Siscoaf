import os
import customtkinter as ctk

from database import inicializar
from interface import AnalisadorSISCOAF, LoginWindow


def main():
    inicializar()

    root = ctk.CTk()
    root.withdraw()

    usuario = {"login": "", "role": "", "serventia": ""}

    def _iniciar_app(login: str, role: str = "admin", serventia: str = "Ambos"):
        usuario["login"] = login
        usuario["role"] = role
        usuario["serventia"] = serventia
        root.destroy()
        app = AnalisadorSISCOAF(usuario=login, role=role, serventia=serventia)
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.ico")
        if os.path.exists(icon_path):
            try:
                app.iconbitmap(icon_path)
            except Exception:
                pass
        app.mainloop()

    login = LoginWindow(on_success=_iniciar_app)
    login.mainloop()


if __name__ == "__main__":
    main()
