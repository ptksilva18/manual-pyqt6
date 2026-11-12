"""QGridLayout: teclado numérico com células mescladas (row/column span)."""
import sys

from PyQt6.QtWidgets import QApplication, QGridLayout, QLineEdit, QPushButton, QWidget


class Teclado(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("QGridLayout")
        g = QGridLayout(self)
        self.visor = QLineEdit(readOnly=True)
        g.addWidget(self.visor, 0, 0, 1, 4)     # linha 0, coluna 0, span 1 x 4
        teclas = ["7", "8", "9", "/", "4", "5", "6", "*", "1", "2", "3", "-"]
        for i, t in enumerate(teclas):
            b = QPushButton(t)
            b.clicked.connect(lambda _=False, t=t: self.visor.insert(t))
            g.addWidget(b, 1 + i // 4, i % 4)
        g.addWidget(QPushButton("0"), 4, 0, 1, 2)         # ocupa 2 colunas
        g.addWidget(QPushButton("."), 4, 2)
        g.addWidget(QPushButton("="), 4, 3)
        g.setColumnStretch(0, 1)                          # colunas crescem igualmente
        for c in range(1, 4):
            g.setColumnStretch(c, 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    t = Teclado()
    t.show()
    lay = t.layout()
    print("linhas x colunas:", lay.rowCount(), "x", lay.columnCount())
    pos = lay.getItemPosition(lay.indexOf(t.visor))
    print("visor em (linha, coluna, rowSpan, colSpan):", pos)
    for tecla in ("7", "*", "3"):
        next(b for b in t.findChildren(QPushButton) if b.text() == tecla).click()
    print("visor:", t.visor.text())
    sys.exit(app.exec())
