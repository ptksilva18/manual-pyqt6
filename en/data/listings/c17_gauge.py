"""Custom widget: analog pressure gauge drawn with QPainter."""

import math
import sys

from PyQt6.QtCore import QPointF, QRectF, QSize, Qt, pyqtProperty, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QPainter, QPen, QPolygonF
from PyQt6.QtWidgets import QApplication, QSizePolicy, QWidget


class Gauge(QWidget):
    valueChanged = pyqtSignal(float)

    def __init__(
        self, maximum: float = 690.0, unit: str = "bar", parent=None
    ) -> None:
        super().__init__(parent)
        self._value, self.maximum, self.unit = 0.0, maximum, unit
        self.bands = [
            (0.0, 0.7, "#70AD47"),
            (0.7, 0.9, "#FFC000"),
            (0.9, 1.0, "#C00000"),
        ]
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def sizeHint(self) -> QSize:
        return QSize(260, 260)

    def minimumSizeHint(self) -> QSize:
        return QSize(120, 120)

    def _get_value(self) -> float:
        return self._value

    def _set_value(self, v: float) -> None:
        v = max(0.0, min(v, self.maximum))
        if v != self._value:
            self._value = v
            self.valueChanged.emit(v)
            # schedules a repaint (does not paint now)
            self.update()

    value = pyqtProperty(float, _get_value, _set_value, notify=valueChanged)

    def paintEvent(self, event) -> None:
        side = min(self.width(), self.height())
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.translate(self.width() / 2, self.height() / 2)
        # logical coordinates: -100..100
        p.scale(side / 200.0, side / 200.0)
        # angles in degrees (clockwise sweep)
        start, sweep = 225.0, -270.0

        p.setPen(QPen(QColor("#595959"), 3))
        p.setBrush(QColor("#FAFAFA"))
        p.drawEllipse(QPointF(0, 0), 95, 95)
        arc = QRectF(-80, -80, 160, 160)
        for a, b, color in self.bands:  # operating bands
            p.setPen(QPen(QColor(color), 10, cap=Qt.PenCapStyle.FlatCap))
            p.drawArc(arc, int((start + sweep * a) * 16), int(sweep * (b - a) * 16))

        p.setPen(QPen(QColor("#1E1E1E"), 2))
        p.setFont(QFont("DejaVu Sans", 7))
        for i in range(11):  # scale ticks and numbers
            ang = math.radians(start + sweep * i / 10)
            c, s = math.cos(ang), -math.sin(ang)
            p.drawLine(QPointF(70 * c, 70 * s), QPointF(86 * c, 86 * s))
            # 1.5 does not become "2" by rounding
            txt = f"{self.maximum * i / 10:g}"
            p.drawText(
                QRectF(58 * c - 15, 58 * s - 7, 30, 14),
                Qt.AlignmentFlag.AlignCenter,
                txt,
            )

        p.setFont(QFont("DejaVu Sans", 11, QFont.Weight.Bold))
        p.drawText(
            QRectF(-50, 58, 100, 20),
            Qt.AlignmentFlag.AlignCenter,
            f"{self._value:.1f} {self.unit}",
        )

        ang = start + sweep * self._value / self.maximum  # needle
        p.rotate(-ang)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor("#C00000"))
        p.drawPolygon(QPolygonF([QPointF(0, -4), QPointF(78, 0), QPointF(0, 4)]))
        p.setBrush(QColor("#1F3864"))
        p.drawEllipse(QPointF(0, 0), 7, 7)
        p.end()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    g = Gauge(maximum=690.0)
    g.valueChanged.connect(lambda v: print(f"valueChanged -> {v:.1f}"))
    g.value = 345.0
    g.setProperty("value", 900.0)  # clamped to the maximum
    g.resize(g.sizeHint())
    g.show()
    image = g.grab()  # renders the paintEvent
    print(
        "rendered:", image.width(), "x", image.height(), "| null?", image.isNull()
    )
    sys.exit(app.exec())
