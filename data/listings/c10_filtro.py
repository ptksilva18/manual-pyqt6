"""Filtro de eventos: um objeto observa e intercepta eventos de outro."""
import sys

from PyQt6.QtCore import QEvent, QObject
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication, QLineEdit


class SomenteLetras(QObject):
    """Bloqueia dígitos em qualquer widget onde for instalado."""

    def eventFilter(self, obj: QObject, ev: QEvent) -> bool:
        if ev.type() == QEvent.Type.KeyPress and ev.text().isdigit():
            print(f"bloqueado: {ev.text()!r} em {obj.objectName()}")
            return True              # True = consumido (não chega ao alvo)
        if ev.type() == QEvent.Type.FocusIn:
            print(f"{obj.objectName()} recebeu foco")
        return super().eventFilter(obj, ev)   # False = segue o caminho normal


if __name__ == "__main__":
    app = QApplication(sys.argv)
    campo = QLineEdit(objectName="campoTag")
    filtro = SomenteLetras(campo)             # o filtro tem pai: não será coletado
    campo.installEventFilter(filtro)
    campo.show()
    QTest.qWaitForWindowExposed(campo)
    campo.setFocus()
    app.processEvents()
    QTest.keyClicks(campo, "PT1x0")
    print("texto final:", campo.text())
    campo.removeEventFilter(filtro)
    QTest.keyClicks(campo, "9")
    print("sem filtro:", campo.text())
