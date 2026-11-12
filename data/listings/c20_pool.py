# runner: ticks=60
"""QThreadPool com QRunnable (sinais via QObject auxiliar) e com callables Python."""

import sys
import threading
import time

from PyQt6.QtCore import QObject, QRunnable, QThreadPool, QTimer, pyqtSignal
from PyQt6.QtWidgets import QApplication


class SinaisTarefa(QObject):
    """QRunnable não é QObject: os sinais ficam em um objeto auxiliar."""

    concluida = pyqtSignal(int, float, int)  # id, resultado, id da thread
    falhou = pyqtSignal(int, str)


class TarefaFadiga(QRunnable):
    """Soma de dano de Miner para um histograma sintético (exemplo de cálculo)."""

    def __init__(self, ident: int, ciclos: int) -> None:
        super().__init__()
        self.ident = ident
        self.ciclos = ciclos
        self.sinais = SinaisTarefa()
        self.setAutoDelete(True)

    def run(self) -> None:
        try:
            if self.ciclos <= 0:
                raise ValueError("número de ciclos deve ser positivo")
            dano = 0.0
            for faixa in range(1, 51):
                s = 5.0 * faixa  # amplitude de tensão (MPa)
                n_resist = 1.0e12 * s**-3.0  # curva S-N: N = A * S^-m
                dano += (self.ciclos / faixa) / n_resist
            time.sleep(0.05)
            self.sinais.concluida.emit(self.ident, dano, threading.get_ident())
        except Exception as exc:
            self.sinais.falhou.emit(self.ident, str(exc))


def main() -> int:
    app = QApplication(sys.argv)
    print(
        f"Pool global: maxThreadCount = {QThreadPool.globalInstance().maxThreadCount()} "
        "(= número de núcleos lógicos)"
    )
    pool = QThreadPool()
    pool.setMaxThreadCount(3)
    resultados: dict[int, float] = {}
    threads: set[int] = set()
    erros: list[str] = []

    def ao_concluir(ident: int, dano: float, tid: int) -> None:
        resultados[ident] = dano
        threads.add(tid)

    for ident, ciclos in enumerate([10_000, 20_000, 40_000, 80_000, 160_000, 0]):
        tarefa = TarefaFadiga(ident, ciclos)
        tarefa.sinais.concluida.connect(ao_concluir)
        tarefa.sinais.falhou.connect(lambda i, msg: erros.append(f"tarefa {i}: {msg}"))
        pool.start(tarefa)

    marcas: list[str] = []
    pool.start(
        lambda: marcas.append("callable executado no pool")
    )  # sobrecarga com callable

    def relatorio() -> None:
        print(
            f"waitForDone: {pool.waitForDone(5000)}; threads ativas: "
            f"{pool.activeThreadCount()}"
        )
        app.processEvents()  # entrega os sinais enfileirados ainda pendentes
        for ident in sorted(resultados):
            print(f"  tarefa {ident}: dano de Miner = {resultados[ident]:.6f}")
        print(f"  erros: {erros}")
        print(f"  {marcas[0]}; threads distintas usadas (máx. 3): {len(threads) <= 3}")
        app.quit()

    QTimer.singleShot(500, relatorio)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
