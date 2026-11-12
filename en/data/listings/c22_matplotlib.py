# runner: ticks=40
"""Embedded Matplotlib: FigureCanvasQTAgg, NavigationToolbar2QT and redrawing per
parameter."""

import os
import sys

import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QApplication,
    QDoubleSpinBox,
    QFormLayout,
    QHBoxLayout,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)


class Canvas(FigureCanvasQTAgg):
    def __init__(self) -> None:
        self.fig = Figure(figsize=(6.0, 4.0), layout="constrained")
        super().__init__(self.fig)  # the canvas IS a QWidget
        self.ax = self.fig.add_subplot()


class StepResponseWindow(QMainWindow):
    """Response of a mass-spring-damper system to a unit step."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Step response — Matplotlib + PyQt6")
        self.canvas = Canvas()
        self.zeta = QDoubleSpinBox(
            minimum=0.05, maximum=2.0, singleStep=0.05, value=0.20
        )
        self.wn = QDoubleSpinBox(
            minimum=0.5, maximum=20.0, singleStep=0.5, value=4.0, suffix=" rad/s"
        )
        form = QFormLayout()
        form.addRow("Damping ζ", self.zeta)
        form.addRow("Natural frequency ωn", self.wn)
        panel = QWidget()
        panel.setLayout(form)
        area = QVBoxLayout()
        area.addWidget(
            NavigationToolbar2QT(self.canvas, self)
        )  # zoom, pan, save figure
        area.addWidget(self.canvas)
        central = QWidget()
        lay = QHBoxLayout(central)
        lay.addLayout(area, 1)
        lay.addWidget(panel)
        self.setCentralWidget(central)
        (self.line,) = self.canvas.ax.plot([], [], lw=2, color="#2E75B6")
        self.canvas.ax.axhline(1.0, color="0.5", ls="--", lw=1)
        self.canvas.ax.set_xlabel("t (s)", fontsize=9)
        self.canvas.ax.set_ylabel("x(t)", fontsize=9)
        self.canvas.ax.tick_params(labelsize=8)
        self.canvas.ax.grid(True, alpha=0.3)
        self.zeta.valueChanged.connect(self.update_plot)
        self.wn.valueChanged.connect(self.update_plot)
        self.update_plot()

    @staticmethod
    def response(t: np.ndarray, zeta: float, wn: float) -> np.ndarray:
        if zeta < 1.0:
            wd = wn * np.sqrt(1.0 - zeta**2)
            phase = np.arccos(zeta)
            return 1.0 - np.exp(-zeta * wn * t) * np.sin(wd * t + phase) / np.sqrt(
                1.0 - zeta**2
            )
        if zeta == 1.0:
            return 1.0 - np.exp(-wn * t) * (1.0 + wn * t)
        s1 = -wn * (zeta - np.sqrt(zeta**2 - 1.0))
        s2 = -wn * (zeta + np.sqrt(zeta**2 - 1.0))
        return 1.0 + (s2 * np.exp(s1 * t) - s1 * np.exp(s2 * t)) / (s1 - s2)

    def update_plot(self) -> None:
        t = np.linspace(0.0, 6.0, 600)
        x = self.response(t, self.zeta.value(), self.wn.value())
        self.line.set_data(t, x)
        self.canvas.ax.relim()
        self.canvas.ax.autoscale_view()
        self.canvas.ax.set_title(
            f"ζ = {self.zeta.value():.2f}, ωn = {self.wn.value():.1f} rad/s"
            f" — overshoot {100 * (x.max() - 1):.1f} %",
            fontsize=9,
        )
        self.canvas.draw_idle()  # schedules the redraw; does not block on every change


def main() -> int:
    app = QApplication(sys.argv)
    window = StepResponseWindow()
    window.resize(980, 500)
    window.show()
    theoretical = 100 * np.exp(-np.pi * 0.2 / np.sqrt(1 - 0.2**2))
    print(f"Title: {window.canvas.ax.get_title()}")
    print(f"Theoretical overshoot for ζ = 0.20: {theoretical:.1f} %")
    window.zeta.setValue(0.70)
    print(f"After ζ = 0.70: {window.canvas.ax.get_title()}")
    window.zeta.setValue(0.20)

    def capture() -> None:
        target = os.environ.get("CAPTURE")
        if target:
            window.grab().save(target)
        app.quit()

    QTimer.singleShot(800, capture)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
