# runner: ticks=40 env=QT_QUICK_CONTROLS_STYLE:Fusion
"""QQmlApplicationEngine: Python singleton, registered type, notify properties and
signals."""

import math
import os
import sys

from PyQt6.QtCore import (
    QMetaObject,
    QObject,
    Qt,
    QTimer,
    QUrl,
    pyqtProperty,
    pyqtSignal,
    pyqtSlot,
)
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import (
    QQmlApplicationEngine,
    qmlRegisterSingletonInstance,
    qmlRegisterType,
)

HERE = os.path.dirname(os.path.abspath(__file__))
BAR_TO_PSI = 14.503773773


class Calculator(QObject):
    unitChanged = pyqtSignal()
    notice = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        self._unit = "bar"

    @pyqtProperty(str, notify=unitChanged)
    def unit(self) -> str:
        return self._unit

    @pyqtSlot(float, result=float)
    def pressure(self, depth_m: float) -> float:
        p_bar = 1030.0 * 9.80665 * depth_m / 1e5 + 1.01325
        return p_bar * BAR_TO_PSI if self._unit == "psi" else p_bar

    @pyqtSlot()
    def toggleUnit(self) -> None:
        self._unit = "psi" if self._unit == "bar" else "bar"
        self.unitChanged.emit()
        self.notice.emit(f"Unit changed to {self._unit}")


class Tank(QObject):
    """Type that can be instantiated in QML: import Engineering 1.0 / Tank { ... }."""

    diameterChanged = pyqtSignal()
    levelChanged = pyqtSignal()
    volumeChanged = pyqtSignal()

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._d, self._h = 1.0, 0.0

    @pyqtProperty(float, notify=diameterChanged)
    def diameter(self) -> float:
        return self._d

    @diameter.setter
    def diameter(self, value: float) -> None:
        if value != self._d:
            self._d = value
            self.diameterChanged.emit()
            self.volumeChanged.emit()

    @pyqtProperty(float, notify=levelChanged)
    def level(self) -> float:
        return self._h

    @level.setter
    def level(self, value: float) -> None:
        if value != self._h:
            self._h = value
            self.levelChanged.emit()
            self.volumeChanged.emit()

    @pyqtProperty(float, notify=volumeChanged)
    def volume(self) -> float:
        return math.pi * self._d**2 / 4.0 * self._h


def main() -> int:
    app = QGuiApplication(sys.argv)
    calc = Calculator()  # keep the reference: QML does not own the object
    qmlRegisterSingletonInstance("Engineering", 1, 0, "Calculator", calc)
    qmlRegisterType(Tank, "Engineering", 1, 0, "Tank")
    engine = QQmlApplicationEngine()
    engine.warnings.connect(lambda errors: [print("QML:", e.toString()) for e in errors])
    engine.load(QUrl.fromLocalFile(os.path.join(HERE, "c26_main.qml")))
    if not engine.rootObjects():
        return 1
    window = engine.rootObjects()[0]

    def text(name: str) -> str:
        return window.findChild(QObject, name).property("text")

    print("Window:", window.property("title"))
    print(text("pressureLabel"), "|", text("volumeLabel"))
    window.findChild(QObject, "depth").setProperty("value", 2000)
    tank = window.property("tank")  # via the "property QtObject" declared in QML
    print(
        "Object created by QML is an instance of Tank (Python):",
        isinstance(tank, Tank),
    )
    tank.level = 4.0
    print(text("pressureLabel"), "|", text("volumeLabel"))
    QMetaObject.invokeMethod(
        window.findChild(QObject, "unitButton"),
        "click",
        Qt.ConnectionType.DirectConnection,
    )
    print(text("pressureLabel"), "|", text("noticeLabel"))
    QTimer.singleShot(300, app.quit)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
