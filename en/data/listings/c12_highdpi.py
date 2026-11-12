"""High-DPI: rounding policy and pixmaps with devicePixelRatio."""

import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QGuiApplication, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel

if __name__ == "__main__":
    # Must be set BEFORE creating the application. PassThrough (the Qt 6 default)
    # uses the exact system factor (e.g. 1.25 or 1.5), without rounding.
    QGuiApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    print("policy:", QGuiApplication.highDpiScaleFactorRoundingPolicy().name)
    print("screen devicePixelRatio:", screen.devicePixelRatio())
    print("logical DPI:", round(screen.logicalDotsPerInch()))

    dpr = screen.devicePixelRatio()
    pm = QPixmap(int(48 * dpr), int(48 * dpr))  # physical pixels
    pm.setDevicePixelRatio(dpr)  # the logical size stays 48 x 48
    pm.fill(QColor("#2E75B6"))
    label = QLabel()
    label.setPixmap(pm)
    logical = pm.deviceIndependentSize().toSize()
    print("logical size of the pixmap:", logical.width(), "x", logical.height())
