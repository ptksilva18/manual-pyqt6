"""QStandardPaths, QDir e QFileInfo: onde guardar cada tipo de arquivo."""

import sys

from PyQt6.QtCore import QDir, QFileInfo, QStandardPaths
from PyQt6.QtWidgets import QApplication

L = QStandardPaths.StandardLocation

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setOrganizationName("Engenharia")
    app.setApplicationName("CalcEng")  # entra no caminho de AppData
    for local in (
        L.AppDataLocation,
        L.AppConfigLocation,
        L.CacheLocation,
        L.DocumentsLocation,
        L.TempLocation,
    ):
        print(f"{local.name:18} {QStandardPaths.writableLocation(local)}")

    dados = QStandardPaths.writableLocation(L.AppDataLocation)
    print("mkpath:", QDir().mkpath(dados + "/ensaios"))
    info = QFileInfo(dados + "/ensaios")
    print("é pasta?", info.isDir(), "| gravável?", info.isWritable())
    print("python3 no PATH:", bool(QStandardPaths.findExecutable("python3")))
