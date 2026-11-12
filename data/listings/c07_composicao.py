"""Composição com layouts aninhados (usada para a Figura 7.2)."""
import sys

from PyQt6.QtWidgets import (
    QApplication, QComboBox, QDoubleSpinBox, QFormLayout, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget,
)


class CalculoTubo(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Verificação de tubo — layouts aninhados")
        raiz = QVBoxLayout(self)                               # 1) coluna principal

        dados = QGroupBox("Dados de entrada")
        form = QFormLayout(dados)                              # 2) formulário
        self.od = QDoubleSpinBox(maximum=2000.0, suffix=" mm", value=273.1)
        self.t = QDoubleSpinBox(maximum=100.0, suffix=" mm", value=12.7)
        self.smys = QDoubleSpinBox(maximum=1000.0, suffix=" MPa", value=448.0)
        grau = QComboBox()
        grau.addItems(["API 5L X52", "API 5L X65", "API 5L X70"])
        grau.setCurrentIndex(1)
        form.addRow("Diâmetro externo (OD):", self.od)
        form.addRow("Espessura (t):", self.t)
        form.addRow("Grau do aço:", grau)
        form.addRow("SMYS:", self.smys)
        raiz.addWidget(dados)

        resultados = QGroupBox("Resultados")
        grade = QGridLayout(resultados)                        # 3) grade de resultados
        linhas = (("D/t", "21.50"), ("Diâmetro interno", "247.7 mm"),
                  ("Pressão de escoamento*", "41.7 MPa"))
        for i, (nome, valor) in enumerate(linhas):
            grade.addWidget(QLabel(nome + ":"), i, 0)
            grade.addWidget(QLabel(f"<b>{valor}</b>"), i, 1)
        grade.addWidget(QLabel("<i>* Barlow: P = 2·SMYS·t/OD</i>"), 3, 0, 1, 2)
        raiz.addWidget(resultados)

        botoes = QHBoxLayout()                                 # 4) linha de botões
        botoes.addStretch()
        botoes.addWidget(QPushButton("Calcular"))
        botoes.addWidget(QPushButton("Exportar…"))
        raiz.addLayout(botoes)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = CalculoTubo()
    w.show()
    od, t, smys = w.od.value(), w.t.value(), w.smys.value()
    print(f"D/t = {od / t:.2f}; DI = {od - 2 * t:.1f} mm;",
          f"P = {2 * smys * t / od:.1f} MPa")
    sys.exit(app.exec())
