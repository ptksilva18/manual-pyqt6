"""Resources without pyrcc: paths relative to the package and QDir search prefixes."""

import sys
from pathlib import Path

from PyQt6.QtCore import QDir, QFile, QFileInfo
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

ROOT = Path(__file__).resolve().parent / "resources"  # works installed or not

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Prefixes: "icons:file" is now looked up in the registered folders
    QDir.addSearchPath("icons", str(ROOT / "icons"))
    QDir.addSearchPath("fonts", str(ROOT / "fonts"))

    print("QFile('icons:valve.svg').exists():", QFile("icons:valve.svg").exists())
    icon = QIcon("icons:valve.svg")
    print("QIcon loaded through the prefix:", not icon.isNull())
    info = QFileInfo("fonts:DejaVuSansMono.ttf")
    print("resolved file:", info.fileName(), f"({info.size() // 1024} KiB)")
    print("unknown prefix:", QFile("images:logo.png").exists())
