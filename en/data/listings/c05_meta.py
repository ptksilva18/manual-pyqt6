"""Dynamic properties and introspection with QMetaObject."""
import sys

from PyQt6.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QApplication, QPushButton


class Valve(QObject):
    openingChanged = pyqtSignal(int)

    def __init__(self) -> None:
        super().__init__()
        self._opening = 0

    @pyqtProperty(int, notify=openingChanged)
    def opening(self) -> int:
        return self._opening

    @opening.setter
    def opening(self, pct: int) -> None:
        self._opening = max(0, min(100, pct))
        self.openingChanged.emit(self._opening)

    @pyqtSlot()
    def close(self) -> None:
        self.opening = 0


if __name__ == "__main__":
    app = QApplication(sys.argv)
    v = Valve()
    mo = v.metaObject()
    print("class:", mo.className())
    span = range(mo.propertyOffset(), mo.propertyCount())
    own = [mo.property(i).name() for i in span]
    print("declared properties:", own)
    methods = [bytes(mo.method(i).methodSignature()).decode()
               for i in range(mo.methodOffset(), mo.methodCount())]
    print("declared signals/slots:", methods)

    v.setProperty("opening", 150)                  # via the setter (clamped to 100)
    print("opening =", v.opening)
    # Dynamic property: created at run time, without a declaration in the class
    button = QPushButton("Run")
    button.setProperty("dangerous", True)         # useful in style sheets (QSS)
    names = [bytes(n).decode() for n in button.dynamicPropertyNames()]
    print("button's dynamic properties:", names)
    print("dangerous =", button.property("dangerous"))
