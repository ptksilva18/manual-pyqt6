# runner: ticks=60
"""Sinais entre threads: tipos de conexão e QMetaObject.invokeMethod."""

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


def nome() -> str:
    return QThread.currentThread().objectName()


class Receptor(QObject):  # vive na thread da GUI
    @pyqtSlot(str)
    def receber(self, tipo: str) -> None:
        print(f"  slot da conexão {tipo:<25} executou em: {nome()}")


class Worker(QObject):  # será movido para a thread "worker"
    s_auto = pyqtSignal(str)
    s_queued = pyqtSignal(str)
    s_direct = pyqtSignal(str)
    s_blocking = pyqtSignal(str)

    @pyqtSlot(str)
    def tarefa(self, texto: str) -> None:
        print(f"invokeMethod -> tarefa({texto!r}) executou em: {nome()}")

    @pyqtSlot()
    def emitir(self) -> None:
        print(f"emitir() executa em: {nome()}")
        self.s_direct.emit("DirectConnection")
        self.s_auto.emit("AutoConnection")
        self.s_queued.emit("QueuedConnection")
        self.s_blocking.emit("BlockingQueuedConnection")
        print("  emitir() continua após BlockingQueued (o slot já terminou)")


def main() -> int:
    app = QApplication(sys.argv)
    QThread.currentThread().setObjectName("GUI")
    receptor = Receptor()
    thread = QThread()
    thread.setObjectName("worker")
    worker = Worker()
    worker.moveToThread(thread)
    worker.s_auto.connect(receptor.receber)  # padrão: AutoConnection
    worker.s_queued.connect(receptor.receber, Qt.ConnectionType.QueuedConnection)
    worker.s_direct.connect(receptor.receber, Qt.ConnectionType.DirectConnection)
    worker.s_blocking.connect(
        receptor.receber, Qt.ConnectionType.BlockingQueuedConnection
    )
    thread.start()

    QMetaObject.invokeMethod(
        worker,
        "tarefa",
        Qt.ConnectionType.QueuedConnection,
        Q_ARG(str, "chamada da GUI"),
    )
    QMetaObject.invokeMethod(worker, "emitir", Qt.ConnectionType.QueuedConnection)

    def fim() -> None:
        thread.quit()
        thread.wait()
        app.quit()

    QTimer.singleShot(500, fim)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
