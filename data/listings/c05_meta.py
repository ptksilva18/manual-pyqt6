"""Propriedades dinâmicas e introspecção com QMetaObject."""
import sys

from PyQt6.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QApplication, QPushButton


class Valvula(QObject):
    aberturaChanged = pyqtSignal(int)

    def __init__(self) -> None:
        super().__init__()
        self._abertura = 0

    @pyqtProperty(int, notify=aberturaChanged)
    def abertura(self) -> int:
        return self._abertura

    @abertura.setter
    def abertura(self, pct: int) -> None:
        self._abertura = max(0, min(100, pct))
        self.aberturaChanged.emit(self._abertura)

    @pyqtSlot()
    def fechar(self) -> None:
        self.abertura = 0


if __name__ == "__main__":
    app = QApplication(sys.argv)
    v = Valvula()
    mo = v.metaObject()
    print("classe:", mo.className())
    faixa = range(mo.propertyOffset(), mo.propertyCount())
    proprias = [mo.property(i).name() for i in faixa]
    print("propriedades declaradas:", proprias)
    metodos = [bytes(mo.method(i).methodSignature()).decode()
               for i in range(mo.methodOffset(), mo.methodCount())]
    print("sinais/slots declarados:", metodos)

    v.setProperty("abertura", 150)                 # passa pelo setter (limita a 100)
    print("abertura =", v.abertura)
    # Propriedade dinâmica: criada em tempo de execução, sem declaração na classe
    botao = QPushButton("Executar")
    botao.setProperty("perigoso", True)           # útil em folhas de estilo (QSS)
    nomes = [bytes(n).decode() for n in botao.dynamicPropertyNames()]
    print("dinâmicas do botão:", nomes)
    print("perigoso =", botao.property("perigoso"))
