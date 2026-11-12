"""QPalette: programmatic dark theme and the system color scheme."""

import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QApplication, QPushButton


def dark_palette() -> QPalette:
    p = QPalette()
    colors = {
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
    for role, color in colors.items():
        p.setColor(role, QColor(color))  # all color groups
    grey = QColor("#6B6E74")  # "disabled" look
    for role in (
        QPalette.ColorRole.Text,
        QPalette.ColorRole.ButtonText,
        QPalette.ColorRole.WindowText,
    ):
        p.setColor(QPalette.ColorGroup.Disabled, role, grey)
    return p


if __name__ == "__main__":
    app = QApplication(sys.argv)
    hints = app.styleHints()
    print("system scheme:", hints.colorScheme().name)
    hints.colorSchemeChanged.connect(lambda s: print("colorSchemeChanged ->", s.name))
    # Fusion follows the palette well
    app.setStyle("Fusion")
    app.setPalette(dark_palette())
    b = QPushButton("Calculate")
    print("button background color:", b.palette().color(QPalette.ColorRole.Button).name())
    b.setEnabled(False)
    color = b.palette().color(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText)
    print("disabled text:", color.name())
    # requests the dark scheme (Qt 6.8+)
    hints.setColorScheme(Qt.ColorScheme.Dark)
