"""QHBoxLayout and QVBoxLayout: margins, spacing, stretch and alignment."""
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QHBoxLayout, QLabel, QPushButton, QTextEdit, QVBoxLayout, QWidget,
)


class Editor(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Box layouts")
        outer = QVBoxLayout(self)                    # passing 'self' installs the layout
        outer.setContentsMargins(12, 12, 12, 12)     # left, top, right, bottom
        outer.setSpacing(8)

        outer.addWidget(QLabel("Test remarks:"))
        outer.addWidget(QTextEdit(), stretch=1)      # receives all extra vertical space

        buttons = QHBoxLayout()
        buttons.addStretch(1)                        # pushes the buttons to the right
        buttons.addWidget(QPushButton("Save"))
        buttons.addWidget(QPushButton("Cancel"))
        outer.addLayout(buttons)                     # nested layouts

        footer = QLabel("Rev. 0")
        outer.addWidget(footer, alignment=Qt.AlignmentFlag.AlignRight)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Editor()
    w.resize(420, 300)
    w.show()
    app.processEvents()                              # forces the geometry calculation
    te = w.findChild(QTextEdit)
    print("QTextEdit height with a 300 px window:", te.height())
    w.resize(420, 500)
    app.processEvents()
    print("QTextEdit height with a 500 px window:", te.height())
    sys.exit(app.exec())
