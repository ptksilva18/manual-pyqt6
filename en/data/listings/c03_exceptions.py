"""Exceptions in slots: without handling, PyQt6 aborts the application (qFatal).

Installing your own sys.excepthook keeps the application alive and logs the error.
"""
import sys
import traceback

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication


def global_handler(exc_type, value, tb) -> None:
    """Logs the exception; a real application would show a QMessageBox."""
    frame = traceback.extract_tb(tb)[-1]           # last frame = where it happened
    print(f"[UNHANDLED ERROR] {exc_type.__name__}: {value}")
    print(f"  origin: function {frame.name}(), line {frame.lineno}")


def faulty_slot() -> None:
    raise ZeroDivisionError("division by zero in the calculation")


if __name__ == "__main__":
    sys.excepthook = global_handler         # install BEFORE app.exec()
    app = QApplication(sys.argv)
    QTimer.singleShot(0, faulty_slot)
    QTimer.singleShot(50, lambda: print("The application is still responding."))
    QTimer.singleShot(100, app.quit)
    print("exit code:", app.exec())
