# runner: ticks=80
"""Measures event loop responsiveness: computation in the GUI thread vs. in a worker."""

import sys
import time

from PyQt6.QtCore import QElapsedTimer, QObject, QThread, QTimer, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QApplication


def heavy_computation(seconds: float) -> int:
    """Pure-Python loop that keeps the CPU busy for the given time."""
    end = time.perf_counter() + seconds
    n = 0
    while time.perf_counter() < end:
        n += 1
    return n


class Monitor(QObject):
    """Records the actual interval between firings of a 20 ms QTimer."""

    def __init__(self) -> None:
        super().__init__()
        self._clock = QElapsedTimer()
        self._timer = QTimer(self)
        self._timer.setInterval(20)
        self._timer.timeout.connect(self._tick)
        self.intervals: list[int] = []

    def start(self) -> None:
        self.intervals.clear()
        self._clock.start()
        self._timer.start()

    def stop(self) -> tuple[int, int]:
        self._timer.stop()
        return len(self.intervals), max(self.intervals, default=0)

    def _tick(self) -> None:
        self.intervals.append(self._clock.restart())


class Worker(QObject):
    done = pyqtSignal(int)

    @pyqtSlot(float)
    def work(self, seconds: float) -> None:
        self.done.emit(heavy_computation(seconds))


class Controller(QObject):
    request_computation = pyqtSignal(float)

    def __init__(self, app: QApplication) -> None:
        super().__init__()
        self.app = app
        self.monitor = Monitor()
        self.thread = QThread()
        self.thread.setObjectName("worker")
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.request_computation.connect(
            self.worker.work
        )  # AutoConnection -> queued
        self.thread.start()

    def phase_1(self) -> None:
        self.monitor.start()
        QTimer.singleShot(100, lambda: heavy_computation(0.6))  # blocks the GUI thread
        QTimer.singleShot(1000, self.end_phase_1)

    def end_phase_1(self) -> None:
        n, worst = self.monitor.stop()
        print(
            f"Computation in the GUI thread: {n:3d} ticks in ~1 s, worst interval "
            f"{worst} ms"
        )
        self.monitor.start()
        QTimer.singleShot(
            100, lambda: self.request_computation.emit(0.6)
        )  # goes to the worker
        QTimer.singleShot(1000, self.end_phase_2)

    def end_phase_2(self) -> None:
        n, worst = self.monitor.stop()
        print(
            f"Computation in the worker   : {n:3d} ticks in ~1 s, worst interval "
            f"{worst} ms"
        )
        self.thread.quit()
        self.thread.wait()
        self.app.quit()


def main() -> int:
    app = QApplication(sys.argv)
    print(f"GIL switch interval: {sys.getswitchinterval() * 1000:.0f} ms")
    ctrl = Controller(app)
    QTimer.singleShot(0, ctrl.phase_1)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
