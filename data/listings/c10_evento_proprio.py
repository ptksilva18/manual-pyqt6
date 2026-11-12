"""Eventos personalizados: registerEventType, postEvent (assíncrono) e sendEvent."""
import sys

from PyQt6.QtCore import QCoreApplication, QEvent, QObject, QTimer
from PyQt6.QtWidgets import QApplication

TIPO_MEDICAO = QEvent.Type(QEvent.registerEventType())   # id livre >= QEvent.User


class EventoMedicao(QEvent):
    def __init__(self, valor: float) -> None:
        super().__init__(TIPO_MEDICAO)
        self.valor = valor


class Registrador(QObject):
    def customEvent(self, ev: QEvent) -> None:          # recebe tipos >= QEvent.User
        if ev.type() == TIPO_MEDICAO:
            print(f"customEvent: medição {ev.valor}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    reg = Registrador()
    print("tipo registrado >= User?", TIPO_MEDICAO.value >= QEvent.Type.User.value)
    QCoreApplication.postEvent(reg, EventoMedicao(1.0))  # enfileirado: entregue depois
    print("postEvent retornou")
    QCoreApplication.sendEvent(reg, EventoMedicao(2.0))  # síncrono: entregue já
    print("sendEvent retornou")
    QTimer.singleShot(0, app.quit)
    app.exec()
