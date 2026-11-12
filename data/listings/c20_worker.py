# runner: ticks=80
"""Padrão worker com moveToThread(): progresso, resultado, erro, cancelamento e
encerramento."""

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


def nome_thread() -> str:
    return QThread.currentThread().objectName() or "sem nome"


class Integrador(QObject):
    """Integra f(x) = sin(x)^2 em [0, pi] pela regra do trapézio, em blocos."""

    progresso = pyqtSignal(int)
    resultado = pyqtSignal(float)
    cancelado = pyqtSignal()
    erro = pyqtSignal(str)
    finalizado = pyqtSignal()

    def __init__(self, n_blocos: int = 50, pontos_por_bloco: int = 2_000) -> None:
        super().__init__()
        self.n_blocos = n_blocos
        self.pontos = pontos_por_bloco

    @pyqtSlot()
    def executar(self) -> None:
        print(f"  executar() roda na thread: {nome_thread()}")
        try:
            n = self.n_blocos * self.pontos
            h = math.pi / n
            soma = 0.5 * (math.sin(0.0) ** 2 + math.sin(math.pi) ** 2)
            for b in range(self.n_blocos):
                if QThread.currentThread().isInterruptionRequested():
                    self.cancelado.emit()
                    return
                for i in range(b * self.pontos + 1, (b + 1) * self.pontos + 1):
                    if i < n:
                        soma += math.sin(i * h) ** 2
                time.sleep(0.004)  # simula E/S entre blocos
                self.progresso.emit(round(100 * (b + 1) / self.n_blocos))
            self.resultado.emit(soma * h)
        except Exception as exc:  # erros do worker viram sinal, nunca exceção perdida
            self.erro.emit(f"{type(exc).__name__}: {exc}")
        finally:
            self.finalizado.emit()


class Janela(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Worker com QThread")
        self.barra = QProgressBar()
        self.rotulo = QLabel("Pronto")
        self.bt_iniciar = QPushButton("Iniciar")
        self.bt_cancelar = QPushButton("Cancelar")
        self.bt_cancelar.setEnabled(False)
        botoes = QHBoxLayout()
        botoes.addWidget(self.bt_iniciar)
        botoes.addWidget(self.bt_cancelar)
        lay = QVBoxLayout(self)
        lay.addWidget(self.barra)
        lay.addWidget(self.rotulo)
        lay.addLayout(botoes)
        self.bt_iniciar.clicked.connect(self.iniciar)
        self.bt_cancelar.clicked.connect(self.cancelar)
        self.thread: QThread | None = None
        self.execucoes = 0

    def iniciar(self) -> None:
        self.execucoes += 1
        self.thread = QThread()
        self.thread.setObjectName(f"integrador-{self.execucoes}")
        self.worker = Integrador()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.executar)
        self.worker.progresso.connect(self.ao_progresso)
        self.worker.resultado.connect(self.ao_resultado)
        self.worker.cancelado.connect(lambda: self.rotulo.setText("Cancelado"))
        self.worker.erro.connect(self.rotulo.setText)
        self.worker.finalizado.connect(self.thread.quit)
        self.worker.finalizado.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.ao_terminar)
        self.thread.finished.connect(self.thread.deleteLater)
        self.bt_iniciar.setEnabled(False)
        self.bt_cancelar.setEnabled(True)
        print(f"Execução {self.execucoes}: iniciar() roda na thread: {nome_thread()}")
        self.thread.start()

    def cancelar(self) -> None:
        if self.thread is not None:
            # pedido cooperativo: o worker decide quando parar
            self.thread.requestInterruption()
            self.bt_cancelar.setEnabled(False)
            self.rotulo.setText("Cancelando...")

    def ao_progresso(self, pct: int) -> None:
        self.barra.setValue(pct)
        if self.execucoes == 2 and pct >= 40 and self.bt_cancelar.isEnabled():
            print(f"  usuário cancela em {pct} % (slot na thread: {nome_thread()})")
            self.bt_cancelar.click()

    def ao_resultado(self, valor: float) -> None:
        self.rotulo.setText(f"Integral = {valor:.10f}")
        print(f"  resultado = {valor:.10f} (exato: pi/2 = {math.pi / 2:.10f})")

    def ao_terminar(self) -> None:
        print(
            f"  thread terminada; rótulo: {self.rotulo.text()!r}; barra: "
            f"{self.barra.value()} %"
        )
        self.thread = None
        self.bt_iniciar.setEnabled(True)
        self.bt_cancelar.setEnabled(False)
        if self.execucoes == 1:
            self.bt_iniciar.click()
        else:
            QApplication.instance().quit()

    def closeEvent(self, event) -> None:  # encerramento seguro ao fechar a janela
        if self.thread is not None:
            self.thread.requestInterruption()
            self.thread.quit()
            self.thread.wait()
        super().closeEvent(event)


def main() -> int:
    app = QApplication(sys.argv)
    QThread.currentThread().setObjectName("GUI")
    janela = Janela()
    janela.show()
    janela.bt_iniciar.click()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
