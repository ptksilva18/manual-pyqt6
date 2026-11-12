"""Promoção de widget: o .ui referencia CampoPressao, definido em c11_widgets.py."""

import sys
from pathlib import Path

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # <header>c11_widgets.h</header> no .ui -> o uic importa o módulo c11_widgets
    w = uic.loadUi(Path(__file__).with_name("c11_promovido.ui"))
    campo = w.campoPressao
    print("classe instanciada:", type(campo).__name__)
    print("herda de:", type(campo).__mro__[1].__name__)
    print(
        "faixa:",
        campo.minimum(),
        "a",
        campo.maximum(),
        "| sufixo:",
        repr(campo.suffix()),
    )
