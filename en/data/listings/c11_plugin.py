"""Widget plugin for Qt Designer written in Python (QtDesigner module)."""

from PyQt6.QtDesigner import QPyDesignerCustomWidgetPlugin
from PyQt6.QtGui import QIcon

from c11_widgets import PressureField


class PressureFieldPlugin(QPyDesignerCustomWidgetPlugin):
    """Describes the widget for Designer's widget box."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._initialized = False

    def initialize(self, core) -> None:
        self._initialized = True

    def isInitialized(self) -> bool:
        return self._initialized

    def createWidget(self, parent):
        return PressureField(parent)

    def name(self) -> str:
        return "PressureField"

    def group(self) -> str:
        return "Engineering"

    def icon(self) -> QIcon:
        return QIcon()

    def toolTip(self) -> str:
        return "Pressure field in bar"

    def whatsThis(self) -> str:
        return self.toolTip()

    def isContainer(self) -> bool:
        return False

    def domXml(self) -> str:
        return '<widget class="PressureField" name="pressureField"/>'

    def includeFile(self) -> str:
        return "c11_widgets"


if __name__ == "__main__":
    import sys

    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    p = PressureFieldPlugin()
    p.initialize(None)
    w = p.createWidget(None)
    print(p.name(), "| group:", p.group(), "| initialized:", p.isInitialized())
    print("widget created:", type(w).__name__, "| domXml:", p.domXml())
