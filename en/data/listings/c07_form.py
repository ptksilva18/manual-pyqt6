"""QFormLayout: aligned labels and fields, with wrapping and growth policies."""
import sys

from PyQt6.QtWidgets import (
    QApplication, QComboBox, QDoubleSpinBox, QFormLayout, QLineEdit, QSpinBox, QWidget,
)


class WellData(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("QFormLayout")
        f = QFormLayout(self)
        f.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapLongRows)
        f.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        self.name = QLineEdit()
        f.addRow("Well &name:", self.name)              # & creates Alt+N (buddy)
        f.addRow("Water depth:", QDoubleSpinBox(maximum=3500.0, suffix=" m"))
        f.addRow("No. of strings:", QSpinBox(minimum=1, maximum=8))
        kind = QComboBox()
        kind.addItems(["Producer", "Injector", "Exploratory"])
        f.addRow("Type:", kind)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    d = WellData()
    d.show()
    f = d.layout()
    print("rows:", f.rowCount())
    label = f.labelForField(d.name)
    print("label of the name field:", label.text())
    print("is the buddy the field?", label.buddy() is d.name)
    sys.exit(app.exec())
