# runner: ticks=40 xcb
"""QtGraphs 3D in Widgets: Q3DSurfaceWidgetItem with QSurfaceDataProxy and theme."""

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


def plate_stress(x: float, y: float) -> float:
    """Illustrative field: smooth stress concentration around a central hole
    (MPa)."""
    r2 = (x - 0.5) ** 2 + (y - 0.5) ** 2
    return 100.0 + 180.0 * math.exp(-r2 / 0.02) * (
        1.0 + 0.3 * math.cos(6.0 * math.atan2(y - 0.5, x - 0.5))
    )


def main() -> int:
    app = QApplication(sys.argv)
    view = QQuickWidget()
    view.setResizeMode(QQuickWidget.ResizeMode.SizeRootObjectToView)
    graph = Q3DSurfaceWidgetItem()
    graph.setWidget(view)  # the item creates and manages the QML scene in the widget

    n = 41
    rows = []
    for i in range(n):  # each row has a constant z; x varies along the row
        y = i / (n - 1)
        rows.append(
            [
                QSurfaceDataItem(x / (n - 1), plate_stress(x / (n - 1), y), y)
                for x in range(n)
            ]
        )
    series = QSurface3DSeries()
    proxy: QSurfaceDataProxy = series.dataProxy()  # default proxy, bound to the series
    proxy.resetArray(rows)
    series.setDrawMode(QSurface3DSeries.DrawFlag.DrawSurfaceAndWireframe)
    series.setShading(QSurface3DSeries.Shading.Smooth)
    gradient = (
        QLinearGradient()
    )  # color proportional to the value (blue -> yellow -> red)
    for pos, color in ((0.0, "#2E75B6"), (0.5, "#FFC000"), (1.0, "#C00000")):
        gradient.setColorAt(pos, QColor(color))
    series.setBaseGradient(gradient)
    series.setColorStyle(QGraphsTheme.ColorStyle.RangeGradient)
    graph.addSeries(series)

    theme = graph.activeTheme()
    theme.setTheme(QGraphsTheme.Theme.QtGreen)
    theme.setColorScheme(QGraphsTheme.ColorScheme.Light)
    graph.axisX().setTitle("x/L")
    graph.axisY().setTitle("Stress (MPa)")
    graph.axisZ().setTitle("y/L")
    for axis in (graph.axisX(), graph.axisY(), graph.axisZ()):
        axis.setTitleVisible(True)
    graph.setCameraPreset(QtGraphs3D.CameraPreset.IsometricRightHigh)
    graph.setCameraZoomLevel(85.0)  # % relative to the default framing

    vals = [item.y() for row in rows for item in row]
    print(
        f"Surface {proxy.rowCount()} x {proxy.columnCount()}; "
        f"stress {min(vals):.1f} to {max(vals):.1f} MPa"
    )
    print("Series in the graph:", len(graph.seriesList()))
    view.resize(800, 560)
    view.show()

    def capture() -> None:
        target = os.environ.get("CAPTURE")
        if target:
            view.grabFramebuffer().save(target)
        app.quit()

    QTimer.singleShot(1500, capture)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
