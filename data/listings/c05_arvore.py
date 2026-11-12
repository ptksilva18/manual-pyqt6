"""Árvore de objetos: pai-filho, objectName, findChild/findChildren e destroyed."""
import sys

from PyQt6.QtCore import QObject, QTimer
from PyQt6.QtWidgets import QApplication, QLineEdit, QPushButton, QVBoxLayout, QWidget


def imprimir_arvore(obj: QObject, nivel: int = 0) -> None:
    nome = obj.objectName() or "(sem nome)"
    print("  " * nivel + f"{type(obj).__name__}: {nome}")
    for filho in obj.children():
        imprimir_arvore(filho, nivel + 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = QWidget(objectName="janela")
    layout = QVBoxLayout(janela)                  # o layout passa a ser filho da janela
    layout.setObjectName("layoutPrincipal")
    for nome in ("campoVazao", "campoPressao"):
        layout.addWidget(QLineEdit(objectName=nome))
    botao = QPushButton("Calcular", objectName="botaoCalcular")
    layout.addWidget(botao)                       # addWidget reparenta para 'janela'

    imprimir_arvore(janela)
    campo = janela.findChild(QLineEdit, "campoPressao")
    print("findChild:", campo.objectName())
    campos = janela.findChildren(QLineEdit)
    print("findChildren(QLineEdit):", [w.objectName() for w in campos])

    botao.destroyed.connect(lambda: print("destroyed: botão destruído"))
    botao.deleteLater()                           # destruição segura no próximo ciclo
    QTimer.singleShot(0, lambda: print("filhos restantes:",
                                       [c.objectName() for c in janela.children()]))
    QTimer.singleShot(10, app.quit)
    app.exec()
