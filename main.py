from database import inicializar
from interface import AnalisadorSISCOAF


def main():
    inicializar()
    app = AnalisadorSISCOAF()
    app.mainloop()


if __name__ == "__main__":
    main()
