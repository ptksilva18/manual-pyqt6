"""Gallery of the fundamental widgets (used for Figure 6.1)."""
import sys

from PyQt6.QtCore import QDate, Qt
from PyQt6.QtWidgets import (
    QApplication, QCheckBox, QComboBox, QDateEdit, QDial, QDoubleSpinBox, QFormLayout,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLCDNumber, QLineEdit, QProgressBar,
    QPushButton, QRadioButton, QSlider, QSpinBox, QTextEdit, QToolButton, QVBoxLayout,
    QWidget,
)


class Gallery(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Widget gallery")
        grid = QGridLayout(self)

        display = QGroupBox("Display")
        f1 = QVBoxLayout(display)
        f1.addWidget(QLabel("QLabel with <b>rich text</b>"))
        lcd = QLCDNumber(5)
        lcd.display(345.7)
        f1.addWidget(lcd)
        bar = QProgressBar()
        bar.setValue(65)
        f1.addWidget(bar)

        buttons = QGroupBox("Buttons")
        f2 = QVBoxLayout(buttons)
        f2.addWidget(QPushButton("QPushButton"))
        row = QHBoxLayout()
        row.addWidget(QToolButton(text="…"))
        row.addWidget(QCheckBox("QCheckBox", checked=True))
        f2.addLayout(row)
        f2.addWidget(QRadioButton("QRadioButton", checked=True))
        f2.addWidget(QRadioButton("Another option"))

        entry = QGroupBox("Data entry")
        f3 = QFormLayout(entry)
        f3.addRow("QLineEdit:", QLineEdit(placeholderText="equipment tag"))
        f3.addRow("QSpinBox:", QSpinBox(value=12, suffix=" pcs"))
        dsb = QDoubleSpinBox(decimals=2, maximum=1000.0, suffix=" bar")
        dsb.setValue(206.84)
        f3.addRow("QDoubleSpinBox:", dsb)
        combo = QComboBox()
        combo.addItems(["Carbon steel", "Stainless 316L", "Duplex 2205"])
        f3.addRow("QComboBox:", combo)
        f3.addRow("QDateEdit:", QDateEdit(QDate(2026, 11, 11), calendarPopup=True,
                                          displayFormat="yyyy-MM-dd"))

        ranges = QGroupBox("Range and text")
        f4 = QVBoxLayout(ranges)
        s = QSlider(Qt.Orientation.Horizontal)
        s.setValue(40)
        f4.addWidget(s)
        dial = QDial(notchesVisible=True)
        dial.setValue(30)
        dial.setFixedHeight(60)
        f4.addWidget(dial)
        te = QTextEdit()
        te.setPlainText("QTextEdit: multi-line text\nwith free editing.")
        te.setFixedHeight(60)
        f4.addWidget(te)

        grid.addWidget(display, 0, 0)
        grid.addWidget(buttons, 0, 1)
        grid.addWidget(entry, 1, 0)
        grid.addWidget(ranges, 1, 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    g = Gallery()
    g.show()
    print("widgets in the gallery:", len(g.findChildren(QWidget)))
    sys.exit(app.exec())
