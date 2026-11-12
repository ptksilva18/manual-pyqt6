# runner: ticks=40
"""Widget sob teste: calculadora de pressão hidrostática com validação e sinal de
resultado."""

import sys

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtWidgets import (
    QApplication,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QWidget,
)

RHO_PADRAO = 1030.0  # kg/m3
G = 9.80665  # m/s2


def pressao_bar(profundidade_m: float, rho: float = RHO_PADRAO) -> float:
    if profundidade_m < 0:
        raise ValueError("profundidade negativa")
    return rho * G * profundidade_m / 1e5 + 1.01325


class Calculadora(QWidget):
    calculado = pyqtSignal(float)

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("calculadora")
        self.entrada = QLineEdit(objectName="entrada")
        validador = QDoubleValidator(0.0, 11_000.0, 2)
        validador.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.entrada.setValidator(validador)
        self.botao = QPushButton("Calcular", objectName="botao")
        self.resultado = QLabel("—", objectName="resultado")
        form = QFormLayout(self)
        form.addRow("Profundidade (m)", self.entrada)
        form.addRow(self.botao)
        form.addRow("Pressão (bar)", self.resultado)
        self.botao.clicked.connect(self.calcular)
        self.entrada.returnPressed.connect(self.calcular)

    def calcular(self) -> None:
        texto = self.entrada.text().replace(",", ".")
        if not self.entrada.hasAcceptableInput():
            self.resultado.setText("entrada inválida")
            return
        p = pressao_bar(float(texto))
        self.resultado.setText(f"{p:.2f}")
        self.calculado.emit(p)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    c = Calculadora()
    c.show()
    c.entrada.setText("1350")
    c.botao.click()
    print("Demonstração:", c.resultado.text(), "bar")
