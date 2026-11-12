"""Embedded fonts (QFontDatabase) and icons (QIcon from SVG)."""

import sys
from pathlib import Path

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QFont, QFontDatabase, QIcon
from PyQt6.QtWidgets import QApplication

RES = Path(__file__).with_name("resources")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fid = QFontDatabase.addApplicationFont(str(RES / "fonts" / "DejaVuSansMono.ttf"))
    print("id of the loaded font:", fid)  # -1 means failure
    families = QFontDatabase.applicationFontFamilies(fid)
    print("families:", families)
    mono = QFont(families[0], 10)
    print("monospaced?", QFontDatabase.isFixedPitch(families[0]))
    system = QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont)
    print("fixed font suggested by the system:", bool(system.family()))

    # SVG: sharp at any scale
    icon = QIcon(str(RES / "icons" / "valve.svg"))
    print("null icon?", icon.isNull())
    for side in (16, 32, 64):
        pm = icon.pixmap(QSize(side, side))
        print(f"pixmap {side}x{side}:", pm.width(), "x", pm.height())
    # theme icon, with a fallback
    theme = QIcon.fromTheme(QIcon.ThemeIcon.DocumentSave, icon)
    print("theme icon (or fallback) available?", not theme.isNull())
