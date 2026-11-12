"""QLineEdit: validators, input mask, echo mode and autocompletion."""
import sys

from PyQt6.QtCore import QLocale, QRegularExpression, Qt
from PyQt6.QtGui import QDoubleValidator, QRegularExpressionValidator, QValidator
from PyQt6.QtWidgets import QApplication, QCompleter, QLineEdit

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 1) Numeric validator: 0 to 690 bar, up to 2 decimals, standard notation
    pressure = QLineEdit()
    v = QDoubleValidator(0.0, 690.0, 2)
    v.setNotation(QDoubleValidator.Notation.StandardNotation)
    v.setLocale(QLocale.c())          # decimal point, regardless of the system language
    pressure.setValidator(v)
    for txt in ("345.5", "345.555", "700", "abc"):
        state, _, _ = v.validate(txt, 0)
        print(f"validate {txt!r:10} -> {state.name}")

    # 2) Regular expression: tag in the format AA-999
    tag = QLineEdit()
    tag.setValidator(QRegularExpressionValidator(QRegularExpression(r"[A-Z]{2}-\d{3}")))
    state, _, _ = tag.validator().validate("PT-101", 0)
    acceptable = state == QValidator.State.Acceptable
    print("tag 'PT-101' ->", state.name, "| acceptable?", acceptable)

    # 3) Input mask: date 99/99/9999
    date = QLineEdit()
    date.setInputMask("99/99/9999;_")
    date.setText("11112026")
    print("mask applied:", date.text(), "| complete?", date.hasAcceptableInput())

    # 4) Password and placeholder
    password = QLineEdit(placeholderText="password")
    password.setEchoMode(QLineEdit.EchoMode.Password)
    password.setText("s3cr3t")
    print("real text:", password.text(), "| displayed:", password.displayText())

    # 5) Autocompletion
    wells = ["PX-001", "PX-002", "PY-010", "PZ-123"]
    search = QLineEdit()
    comp = QCompleter(wells)
    comp.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
    search.setCompleter(comp)
    comp.setCompletionPrefix("px")
    model = comp.completionModel()
    suggestions = [model.index(i, 0).data() for i in range(comp.completionCount())]
    print("suggestions for 'px':", suggestions)
