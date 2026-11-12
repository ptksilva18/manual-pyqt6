# runner: ticks=40
"""QtSensors: backend discovery, connection, reading and filters (with absence
handled)."""

import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtSensors import QAccelerometer, QAccelerometerFilter, QSensor
from PyQt6.QtWidgets import QApplication


class ImpactFilter(QAccelerometerFilter):
    """Lets through only readings with |a| above the limit (others are discarded)."""

    def __init__(self, limit_ms2: float) -> None:
        super().__init__()
        self.limit = limit_ms2

    def filter(self, reading) -> bool:
        a = (reading.x() ** 2 + reading.y() ** 2 + reading.z() ** 2) ** 0.5
        return a > self.limit


def main() -> int:
    app = QApplication(sys.argv)
    types = QSensor.sensorTypes()
    print(
        "Sensor types with a backend on this machine:", [bytes(t).decode() for t in types]
    )
    accel = QAccelerometer()
    accel.setAccelerationMode(QAccelerometer.AccelerationMode.User)  # removes gravity
    impact_filter = ImpactFilter(limit_ms2=15.0)
    accel.addFilter(impact_filter)
    accel.readingChanged.connect(
        lambda: print(
            "reading:", accel.reading().x(), accel.reading().y(), accel.reading().z()
        )
    )
    if not accel.connectToBackend():
        print(
            "Accelerometer unavailable: connectToBackend() = False — the interface "
            "should hide the feature or use another data source."
        )
        QTimer.singleShot(0, app.quit)
    else:
        accel.setDataRate(50)  # Hz, if the backend allows it
        print(
            "Started:",
            accel.start(),
            "| identifier:",
            bytes(accel.identifier()).decode(),
        )
        QTimer.singleShot(2000, app.quit)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
