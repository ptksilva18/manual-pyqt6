"""Composition with nested layouts (used for Figure 7.2)."""
import sys

from PyQt6.QtWidgets import (
    QApplication, QComboBox, QDoubleSpinBox, QFormLayout, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget,
)


class PipeCheck(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Pipe check — nested layouts")
        root = QVBoxLayout(self)                               # 1) main column

        inputs = QGroupBox("Input data")
        form = QFormLayout(inputs)                             # 2) form
        self.od = QDoubleSpinBox(maximum=2000.0, suffix=" mm", value=273.1)
        self.t = QDoubleSpinBox(maximum=100.0, suffix=" mm", value=12.7)
        self.smys = QDoubleSpinBox(maximum=1000.0, suffix=" MPa", value=448.0)
        grade = QComboBox()
        grade.addItems(["API 5L X52", "API 5L X65", "API 5L X70"])
        grade.setCurrentIndex(1)
        form.addRow("Outside diameter (OD):", self.od)
        form.addRow("Wall thickness (t):", self.t)
        form.addRow("Steel grade:", grade)
        form.addRow("SMYS:", self.smys)
        root.addWidget(inputs)

        results = QGroupBox("Results")
        grid = QGridLayout(results)                            # 3) results grid
        rows = (("D/t", "21.50"), ("Inside diameter", "247.7 mm"),
                ("Yield pressure*", "41.7 MPa"))
        for i, (name, value) in enumerate(rows):
            grid.addWidget(QLabel(name + ":"), i, 0)
            grid.addWidget(QLabel(f"<b>{value}</b>"), i, 1)
        grid.addWidget(QLabel("<i>* Barlow: P = 2·SMYS·t/OD</i>"), 3, 0, 1, 2)
        root.addWidget(results)

        buttons = QHBoxLayout()                                # 4) row of buttons
        buttons.addStretch()
        buttons.addWidget(QPushButton("Calculate"))
        buttons.addWidget(QPushButton("Export…"))
        root.addLayout(buttons)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = PipeCheck()
    w.show()
    od, t, smys = w.od.value(), w.t.value(), w.smys.value()
    print(f"D/t = {od / t:.2f}; ID = {od - 2 * t:.1f} mm;",
          f"P = {2 * smys * t / od:.1f} MPa")
    sys.exit(app.exec())
