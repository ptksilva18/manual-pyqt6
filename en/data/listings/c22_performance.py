# runner: ticks=600 timeout=120
"""Cost per update (data + painting) of pyqtgraph, QtCharts and Matplotlib."""

import sys
import time

import numpy as np
import pyqtgraph as pg
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtWidgets import QApplication, QGraphicsView

N_POINTS, N_FRAMES = 20_000, 30


def measure(name: str, prepare, update, widget) -> float:
    widget.resize(800, 400)
    widget.show()
    prepare()
    QApplication.processEvents()
    times = []
    for k in range(N_FRAMES):
        t0 = time.perf_counter()
        update(k)
        # Synchronous painting to measure the full cycle. In QGraphicsView (pyqtgraph and
        # QtCharts) the scene is drawn in the viewport: repaint() of the frame won't do.
        target = widget.viewport() if isinstance(widget, QGraphicsView) else widget
        target.repaint()
        times.append(time.perf_counter() - t0)
    widget.close()
    median = 1000.0 * float(np.median(times))
    print(
        f"{name:<34} median {median:7.1f} ms/frame  (~{1000.0 / median:5.0f} "
        "frames/s)"
    )
    return median


def main() -> int:
    app = QApplication(sys.argv)
    x = np.linspace(0.0, 10.0, N_POINTS)

    def signal(k: int) -> np.ndarray:
        return np.sin(2 * np.pi * (x + 0.05 * k)) + 0.1 * np.cos(40.0 * x)

    pw = pg.PlotWidget()
    curve = pw.plot(pen="b")
    measure("pyqtgraph setData", lambda: None, lambda k: curve.setData(x, signal(k)), pw)

    chart = QChart()
    series = QLineSeries()
    chart.addSeries(series)
    ax, ay = QValueAxis(), QValueAxis()
    ax.setRange(0, 10)
    ay.setRange(-1.2, 1.2)
    chart.addAxis(ax, Qt.AlignmentFlag.AlignBottom)
    chart.addAxis(ay, Qt.AlignmentFlag.AlignLeft)
    series.attachAxis(ax)
    series.attachAxis(ay)
    view = QChartView(chart)
    measure(
        "QtCharts replace(QPointF list)",
        lambda: None,
        lambda k: series.replace([QPointF(a, b) for a, b in zip(x, signal(k))]),
        view,
    )

    fig = Figure(figsize=(8, 4))
    canvas = FigureCanvasQTAgg(fig)
    axes = fig.add_subplot()
    (line,) = axes.plot(x, signal(0))

    def mpl(k: int) -> None:
        line.set_ydata(signal(k))
        canvas.draw()  # full redraw (no blitting)

    measure("Matplotlib set_ydata + draw()", lambda: None, mpl, canvas)
    print(
        f"({N_POINTS} points per frame; values depend on the machine and the graphics "
        "backend)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
