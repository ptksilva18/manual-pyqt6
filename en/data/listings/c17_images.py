"""QImage (pixels), QPixmap (display), QFontMetrics (text) and QStylePainter."""

import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFontMetrics, QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel

if __name__ == "__main__":
    app = QApplication(sys.argv)
    img = QImage(256, 64, QImage.Format.Format_RGB32)
    for x in range(256):  # pixel-by-pixel gradient
        for y in range(64):
            img.setPixelColor(x, y, QColor(x, 64 + y, 255 - x))
    grey = img.convertToFormat(QImage.Format.Format_Grayscale8)
    smaller = img.scaled(
        64,
        16,
        Qt.AspectRatioMode.KeepAspectRatio,
        Qt.TransformationMode.SmoothTransformation,
    )
    print("formats:", img.format().name, "->", grey.format().name)
    print("resized:", smaller.width(), "x", smaller.height())
    print("pixel (200, 10):", img.pixelColor(200, 10).getRgb()[:3])

    # QPixmap: optimized for the screen
    pm = QPixmap.fromImage(img)
    label = QLabel()
    label.setPixmap(pm)
    print("QPixmap:", pm.width(), "x", pm.height(), "| depth:", pm.depth())

    fm = QFontMetrics(label.font())
    text = "Integrity report of the drilling riser"
    elided = fm.elidedText(text, Qt.TextElideMode.ElideMiddle, 150)
    print("text elided to 150 px:", elided)
    print("line height:", fm.height(), "px")
