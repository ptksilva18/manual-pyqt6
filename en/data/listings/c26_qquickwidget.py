# runner: ticks=40
"""QQuickWidget: QML component inside a Widgets window, with communication in both
directions."""

import os
import sys

from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtQuickWidgets import QQuickWidget
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QSlider,
    QVBoxLayout,
    QWidget,
)

HERE = os.path.dirname(os.path.abspath(__file__))


class Window(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Widgets + QML")
        self.indicator = QQuickWidget()
        self.indicator.setResizeMode(QQuickWidget.ResizeMode.SizeRootObjectToView)
        self.indicator.setClearColor(Qt.GlobalColor.white)
        self.indicator.setSource(
            QUrl.fromLocalFile(os.path.join(HERE, "c26_indicator.qml"))
        )
        self.root = self.indicator.rootObject()
        self.control = QSlider(Qt.Orientation.Vertical)
        self.control.setRange(0, 400)
        self.status = QLabel("Normal")
        self.control.valueChanged.connect(
            lambda v: self.root.setProperty("value", float(v))
        )
        self.root.alarm.connect(self.on_alarm)  # signal declared in QML
        lay = QHBoxLayout()
        lay.addWidget(self.indicator, 1)
        lay.addWidget(self.control)
        column = QVBoxLayout()
        column.addLayout(lay)
        column.addWidget(self.status)
        central = QWidget()
        central.setLayout(column)
        self.setCentralWidget(central)

    def on_alarm(self, value: float) -> None:
        self.status.setText(f"ALARM: {value:.0f} bar above 80 % of full scale")


def main() -> int:
    app = QApplication(sys.argv)
    window = Window()
    window.resize(420, 300)
    window.show()
    print("QML status:", window.indicator.status().name)
    window.control.setValue(250)

    def later() -> None:
        print(
            "value in QML:",
            window.root.property("value"),
            "| status:",
            window.status.text(),
        )
        window.control.setValue(345)
        QTimer.singleShot(400, finish)

    def finish() -> None:
        print(
            "value in QML:",
            window.root.property("value"),
            "| status:",
            window.status.text(),
        )
        if os.environ.get("CAPTURE"):
            window.grab().save(os.environ["CAPTURE"])
        app.quit()

    QTimer.singleShot(400, later)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
