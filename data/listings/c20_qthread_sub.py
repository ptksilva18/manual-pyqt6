# runner: ticks=40
"""Subclasse de QThread: run() roda na nova thread; os slots da subclasse, não."""

import sys

from PyQt6.QtCore import QDeadlineTimer, QObject, QThread, QTimer, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QApplication


def nome() -> str:
    return QThread.currentThread().objectName()


class Aquisicao(QThread):
    amostra = pyqtSignal(int)

    def run(self) -> None:  # único método executado na nova thread
        print(f"run() executa em: {nome()}")
        n = 0
        while not self.isInterruptionRequested():
            n += 1
            self.amostra.emit(n)
            self.msleep(20)
        print(f"run() encerrou após {n} amostras")

    @pyqtSlot()
    def slot_da_subclasse(self) -> None:
        # O objeto QThread "vive" na thread que o criou (GUI), não em run().
        print(f"slot_da_subclasse() executa em: {nome()}")


class Emissor(QObject):
    sinal = pyqtSignal()


def main() -> int:
    app = QApplication(sys.argv)
    QThread.currentThread().setObjectName("GUI")
    t = Aquisicao()
    t.setObjectName("aquisicao")
    recebidas: list[int] = []
    t.amostra.connect(recebidas.append)  # enfileirada: executa na GUI
    t.finished.connect(
        lambda: print(f"finished emitido; amostras recebidas: {len(recebidas)}")
    )
    emissor = Emissor()
    emissor.sinal.connect(t.slot_da_subclasse)
    print(f"t.thread() é a thread da GUI? {t.thread() is QThread.currentThread()}")
    t.start()
    QTimer.singleShot(100, emissor.sinal.emit)

    def parar() -> None:
        t.requestInterruption()
        terminou = t.wait(QDeadlineTimer(2000))
        print(f"wait() retornou {terminou}; isRunning() = {t.isRunning()}")
        QTimer.singleShot(0, app.quit)  # deixa entregar o sinal finished antes de sair

    QTimer.singleShot(300, parar)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
