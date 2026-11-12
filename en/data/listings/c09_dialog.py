"""Custom dialog with QDialogButtonBox and validation before accept()."""
import sys
from dataclasses import dataclass

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QApplication, QDialog, QDialogButtonBox, QDoubleSpinBox, QFormLayout, QLabel,
    QLineEdit, QVBoxLayout,
)


@dataclass
class PressureTest:
    tag: str
    pressure_bar: float
    duration_min: float


class TestDialog(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("New hydrostatic test")
        self.tag = QLineEdit(placeholderText="e.g. BOP-01")
        self.pressure = QDoubleSpinBox(maximum=1035.0, decimals=1, suffix=" bar")
        self.duration = QDoubleSpinBox(maximum=240.0, decimals=0, suffix=" min", value=15)
        self.error = QLabel(styleSheet="color: #C00000")
        form = QFormLayout()
        form.addRow("Tag:", self.tag)
        form.addRow("Test pressure:", self.pressure)
        form.addRow("Duration:", self.duration)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok
                                   | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)          # accept() will validate the data
        buttons.rejected.connect(self.reject)
        lay = QVBoxLayout(self)
        lay.addLayout(form)
        lay.addWidget(self.error)
        lay.addWidget(buttons)

    def accept(self) -> None:                           # reimplemented: validates first
        if not self.tag.text().strip():
            self.error.setText("Enter the equipment tag.")
            self.tag.setFocus()
            return                                      # keeps the dialog open
        if self.pressure.value() <= 0:
            self.error.setText("The test pressure must be positive.")
            return
        super().accept()

    def result_data(self) -> PressureTest:
        return PressureTest(self.tag.text().strip(), self.pressure.value(),
                            self.duration.value())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = TestDialog()

    def simulate_user() -> None:                        # demonstration script
        dlg.accept()                                     # 1st attempt: no tag
        print("message:", dlg.error.text())
        dlg.tag.setText("BOP-01")
        dlg.pressure.setValue(1034.2)
        dlg.accept()                                     # 2nd attempt: valid

    QTimer.singleShot(0, simulate_user)
    if dlg.exec() == QDialog.DialogCode.Accepted:
        print("accepted:", dlg.result_data())
