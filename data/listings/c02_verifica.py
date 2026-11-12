"""Verifica a instalação do PyQt6 e dos pacotes add-on."""
from importlib import metadata

from PyQt6.QtCore import PYQT_VERSION_STR, QT_VERSION_STR, QLibraryInfo

print(f"PyQt6 ............ {PYQT_VERSION_STR}")
print(f"Qt (runtime) ..... {QT_VERSION_STR}")
print(f"Qt (build) ....... {QLibraryInfo.version().toString()}")

for dist in ("PyQt6-Charts", "PyQt6-Graphs", "PyQt6-WebEngine",
             "PyQt6-3D", "PyQt6-DataVisualization", "PyQt6-NetworkAuth"):
    try:
        print(f"{dist:<24} {metadata.version(dist)}")
    except metadata.PackageNotFoundError:
        print(f"{dist:<24} (não instalado)")
