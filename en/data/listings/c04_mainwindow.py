"""Main window as a QMainWindow subclass."""
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Engineering Calculator")
        self.resize(640, 400)
        self.setMinimumSize(480, 300)

        label = QLabel("Work area")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(label)           # QMainWindow requires a central widget

        self.statusBar().showMessage("Ready")  # creates the status bar on demand


def main() -> int:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
