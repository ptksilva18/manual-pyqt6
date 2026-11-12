"""Qt Style Sheets: light and dark themes, selectors, subcontrols and pseudo-states."""

import sys

from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

BASE = """
QWidget            { font-size: 10pt; }
QGroupBox          { border: 1px solid %(edge)s; border-radius: 6px;
                     margin-top: 14px; padding: 10px 8px 8px 8px; }
QGroupBox::title   { subcontrol-origin: margin; left: 10px; padding: 0 4px;
                     color: %(accent)s; font-weight: bold; }
QLineEdit, QDoubleSpinBox, QComboBox {
                     background: %(field)s; color: %(text)s;
                     border: 1px solid %(edge)s; border-radius: 4px; padding: 3px 6px; }
QLineEdit:focus, QDoubleSpinBox:focus, QComboBox:focus { border: 2px solid %(accent)s; }
QPushButton        { background: %(button)s; color: %(text)s; border: 1px solid %(edge)s;
                     border-radius: 4px; padding: 5px 16px; }
QPushButton:hover  { border-color: %(accent)s; }
QPushButton:pressed { background: %(accent)s; color: white; }
QPushButton#primary { background: %(accent)s; color: white; border: none; }
QPushButton[dangerous="true"] { background: #C00000; color: white; border: none; }
QWidget#root       { background: %(bg)s; color: %(text)s; }
QCheckBox          { color: %(text)s; }
QGroupBox QLabel   { color: %(text)s; }
"""
LIGHT = dict(
    bg="#F7F8FA",
    field="#FFFFFF",
    text="#1E1E1E",
    edge="#BFC5CF",
    button="#FFFFFF",
    accent="#2E75B6",
)
DARK = dict(
    bg="#1E1F22",
    field="#2B2D31",
    text="#E6E6E6",
    edge="#4A4D55",
    button="#2B2D31",
    accent="#4E9BE0",
)


class Form(QWidget):
    def __init__(self) -> None:
        super().__init__(objectName="root")
        group = QGroupBox("Test data")
        f = QFormLayout(group)
        f.addRow("Tag:", QLineEdit("BOP-01"))
        f.addRow("Pressure:", QDoubleSpinBox(maximum=1035.0, value=345.0, suffix=" bar"))
        combo = QComboBox()
        combo.addItems(["Hydrostatic", "Functional", "Leak test"])
        f.addRow("Type:", combo)
        f.addRow("", QCheckBox("Record in the log", checked=True))
        buttons = QHBoxLayout()
        buttons.addStretch()
        delete = QPushButton("Delete")
        delete.setProperty("dangerous", True)  # selector [dangerous="true"]
        buttons.addWidget(delete)
        buttons.addWidget(QPushButton("Cancel"))
        # selector #primary
        buttons.addWidget(QPushButton("Save", objectName="primary"))
        lay = QVBoxLayout(self)
        lay.addWidget(group)
        lay.addLayout(buttons)

    def apply_theme(self, colors: dict) -> None:
        self.setStyleSheet(BASE % colors)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    w = Form()
    w.apply_theme(DARK)
    w.show()
    delete = next(b for b in w.findChildren(QPushButton) if b.text() == "Delete")
    print("QSS applied (characters):", len(w.styleSheet()))
    print("dynamic property dangerous =", delete.property("dangerous"))
    delete.setProperty("dangerous", False)  # it changed: re-polish the widget
    delete.style().unpolish(delete)
    delete.style().polish(delete)
    print("re-polished after changing the property")
    sys.exit(app.exec())
