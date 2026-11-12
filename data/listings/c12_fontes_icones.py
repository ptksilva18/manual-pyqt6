"""Fontes embarcadas (QFontDatabase) e ícones (QIcon a partir de SVG)."""

import sys
from pathlib import Path

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QFont, QFontDatabase, QIcon
from PyQt6.QtWidgets import QApplication

RES = Path(__file__).with_name("resources")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fid = QFontDatabase.addApplicationFont(str(RES / "fonts" / "DejaVuSansMono.ttf"))
    print("id da fonte carregada:", fid)  # -1 indica falha
    familias = QFontDatabase.applicationFontFamilies(fid)
    print("famílias:", familias)
    mono = QFont(familias[0], 10)
    print("monoespaçada?", QFontDatabase.isFixedPitch(familias[0]))
    sistema = QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont)
    print("fonte fixa sugerida pelo sistema:", bool(sistema.family()))

    # SVG: nítido em qualquer escala
    icone = QIcon(str(RES / "icones" / "valvula.svg"))
    print("ícone nulo?", icone.isNull())
    for lado in (16, 32, 64):
        pm = icone.pixmap(QSize(lado, lado))
        print(f"pixmap {lado}x{lado}:", pm.width(), "x", pm.height())
    # tema, com alternativa
    tema = QIcon.fromTheme(QIcon.ThemeIcon.DocumentSave, icone)
    print("ícone de tema (ou alternativa) disponível?", not tema.isNull())
