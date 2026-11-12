# runner: ticks=40
"""QtSensors: descoberta de backends, conexão, leitura e filtros (com ausência
tratada)."""

import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtSensors import QAccelerometer, QAccelerometerFilter, QSensor
from PyQt6.QtWidgets import QApplication


class FiltroImpacto(QAccelerometerFilter):
    """Deixa passar só leituras com |a| acima do limite (outras são descartadas)."""

    def __init__(self, limite_ms2: float) -> None:
        super().__init__()
        self.limite = limite_ms2

    def filter(self, leitura) -> bool:
        a = (leitura.x() ** 2 + leitura.y() ** 2 + leitura.z() ** 2) ** 0.5
        return a > self.limite


def main() -> int:
    app = QApplication(sys.argv)
    tipos = QSensor.sensorTypes()
    print(
        "Tipos de sensor com backend nesta máquina:", [bytes(t).decode() for t in tipos]
    )
    acel = QAccelerometer()
    acel.setAccelerationMode(QAccelerometer.AccelerationMode.User)  # remove a gravidade
    filtro = FiltroImpacto(limite_ms2=15.0)
    acel.addFilter(filtro)
    acel.readingChanged.connect(
        lambda: print(
            "leitura:", acel.reading().x(), acel.reading().y(), acel.reading().z()
        )
    )
    if not acel.connectToBackend():
        print(
            "Acelerômetro indisponível: connectToBackend() = False — a interface deve "
            "ocultar a função ou usar outra fonte de dados."
        )
        QTimer.singleShot(0, app.quit)
    else:
        acel.setDataRate(50)  # Hz, se o backend permitir
        print(
            "Iniciado:",
            acel.start(),
            "| identificador:",
            bytes(acel.identifier()).decode(),
        )
        QTimer.singleShot(2000, app.quit)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
