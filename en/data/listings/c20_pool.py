# runner: ticks=60
"""QThreadPool with QRunnable (signals via a helper QObject) and with Python callables."""

import sys
import threading
import time

from PyQt6.QtCore import QObject, QRunnable, QThreadPool, QTimer, pyqtSignal
from PyQt6.QtWidgets import QApplication


class TaskSignals(QObject):
    """QRunnable is not a QObject: the signals live in a helper object."""

    completed = pyqtSignal(int, float, int)  # id, result, thread id
    failed = pyqtSignal(int, str)


class FatigueTask(QRunnable):
    """Miner's damage sum for a synthetic histogram (calculation example)."""

    def __init__(self, ident: int, cycles: int) -> None:
        super().__init__()
        self.ident = ident
        self.cycles = cycles
        self.signals = TaskSignals()
        self.setAutoDelete(True)

    def run(self) -> None:
        try:
            if self.cycles <= 0:
                raise ValueError("number of cycles must be positive")
            damage = 0.0
            for band in range(1, 51):
                s = 5.0 * band  # stress range (MPa)
                n_allow = 1.0e12 * s**-3.0  # S-N curve: N = A * S^-m
                damage += (self.cycles / band) / n_allow
            time.sleep(0.05)
            self.signals.completed.emit(self.ident, damage, threading.get_ident())
        except Exception as exc:
            self.signals.failed.emit(self.ident, str(exc))


def main() -> int:
    app = QApplication(sys.argv)
    print(
        f"Global pool: maxThreadCount = {QThreadPool.globalInstance().maxThreadCount()} "
        "(= number of logical cores)"
    )
    pool = QThreadPool()
    pool.setMaxThreadCount(3)
    results: dict[int, float] = {}
    threads: set[int] = set()
    errors: list[str] = []

    def on_completed(ident: int, damage: float, tid: int) -> None:
        results[ident] = damage
        threads.add(tid)

    for ident, cycles in enumerate([10_000, 20_000, 40_000, 80_000, 160_000, 0]):
        task = FatigueTask(ident, cycles)
        task.signals.completed.connect(on_completed)
        task.signals.failed.connect(lambda i, msg: errors.append(f"task {i}: {msg}"))
        pool.start(task)

    marks: list[str] = []
    pool.start(
        lambda: marks.append("callable executed in the pool")
    )  # overload that takes a callable

    def report() -> None:
        print(
            f"waitForDone: {pool.waitForDone(5000)}; active threads: "
            f"{pool.activeThreadCount()}"
        )
        app.processEvents()  # delivers the queued signals still pending
        for ident in sorted(results):
            print(f"  task {ident}: Miner damage = {results[ident]:.6f}")
        print(f"  errors: {errors}")
        print(f"  {marks[0]}; distinct threads used (max. 3): {len(threads) <= 3}")
        app.quit()

    QTimer.singleShot(500, report)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
