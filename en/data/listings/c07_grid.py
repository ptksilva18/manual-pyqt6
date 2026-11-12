"""QGridLayout: numeric keypad with merged cells (row/column span)."""
import sys

from PyQt6.QtWidgets import QApplication, QGridLayout, QLineEdit, QPushButton, QWidget


class Keypad(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("QGridLayout")
        g = QGridLayout(self)
        self.display = QLineEdit(readOnly=True)
        g.addWidget(self.display, 0, 0, 1, 4)   # row 0, column 0, span 1 x 4
        keys = ["7", "8", "9", "/", "4", "5", "6", "*", "1", "2", "3", "-"]
        for i, k in enumerate(keys):
            b = QPushButton(k)
            b.clicked.connect(lambda _=False, k=k: self.display.insert(k))
            g.addWidget(b, 1 + i // 4, i % 4)
        g.addWidget(QPushButton("0"), 4, 0, 1, 2)         # takes 2 columns
        g.addWidget(QPushButton("."), 4, 2)
        g.addWidget(QPushButton("="), 4, 3)
        g.setColumnStretch(0, 1)                          # columns grow equally
        for c in range(1, 4):
            g.setColumnStretch(c, 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    k = Keypad()
    k.show()
    lay = k.layout()
    print("rows x columns:", lay.rowCount(), "x", lay.columnCount())
    pos = lay.getItemPosition(lay.indexOf(k.display))
    print("display at (row, column, rowSpan, colSpan):", pos)
    for key in ("7", "*", "3"):
        next(b for b in k.findChildren(QPushButton) if b.text() == key).click()
    print("display:", k.display.text())
    sys.exit(app.exec())
