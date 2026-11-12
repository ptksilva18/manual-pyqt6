# runner: ticks=40 env=QT_QUICK_CONTROLS_STYLE:Fusion
"""QQmlApplicationEngine: singleton Python, tipo registrado, propriedades notify e
sinais."""

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

AQUI = os.path.dirname(os.path.abspath(__file__))
BAR_PARA_PSI = 14.503773773


class Calculadora(QObject):
    unidadeChanged = pyqtSignal()
    aviso = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        self._unidade = "bar"

    @pyqtProperty(str, notify=unidadeChanged)
    def unidade(self) -> str:
        return self._unidade

    @pyqtSlot(float, result=float)
    def pressao(self, profundidade_m: float) -> float:
        p_bar = 1030.0 * 9.80665 * profundidade_m / 1e5 + 1.01325
        return p_bar * BAR_PARA_PSI if self._unidade == "psi" else p_bar

    @pyqtSlot()
    def alternarUnidade(self) -> None:
        self._unidade = "psi" if self._unidade == "bar" else "bar"
        self.unidadeChanged.emit()
        self.aviso.emit(f"Unidade alterada para {self._unidade}")


class Tanque(QObject):
    """Tipo instanciável em QML: import Engenharia 1.0 / Tanque { ... }."""

    diametroChanged = pyqtSignal()
    nivelChanged = pyqtSignal()
    volumeChanged = pyqtSignal()

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._d, self._h = 1.0, 0.0

    @pyqtProperty(float, notify=diametroChanged)
    def diametro(self) -> float:
        return self._d

    @diametro.setter
    def diametro(self, valor: float) -> None:
        if valor != self._d:
            self._d = valor
            self.diametroChanged.emit()
            self.volumeChanged.emit()

    @pyqtProperty(float, notify=nivelChanged)
    def nivel(self) -> float:
        return self._h

    @nivel.setter
    def nivel(self, valor: float) -> None:
        if valor != self._h:
            self._h = valor
            self.nivelChanged.emit()
            self.volumeChanged.emit()

    @pyqtProperty(float, notify=volumeChanged)
    def volume(self) -> float:
        return math.pi * self._d**2 / 4.0 * self._h


def main() -> int:
    app = QGuiApplication(sys.argv)
    calc = Calculadora()  # manter a referência: o QML não é dono do objeto
    qmlRegisterSingletonInstance("Engenharia", 1, 0, "Calculadora", calc)
    qmlRegisterType(Tanque, "Engenharia", 1, 0, "Tanque")
    motor = QQmlApplicationEngine()
    motor.warnings.connect(lambda erros: [print("QML:", e.toString()) for e in erros])
    motor.load(QUrl.fromLocalFile(os.path.join(AQUI, "c26_main.qml")))
    if not motor.rootObjects():
        return 1
    janela = motor.rootObjects()[0]

    def texto(nome: str) -> str:
        return janela.findChild(QObject, nome).property("text")

    print("Janela:", janela.property("title"))
    print(texto("rotuloPressao"), "|", texto("rotuloVolume"))
    janela.findChild(QObject, "prof").setProperty("value", 2000)
    tanque = janela.property("tanque")  # via "property alias" declarada no QML
    print(
        "Objeto criado pelo QML é instância de Tanque (Python):",
        isinstance(tanque, Tanque),
    )
    tanque.nivel = 4.0
    print(texto("rotuloPressao"), "|", texto("rotuloVolume"))
    QMetaObject.invokeMethod(
        janela.findChild(QObject, "botaoUnidade"),
        "click",
        Qt.ConnectionType.DirectConnection,
    )
    print(texto("rotuloPressao"), "|", texto("rotuloAviso"))
    QTimer.singleShot(300, app.quit)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
