"""Botões checáveis, QButtonGroup exclusivo e QDialogButtonBox."""
import sys

from PyQt6.QtWidgets import (
    QApplication, QButtonGroup, QDialogButtonBox, QPushButton, QRadioButton, QVBoxLayout,
    QWidget,
)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = QWidget()
    lay = QVBoxLayout(janela)

    grupo = QButtonGroup(janela)              # exclusivo por padrão
    for ident, texto in enumerate(["SI", "Imperial", "Petroleiro"]):
        rb = QRadioButton(texto)
        lay.addWidget(rb)
        grupo.addButton(rb, ident)            # id inteiro associado ao botão
    grupo.idClicked.connect(lambda i: print("sistema de unidades id =", i))
    grupo.button(0).setChecked(True)
    grupo.button(2).click()
    print("marcado:", grupo.checkedButton().text())

    alternar = QPushButton("Modo edição", checkable=True)
    alternar.toggled.connect(
        lambda on: print("modo edição:", "ligado" if on else "desligado"))
    lay.addWidget(alternar)
    alternar.click()
    alternar.click()

    caixa = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok
                             | QDialogButtonBox.StandardButton.Cancel)
    caixa.accepted.connect(lambda: print("accepted"))
    caixa.rejected.connect(lambda: print("rejected"))
    lay.addWidget(caixa)
    caixa.button(QDialogButtonBox.StandardButton.Ok).click()
