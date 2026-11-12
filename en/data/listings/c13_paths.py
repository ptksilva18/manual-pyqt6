"""QStandardPaths, QDir and QFileInfo: where to store each kind of file."""

import sys

from PyQt6.QtCore import QDir, QFileInfo, QStandardPaths
from PyQt6.QtWidgets import QApplication

L = QStandardPaths.StandardLocation

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setOrganizationName("Engineering")
    app.setApplicationName("EngCalc")  # becomes part of the AppData path
    for location in (
        L.AppDataLocation,
        L.AppConfigLocation,
        L.CacheLocation,
        L.DocumentsLocation,
        L.TempLocation,
    ):
        print(f"{location.name:18} {QStandardPaths.writableLocation(location)}")

    data = QStandardPaths.writableLocation(L.AppDataLocation)
    print("mkpath:", QDir().mkpath(data + "/tests"))
    info = QFileInfo(data + "/tests")
    print("is it a folder?", info.isDir(), "| writable?", info.isWritable())
    print("python3 in the PATH:", bool(QStandardPaths.findExecutable("python3")))
