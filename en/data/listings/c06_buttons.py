"""Checkable buttons, exclusive QButtonGroup and QDialogButtonBox."""
import sys

from PyQt6.QtWidgets import (
    QApplication, QButtonGroup, QDialogButtonBox, QPushButton, QRadioButton, QVBoxLayout,
    QWidget,
)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    lay = QVBoxLayout(window)

    group = QButtonGroup(window)              # exclusive by default
    for ident, text in enumerate(["SI", "Imperial", "Oilfield"]):
        rb = QRadioButton(text)
        lay.addWidget(rb)
        group.addButton(rb, ident)            # integer id associated with the button
    group.idClicked.connect(lambda i: print("unit system id =", i))
    group.button(0).setChecked(True)
    group.button(2).click()
    print("checked:", group.checkedButton().text())

    toggle = QPushButton("Edit mode", checkable=True)
    toggle.toggled.connect(
        lambda on: print("edit mode:", "on" if on else "off"))
    lay.addWidget(toggle)
    toggle.click()
    toggle.click()

    box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok
                           | QDialogButtonBox.StandardButton.Cancel)
    box.accepted.connect(lambda: print("accepted"))
    box.rejected.connect(lambda: print("rejected"))
    lay.addWidget(box)
    box.button(QDialogButtonBox.StandardButton.Ok).click()
