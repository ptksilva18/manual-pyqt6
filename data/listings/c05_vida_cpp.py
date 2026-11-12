"""Ciclo de vida C++ x Python: referência Python para objeto C++ já destruído."""
import sys

from PyQt6 import sip
from PyQt6.QtWidgets import QApplication, QLabel, QWidget

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pai = QWidget()
    rotulo = QLabel("filho", pai)          # o pai C++ é dono do rótulo
    sip.delete(pai)                        # destrói o pai (e, com ele, os filhos) já
    print("rotulo ainda existe em Python?", rotulo is not None)
    print("objeto C++ destruído?", sip.isdeleted(rotulo))
    try:
        rotulo.text()
    except RuntimeError as erro:
        print("RuntimeError:", erro)
