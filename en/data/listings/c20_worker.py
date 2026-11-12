# runner: ticks=80
"""Worker pattern with moveToThread(): progress, result, error, cancellation and
shutdown."""

import math
import sys
import time

from PyQt6.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


def thread_name() -> str:
    return QThread.currentThread().objectName() or "unnamed"


class Integrator(QObject):
    """Integrates f(x) = sin(x)^2 over [0, pi] with the trapezoidal rule, in blocks."""

    progress = pyqtSignal(int)
    result = pyqtSignal(float)
    canceled = pyqtSignal()
    error = pyqtSignal(str)
    done = pyqtSignal()

    def __init__(self, n_blocks: int = 50, points_per_block: int = 2_000) -> None:
        super().__init__()
        self.n_blocks = n_blocks
        self.points = points_per_block

    @pyqtSlot()
    def work(self) -> None:
        print(f"  work() runs in thread: {thread_name()}")
        try:
            n = self.n_blocks * self.points
            h = math.pi / n
            total = 0.5 * (math.sin(0.0) ** 2 + math.sin(math.pi) ** 2)
            for b in range(self.n_blocks):
                if QThread.currentThread().isInterruptionRequested():
                    self.canceled.emit()
                    return
                for i in range(b * self.points + 1, (b + 1) * self.points + 1):
                    if i < n:
                        total += math.sin(i * h) ** 2
                time.sleep(0.004)  # simulates I/O between blocks
                self.progress.emit(round(100 * (b + 1) / self.n_blocks))
            self.result.emit(total * h)
        except Exception as exc:  # worker errors become a signal, never a lost exception
            self.error.emit(f"{type(exc).__name__}: {exc}")
        finally:
            self.done.emit()


class Window(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Worker with QThread")
        self.bar = QProgressBar()
        self.label = QLabel("Ready")
        self.btn_start = QPushButton("Start")
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setEnabled(False)
        buttons = QHBoxLayout()
        buttons.addWidget(self.btn_start)
        buttons.addWidget(self.btn_cancel)
        lay = QVBoxLayout(self)
        lay.addWidget(self.bar)
        lay.addWidget(self.label)
        lay.addLayout(buttons)
        self.btn_start.clicked.connect(self.start)
        self.btn_cancel.clicked.connect(self.cancel)
        self.thread: QThread | None = None
        self.runs = 0

    def start(self) -> None:
        self.runs += 1
        self.thread = QThread()
        self.thread.setObjectName(f"integrator-{self.runs}")
        self.worker = Integrator()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.work)
        self.worker.progress.connect(self.on_progress)
        self.worker.result.connect(self.on_result)
        self.worker.canceled.connect(lambda: self.label.setText("Canceled"))
        self.worker.error.connect(self.label.setText)
        self.worker.done.connect(self.thread.quit)
        self.worker.done.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.on_finished)
        self.thread.finished.connect(self.thread.deleteLater)
        self.btn_start.setEnabled(False)
        self.btn_cancel.setEnabled(True)
        print(f"Run {self.runs}: start() runs in thread: {thread_name()}")
        self.thread.start()

    def cancel(self) -> None:
        if self.thread is not None:
            # cooperative request: the worker decides when to stop
            self.thread.requestInterruption()
            self.btn_cancel.setEnabled(False)
            self.label.setText("Canceling...")

    def on_progress(self, pct: int) -> None:
        self.bar.setValue(pct)
        if self.runs == 2 and pct >= 40 and self.btn_cancel.isEnabled():
            print(f"  user cancels at {pct} % (slot in thread: {thread_name()})")
            self.btn_cancel.click()

    def on_result(self, value: float) -> None:
        self.label.setText(f"Integral = {value:.10f}")
        print(f"  result = {value:.10f} (exact: pi/2 = {math.pi / 2:.10f})")

    def on_finished(self) -> None:
        print(
            f"  thread finished; label: {self.label.text()!r}; bar: "
            f"{self.bar.value()} %"
        )
        self.thread = None
        self.btn_start.setEnabled(True)
        self.btn_cancel.setEnabled(False)
        if self.runs == 1:
            self.btn_start.click()
        else:
            QApplication.instance().quit()

    def closeEvent(self, event) -> None:  # safe shutdown when the window is closed
        if self.thread is not None:
            self.thread.requestInterruption()
            self.thread.quit()
            self.thread.wait()
        super().closeEvent(event)


def main() -> int:
    app = QApplication(sys.argv)
    QThread.currentThread().setObjectName("GUI")
    window = Window()
    window.show()
    window.btn_start.click()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
