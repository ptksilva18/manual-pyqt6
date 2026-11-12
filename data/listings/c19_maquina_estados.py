"""QStateMachine: estados, transições por sinal, propriedades atribuídas e histórico."""

import sys

from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from PyQt6.QtStateMachine import QFinalState, QHistoryState, QState, QStateMachine
from PyQt6.QtWidgets import QApplication, QLabel


class Painel(QObject):
    iniciar = pyqtSignal()
    pausar = pyqtSignal()
    retomar = pyqtSignal()
    concluir = pyqtSignal()
    avancar = pyqtSignal()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui, rotulo = Painel(), QLabel()
    m = QStateMachine()

    parado = QState(m)
    # estado composto (com subestados)
    ensaio = QState(m)
    pressurizando = QState(ensaio)
    estabilizando = QState(ensaio)
    ensaio.setInitialState(pressurizando)
    historico = QHistoryState(ensaio)  # lembra o subestado ativo
    pausado = QState(m)
    fim = QFinalState(m)

    parado.assignProperty(rotulo, "text", "Parado")  # propriedades por estado
    pressurizando.assignProperty(rotulo, "text", "Pressurizando")
    estabilizando.assignProperty(rotulo, "text", "Estabilizando")
    pausado.assignProperty(rotulo, "text", "Pausado")

    parado.addTransition(ui.iniciar, ensaio)
    pressurizando.addTransition(ui.avancar, estabilizando)
    ensaio.addTransition(ui.pausar, pausado)
    pausado.addTransition(ui.retomar, historico)  # volta ao subestado anterior
    ensaio.addTransition(ui.concluir, fim)
    m.setInitialState(parado)

    for nome, estado in (
        ("parado", parado),
        ("pressurizando", pressurizando),
        ("estabilizando", estabilizando),
        ("pausado", pausado),
    ):
        estado.entered.connect(
            lambda n=nome: print("entrou:", n, "| rótulo:", rotulo.text())
        )
    m.finished.connect(lambda: (print("máquina finalizada"), app.quit()))

    roteiro = [ui.iniciar, ui.avancar, ui.pausar, ui.retomar, ui.concluir]
    for i, sinal in enumerate(roteiro, start=1):
        QTimer.singleShot(50 * i, sinal.emit)
    # assíncrona: roda no event loop
    m.start()
    app.exec()
