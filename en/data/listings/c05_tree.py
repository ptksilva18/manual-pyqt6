"""Object tree: parent-child, objectName, findChild/findChildren and destroyed."""
import sys

from PyQt6.QtCore import QObject, QTimer
from PyQt6.QtWidgets import QApplication, QLineEdit, QPushButton, QVBoxLayout, QWidget


def print_tree(obj: QObject, level: int = 0) -> None:
    name = obj.objectName() or "(no name)"
    print("  " * level + f"{type(obj).__name__}: {name}")
    for child in obj.children():
        print_tree(child, level + 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget(objectName="window")
    layout = QVBoxLayout(window)                  # layout becomes a child of window
    layout.setObjectName("mainLayout")
    for name in ("flowField", "pressureField"):
        layout.addWidget(QLineEdit(objectName=name))
    button = QPushButton("Calculate", objectName="calculateButton")
    layout.addWidget(button)                      # addWidget reparents it to 'window'

    print_tree(window)
    field = window.findChild(QLineEdit, "pressureField")
    print("findChild:", field.objectName())
    fields = window.findChildren(QLineEdit)
    print("findChildren(QLineEdit):", [w.objectName() for w in fields])

    button.destroyed.connect(lambda: print("destroyed: button destroyed"))
    button.deleteLater()                          # safe destruction in the next cycle
    QTimer.singleShot(0, lambda: print("remaining children:",
                                       [c.objectName() for c in window.children()]))
    QTimer.singleShot(10, app.quit)
    app.exec()
