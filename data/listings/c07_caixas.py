"""QHBoxLayout e QVBoxLayout: margens, espaçamento, stretch e alinhamento."""
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QHBoxLayout, QLabel, QPushButton, QTextEdit, QVBoxLayout, QWidget,
)


class Editor(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Box layouts")
        externo = QVBoxLayout(self)                  # passar 'self' instala o layout
        externo.setContentsMargins(12, 12, 12, 12)   # esquerda, topo, direita, base
        externo.setSpacing(8)

        externo.addWidget(QLabel("Observações do ensaio:"))
        externo.addWidget(QTextEdit(), stretch=1)    # recebe todo o espaço vertical extra

        botoes = QHBoxLayout()
        botoes.addStretch(1)                         # empurra os botões para a direita
        botoes.addWidget(QPushButton("Salvar"))
        botoes.addWidget(QPushButton("Cancelar"))
        externo.addLayout(botoes)                    # layouts aninhados

        rodape = QLabel("Rev. 0B")
        externo.addWidget(rodape, alignment=Qt.AlignmentFlag.AlignRight)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Editor()
    w.resize(420, 300)
    w.show()
    app.processEvents()                              # força o cálculo da geometria
    te = w.findChild(QTextEdit)
    print("altura do QTextEdit com janela de 300 px:", te.height())
    w.resize(420, 500)
    app.processEvents()
    print("altura do QTextEdit com janela de 500 px:", te.height())
    sys.exit(app.exec())
