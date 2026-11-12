"""Event filter: one object watches and intercepts the events of another."""
import sys

from PyQt6.QtCore import QEvent, QObject
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication, QLineEdit


class LettersOnly(QObject):
    """Blocks digits in any widget where it is installed."""

    def eventFilter(self, obj: QObject, ev: QEvent) -> bool:
        if ev.type() == QEvent.Type.KeyPress and ev.text().isdigit():
            print(f"blocked: {ev.text()!r} in {obj.objectName()}")
            return True              # True = consumed (does not reach the target)
        if ev.type() == QEvent.Type.FocusIn:
            print(f"{obj.objectName()} received focus")
        return super().eventFilter(obj, ev)   # False = follows the normal path


if __name__ == "__main__":
    app = QApplication(sys.argv)
    field = QLineEdit(objectName="tagField")
    flt = LettersOnly(field)                  # the filter has a parent: not collected
    field.installEventFilter(flt)
    field.show()
    QTest.qWaitForWindowExposed(field)
    field.setFocus()
    app.processEvents()
    QTest.keyClicks(field, "PT1x0")
    print("final text:", field.text())
    field.removeEventFilter(flt)
    QTest.keyClicks(field, "9")
    print("without the filter:", field.text())
