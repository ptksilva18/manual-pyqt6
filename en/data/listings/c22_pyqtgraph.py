# runner: ticks=60
"""pyqtgraph: real-time chart with a numpy circular buffer and QTimer."""

import os
import sys
import time

import numpy as np
import pyqtgraph as pg
from PyQt6.QtCore import QElapsedTimer, QTimer
from PyQt6.QtWidgets import QApplication


class Oscilloscope(pg.PlotWidget):
    def __init__(self, n_points: int = 2_000, rate_hz: float = 1_000.0) -> None:
        super().__init__(background="w")
        self.n, self.dt = n_points, 1.0 / rate_hz
        self.t = np.arange(-n_points, 0) * self.dt
        self.y = np.zeros(n_points)
        self.phase = 0.0
        self.setLabel("bottom", "Time", units="s")
        self.setLabel("left", "Acceleration", units="g")
        self.showGrid(x=True, y=True, alpha=0.3)
        self.setYRange(-1.5, 1.5)
        self.curve = self.plot(self.t, self.y, pen=pg.mkPen("#2E75B6", width=1.5))
        self.curve.setClipToView(True)  # draws only the visible part
        self.curve.setDownsampling(
            auto=True, method="peak"
        )  # preserves peaks when reducing
        self.frames = 0
        self.clock = QElapsedTimer()
        self.clock.start()

    def new_samples(self, k: int) -> np.ndarray:
        tt = self.phase + np.arange(1, k + 1) * self.dt
        self.phase = tt[-1]
        return 0.8 * np.sin(2 * np.pi * 12.0 * tt) + 0.2 * np.sin(2 * np.pi * 95.0 * tt)

    def update_plot(self) -> None:
        k = 20  # 20 samples per 20 ms frame = 1 kHz
        self.y = np.roll(self.y, -k)
        self.y[-k:] = self.new_samples(k)
        self.t = self.t + k * self.dt
        self.curve.setData(self.t, self.y)  # replaces the data; no items recreated
        self.frames += 1


def main() -> int:
    pg.setConfigOptions(antialias=False)  # faster for dense signals
    app = QApplication(sys.argv)
    osc = Oscilloscope()
    osc.resize(800, 360)
    osc.show()
    timer = QTimer()
    timer.setInterval(20)
    timer.timeout.connect(osc.update_plot)
    timer.start()

    def finish() -> None:
        timer.stop()
        sec = osc.clock.elapsed() / 1000.0
        print(
            f"pyqtgraph {pg.__version__}: {osc.frames} frames in {sec:.1f} s "
            f"(~{osc.frames / sec:.0f} frames/s; target 50)"
        )
        print(
            f"Data window: {osc.n} points, t = [{osc.t[0]:.3f}; {osc.t[-1]:.3f}] s"
        )
        target = os.environ.get("CAPTURE")
        if target:
            osc.grab().save(target)
        app.quit()

    QTimer.singleShot(3000, finish)
    t0 = time.perf_counter()
    code = app.exec()
    print(f"Total time in the event loop: {time.perf_counter() - t0:.1f} s")
    return code


if __name__ == "__main__":
    sys.exit(main())
