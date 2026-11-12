"""Decoradores: um decorador próprio empilhado com @pyqtSlot."""
import functools
import sys
import time

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QApplication


def cronometrado(func):
    """Mede e imprime o tempo de execução da função decorada."""
    @functools.wraps(func)             # preserva nome e assinatura da original
    def envoltorio(*args, **kwargs):
        t0 = time.perf_counter()
        resultado = func(*args, **kwargs)
        dt = (time.perf_counter() - t0) * 1e3
        print(f"{func.__name__} executado ({'<1' if dt < 1 else f'{dt:.0f}'} ms)")
        return resultado
    return envoltorio


class Calculadora(QObject):
    resultado = pyqtSignal(float)

    @pyqtSlot(float, float)            # @pyqtSlot deve ser o decorador mais externo
    @cronometrado
    def dividir(self, a: float, b: float) -> None:
        self.resultado.emit(a / b)


class Emissor(QObject):
    pedido = pyqtSignal(float, float)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    calc, emissor = Calculadora(), Emissor()
    emissor.pedido.connect(calc.dividir)
    calc.resultado.connect(lambda r: print(f"resultado = {r:.4f}"))
    emissor.pedido.emit(10.0, 4.0)
    print("nome preservado:", Calculadora.dividir.__name__)
