"""@property (Python) versus pyqtProperty (visível ao sistema de metaobjetos)."""
import sys

from PyQt6.QtCore import QObject, pyqtProperty, pyqtSignal
from PyQt6.QtWidgets import QApplication


class Tanque(QObject):
    nivelChanged = pyqtSignal(float)

    def __init__(self, capacidade_m3: float) -> None:
        super().__init__()
        self._capacidade = capacidade_m3
        self._nivel = 0.0

    @property                      # só existe no lado Python
    def capacidade(self) -> float:
        return self._capacidade

    def _get_nivel(self) -> float:
        return self._nivel

    def _set_nivel(self, valor: float) -> None:
        valor = max(0.0, min(valor, self._capacidade))
        if valor != self._nivel:
            self._nivel = valor
            self.nivelChanged.emit(valor)

    # registrada no QMetaObject: acessível por property()/setProperty(), QML, Designer
    nivel = pyqtProperty(float, fget=_get_nivel, fset=_set_nivel, notify=nivelChanged)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    t = Tanque(capacidade_m3=50.0)
    t.nivelChanged.connect(lambda v: print(f"sinal nivelChanged -> {v}"))
    t.nivel = 12.5                       # uso Python normal
    t.setProperty("nivel", 80.0)         # via metaobjeto (limitado à capacidade)
    print("property('nivel') =", t.property("nivel"))
    print("property('capacidade') =", t.property("capacidade"))   # @property: invisível
    mo = t.metaObject()
    print("'nivel' no QMetaObject?", mo.indexOfProperty("nivel") >= 0)
    print("'capacidade' no QMetaObject?", mo.indexOfProperty("capacidade") >= 0)
