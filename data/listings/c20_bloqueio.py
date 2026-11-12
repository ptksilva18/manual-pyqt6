# runner: ticks=80
"""Mede a responsividade do event loop: cálculo na thread da GUI versus em worker."""

import sys
import time

from PyQt6.QtCore import QElapsedTimer, QObject, QThread, QTimer, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QApplication


def calculo_pesado(segundos: float) -> int:
    """Laço puramente Python que ocupa a CPU pelo tempo indicado."""
    fim = time.perf_counter() + segundos
    n = 0
    while time.perf_counter() < fim:
        n += 1
    return n


class Monitor(QObject):
    """Registra o intervalo real entre disparos de um QTimer de 20 ms."""

    def __init__(self) -> None:
        super().__init__()
        self._relogio = QElapsedTimer()
        self._timer = QTimer(self)
        self._timer.setInterval(20)
        self._timer.timeout.connect(self._tique)
        self.intervalos: list[int] = []

    def iniciar(self) -> None:
        self.intervalos.clear()
        self._relogio.start()
        self._timer.start()

    def parar(self) -> tuple[int, int]:
        self._timer.stop()
        return len(self.intervalos), max(self.intervalos, default=0)

    def _tique(self) -> None:
        self.intervalos.append(self._relogio.restart())


class Worker(QObject):
    concluido = pyqtSignal(int)

    @pyqtSlot(float)
    def executar(self, segundos: float) -> None:
        self.concluido.emit(calculo_pesado(segundos))


class Controlador(QObject):
    pedir_calculo = pyqtSignal(float)

    def __init__(self, app: QApplication) -> None:
        super().__init__()
        self.app = app
        self.monitor = Monitor()
        self.thread = QThread()
        self.thread.setObjectName("worker")
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.pedir_calculo.connect(
            self.worker.executar
        )  # AutoConnection -> enfileirada
        self.thread.start()

    def fase_1(self) -> None:
        self.monitor.iniciar()
        QTimer.singleShot(100, lambda: calculo_pesado(0.6))  # bloqueia a thread da GUI
        QTimer.singleShot(1000, self.fim_fase_1)

    def fim_fase_1(self) -> None:
        n, pior = self.monitor.parar()
        print(
            f"Cálculo na thread da GUI : {n:3d} tiques em ~1 s, pior intervalo {pior} ms"
        )
        self.monitor.iniciar()
        QTimer.singleShot(
            100, lambda: self.pedir_calculo.emit(0.6)
        )  # vai para o worker
        QTimer.singleShot(1000, self.fim_fase_2)

    def fim_fase_2(self) -> None:
        n, pior = self.monitor.parar()
        print(
            f"Cálculo no worker (QThread): {n:3d} tiques em ~1 s, pior intervalo "
            f"{pior} ms"
        )
        self.thread.quit()
        self.thread.wait()
        self.app.quit()


def main() -> int:
    app = QApplication(sys.argv)
    print(f"Intervalo de troca do GIL: {sys.getswitchinterval() * 1000:.0f} ms")
    ctrl = Controlador(app)
    QTimer.singleShot(0, ctrl.fase_1)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
