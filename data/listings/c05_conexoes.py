"""Tipos de conexão, UniqueConnection, SingleShotConnection e bloqueio de sinais."""
import sys

from PyQt6.QtCore import QObject, QSignalBlocker, Qt, QTimer, pyqtSignal
from PyQt6.QtWidgets import QApplication


class Fonte(QObject):
    disparo = pyqtSignal(int)


def receptor(n: int) -> None:
    print(f"  recebido {n}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    f = Fonte()

    print("1) UniqueConnection impede duplicatas:")
    f.disparo.connect(receptor, Qt.ConnectionType.UniqueConnection)
    try:
        f.disparo.connect(receptor, Qt.ConnectionType.UniqueConnection)
    except TypeError as e:
        print("  segunda conexão recusada:", e)
    f.disparo.emit(1)
    f.disparo.disconnect()                       # remove todas as conexões

    print("2) SingleShotConnection desconecta após a 1ª emissão:")
    f.disparo.connect(receptor, Qt.ConnectionType.SingleShotConnection)
    f.disparo.emit(2)
    f.disparo.emit(3)                            # ninguém recebe

    print("3) blockSignals / QSignalBlocker:")
    f.disparo.connect(receptor)
    with QSignalBlocker(f):                      # bloqueia dentro do bloco 'with'
        f.disparo.emit(4)
    f.disparo.emit(5)

    print("4) QueuedConnection: entrega só quando o event loop roda:")
    f.disparo.disconnect()
    f.disparo.connect(receptor, Qt.ConnectionType.QueuedConnection)
    f.disparo.emit(6)
    print("  (emit retornou antes da entrega)")
    QTimer.singleShot(0, app.quit)
    app.exec()
