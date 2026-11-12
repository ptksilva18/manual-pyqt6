"""QTimer (periodic and singleShot), QElapsedTimer and QBasicTimer."""
import sys

from PyQt6.QtCore import QBasicTimer, QElapsedTimer, QObject, Qt, QTimer
from PyQt6.QtWidgets import QApplication


class Counter(QObject):
    """Uses QBasicTimer + timerEvent(): lightweight, no signals."""

    def __init__(self) -> None:
        super().__init__()
        self.ticks = 0
        self.timer = QBasicTimer()
        self.timer.start(20, Qt.TimerType.PreciseTimer, self)

    def timerEvent(self, event) -> None:
        if event.timerId() == self.timer.timerId():
            self.ticks += 1
            if self.ticks == 3:
                self.timer.stop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    clock = QElapsedTimer()
    clock.start()
    readings: list[int] = []

    periodic = QTimer()
    periodic.setInterval(50)                        # milliseconds
    periodic.timeout.connect(lambda: readings.append(len(readings) + 1))
    periodic.start()

    counter = Counter()

    def finish() -> None:
        periodic.stop()
        print(f"periodic readings: {readings}")
        print(f"QBasicTimer: {counter.ticks} ticks")
        print(f"elapsed time >= 260 ms? {clock.elapsed() >= 260}")
        app.quit()

    QTimer.singleShot(260, finish)                  # fires a single time
    app.exec()
