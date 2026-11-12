# runner: ticks=150 timeout=90
"""concurrent.futures (threads e processos) integrado ao Qt por sinais."""

import math
import multiprocessing as mp
import os
import sys
from concurrent.futures import Future, ProcessPoolExecutor, ThreadPoolExecutor

from PyQt6.QtCore import QObject, QThread, QTimer, pyqtSignal
from PyQt6.QtWidgets import QApplication


def primos_ate(n: int) -> int:
    """Crivo de Eratóstenes (CPU-bound): conta os primos <= n."""
    crivo = bytearray([1]) * (n + 1)
    crivo[0:2] = b"\x00\x00"
    for i in range(2, math.isqrt(n) + 1):
        if crivo[i]:
            crivo[i * i :: i] = bytearray(len(range(i * i, n + 1, i)))
    return sum(crivo)


def ler_arquivo_lento(caminho: str) -> int:
    """Tarefa de E/S: o GIL é liberado durante a leitura."""
    with open(caminho, "rb") as f:
        return len(f.read())


class Ponte(QObject):
    """Recebe callbacks de futures (em outras threads) e reemite como sinal Qt."""

    pronto = pyqtSignal(str, object)

    def acompanhar(self, rotulo: str, futuro: Future) -> None:
        def callback(f: Future) -> None:  # roda na thread que concluiu o futuro
            try:
                self.pronto.emit(rotulo, f.result())
            except Exception as exc:
                self.pronto.emit(rotulo, exc)

        futuro.add_done_callback(callback)


def main() -> int:
    app = QApplication(sys.argv)
    QThread.currentThread().setObjectName("GUI")
    ponte = Ponte()
    pendentes = {"proc-1e6", "proc-2e6", "proc-erro", "thread-io"}

    def ao_pronto(rotulo: str, valor: object) -> None:  # executa na thread da GUI
        thread = QThread.currentThread().objectName()
        print(f"{rotulo:<10} -> {valor!r:<45} (tratado na thread {thread})")
        pendentes.discard(rotulo)
        if not pendentes:
            app.quit()

    ponte.pronto.connect(ao_pronto)
    ctx = mp.get_context(
        "spawn"
    )  # igual em Windows, macOS e Linux; exige o guarda __main__
    with ProcessPoolExecutor(
        max_workers=2, mp_context=ctx
    ) as procs, ThreadPoolExecutor(max_workers=2) as threads:
        ponte.acompanhar("proc-1e6", procs.submit(primos_ate, 1_000_000))
        ponte.acompanhar("proc-2e6", procs.submit(primos_ate, 2_000_000))
        ponte.acompanhar("proc-erro", procs.submit(primos_ate, -5))
        ponte.acompanhar("thread-io", threads.submit(ler_arquivo_lento, os.__file__))
        QTimer.singleShot(60_000, app.quit)  # salvaguarda
        codigo = app.exec()
    return codigo


if __name__ == "__main__":
    sys.exit(main())
