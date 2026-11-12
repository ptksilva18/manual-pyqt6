"""Synchronizing QSlider and QDoubleSpinBox; QComboBox with associated data."""
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QComboBox, QDoubleSpinBox, QHBoxLayout, QSlider, QWidget,
)


class OpeningControl(QWidget):
    """Integer slider (0–1000) mapped to 0.0–100.0 % in the spin box."""

    def __init__(self) -> None:
        super().__init__()
        self.slider = QSlider(Qt.Orientation.Horizontal, minimum=0, maximum=1000)
        self.spin = QDoubleSpinBox(minimum=0.0, maximum=100.0, decimals=1, suffix=" %")
        self.spin.setSingleStep(0.5)
        lay = QHBoxLayout(self)
        lay.addWidget(self.slider)
        lay.addWidget(self.spin)
        self.slider.valueChanged.connect(lambda v: self.spin.setValue(v / 10))
        self.spin.valueChanged.connect(lambda x: self.slider.setValue(round(x * 10)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    c = OpeningControl()
    c.spin.setValue(37.5)
    print("slider after spin = 37.5 %:", c.slider.value())
    c.slider.setValue(820)
    print("spin after slider = 820:", c.spin.value())

    units = QComboBox()
    for text, factor in (("bar", 1.0), ("psi", 14.503773773), ("MPa", 0.1)):
        units.addItem(text, factor)         # conversion factor from bar
    def convert(i: int) -> None:
        print(f"345 bar = {345 * units.itemData(i):.2f} {units.itemText(i)}")

    units.currentIndexChanged.connect(convert)
    units.setCurrentIndex(1)
    units.setCurrentText("MPa")
