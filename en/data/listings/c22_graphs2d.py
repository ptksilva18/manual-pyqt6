# runner: ticks=40 xcb
"""QtGraphs 2D: GraphsView (QML) inside a Widgets application, fed by
Python."""

import os
import sys

from PyQt6.QtCore import QPointF, QTimer, QUrl
from PyQt6.QtGraphs import QLineSeries, QScatterSeries, QValueAxis
from PyQt6.QtQuickWidgets import QQuickWidget
from PyQt6.QtWidgets import QApplication

HERE = os.path.dirname(os.path.abspath(__file__))
RHO_FLUID = 1030.0  # kg/m3 (seawater)
G = 9.80665  # m/s2


def pressure_bar(depth_m: float) -> float:
    return RHO_FLUID * G * depth_m / 1e5 + 1.01325


def main() -> int:
    app = QApplication(sys.argv)
    view = QQuickWidget()
    view.setResizeMode(QQuickWidget.ResizeMode.SizeRootObjectToView)
    view.setSource(QUrl.fromLocalFile(os.path.join(HERE, "c22_graphs2d.qml")))
    if view.status() != QQuickWidget.Status.Ready:
        for error in view.errors():
            print(error.toString())
        return 1
    root = view.rootObject()
    line = root.findChild(QLineSeries, "hydrostatic")
    points = root.findChild(QScatterSeries, "measured")
    y_axis = root.findChild(QValueAxis, "yAxis")
    print("Series found:", type(line).__name__, type(points).__name__)

    line.replace(
        [QPointF(z, pressure_bar(z)) for z in range(0, 3001, 100)]
    )  # a single signal
    measurements = [(800.0, 84.1), (1500.0, 155.9), (2200.0, 228.6), (2900.0, 301.0)]
    for z, p in measurements:
        points.append(z, p)
    y_axis.setMax(350.0)
    print(
        f"Points: line = {line.count()}, measurements = {points.count()}; "
        f"Y axis up to {y_axis.max():.0f} bar"
    )
    print(f"theoretical p(2900 m) = {pressure_bar(2900):.1f} bar")

    view.resize(760, 440)
    view.show()

    def capture() -> None:
        target = os.environ.get("CAPTURE")
        if target:
            view.grabFramebuffer().save(target)
        app.quit()

    QTimer.singleShot(1200, capture)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
