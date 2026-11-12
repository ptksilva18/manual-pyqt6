"""Sinais personalizados: declaração, argumentos, sobrecarga e conexões."""
import sys

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QApplication


class Sensor(QObject):
    # Sinais são ATRIBUTOS DE CLASSE; cada instância recebe seu sinal "ligado"
    leituraMudou = pyqtSignal(float)                 # um argumento float
    alarme = pyqtSignal(str, float)                  # dois argumentos
    valorBruto = pyqtSignal([int], [str])            # sinal sobrecarregado

    def __init__(self, tag: str, limite: float) -> None:
        super().__init__()
        self.tag, self.limite, self._valor = tag, limite, 0.0

    def atualizar(self, valor: float) -> None:
        if valor == self._valor:
            return                                    # só emite se houver mudança
        self._valor = valor
        self.leituraMudou.emit(valor)
        if valor > self.limite:
            self.alarme.emit(self.tag, valor)


class Painel(QObject):
    @pyqtSlot(float)
    def exibir(self, v: float) -> None:
        print(f"painel: {v:.1f} bar")

    @pyqtSlot(str, float)
    def registrar_alarme(self, tag: str, v: float) -> None:
        print(f"ALARME em {tag}: {v:.1f} bar")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    sensor, painel = Sensor("PT-101", limite=300.0), Painel()

    sensor.leituraMudou.connect(painel.exibir)        # método decorado como slot
    sensor.alarme.connect(painel.registrar_alarme)
    sensor.leituraMudou.connect(lambda v: print(f"log: {v}"))   # vários receptores

    sensor.valorBruto[int].connect(lambda n: print("bruto int:", n))
    sensor.valorBruto[str].connect(lambda s: print("bruto str:", s))

    for v in (250.0, 250.0, 310.0):
        sensor.atualizar(v)
    sensor.valorBruto[int].emit(4095)
    sensor.valorBruto[str].emit("0x0FFF")

    sensor.leituraMudou.disconnect(painel.exibir)     # desconecta um receptor específico
    sensor.atualizar(100.0)
