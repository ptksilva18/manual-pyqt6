"""Metadata, aboutToQuit and quitOnLastWindowClosed."""
import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QWidget


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("EngCalc")
    app.setOrganizationName("Engineering")
    app.setOrganizationDomain("example.com")
    app.setApplicationVersion("0.1.0")
    app.setApplicationDisplayName("Engineering Calculator")

    app.aboutToQuit.connect(lambda: print("aboutToQuit: save the settings here"))
    print("quitOnLastWindowClosed =", app.quitOnLastWindowClosed())

    window = QWidget()
    window.setWindowTitle("Single window")
    window.show()
    print("title:", window.windowTitle(), "|", app.applicationDisplayName())

    QTimer.singleShot(100, window.close)   # closing the last window ends the event loop
    code = app.exec()
    print("event loop finished; code =", code)
    return code


if __name__ == "__main__":
    sys.exit(main())
