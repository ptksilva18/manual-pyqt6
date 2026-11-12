# runner: ticks=60
"""Signals between threads: connection types and QMetaObject.invokeMethod."""

import sys

from PyQt6.QtCore import (
    Q_ARG,
    QMetaObject,
    QObject,
    Qt,
    QThread,
    QTimer,
    pyqtSignal,
    pyqtSlot,
)
from PyQt6.QtWidgets import QApplication


def name() -> str:
    return QThread.currentThread().objectName()


class Receiver(QObject):  # lives in the GUI thread
    @pyqtSlot(str)
    def receive(self, kind: str) -> None:
        print(f"  slot of connection {kind:<25} executed in: {name()}")


class Worker(QObject):  # will be moved to the "worker" thread
    s_auto = pyqtSignal(str)
    s_queued = pyqtSignal(str)
    s_direct = pyqtSignal(str)
    s_blocking = pyqtSignal(str)

    @pyqtSlot(str)
    def task(self, text: str) -> None:
        print(f"invokeMethod -> task({text!r}) executed in: {name()}")

    @pyqtSlot()
    def emit_all(self) -> None:
        print(f"emit_all() executes in: {name()}")
        self.s_direct.emit("DirectConnection")
        self.s_auto.emit("AutoConnection")
        self.s_queued.emit("QueuedConnection")
        self.s_blocking.emit("BlockingQueuedConnection")
        print("  emit_all() continues after BlockingQueued (the slot has already ended)")


def main() -> int:
    app = QApplication(sys.argv)
    QThread.currentThread().setObjectName("GUI")
    receiver = Receiver()
    thread = QThread()
    thread.setObjectName("worker")
    worker = Worker()
    worker.moveToThread(thread)
    worker.s_auto.connect(receiver.receive)  # default: AutoConnection
    worker.s_queued.connect(receiver.receive, Qt.ConnectionType.QueuedConnection)
    worker.s_direct.connect(receiver.receive, Qt.ConnectionType.DirectConnection)
    worker.s_blocking.connect(
        receiver.receive, Qt.ConnectionType.BlockingQueuedConnection
    )
    thread.start()

    QMetaObject.invokeMethod(
        worker,
        "task",
        Qt.ConnectionType.QueuedConnection,
        Q_ARG(str, "call from the GUI"),
    )
    QMetaObject.invokeMethod(worker, "emit_all", Qt.ConnectionType.QueuedConnection)

    def finish() -> None:
        thread.quit()
        thread.wait()
        app.quit()

    QTimer.singleShot(500, finish)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
