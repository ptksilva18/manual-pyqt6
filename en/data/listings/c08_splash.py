"""QSplashScreen during start-up."""
import sys
import time

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QSplashScreen

if __name__ == "__main__":
    app = QApplication(sys.argv)
    image = QPixmap(400, 200)
    image.fill(QColor("#1F3864"))
    splash = QSplashScreen(image)
    splash.show()
    for step in ("Loading settings…", "Connecting to the database…", "Ready."):
        alignment = Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter
        splash.showMessage(step, alignment, QColor("white"))
        app.processEvents()                 # keeps the splash responsive
        time.sleep(0.05)                    # simulates start-up work
        print(step)
    window = QMainWindow()
    window.show()
    splash.finish(window)                   # disappears when the main window shows up
    print("splash visible?", splash.isVisible())
    sys.exit(app.exec())
