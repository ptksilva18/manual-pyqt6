# runner: ticks=40
"""QThread subclass: run() runs in the new thread; the subclass's slots do not."""

import sys

from PyQt6.QtCore import QDeadlineTimer, QObject, QThread, QTimer, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QApplication


def name() -> str:
    return QThread.currentThread().objectName()


class Acquisition(QThread):
    sample = pyqtSignal(int)

    def run(self) -> None:  # the only method executed in the new thread
        print(f"run() executes in: {name()}")
        n = 0
        while not self.isInterruptionRequested():
            n += 1
            self.sample.emit(n)
            self.msleep(20)
        print(f"run() ended after {n} samples")

    @pyqtSlot()
    def subclass_slot(self) -> None:
        # The QThread object "lives" in the thread that created it (GUI), not in run().
        print(f"subclass_slot() executes in: {name()}")


class Emitter(QObject):
    signal = pyqtSignal()


def main() -> int:
    app = QApplication(sys.argv)
    QThread.currentThread().setObjectName("GUI")
    t = Acquisition()
    t.setObjectName("acquisition")
    received: list[int] = []
    t.sample.connect(received.append)  # queued: executes in the GUI
    t.finished.connect(
        lambda: print(f"finished emitted; samples received: {len(received)}")
    )
    emitter = Emitter()
    emitter.signal.connect(t.subclass_slot)
    print(f"is t.thread() the GUI thread? {t.thread() is QThread.currentThread()}")
    t.start()
    QTimer.singleShot(100, emitter.signal.emit)

    def stop() -> None:
        t.requestInterruption()
        ended = t.wait(QDeadlineTimer(2000))
        print(f"wait() returned {ended}; isRunning() = {t.isRunning()}")
        QTimer.singleShot(0, app.quit)  # lets finished be delivered before exiting

    QTimer.singleShot(300, stop)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
