"""Galeria dos widgets fundamentais (usada para a Figura 6.1)."""
import sys

from PyQt6.QtCore import QDate, Qt
from PyQt6.QtWidgets import (
    QApplication, QCheckBox, QComboBox, QDateEdit, QDial, QDoubleSpinBox, QFormLayout,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLCDNumber, QLineEdit, QProgressBar,
    QPushButton, QRadioButton, QSlider, QSpinBox, QTextEdit, QToolButton, QVBoxLayout,
    QWidget,
)


class Galeria(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Galeria de widgets")
        grade = QGridLayout(self)

        exibicao = QGroupBox("Exibição")
        f1 = QVBoxLayout(exibicao)
        f1.addWidget(QLabel("QLabel com <b>rich text</b>"))
        lcd = QLCDNumber(5)
        lcd.display(345.7)
        f1.addWidget(lcd)
        barra = QProgressBar()
        barra.setValue(65)
        f1.addWidget(barra)

        botoes = QGroupBox("Botões")
        f2 = QVBoxLayout(botoes)
        f2.addWidget(QPushButton("QPushButton"))
        linha = QHBoxLayout()
        linha.addWidget(QToolButton(text="…"))
        linha.addWidget(QCheckBox("QCheckBox", checked=True))
        f2.addLayout(linha)
        f2.addWidget(QRadioButton("QRadioButton", checked=True))
        f2.addWidget(QRadioButton("Outra opção"))

        entrada = QGroupBox("Entrada de dados")
        f3 = QFormLayout(entrada)
        f3.addRow("QLineEdit:", QLineEdit(placeholderText="tag do equipamento"))
        f3.addRow("QSpinBox:", QSpinBox(value=12, suffix=" un"))
        dsb = QDoubleSpinBox(decimals=2, maximum=1000.0, suffix=" bar")
        dsb.setValue(206.84)
        f3.addRow("QDoubleSpinBox:", dsb)
        combo = QComboBox()
        combo.addItems(["Aço carbono", "Inox 316L", "Duplex 2205"])
        f3.addRow("QComboBox:", combo)
        f3.addRow("QDateEdit:", QDateEdit(QDate(2026, 11, 11), calendarPopup=True,
                                          displayFormat="dd/MM/yyyy"))

        faixa = QGroupBox("Faixa e texto")
        f4 = QVBoxLayout(faixa)
        s = QSlider(Qt.Orientation.Horizontal)
        s.setValue(40)
        f4.addWidget(s)
        dial = QDial(notchesVisible=True)
        dial.setValue(30)
        dial.setFixedHeight(60)
        f4.addWidget(dial)
        te = QTextEdit()
        te.setPlainText("QTextEdit: texto multilinha\ncom edição livre.")
        te.setFixedHeight(60)
        f4.addWidget(te)

        grade.addWidget(exibicao, 0, 0)
        grade.addWidget(botoes, 0, 1)
        grade.addWidget(entrada, 1, 0)
        grade.addWidget(faixa, 1, 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    g = Galeria()
    g.show()
    print("widgets na galeria:", len(g.findChildren(QWidget)))
    sys.exit(app.exec())
