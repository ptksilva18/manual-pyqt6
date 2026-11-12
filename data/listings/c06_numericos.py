"""Sincronizando QSlider e QDoubleSpinBox; QComboBox com dados associados."""
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QComboBox, QDoubleSpinBox, QHBoxLayout, QSlider, QWidget,
)


class ControleAbertura(QWidget):
    """Slider inteiro (0–1000) mapeado para 0,0–100,0 % no spin box."""

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
    c = ControleAbertura()
    c.spin.setValue(37.5)
    print("slider após spin = 37.5 %:", c.slider.value())
    c.slider.setValue(820)
    print("spin após slider = 820:", c.spin.value())

    unidades = QComboBox()
    for texto, fator in (("bar", 1.0), ("psi", 14.503773773), ("MPa", 0.1)):
        unidades.addItem(texto, fator)      # fator de conversão a partir de bar
    def converter(i: int) -> None:
        print(f"345 bar = {345 * unidades.itemData(i):.2f} {unidades.itemText(i)}")

    unidades.currentIndexChanged.connect(converter)
    unidades.setCurrentIndex(1)
    unidades.setCurrentText("MPa")
