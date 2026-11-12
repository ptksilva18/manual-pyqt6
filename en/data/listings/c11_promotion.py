"""Widget promotion: the .ui refers to PressureField, defined in c11_widgets.py."""

import sys
from pathlib import Path

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # <header>c11_widgets.h</header> in the .ui -> uic imports the c11_widgets module
    w = uic.loadUi(Path(__file__).with_name("c11_promoted.ui"))
    field = w.pressureField
    print("class instantiated:", type(field).__name__)
    print("inherits from:", type(field).__mro__[1].__name__)
    print(
        "range:",
        field.minimum(),
        "to",
        field.maximum(),
        "| suffix:",
        repr(field.suffix()),
    )
