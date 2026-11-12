# runner: ticks=40
"""Widget under test: hydrostatic pressure calculator with validation and a result
signal."""

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

DEFAULT_RHO = 1030.0  # kg/m3
G = 9.80665  # m/s2


def pressure_bar(depth_m: float, rho: float = DEFAULT_RHO) -> float:
    if depth_m < 0:
        raise ValueError("negative depth")
    return rho * G * depth_m / 1e5 + 1.01325


class Calculator(QWidget):
    computed = pyqtSignal(float)

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("calculator")
        self.entry = QLineEdit(objectName="entry")
        validator = QDoubleValidator(0.0, 11_000.0, 2)
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.entry.setValidator(validator)
        self.button = QPushButton("Compute", objectName="button")
        self.result = QLabel("—", objectName="result")
        form = QFormLayout(self)
        form.addRow("Depth (m)", self.entry)
        form.addRow(self.button)
        form.addRow("Pressure (bar)", self.result)
        self.button.clicked.connect(self.compute)
        self.entry.returnPressed.connect(self.compute)

    def compute(self) -> None:
        text = self.entry.text().replace(",", ".")
        if not self.entry.hasAcceptableInput():
            self.result.setText("invalid input")
            return
        p = pressure_bar(float(text))
        self.result.setText(f"{p:.2f}")
        self.computed.emit(p)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    c = Calculator()
    c.show()
    c.entry.setText("1350")
    c.button.click()
    print("Demonstration:", c.result.text(), "bar")
