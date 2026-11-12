"""QStackedWidget, QSplitter and QScrollArea."""
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QLabel, QListWidget, QScrollArea, QSplitter, QStackedWidget,
    QVBoxLayout, QWidget,
)


def long_page(n: int) -> QScrollArea:
    content = QWidget()
    lay = QVBoxLayout(content)
    for i in range(n):
        lay.addWidget(QLabel(f"Checklist item {i + 1}"))
    area = QScrollArea()
    area.setWidget(content)
    area.setWidgetResizable(True)                     # the content follows the width
    return area


if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = QListWidget()
    menu.addItems(["General", "Checklist", "About"])
    pages = QStackedWidget()
    center = Qt.AlignmentFlag.AlignCenter
    pages.addWidget(QLabel("General settings", alignment=center))
    pages.addWidget(long_page(40))
    pages.addWidget(QLabel("Version 0.1.0", alignment=center))
    menu.currentRowChanged.connect(pages.setCurrentIndex)     # navigation

    splitter = QSplitter(Qt.Orientation.Horizontal)
    splitter.addWidget(menu)
    splitter.addWidget(pages)
    splitter.setStretchFactor(1, 3)                   # right panel grows 3x more
    splitter.setWindowTitle("QSplitter + QStackedWidget + QScrollArea")
    splitter.resize(600, 300)
    splitter.show()

    menu.setCurrentRow(1)
    print("current page:", pages.currentIndex())
    app.processEvents()
    print("splitter sizes (px):", splitter.sizes())
    state = splitter.saveState()                      # can be stored in QSettings
    print("serialized state (bytes):", len(state))
    sys.exit(app.exec())
