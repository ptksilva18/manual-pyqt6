"""Serviço de análise em segundo plano (QThreadPool) com resultado entregue por sinal."""

from PyQt6.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal

from .dominio import Criterio, ErroDados, Leitura, analisar


class _Sinais(QObject):
    concluido = pyqtSignal(int, object)  # ensaio_id, Resultado
    falhou = pyqtSignal(int, str)


class _Tarefa(QRunnable):
    def __init__(
        self,
        ensaio_id: int,
        leituras: list[Leitura],
        criterio: Criterio,
        sinais: _Sinais,
    ) -> None:
        super().__init__()
        self.args = (ensaio_id, leituras, criterio)
        self.sinais = sinais

    def run(self) -> None:  # executa em uma thread do pool: nada de widgets aqui
        ensaio_id, leituras, criterio = self.args
        try:
            self.sinais.concluido.emit(ensaio_id, analisar(leituras, criterio))
        except ErroDados as exc:
            self.sinais.falhou.emit(ensaio_id, str(exc))


class ServicoAnalise(QObject):
    concluido = pyqtSignal(int, object)
    falhou = pyqtSignal(int, str)

    def __init__(self) -> None:
        super().__init__()
        self.pool = QThreadPool()
        self.pool.setMaxThreadCount(2)
        self._sinais = (
            _Sinais()
        )  # vive na thread da GUI: as emissões chegam enfileiradas
        self._sinais.concluido.connect(self.concluido)
        self._sinais.falhou.connect(self.falhou)

    def analisar(
        self, ensaio_id: int, leituras: list[Leitura], criterio: Criterio
    ) -> None:
        self.pool.start(_Tarefa(ensaio_id, list(leituras), criterio, self._sinais))

    def aguardar(self, ms: int = 5000) -> bool:
        return self.pool.waitForDone(ms)
