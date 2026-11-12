"""Custom signals: declaration, arguments, overloads and connections."""
import sys

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QApplication


class Sensor(QObject):
    # Signals are CLASS ATTRIBUTES; each instance receives its own "bound" signal
    readingChanged = pyqtSignal(float)               # one float argument
    alarm = pyqtSignal(str, float)                   # two arguments
    rawValue = pyqtSignal([int], [str])              # overloaded signal

    def __init__(self, tag: str, limit: float) -> None:
        super().__init__()
        self.tag, self.limit, self._value = tag, limit, 0.0

    def update(self, value: float) -> None:
        if value == self._value:
            return                                    # emits only when it changes
        self._value = value
        self.readingChanged.emit(value)
        if value > self.limit:
            self.alarm.emit(self.tag, value)


class Panel(QObject):
    @pyqtSlot(float)
    def display(self, v: float) -> None:
        print(f"panel: {v:.1f} bar")

    @pyqtSlot(str, float)
    def log_alarm(self, tag: str, v: float) -> None:
        print(f"ALARM at {tag}: {v:.1f} bar")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    sensor, panel = Sensor("PT-101", limit=300.0), Panel()

    sensor.readingChanged.connect(panel.display)      # method decorated as a slot
    sensor.alarm.connect(panel.log_alarm)
    sensor.readingChanged.connect(lambda v: print(f"log: {v}"))   # several receivers

    sensor.rawValue[int].connect(lambda n: print("raw int:", n))
    sensor.rawValue[str].connect(lambda s: print("raw str:", s))

    for v in (250.0, 250.0, 310.0):
        sensor.update(v)
    sensor.rawValue[int].emit(4095)
    sensor.rawValue[str].emit("0x0FFF")

    sensor.readingChanged.disconnect(panel.display)   # disconnects a specific receiver
    sensor.update(100.0)
