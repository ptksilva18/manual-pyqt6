# runner: ticks=100
"""QtRemoteObjects: one process publishes a QObject; another uses a dynamic replica.

Usage: python c21_remoteobjects.py            (source; starts the replica automatically)
       python c21_remoteobjects.py --replica  (replica)
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

ADDRESS = QUrl(
    "local:pyqt6_manual_meter"
)  # local: = local socket; tcp://host:port also works


class Meter(QObject):
    pressureChanged = pyqtSignal(float)

    def __init__(self) -> None:
        super().__init__()
        self._pressure = 100.0

    @pyqtProperty(float, notify=pressureChanged)
    def pressure(self) -> float:
        return self._pressure

    @pressure.setter
    def pressure(self, value: float) -> None:
        if value != self._pressure:
            self._pressure = value
            self.pressureChanged.emit(value)

    @pyqtSlot(float)
    def set_reference(self, value: float) -> None:
        print(f"[source]  set_reference({value}) called remotely")
        self.pressure = value


def source(app: QCoreApplication) -> int:
    meter = Meter()
    host = QRemoteObjectHost(ADDRESS)
    print("[source]  published:", host.enableRemoting(meter, "Meter"))
    proc = QProcess()
    proc.setProcessChannelMode(QProcess.ProcessChannelMode.ForwardedChannels)
    proc.finished.connect(
        lambda code, _status: (
            print(f"[source]  replica ended with code {code}"),
            app.quit(),
        )
    )
    proc.start(sys.executable, [__file__, "--replica"])
    QTimer.singleShot(1500, lambda: setattr(meter, "pressure", 151.5))  # local change
    return app.exec()


def replica(app: QCoreApplication) -> int:
    node = QRemoteObjectNode()
    node.connectToNode(ADDRESS)
    rep = node.acquireDynamic(
        "Meter"
    )  # no .rep file: interface discovered at run time

    def initialized() -> None:
        print(
            f"[replica] state {rep.state().name}; pressure = {rep.property('pressure')}"
        )
        rep.pressureChanged.connect(lambda v: print(f"[replica] pressureChanged -> {v}"))
        QMetaObject.invokeMethod(
            rep,
            "set_reference",
            Qt.ConnectionType.DirectConnection,
            Q_ARG(float, 0.0),
        )

    rep.initialized.connect(initialized)
    rep.stateChanged.connect(
        lambda new, _old: new == QRemoteObjectReplica.State.Suspect
        and print("[replica] source unavailable")
    )
    QTimer.singleShot(2500, app.quit)
    return app.exec()


if __name__ == "__main__":
    application = QCoreApplication(sys.argv)
    sys.exit(replica(application) if "--replica" in sys.argv else source(application))
