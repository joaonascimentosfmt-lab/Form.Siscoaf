import os

from database import inicializar
from interface import AnalisadorSISCOAF


def main():
    inicializar()
    app = AnalisadorSISCOAF()
    icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.ico")
    if os.path.exists(icon_path):
        try:
            app.iconbitmap(icon_path)
        except Exception:
            pass
    app.mainloop()


if __name__ == "__main__":
    main()
