"""@property (Python) versus pyqtProperty (visible to the meta-object system)."""
import sys

from PyQt6.QtCore import QObject, pyqtProperty, pyqtSignal
from PyQt6.QtWidgets import QApplication


class Tank(QObject):
    levelChanged = pyqtSignal(float)

    def __init__(self, capacity_m3: float) -> None:
        super().__init__()
        self._capacity = capacity_m3
        self._level = 0.0

    @property                      # exists only on the Python side
    def capacity(self) -> float:
        return self._capacity

    def _get_level(self) -> float:
        return self._level

    def _set_level(self, value: float) -> None:
        value = max(0.0, min(value, self._capacity))
        if value != self._level:
            self._level = value
            self.levelChanged.emit(value)

    # registered in the QMetaObject: reachable by property()/setProperty(), QML, Designer
    level = pyqtProperty(float, fget=_get_level, fset=_set_level, notify=levelChanged)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    t = Tank(capacity_m3=50.0)
    t.levelChanged.connect(lambda v: print(f"signal levelChanged -> {v}"))
    t.level = 12.5                       # normal Python use
    t.setProperty("level", 80.0)         # through the meta-object (clamped to capacity)
    print("property('level') =", t.property("level"))
    print("property('capacity') =", t.property("capacity"))   # @property: invisible
    mo = t.metaObject()
    print("'level' in the QMetaObject?", mo.indexOfProperty("level") >= 0)
    print("'capacity' in the QMetaObject?", mo.indexOfProperty("capacity") >= 0)
