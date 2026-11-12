"""QTimer (periódico e singleShot), QElapsedTimer e QBasicTimer."""
import sys

from PyQt6.QtCore import QBasicTimer, QElapsedTimer, QObject, Qt, QTimer
from PyQt6.QtWidgets import QApplication


class Contador(QObject):
    """Usa QBasicTimer + timerEvent(): leve, sem sinais."""

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
    relogio = QElapsedTimer()
    relogio.start()
    leituras: list[int] = []

    periodico = QTimer()
    periodico.setInterval(50)                       # milissegundos
    periodico.timeout.connect(lambda: leituras.append(len(leituras) + 1))
    periodico.start()

    contador = Contador()

    def finalizar() -> None:
        periodico.stop()
        print(f"leituras periódicas: {leituras}")
        print(f"QBasicTimer: {contador.ticks} ticks")
        print(f"tempo decorrido >= 260 ms? {relogio.elapsed() >= 260}")
        app.quit()

    QTimer.singleShot(260, finalizar)               # dispara uma única vez
    app.exec()
