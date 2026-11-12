"""Janela principal como subclasse de QMainWindow."""
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow


class JanelaPrincipal(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Calculadora de Engenharia")
        self.resize(640, 400)
        self.setMinimumSize(480, 300)

        rotulo = QLabel("Área de trabalho")
        rotulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(rotulo)          # QMainWindow exige um widget central

        self.statusBar().showMessage("Pronto")  # cria a barra de status sob demanda


def main() -> int:
    app = QApplication(sys.argv)
    janela = JanelaPrincipal()
    janela.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
