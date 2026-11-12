# runner: ticks=150
"""QtPositioning: fonte NMEA (arquivo em modo simulação), QGeoCoordinate e geodésia."""

import os
import sys

from PyQt6.QtCore import QFile, QIODevice, QTimer
from PyQt6.QtPositioning import (
    QGeoCircle,
    QGeoCoordinate,
    QGeoPositionInfo,
    QGeoPositionInfoSource,
    QNmeaPositionInfoSource,
)
from PyQt6.QtWidgets import QApplication

AQUI = os.path.dirname(os.path.abspath(__file__))
PLATAFORMA = QGeoCoordinate(-22.49990, -39.99988)  # ponto de referência fictício
FORMATO = QGeoCoordinate.CoordinateFormat.DegreesMinutesWithHemisphere


def main() -> int:
    app = QApplication(sys.argv)
    print("Fontes de posição disponíveis:", QGeoPositionInfoSource.availableSources())
    arquivo = QFile(os.path.join(AQUI, "resources", "trajeto.nmea"))
    arquivo.open(QIODevice.OpenModeFlag.ReadOnly)
    # SimulationMode reproduz o arquivo respeitando os horários das sentenças (1 s aqui).
    fonte = QNmeaPositionInfoSource(QNmeaPositionInfoSource.UpdateMode.SimulationMode)
    fonte.setDevice(arquivo)  # em campo: QSerialPort ou QTcpSocket com o receptor GNSS
    zona = QGeoCircle(PLATAFORMA, 10.0)  # raio de 10 m
    posicoes: list[QGeoCoordinate] = []

    def atualizar(info: QGeoPositionInfo) -> None:
        c = info.coordinate()
        posicoes.append(c)
        vel = info.attribute(QGeoPositionInfo.Attribute.GroundSpeed)  # m/s
        rumo = info.attribute(QGeoPositionInfo.Attribute.Direction)  # graus
        dist = c.distanceTo(PLATAFORMA)
        print(
            f"{info.timestamp().toString('HH:mm:ss')} {c.toString(FORMATO)}"
            f" | {vel / 0.514444:3.1f} nós, rumo {rumo:4.1f}° | até a referência "
            f"{dist:5.1f} m"
            f"{'  [zona de 10 m]' if zona.contains(c) else ''}"
        )

    fonte.positionUpdated.connect(atualizar)
    fonte.errorOccurred.connect(lambda e: print("erro:", e.name))

    def resumo() -> None:
        fonte.stopUpdates()
        a, b = posicoes[0], posicoes[-1]
        print(
            f"{len(posicoes)} posições; deslocamento {a.distanceTo(b):.1f} m, "
            f"azimute {a.azimuthTo(b):.1f}°"
        )
        meio = a.atDistanceAndAzimuth(a.distanceTo(b) / 2, a.azimuthTo(b))
        print(f"Ponto médio: {meio.latitude():.6f}, {meio.longitude():.6f}")
        app.quit()

    fonte.startUpdates()
    QTimer.singleShot(8500, resumo)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
