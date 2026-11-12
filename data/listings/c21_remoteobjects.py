# runner: ticks=100
"""QtRemoteObjects: um processo publica um QObject; outro usa uma réplica dinâmica.

Uso: python c21_remoteobjects.py            (fonte; inicia a réplica automaticamente)
     python c21_remoteobjects.py --replica  (réplica)
"""

import sys

from PyQt6.QtCore import (
    Q_ARG,
    QCoreApplication,
    QMetaObject,
    QObject,
    QProcess,
    Qt,
    QTimer,
    QUrl,
    pyqtProperty,
    pyqtSignal,
    pyqtSlot,
)
from PyQt6.QtRemoteObjects import (
    QRemoteObjectHost,
    QRemoteObjectNode,
    QRemoteObjectReplica,
)

ENDERECO = QUrl(
    "local:manual_pyqt6_medidor"
)  # local: = soquete local; tcp://host:porta também


class Medidor(QObject):
    pressaoChanged = pyqtSignal(float)

    def __init__(self) -> None:
        super().__init__()
        self._pressao = 100.0

    @pyqtProperty(float, notify=pressaoChanged)
    def pressao(self) -> float:
        return self._pressao

    @pressao.setter
    def pressao(self, valor: float) -> None:
        if valor != self._pressao:
            self._pressao = valor
            self.pressaoChanged.emit(valor)

    @pyqtSlot(float)
    def ajustar_referencia(self, valor: float) -> None:
        print(f"[fonte]   ajustar_referencia({valor}) chamado remotamente")
        self.pressao = valor


def fonte(app: QCoreApplication) -> int:
    medidor = Medidor()
    host = QRemoteObjectHost(ENDERECO)
    print("[fonte]   publicado:", host.enableRemoting(medidor, "Medidor"))
    proc = QProcess()
    proc.setProcessChannelMode(QProcess.ProcessChannelMode.ForwardedChannels)
    proc.finished.connect(
        lambda codigo, _status: (
            print(f"[fonte]   réplica terminou com código {codigo}"),
            app.quit(),
        )
    )
    proc.start(sys.executable, [__file__, "--replica"])
    QTimer.singleShot(1500, lambda: setattr(medidor, "pressao", 151.5))  # mudança local
    return app.exec()


def replica(app: QCoreApplication) -> int:
    no = QRemoteObjectNode()
    no.connectToNode(ENDERECO)
    rep = no.acquireDynamic(
        "Medidor"
    )  # sem arquivo .rep: interface descoberta em execução

    def inicializada() -> None:
        print(
            f"[réplica] estado {rep.state().name}; pressao = {rep.property('pressao')}"
        )
        rep.pressaoChanged.connect(lambda v: print(f"[réplica] pressaoChanged -> {v}"))
        QMetaObject.invokeMethod(
            rep,
            "ajustar_referencia",
            Qt.ConnectionType.DirectConnection,
            Q_ARG(float, 0.0),
        )

    rep.initialized.connect(inicializada)
    rep.stateChanged.connect(
        lambda novo, _ant: novo == QRemoteObjectReplica.State.Suspect
        and print("[réplica] fonte indisponível")
    )
    QTimer.singleShot(2500, app.quit)
    return app.exec()


if __name__ == "__main__":
    aplicacao = QCoreApplication(sys.argv)
    sys.exit(replica(aplicacao) if "--replica" in sys.argv else fonte(aplicacao))
