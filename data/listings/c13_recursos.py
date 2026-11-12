"""Recursos sem pyrcc: caminhos relativos ao pacote e prefixos de busca do QDir."""

import sys
from pathlib import Path

from PyQt6.QtCore import QDir, QFile, QFileInfo
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

RAIZ = Path(__file__).resolve().parent / "resources"  # funciona instalado ou não

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Prefixos: "icones:arquivo" passa a ser procurado nas pastas registradas
    QDir.addSearchPath("icones", str(RAIZ / "icones"))
    QDir.addSearchPath("fontes", str(RAIZ / "fonts"))

    print("QFile('icones:valvula.svg').exists():", QFile("icones:valvula.svg").exists())
    icone = QIcon("icones:valvula.svg")
    print("QIcon carregado pelo prefixo:", not icone.isNull())
    info = QFileInfo("fontes:DejaVuSansMono.ttf")
    print("arquivo resolvido:", info.fileName(), f"({info.size() // 1024} KiB)")
    print("prefixo inexistente:", QFile("imagens:logo.png").exists())
