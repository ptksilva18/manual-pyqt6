"""First PyQt6 application: a minimal window with a centered label."""
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel


def main() -> int:
    app = QApplication(sys.argv)            # 1. application object (only one)
    label = QLabel("Hello, PyQt6!")         # 2. widget without a parent = window
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.resize(320, 120)
    label.setWindowTitle("First application")
    label.show()                            # 3. makes the window visible
    return app.exec()                       # 4. enters the event loop


if __name__ == "__main__":
    sys.exit(main())
