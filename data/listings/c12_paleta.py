"""QPalette: tema escuro programático e esquema de cores do sistema."""

import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QApplication, QPushButton


def paleta_escura() -> QPalette:
    p = QPalette()
    cores = {
        QPalette.ColorRole.Window: "#1E1F22",
        QPalette.ColorRole.WindowText: "#E6E6E6",
        QPalette.ColorRole.Base: "#2B2D31",
        QPalette.ColorRole.AlternateBase: "#313338",
        QPalette.ColorRole.Text: "#E6E6E6",
        QPalette.ColorRole.Button: "#2B2D31",
        QPalette.ColorRole.ButtonText: "#E6E6E6",
        QPalette.ColorRole.Highlight: "#2E75B6",
        QPalette.ColorRole.HighlightedText: "#FFFFFF",
        QPalette.ColorRole.ToolTipBase: "#313338",
        QPalette.ColorRole.ToolTipText: "#E6E6E6",
        QPalette.ColorRole.PlaceholderText: "#8A8D93",
        QPalette.ColorRole.Link: "#6CB4F5",
    }
    for papel, cor in cores.items():
        p.setColor(papel, QColor(cor))  # todos os grupos de cor
    cinza = QColor("#6B6E74")  # aparência "desabilitado"
    for papel in (
        QPalette.ColorRole.Text,
        QPalette.ColorRole.ButtonText,
        QPalette.ColorRole.WindowText,
    ):
        p.setColor(QPalette.ColorGroup.Disabled, papel, cinza)
    return p


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dicas = app.styleHints()
    print("esquema do sistema:", dicas.colorScheme().name)
    dicas.colorSchemeChanged.connect(lambda e: print("colorSchemeChanged ->", e.name))
    # Fusion respeita bem a paleta
    app.setStyle("Fusion")
    app.setPalette(paleta_escura())
    b = QPushButton("Calcular")
    print("cor de fundo do botão:", b.palette().color(QPalette.ColorRole.Button).name())
    b.setEnabled(False)
    cor = b.palette().color(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText)
    print("texto desabilitado:", cor.name())
    # pede o esquema escuro (Qt 6.8+)
    dicas.setColorScheme(Qt.ColorScheme.Dark)
