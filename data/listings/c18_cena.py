"""Graphics View: cena com itens padrão e personalizados, duas visões, colisão e zoom."""

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


class Valvula(QGraphicsObject):
    """Item personalizado: define boundingRect(), shape() e paint()."""

    def __init__(self, tag: str) -> None:
        super().__init__()
        self.tag = tag
        self.aberta = True
        f = QGraphicsItem.GraphicsItemFlag
        self.setFlags(f.ItemIsMovable | f.ItemIsSelectable | f.ItemSendsGeometryChanges)

    def boundingRect(self) -> QRectF:  # área que o item pode pintar
        return QRectF(-32, -32, 64, 70)

    # forma exata (clique e colisão)
    def shape(self) -> QPainterPath:
        caminho = QPainterPath()
        caminho.moveTo(-30, -18)
        caminho.lineTo(30, 18)
        caminho.lineTo(30, -18)
        caminho.lineTo(-30, 18)
        caminho.closeSubpath()
        return caminho

    def paint(self, p: QPainter, opcao, widget=None) -> None:
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        cor = QColor("#70AD47") if self.aberta else QColor("#C00000")
        p.setBrush(cor)
        p.setPen(QPen(QColor("#1F3864"), 3 if self.isSelected() else 1.5))
        p.drawPath(self.shape())
        p.setFont(QFont("DejaVu Sans", 8))
        p.drawText(QRectF(-32, 20, 64, 16), Qt.AlignmentFlag.AlignCenter, self.tag)

    def mouseDoubleClickEvent(self, evento) -> None:
        self.aberta = not self.aberta
        self.update()

    def itemChange(self, mudanca, valor):
        if mudanca == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            # grade
            return QPointF(round(valor.x() / 10) * 10, round(valor.y() / 10) * 10)
        return super().itemChange(mudanca, valor)


class VisaoZoom(QGraphicsView):
    # zoom com a roda, ancorado no mouse
    def wheelEvent(self, e) -> None:
        fator = 1.15 if e.angleDelta().y() > 0 else 1 / 1.15
        self.scale(fator, fator)


def montar_cena() -> QGraphicsScene:
    cena = QGraphicsScene(QRectF(0, 0, 420, 260))
    cena.setBackgroundBrush(QColor("#F7F9FC"))
    tubo = cena.addRect(
        QRectF(20, 115, 380, 30), QPen(QColor("#595959")), QBrush(QColor("#D9E2F3"))
    )
    tubo.setZValue(-1)  # atrás das válvulas
    for i, tag in enumerate(("XV-101", "XV-102", "XV-103")):
        v = Valvula(tag)
        v.setPos(90 + i * 120, 130)
        cena.addItem(v)
    cena.addText("Linha de serviço", QFont("DejaVu Sans", 10)).setPos(20, 80)
    campo = QLineEdit("345.0 bar")  # widget comum dentro da cena
    proxy = cena.addWidget(campo)
    proxy.setPos(300, 200)
    sombra = QGraphicsDropShadowEffect(blurRadius=12, offset=QPointF(3, 3))
    proxy.setGraphicsEffect(sombra)
    return cena


if __name__ == "__main__":
    app = QApplication(sys.argv)
    cena = montar_cena()
    v1, v2 = VisaoZoom(cena), QGraphicsView(cena)  # duas visões da MESMA cena
    v1.setRenderHint(QPainter.RenderHint.Antialiasing)
    v2.setRenderHint(QPainter.RenderHint.Antialiasing)
    v2.scale(0.6, 0.6)
    v2.rotate(-8)
    janela = QWidget()
    lay = QHBoxLayout(janela)
    lay.addWidget(v1, 3)
    lay.addWidget(v2, 2)
    janela.resize(900, 320)
    janela.show()

    valvulas = [i for i in cena.items() if isinstance(i, Valvula)]
    print(
        "itens na cena:",
        len(cena.items()),
        "| válvulas:",
        sorted(v.tag for v in valvulas),
    )
    xv = next(v for v in valvulas if v.tag == "XV-101")
    # itemChange ajusta à grade de 10
    xv.setPos(213, 127)
    print("posição ajustada à grade:", xv.pos().x(), xv.pos().y())
    print(
        "colide com:",
        sorted(getattr(i, "tag", type(i).__name__) for i in xv.collidingItems()),
    )
    item = cena.itemAt(QPointF(330, 130), v1.transform())
    print("item em (330, 130):", getattr(item, "tag", type(item).__name__))
    sys.exit(app.exec())
