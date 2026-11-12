"""Metadados, aboutToQuit e quitOnLastWindowClosed."""
import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QWidget


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("CalcEng")
    app.setOrganizationName("Engenharia")
    app.setOrganizationDomain("exemplo.com.br")
    app.setApplicationVersion("0.1.0")
    app.setApplicationDisplayName("Calculadora de Engenharia")

    app.aboutToQuit.connect(lambda: print("aboutToQuit: salvar configurações aqui"))
    print("quitOnLastWindowClosed =", app.quitOnLastWindowClosed())

    janela = QWidget()
    janela.setWindowTitle("Janela única")
    janela.show()
    print("título:", janela.windowTitle(), "|", app.applicationDisplayName())

    QTimer.singleShot(100, janela.close)   # fechar a última janela encerra o event loop
    codigo = app.exec()
    print("event loop encerrado; código =", codigo)
    return codigo


if __name__ == "__main__":
    sys.exit(main())
