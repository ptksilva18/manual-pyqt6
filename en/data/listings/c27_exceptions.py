# runner: ticks=60
"""Global exception handling: sys.excepthook, threading.excepthook and error
report."""

import logging
import platform
import sys
import threading
import traceback

from PyQt6.QtCore import PYQT_VERSION_STR, QT_VERSION_STR, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox

logging.basicConfig(
    stream=sys.stdout, level=logging.INFO, format="%(levelname)s %(message)s"
)
log = logging.getLogger("tests")


def report(exc_type, value, tb) -> str:
    stack = "".join(traceback.format_exception(exc_type, value, tb))
    environment = (
        f"Python {platform.python_version()}, PyQt6 {PYQT_VERSION_STR}, "
        f"Qt {QT_VERSION_STR}, {platform.system()}"
    )
    return f"{environment}\n{stack}"


def handle_exception(exc_type, value, tb) -> None:
    """Replaces PyQt6's default behavior (aborting the process) — Chapter 3."""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, value, tb)
        return
    text = report(exc_type, value, tb)
    log.error("unhandled exception:\n%s", text.splitlines()[-1])
    box = QMessageBox(
        QMessageBox.Icon.Critical,
        "Unexpected error",
        "An error occurred. The operation was canceled, and the application carries on.",
    )
    box.setDetailedText(text)  # the user can copy it and send it to support
    box.exec()


def handle_thread_exception(args: threading.ExceptHookArgs) -> None:
    log.error(
        "exception in thread %s: %s: %s",
        args.thread.name,
        args.exc_type.__name__,
        args.exc_value,
    )


def main() -> int:
    sys.excepthook = handle_exception  # before creating the QApplication
    threading.excepthook = handle_thread_exception
    app = QApplication(sys.argv)
    window = QMainWindow()  # with no open window, closing the error box would end the app
    window.setWindowTitle("Test monitor")
    window.show()

    def faulty_slot() -> None:
        data = {"PT-101": 345.0}
        log.info("computing with %s", data["PT-102"])  # KeyError inside a slot

    QTimer.singleShot(100, faulty_slot)
    threading.Thread(target=lambda: 1 / 0, name="exporter").start()

    def carry_on() -> None:
        log.info("the application kept running after the errors")
        app.quit()

    QTimer.singleShot(600, carry_on)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
