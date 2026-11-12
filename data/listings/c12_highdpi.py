"""High-DPI: política de arredondamento e pixmaps com devicePixelRatio."""

import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QGuiApplication, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel

if __name__ == "__main__":
    # Deve ser definida ANTES de criar a aplicação. PassThrough (padrão no Qt 6)
    # usa o fator exato do sistema (ex.: 1.25 ou 1.5), sem arredondar.
    QGuiApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    app = QApplication(sys.argv)
    tela = app.primaryScreen()
    print("política:", QGuiApplication.highDpiScaleFactorRoundingPolicy().name)
    print("devicePixelRatio da tela:", tela.devicePixelRatio())
    print("DPI lógico:", round(tela.logicalDotsPerInch()))

    dpr = tela.devicePixelRatio()
    pm = QPixmap(int(48 * dpr), int(48 * dpr))  # pixels físicos
    pm.setDevicePixelRatio(dpr)  # tamanho lógico continua 48 x 48
    pm.fill(QColor("#2E75B6"))
    rotulo = QLabel()
    rotulo.setPixmap(pm)
    logico = pm.deviceIndependentSize().toSize()
    print("tamanho lógico do pixmap:", logico.width(), "x", logico.height())
