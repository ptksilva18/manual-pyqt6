"""Connection types, UniqueConnection, SingleShotConnection and signal blocking."""
import sys

from PyQt6.QtCore import QObject, QSignalBlocker, Qt, QTimer, pyqtSignal
from PyQt6.QtWidgets import QApplication


class Source(QObject):
    fired = pyqtSignal(int)


def receiver(n: int) -> None:
    print(f"  received {n}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    s = Source()

    print("1) UniqueConnection prevents duplicates:")
    s.fired.connect(receiver, Qt.ConnectionType.UniqueConnection)
    try:
        s.fired.connect(receiver, Qt.ConnectionType.UniqueConnection)
    except TypeError as e:
        print("  second connection refused:", e)
    s.fired.emit(1)
    s.fired.disconnect()                         # removes all connections

    print("2) SingleShotConnection disconnects after the 1st emission:")
    s.fired.connect(receiver, Qt.ConnectionType.SingleShotConnection)
    s.fired.emit(2)
    s.fired.emit(3)                              # nobody receives it

    print("3) blockSignals / QSignalBlocker:")
    s.fired.connect(receiver)
    with QSignalBlocker(s):                      # blocks inside the 'with' block
        s.fired.emit(4)
    s.fired.emit(5)

    print("4) QueuedConnection: delivered only when the event loop runs:")
    s.fired.disconnect()
    s.fired.connect(receiver, Qt.ConnectionType.QueuedConnection)
    s.fired.emit(6)
    print("  (emit returned before the delivery)")
    QTimer.singleShot(0, app.quit)
    app.exec()
