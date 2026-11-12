# runner: ticks=60
"""Sincronização: QMutex, QReadWriteLock e buffer limitado com QWaitCondition."""

import sys
from collections import deque

from PyQt6.QtCore import (
    QMutex,
    QReadLocker,
    QReadWriteLock,
    QSemaphore,
    QThread,
    QWaitCondition,
    QWriteLocker,
)
from PyQt6.QtWidgets import QApplication


class Contador:
    def __init__(self) -> None:
        self._mutex = QMutex()
        self.valor = 0

    def incrementar(self) -> None:
        # No PyQt6 6.12, QMutexLocker falhou de forma intermitente sob disputa entre
        # threads (falha de segmentação, verificada); lock()/unlock() com try/finally não.
        self._mutex.lock()
        try:
            self.valor += 1
        finally:  # libera o mutex mesmo se houver exceção
            self._mutex.unlock()


class Incrementador(QThread):
    def __init__(self, contador: Contador, n: int) -> None:
        super().__init__()
        self.contador, self.n = contador, n

    def run(self) -> None:
        for _ in range(self.n):
            self.contador.incrementar()


class TabelaPropriedades:
    """Muitos leitores simultâneos, um escritor por vez."""

    def __init__(self) -> None:
        self._lock = QReadWriteLock()
        self._dados = {"aco_E_GPa": 207.0}
        self.leituras = 0

    def ler(self, chave: str) -> float:
        with QReadLocker(self._lock):
            self.leituras += 1  # contagem aproximada: só ilustra o acesso concorrente
            return self._dados[chave]

    def gravar(self, chave: str, valor: float) -> None:
        with QWriteLocker(self._lock):
            self._dados[chave] = valor


class BufferLimitado:
    """Fila de capacidade fixa: produtor espera se cheia; consumidor, se vazia."""

    def __init__(self, capacidade: int) -> None:
        self._fila: deque[float | None] = deque()
        self._cap = capacidade
        self._mutex = QMutex()
        self._nao_cheia = QWaitCondition()
        self._nao_vazia = QWaitCondition()
        self.max_ocupacao = 0

    def colocar(self, item: float | None) -> None:
        self._mutex.lock()
        try:
            while len(self._fila) >= self._cap:
                self._nao_cheia.wait(self._mutex)  # libera o mutex enquanto espera
            self._fila.append(item)
            self.max_ocupacao = max(self.max_ocupacao, len(self._fila))
            self._nao_vazia.wakeOne()
        finally:
            self._mutex.unlock()

    def retirar(self) -> float | None:
        self._mutex.lock()
        try:
            while not self._fila:
                self._nao_vazia.wait(self._mutex)
            item = self._fila.popleft()
            self._nao_cheia.wakeOne()
            return item
        finally:
            self._mutex.unlock()


class ThreadFuncao(QThread):
    """Executa uma função qualquer em run() (o PyQt6 não expõe QThread.create())."""

    def __init__(self, funcao) -> None:
        super().__init__()
        self.funcao = funcao

    def run(self) -> None:
        self.funcao()


class Produtor(QThread):
    def __init__(self, buf: BufferLimitado, n: int) -> None:
        super().__init__()
        self.buf, self.n = buf, n

    def run(self) -> None:
        for i in range(self.n):
            self.buf.colocar(float(i))
        self.buf.colocar(None)  # sentinela de fim


class Consumidor(QThread):
    def __init__(self, buf: BufferLimitado) -> None:
        super().__init__()
        self.buf, self.soma, self.qtd = buf, 0.0, 0

    def run(self) -> None:
        while (item := self.buf.retirar()) is not None:
            self.soma += item
            self.qtd += 1


def main() -> int:
    app = QApplication(sys.argv)

    contador = Contador()
    threads = [Incrementador(contador, 50_000) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.wait()
    print(f"QMutex: contador = {contador.valor} (esperado {4 * 50_000})")

    tabela = TabelaPropriedades()
    leitores = [
        ThreadFuncao(lambda: [tabela.ler("aco_E_GPa") for _ in range(2_000)])
        for _ in range(3)
    ]
    escritor = ThreadFuncao(lambda: tabela.gravar("aco_E_GPa", 210.0))
    for t in (*leitores, escritor):
        t.start()
    for t in (*leitores, escritor):
        t.wait()
    print(f"QReadWriteLock: valor final = {tabela.ler('aco_E_GPa')} GPa")

    buf = BufferLimitado(capacidade=8)
    prod, cons = Produtor(buf, 10_000), Consumidor(buf)
    cons.start()
    prod.start()
    prod.wait()
    cons.wait()
    print(
        f"QWaitCondition: consumidos {cons.qtd} itens, soma = {cons.soma:.0f} "
        f"(esperado {sum(range(10_000))}); ocupação máxima = {buf.max_ocupacao} <= 8"
    )

    vagas = QSemaphore(2)  # no máximo 2 acessos simultâneos a um recurso
    print(
        f"QSemaphore: disponíveis = {vagas.available()}; tryAcquire(2) = "
        f"{vagas.tryAcquire(2)}; tryAcquire(1) = {vagas.tryAcquire(1)}"
    )
    vagas.release(2)
    print(f"QSemaphore: após release(2), disponíveis = {vagas.available()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
