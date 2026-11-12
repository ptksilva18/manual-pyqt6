"""QPainter on a QImage: pens, brushes, gradients, paths, transformations and text."""

import sys
import tempfile
from pathlib import Path

from PyQt6.QtCore import QPointF, QRectF, Qt
from PyQt6.QtGui import (
    QBrush,
    QColor,
    QFont,
    QFontMetrics,
    QImage,
    QLinearGradient,
    QPainter,
    QPainterPath,
    QPen,
    QRadialGradient,
)
from PyQt6.QtWidgets import QApplication


def draw(img: QImage) -> None:
    p = QPainter(img)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)  # smooth edges
    p.fillRect(img.rect(), QColor("white"))

    p.setPen(QPen(QColor("#1F3864"), 3, Qt.PenStyle.DashLine))  # pen: outline
    p.setBrush(QBrush(QColor("#EAF1FA")))  # brush: fill
    p.drawRoundedRect(QRectF(20, 20, 160, 100), 12, 12)

    grad = QLinearGradient(QPointF(220, 20), QPointF(380, 120))
    grad.setColorAt(0.0, QColor("#2E75B6"))
    grad.setColorAt(1.0, QColor("#C5E0B4"))
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(grad)
    p.drawEllipse(QRectF(220, 20, 160, 100))

    path = QPainterPath()  # composite curve
    path.moveTo(20, 220)
    path.cubicTo(80, 140, 140, 300, 200, 200)
    path.lineTo(200, 260)
    path.closeSubpath()
    radial = QRadialGradient(QPointF(110, 220), 90)
    radial.setColorAt(0, QColor("#F4B183"))
    radial.setColorAt(1, QColor("#C55A11"))
    p.setBrush(radial)
    p.setPen(QPen(QColor("#7F3F0F"), 2))
    p.drawPath(path)

    p.save()  # saves the state
    # new coordinate system
    p.translate(300, 220)
    for i in range(12):
        p.rotate(30)
        p.drawLine(QPointF(30, 0), QPointF(55, 0))
    p.restore()  # back to the saved state

    font = QFont("DejaVu Sans", 14, QFont.Weight.Bold)
    p.setFont(font)
    p.setPen(QColor("#1F3864"))
    text = "QPainter: 345.0 bar"
    width = QFontMetrics(font).horizontalAdvance(text)
    # respects High-DPI images
    logical_width = img.width() / img.devicePixelRatio()
    p.drawText(QPointF((logical_width - width) / 2, 300), text)  # centered
    p.end()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    img = QImage(400, 320, QImage.Format.Format_ARGB32_Premultiplied)
    draw(img)
    target = Path(tempfile.gettempdir()) / "primitives.png"
    print("saved:", img.save(str(target)), "|", img.width(), "x", img.height())
    print(
        "pixel (100, 70):",
        img.pixelColor(100, 70).name(),
        "(fill of the rectangle)",
    )
