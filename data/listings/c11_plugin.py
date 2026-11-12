"""Plugin de widget para o Qt Designer escrito em Python (módulo QtDesigner)."""

from PyQt6.QtDesigner import QPyDesignerCustomWidgetPlugin
from PyQt6.QtGui import QIcon

from c11_widgets import CampoPressao


class CampoPressaoPlugin(QPyDesignerCustomWidgetPlugin):
    """Descreve o widget para a caixa de widgets do Designer."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._iniciado = False

    def initialize(self, core) -> None:
        self._iniciado = True

    def isInitialized(self) -> bool:
        return self._iniciado

    def createWidget(self, parent):
        return CampoPressao(parent)

    def name(self) -> str:
        return "CampoPressao"

    def group(self) -> str:
        return "Engenharia"

    def icon(self) -> QIcon:
        return QIcon()

    def toolTip(self) -> str:
        return "Campo de pressão em bar"

    def whatsThis(self) -> str:
        return self.toolTip()

    def isContainer(self) -> bool:
        return False

    def domXml(self) -> str:
        return '<widget class="CampoPressao" name="campoPressao"/>'

    def includeFile(self) -> str:
        return "c11_widgets"


if __name__ == "__main__":
    import sys

    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    p = CampoPressaoPlugin()
    p.initialize(None)
    w = p.createWidget(None)
    print(p.name(), "| grupo:", p.group(), "| inicializado:", p.isInitialized())
    print("widget criado:", type(w).__name__, "| domXml:", p.domXml())
