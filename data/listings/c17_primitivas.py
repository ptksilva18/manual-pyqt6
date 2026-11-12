"""QPainter em QImage: canetas, pincéis, gradientes, caminhos, transformações e texto."""

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


def desenhar(img: QImage) -> None:
    p = QPainter(img)
    p.setRenderHint(QPainter.RenderHint.Antialiasing)  # bordas suaves
    p.fillRect(img.rect(), QColor("white"))

    p.setPen(QPen(QColor("#1F3864"), 3, Qt.PenStyle.DashLine))  # caneta: contorno
    p.setBrush(QBrush(QColor("#EAF1FA")))  # pincel: preenchimento
    p.drawRoundedRect(QRectF(20, 20, 160, 100), 12, 12)

    grad = QLinearGradient(QPointF(220, 20), QPointF(380, 120))
    grad.setColorAt(0.0, QColor("#2E75B6"))
    grad.setColorAt(1.0, QColor("#C5E0B4"))
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(grad)
    p.drawEllipse(QRectF(220, 20, 160, 100))

    caminho = QPainterPath()  # curva composta
    caminho.moveTo(20, 220)
    caminho.cubicTo(80, 140, 140, 300, 200, 200)
    caminho.lineTo(200, 260)
    caminho.closeSubpath()
    radial = QRadialGradient(QPointF(110, 220), 90)
    radial.setColorAt(0, QColor("#F4B183"))
    radial.setColorAt(1, QColor("#C55A11"))
    p.setBrush(radial)
    p.setPen(QPen(QColor("#7F3F0F"), 2))
    p.drawPath(caminho)

    p.save()  # salva o estado
    # novo sistema de coordenadas
    p.translate(300, 220)
    for i in range(12):
        p.rotate(30)
        p.drawLine(QPointF(30, 0), QPointF(55, 0))
    p.restore()  # volta ao estado salvo

    fonte = QFont("DejaVu Sans", 14, QFont.Weight.Bold)
    p.setFont(fonte)
    p.setPen(QColor("#1F3864"))
    texto = "QPainter: 345,0 bar"
    largura = QFontMetrics(fonte).horizontalAdvance(texto)
    # respeita imagens High-DPI
    larg_logica = img.width() / img.devicePixelRatio()
    p.drawText(QPointF((larg_logica - largura) / 2, 300), texto)  # centralizado
    p.end()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    img = QImage(400, 320, QImage.Format.Format_ARGB32_Premultiplied)
    desenhar(img)
    destino = Path(tempfile.gettempdir()) / "primitivas.png"
    print("salvo:", img.save(str(destino)), "|", img.width(), "x", img.height())
    print(
        "pixel (100, 70):",
        img.pixelColor(100, 70).name(),
        "(preenchimento do retângulo)",
    )
