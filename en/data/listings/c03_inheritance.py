"""Inheritance and super(): a QWidget subclass with its own parameters."""
import sys

from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget


class TitledPanel(QWidget):
    """Panel with a fixed title; accepts 'parent' like any QWidget."""

    def __init__(self, title: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)              # initializes the C++ part of the QWidget
        self.title = title                    # ordinary Python attribute
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"<b>{title}</b>"))

    def description(self) -> str:
        return f"{type(self).__name__}('{self.title}')"


class ResultPanel(TitledPanel):
    """Specialization: adds a value label."""

    def __init__(self, title: str, unit: str, parent: QWidget | None = None) -> None:
        super().__init__(title, parent)       # reuses the base-class initialization
        self.unit = unit
        self.value = QLabel(f"— {unit}")
        self.layout().addWidget(self.value)

    def show_value(self, x: float) -> None:
        self.value.setText(f"{x:.2f} {self.unit}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    panel = ResultPanel("Test pressure", "bar")
    panel.show_value(345.0)
    print(panel.description())
    print("MRO:", [c.__name__ for c in type(panel).__mro__][:4])
    print("Displayed text:", panel.value.text())
