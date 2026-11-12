"""Graphics View: scene with standard and custom items, two views, collision and zoom."""

import sys

from PyQt6.QtCore import QPointF, QRectF, Qt
from PyQt6.QtGui import QBrush, QColor, QFont, QPainter, QPainterPath, QPen
from PyQt6.QtWidgets import (
    QApplication,
    QGraphicsDropShadowEffect,
    QGraphicsItem,
    QGraphicsObject,
    QGraphicsScene,
    QGraphicsView,
    QHBoxLayout,
    QLineEdit,
    QWidget,
)


class Valve(QGraphicsObject):
    """Custom item: defines boundingRect(), shape() and paint()."""

    def __init__(self, tag: str) -> None:
        super().__init__()
        self.tag = tag
        self.is_open = True
        f = QGraphicsItem.GraphicsItemFlag
        self.setFlags(f.ItemIsMovable | f.ItemIsSelectable | f.ItemSendsGeometryChanges)

    def boundingRect(self) -> QRectF:  # area the item may paint
        return QRectF(-32, -32, 64, 70)

    # exact shape (clicks and collision)
    def shape(self) -> QPainterPath:
        path = QPainterPath()
        path.moveTo(-30, -18)
        path.lineTo(30, 18)
        path.lineTo(30, -18)
        path.lineTo(-30, 18)
        path.closeSubpath()
        return path

    def paint(self, p: QPainter, option, widget=None) -> None:
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        color = QColor("#70AD47") if self.is_open else QColor("#C00000")
        p.setBrush(color)
        p.setPen(QPen(QColor("#1F3864"), 3 if self.isSelected() else 1.5))
        p.drawPath(self.shape())
        p.setFont(QFont("DejaVu Sans", 8))
        p.drawText(QRectF(-32, 20, 64, 16), Qt.AlignmentFlag.AlignCenter, self.tag)

    def mouseDoubleClickEvent(self, event) -> None:
        self.is_open = not self.is_open
        self.update()

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            # grid
            return QPointF(round(value.x() / 10) * 10, round(value.y() / 10) * 10)
        return super().itemChange(change, value)


class ZoomView(QGraphicsView):
    # zoom with the wheel, anchored at the mouse
    def wheelEvent(self, e) -> None:
        factor = 1.15 if e.angleDelta().y() > 0 else 1 / 1.15
        self.scale(factor, factor)


def build_scene() -> QGraphicsScene:
    scene = QGraphicsScene(QRectF(0, 0, 420, 260))
    scene.setBackgroundBrush(QColor("#F7F9FC"))
    pipe = scene.addRect(
        QRectF(20, 115, 380, 30), QPen(QColor("#595959")), QBrush(QColor("#D9E2F3"))
    )
    pipe.setZValue(-1)  # behind the valves
    for i, tag in enumerate(("XV-101", "XV-102", "XV-103")):
        v = Valve(tag)
        v.setPos(90 + i * 120, 130)
        scene.addItem(v)
    scene.addText("Service line", QFont("DejaVu Sans", 10)).setPos(20, 80)
    field = QLineEdit("345.0 bar")  # ordinary widget inside the scene
    proxy = scene.addWidget(field)
    proxy.setPos(300, 200)
    shadow = QGraphicsDropShadowEffect(blurRadius=12, offset=QPointF(3, 3))
    proxy.setGraphicsEffect(shadow)
    return scene


if __name__ == "__main__":
    app = QApplication(sys.argv)
    scene = build_scene()
    v1, v2 = ZoomView(scene), QGraphicsView(scene)  # two views of the SAME scene
    v1.setRenderHint(QPainter.RenderHint.Antialiasing)
    v2.setRenderHint(QPainter.RenderHint.Antialiasing)
    v2.scale(0.6, 0.6)
    v2.rotate(-8)
    window = QWidget()
    lay = QHBoxLayout(window)
    lay.addWidget(v1, 3)
    lay.addWidget(v2, 2)
    window.resize(900, 320)
    window.show()

    valves = [i for i in scene.items() if isinstance(i, Valve)]
    print(
        "items in the scene:",
        len(scene.items()),
        "| valves:",
        sorted(v.tag for v in valves),
    )
    xv = next(v for v in valves if v.tag == "XV-101")
    # itemChange snaps it to the 10-unit grid
    xv.setPos(213, 127)
    print("position snapped to the grid:", xv.pos().x(), xv.pos().y())
    print(
        "collides with:",
        sorted(getattr(i, "tag", type(i).__name__) for i in xv.collidingItems()),
    )
    item = scene.itemAt(QPointF(330, 130), v1.transform())
    print("item at (330, 130):", getattr(item, "tag", type(item).__name__))
    sys.exit(app.exec())
