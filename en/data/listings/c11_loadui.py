"""Loading a .ui file dynamically with uic.loadUi()."""

import sys
from pathlib import Path

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QDoubleSpinBox, QLineEdit, QWidget

# path relative to the module
UI_FILE = Path(__file__).with_name("c11_well_data.ui")


class WellData(QWidget):
    # Annotations only document the attributes created by loadUi (objectName -> attribute)
    nameField: QLineEdit
    depthField: QDoubleSpinBox

    def __init__(self) -> None:
        super().__init__()
        uic.loadUi(UI_FILE, self)  # builds the widgets INSIDE self
        self.buttons.accepted.connect(self.confirm)
        self.buttons.rejected.connect(self.close)

    def confirm(self) -> None:
        print(f"well {self.nameField.text()!r}, WD = {self.depthField.value():.0f} m")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = WellData()
    print("title coming from the .ui:", w.windowTitle())
    print("buddy of the label:", w.nameLabel.buddy().objectName())
    w.nameField.setText("PZ-123")
    w.depthField.setValue(2140)
    w.buttons.accepted.emit()  # simulates clicking OK
    w.show()
    sys.exit(app.exec())
