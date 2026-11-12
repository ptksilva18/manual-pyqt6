"""Carga dinâmica de um arquivo .ui com uic.loadUi()."""

import sys
from pathlib import Path

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QDoubleSpinBox, QLineEdit, QWidget

# caminho relativo ao módulo
ARQUIVO_UI = Path(__file__).with_name("c11_dados_poco.ui")


class DadosPoco(QWidget):
    # Anotações apenas documentam os atributos criados por loadUi (objectName -> atributo)
    campoNome: QLineEdit
    campoLamina: QDoubleSpinBox

    def __init__(self) -> None:
        super().__init__()
        uic.loadUi(ARQUIVO_UI, self)  # constrói os widgets DENTRO de self
        self.botoes.accepted.connect(self.confirmar)
        self.botoes.rejected.connect(self.close)

    def confirmar(self) -> None:
        print(f"poço {self.campoNome.text()!r}, LDA = {self.campoLamina.value():.0f} m")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = DadosPoco()
    print("título vindo do .ui:", w.windowTitle())
    print("buddy do rótulo:", w.rotuloNome.buddy().objectName())
    w.campoNome.setText("PZ-123")
    w.campoLamina.setValue(2140)
    w.botoes.accepted.emit()  # simula o clique em OK
    w.show()
    sys.exit(app.exec())
