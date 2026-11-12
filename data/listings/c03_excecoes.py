"""Exceções em slots: sem tratamento, o PyQt6 aborta a aplicação (qFatal).

Instalar um sys.excepthook próprio mantém a aplicação viva e registra o erro.
"""
import sys
import traceback

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication


def tratador_global(tipo, valor, tb) -> None:
    """Registra a exceção; em uma aplicação real, exibiria um QMessageBox."""
    quadro = traceback.extract_tb(tb)[-1]          # último quadro = onde ocorreu
    print(f"[ERRO NÃO TRATADO] {tipo.__name__}: {valor}")
    print(f"  origem: função {quadro.name}(), linha {quadro.lineno}")


def slot_com_defeito() -> None:
    raise ZeroDivisionError("divisão por zero no cálculo")


if __name__ == "__main__":
    sys.excepthook = tratador_global        # instalar ANTES de app.exec()
    app = QApplication(sys.argv)
    QTimer.singleShot(0, slot_com_defeito)
    QTimer.singleShot(50, lambda: print("A aplicação continua respondendo."))
    QTimer.singleShot(100, app.quit)
    print("código de saída:", app.exec())
