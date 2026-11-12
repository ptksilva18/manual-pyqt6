"""Código gerado pelo pyuic6: integração por composição e por herança múltipla."""

import sys

from PyQt6.QtWidgets import QApplication, QWidget

from ui_dados_poco import Ui_DadosPoco  # gerado: pyuic6 c11_dados_poco.ui -o ...


class FormularioComposicao(QWidget):
    """Composição: a interface fica em self.ui (recomendado)."""

    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_DadosPoco()
        self.ui.setupUi(self)
        self.ui.botoes.accepted.connect(lambda: print("composição: OK"))


class FormularioHeranca(QWidget, Ui_DadosPoco):
    """Herança múltipla: os widgets viram atributos diretos de self."""

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.botoes.accepted.connect(lambda: print("herança: OK"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    a, b = FormularioComposicao(), FormularioHeranca()
    a.ui.botoes.accepted.emit()
    b.botoes.accepted.emit()
    print("campo via composição:", a.ui.campoNome.objectName())
    print("campo via herança:   ", b.campoNome.objectName())
