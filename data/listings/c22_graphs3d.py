# runner: ticks=40 xcb
"""QtGraphs 3D em Widgets: Q3DSurfaceWidgetItem com QSurfaceDataProxy e tema."""

import math
import os
import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QColor, QLinearGradient
from PyQt6.QtGraphs import (
    QGraphsTheme,
    QSurface3DSeries,
    QSurfaceDataItem,
    QSurfaceDataProxy,
    QtGraphs3D,
)
from PyQt6.QtGraphsWidgets import Q3DSurfaceWidgetItem
from PyQt6.QtQuickWidgets import QQuickWidget
from PyQt6.QtWidgets import QApplication


def tensao_placa(x: float, y: float) -> float:
    """Campo ilustrativo: concentração de tensão suave ao redor de um furo central
    (MPa)."""
    r2 = (x - 0.5) ** 2 + (y - 0.5) ** 2
    return 100.0 + 180.0 * math.exp(-r2 / 0.02) * (
        1.0 + 0.3 * math.cos(6.0 * math.atan2(y - 0.5, x - 0.5))
    )


def main() -> int:
    app = QApplication(sys.argv)
    vista = QQuickWidget()
    vista.setResizeMode(QQuickWidget.ResizeMode.SizeRootObjectToView)
    grafico = Q3DSurfaceWidgetItem()
    grafico.setWidget(vista)  # o item cria e gerencia a cena QML dentro do QQuickWidget

    n = 41
    linhas = []
    for i in range(n):  # cada linha tem z constante; x varia ao longo da linha
        y = i / (n - 1)
        linhas.append(
            [
                QSurfaceDataItem(x / (n - 1), tensao_placa(x / (n - 1), y), y)
                for x in range(n)
            ]
        )
    serie = QSurface3DSeries()
    proxy: QSurfaceDataProxy = serie.dataProxy()  # proxy padrão, já ligado à série
    proxy.resetArray(linhas)
    serie.setDrawMode(QSurface3DSeries.DrawFlag.DrawSurfaceAndWireframe)
    serie.setShading(QSurface3DSeries.Shading.Smooth)
    gradiente = (
        QLinearGradient()
    )  # cor proporcional ao valor (azul -> amarelo -> vermelho)
    for pos, cor in ((0.0, "#2E75B6"), (0.5, "#FFC000"), (1.0, "#C00000")):
        gradiente.setColorAt(pos, QColor(cor))
    serie.setBaseGradient(gradiente)
    serie.setColorStyle(QGraphsTheme.ColorStyle.RangeGradient)
    grafico.addSeries(serie)

    tema = grafico.activeTheme()
    tema.setTheme(QGraphsTheme.Theme.QtGreen)
    tema.setColorScheme(QGraphsTheme.ColorScheme.Light)
    grafico.axisX().setTitle("x/L")
    grafico.axisY().setTitle("Tensão (MPa)")
    grafico.axisZ().setTitle("y/L")
    for eixo in (grafico.axisX(), grafico.axisY(), grafico.axisZ()):
        eixo.setTitleVisible(True)
    grafico.setCameraPreset(QtGraphs3D.CameraPreset.IsometricRightHigh)
    grafico.setCameraZoomLevel(85.0)  # % em relação ao enquadramento padrão

    vals = [item.y() for linha in linhas for item in linha]
    print(
        f"Superfície {proxy.rowCount()} x {proxy.columnCount()}; "
        f"tensão {min(vals):.1f} a {max(vals):.1f} MPa"
    )
    print("Séries no gráfico:", len(grafico.seriesList()))
    vista.resize(800, 560)
    vista.show()

    def capturar() -> None:
        destino = os.environ.get("CAPTURA")
        if destino:
            vista.grabFramebuffer().save(destino)
        app.quit()

    QTimer.singleShot(1500, capturar)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
