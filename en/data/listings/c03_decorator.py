"""Decorators: a custom decorator stacked with @pyqtSlot."""
import functools
import sys
import time

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QApplication


def timed(func):
    """Measures and prints the run time of the decorated function."""
    @functools.wraps(func)             # preserves the original's name and signature
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        dt = (time.perf_counter() - t0) * 1e3
        print(f"{func.__name__} executed ({'<1' if dt < 1 else f'{dt:.0f}'} ms)")
        return result
    return wrapper


class Calculator(QObject):
    result = pyqtSignal(float)

    @pyqtSlot(float, float)            # @pyqtSlot must be the outermost decorator
    @timed
    def divide(self, a: float, b: float) -> None:
        self.result.emit(a / b)


class Emitter(QObject):
    request = pyqtSignal(float, float)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    calc, emitter = Calculator(), Emitter()
    emitter.request.connect(calc.divide)
    calc.result.connect(lambda r: print(f"result = {r:.4f}"))
    emitter.request.emit(10.0, 4.0)
    print("name preserved:", Calculator.divide.__name__)
