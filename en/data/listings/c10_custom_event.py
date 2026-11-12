"""Custom events: registerEventType, postEvent (asynchronous) and sendEvent."""
import sys

from PyQt6.QtCore import QCoreApplication, QEvent, QObject, QTimer
from PyQt6.QtWidgets import QApplication

MEASUREMENT_TYPE = QEvent.Type(QEvent.registerEventType())   # free id >= QEvent.User


class MeasurementEvent(QEvent):
    def __init__(self, value: float) -> None:
        super().__init__(MEASUREMENT_TYPE)
        self.value = value


class Recorder(QObject):
    def customEvent(self, ev: QEvent) -> None:          # receives types >= QEvent.User
        if ev.type() == MEASUREMENT_TYPE:
            print(f"customEvent: measurement {ev.value}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    rec = Recorder()
    print("registered type >= User?", MEASUREMENT_TYPE.value >= QEvent.Type.User.value)
    QCoreApplication.postEvent(rec, MeasurementEvent(1.0))  # queued: delivered later
    print("postEvent returned")
    QCoreApplication.sendEvent(rec, MeasurementEvent(2.0))  # synchronous: delivered now
    print("sendEvent returned")
    QTimer.singleShot(0, app.quit)
    app.exec()
