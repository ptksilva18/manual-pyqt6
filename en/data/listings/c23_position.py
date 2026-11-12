# runner: ticks=150
"""QtPositioning: NMEA source (file in simulation mode), QGeoCoordinate and geodesy."""

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

HERE = os.path.dirname(os.path.abspath(__file__))
PLATFORM = QGeoCoordinate(-22.49990, -39.99988)  # fictitious reference point
FORMAT = QGeoCoordinate.CoordinateFormat.DegreesMinutesWithHemisphere


def main() -> int:
    app = QApplication(sys.argv)
    print("Available position sources:", QGeoPositionInfoSource.availableSources())
    nmea_file = QFile(os.path.join(HERE, "resources", "route.nmea"))
    nmea_file.open(QIODevice.OpenModeFlag.ReadOnly)
    # SimulationMode replays the file following the sentence timestamps (1 s here).
    source = QNmeaPositionInfoSource(QNmeaPositionInfoSource.UpdateMode.SimulationMode)
    source.setDevice(nmea_file)  # in the field: QSerialPort or QTcpSocket (GNSS receiver)
    zone = QGeoCircle(PLATFORM, 10.0)  # 10 m radius
    positions: list[QGeoCoordinate] = []

    def update(info: QGeoPositionInfo) -> None:
        c = info.coordinate()
        positions.append(c)
        speed = info.attribute(QGeoPositionInfo.Attribute.GroundSpeed)  # m/s
        course = info.attribute(QGeoPositionInfo.Attribute.Direction)  # degrees
        dist = c.distanceTo(PLATFORM)
        print(
            f"{info.timestamp().toString('HH:mm:ss')} {c.toString(FORMAT)}"
            f" | {speed / 0.514444:3.1f} kn, course {course:4.1f}° | to the reference "
            f"{dist:5.1f} m"
            f"{'  [10 m zone]' if zone.contains(c) else ''}"
        )

    source.positionUpdated.connect(update)
    source.errorOccurred.connect(lambda e: print("error:", e.name))

    def summary() -> None:
        source.stopUpdates()
        a, b = positions[0], positions[-1]
        print(
            f"{len(positions)} positions; displacement {a.distanceTo(b):.1f} m, "
            f"azimuth {a.azimuthTo(b):.1f}°"
        )
        mid = a.atDistanceAndAzimuth(a.distanceTo(b) / 2, a.azimuthTo(b))
        print(f"Midpoint: {mid.latitude():.6f}, {mid.longitude():.6f}")
        app.quit()

    source.startUpdates()
    QTimer.singleShot(8500, summary)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
