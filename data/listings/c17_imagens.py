"""QImage (pixels), QPixmap (exibição), QFontMetrics (texto) e QStylePainter."""

import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFontMetrics, QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel

if __name__ == "__main__":
    app = QApplication(sys.argv)
    img = QImage(256, 64, QImage.Format.Format_RGB32)
    for x in range(256):  # gradiente pixel a pixel
        for y in range(64):
            img.setPixelColor(x, y, QColor(x, 64 + y, 255 - x))
    cinza = img.convertToFormat(QImage.Format.Format_Grayscale8)
    menor = img.scaled(
        64,
        16,
        Qt.AspectRatioMode.KeepAspectRatio,
        Qt.TransformationMode.SmoothTransformation,
    )
    print("formatos:", img.format().name, "->", cinza.format().name)
    print("redimensionada:", menor.width(), "x", menor.height())
    print("pixel (200, 10):", img.pixelColor(200, 10).getRgb()[:3])

    # QPixmap: otimizado para tela
    pm = QPixmap.fromImage(img)
    rotulo = QLabel()
    rotulo.setPixmap(pm)
    print("QPixmap:", pm.width(), "x", pm.height(), "| profundidade:", pm.depth())

    fm = QFontMetrics(rotulo.font())
    texto = "Relatório de integridade do riser de perfuração"
    elidido = fm.elidedText(texto, Qt.TextElideMode.ElideMiddle, 150)
    print("texto elidido em 150 px:", elidido)
    print("altura da linha:", fm.height(), "px")
