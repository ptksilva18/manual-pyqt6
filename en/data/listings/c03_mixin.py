"""Pure-Python mixin combined with a single Qt class."""
import sys

from PyQt6.QtWidgets import QApplication, QLineEdit


class LogMixin:
    """Mixin without a Qt base: adds a message history."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)     # passes everything along (cooperative)
        self._history: list[str] = []

    def log(self, msg: str) -> None:
        self._history.append(msg)

    @property
    def history(self) -> tuple[str, ...]:
        return tuple(self._history)


class AuditedField(LogMixin, QLineEdit):
    """Inherits from ONE Qt class (QLineEdit) and from a Python mixin."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.textChanged.connect(lambda t: self.log(f"text={t!r}"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    field = AuditedField()
    field.setText("ABC")
    field.setText("ABCD")
    print(field.history)
    print("Is it a QLineEdit?", isinstance(field, QLineEdit))
