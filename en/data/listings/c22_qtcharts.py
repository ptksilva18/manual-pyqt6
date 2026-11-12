# runner: ticks=40
"""QtCharts (legacy): QChart/QChartView with line, scatter, bars, axes and pie."""

import math
import os
import sys

from PyQt6.QtCharts import (
    QBarCategoryAxis,
    QBarSeries,
    QBarSet,
    QChart,
    QChartView,
    QLineSeries,
    QLogValueAxis,
    QPieSeries,
    QScatterSeries,
    QSplineSeries,
    QValueAxis,
)
from PyQt6.QtCore import QPointF, Qt, QTimer
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QApplication, QGridLayout, QWidget


def decay_chart() -> QChart:
    """Pressure in a leak test: measurements (scatter) and fit (spline)."""
    ch = QChart()
    ch.setTitle("Leak test")
    measured, fit = QScatterSeries(), QSplineSeries()
    measured.setName("Measured")
    measured.setMarkerSize(8.0)
    fit.setName("Exponential fit")
    for t in range(0, 61, 5):
        p = 345.0 - 6.0 * (1.0 - math.exp(-t / 15.0))
        fit.append(float(t), p)
        measured.append(float(t), p + (0.6 if t % 10 else -0.5))
    ch.addSeries(fit)
    ch.addSeries(measured)
    x_axis, y_axis = QValueAxis(), QValueAxis()
    x_axis.setRange(0, 60)
    x_axis.setTitleText("Time (min)")
    x_axis.setLabelFormat("%.0f")
    y_axis.setRange(337, 347)
    y_axis.setTitleText("Pressure (bar)")
    ch.addAxis(x_axis, Qt.AlignmentFlag.AlignBottom)
    ch.addAxis(y_axis, Qt.AlignmentFlag.AlignLeft)
    for s in (fit, measured):  # the series must be in the chart before attachAxis
        s.attachAxis(x_axis)
        s.attachAxis(y_axis)
    return ch


def sn_curve_chart() -> QChart:
    ch = QChart()
    ch.setTitle("S-N curve (log scale)")
    curve = QLineSeries()
    curve.setName("N = 1e12 S^-3")
    curve.replace([QPointF(1e12 * s**-3.0, s) for s in (20, 40, 60, 80, 100, 150, 200)])
    ch.addSeries(curve)
    n_axis = QLogValueAxis()
    n_axis.setBase(10.0)
    n_axis.setRange(1e5, 2e8)
    n_axis.setLabelFormat("%.0e")
    n_axis.setTitleText("Cycles N")
    s_axis = QValueAxis()
    s_axis.setRange(0, 220)
    s_axis.setTitleText("S (MPa)")
    s_axis.setLabelFormat("%.0f")
    ch.addAxis(n_axis, Qt.AlignmentFlag.AlignBottom)
    ch.addAxis(s_axis, Qt.AlignmentFlag.AlignLeft)
    curve.attachAxis(n_axis)
    curve.attachAxis(s_axis)
    ch.legend().setVisible(False)
    return ch


def bar_chart() -> QChart:
    ch = QChart()
    ch.setTitle("Operating hours per month")
    series = QBarSeries()
    for name, values in (("Rig A", [610, 702, 655]), ("Rig B", [580, 690, 720])):
        bar_set = QBarSet(name)
        bar_set.append([float(v) for v in values])
        series.append(bar_set)
    ch.addSeries(series)
    cat_axis = QBarCategoryAxis()
    cat_axis.append(["Jan", "Feb", "Mar"])
    v_axis = QValueAxis()
    v_axis.setRange(0, 800)
    v_axis.setLabelFormat("%.0f")
    ch.addAxis(cat_axis, Qt.AlignmentFlag.AlignBottom)
    ch.addAxis(v_axis, Qt.AlignmentFlag.AlignLeft)
    series.attachAxis(cat_axis)
    series.attachAxis(v_axis)
    return ch


def pie_chart() -> QChart:
    ch = QChart()
    ch.setTitle("Non-productive time by cause")
    pie = QPieSeries()
    for cause, hours in (
        ("Weather", 42.0),
        ("Equipment", 31.0),
        ("Logistics", 17.0),
        ("Other", 10.0),
    ):
        pie.append(cause, hours)
    for pie_slice in pie.slices():  # percentage() is only final after all the slices
        pie_slice.setLabel(f"{pie_slice.label()} {pie_slice.percentage() * 100:.0f}%")
        pie_slice.setLabelVisible(True)
    pie.slices()[0].setExploded(True)
    ch.addSeries(pie)
    ch.legend().setVisible(False)
    return ch


def main() -> int:
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("QtCharts")
    grid = QGridLayout(window)
    charts = [
        decay_chart(),
        sn_curve_chart(),
        bar_chart(),
        pie_chart(),
    ]
    for i, ch in enumerate(charts):
        ch.setAnimationOptions(QChart.AnimationOption.NoAnimation)
        view = QChartView(ch)
        view.setRenderHint(QPainter.RenderHint.Antialiasing)
        grid.addWidget(view, i // 2, i % 2)
        kinds = sorted({type(s).__name__ for s in ch.series()})
        axes = [type(a).__name__ for a in ch.axes()]
        print(f"{ch.title():<32} series={kinds} axes={axes}")
    print("Pie labels:", [s.label() for s in charts[3].series()[0].slices()])
    window.resize(1100, 760)
    window.show()

    def capture() -> None:
        target = os.environ.get("CAPTURE")
        if target:
            window.grab().save(target)
        app.quit()

    QTimer.singleShot(600, capture)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
