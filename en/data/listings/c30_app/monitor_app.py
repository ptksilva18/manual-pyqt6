"""Minimal application to be packaged: resources, theme, Qt translation and self-test."""

import sys
from pathlib import Path

from PyQt6.QtCore import QCoreApplication, QLibraryInfo, QLocale, QTimer, QTranslator
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

VERSION = "1.0.0"


def resource(relative: str) -> Path:
    """Path of a data file in the source code or in the frozen application."""
    if hasattr(
        sys, "_MEIPASS"
    ):  # PyInstaller (onedir: _internal; onefile: temporary folder)
        base = Path(sys._MEIPASS)
    elif getattr(sys, "frozen", False):  # cx_Freeze: data next to the executable
        base = Path(sys.executable).resolve().parent
    else:  # source code (and Nuitka standalone, which preserves __file__)
        base = Path(__file__).resolve().parent
    return base / relative


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Test Monitor")
    app.setApplicationVersion(VERSION)
    app.setStyleSheet(resource("resources/theme.qss").read_text(encoding="utf-8"))
    translator = QTranslator(app)
    tr_folder = QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)
    translated = translator.load(QLocale("pt_BR"), "qtbase", "_", tr_folder)
    app.installTranslator(translator)

    window = QWidget()
    title = QLabel(f"Test Monitor {VERSION}", objectName="title")
    QVBoxLayout(window).addWidget(title)
    window.show()

    if "--selftest" in sys.argv:  # check used after packaging
        plugins = Path(QLibraryInfo.path(QLibraryInfo.LibraryPath.PluginsPath))
        print(
            f"frozen: {getattr(sys, 'frozen', False)}; PyInstaller: "
            f"{hasattr(sys, '_MEIPASS')}"
        )
        print(f"Qt platform: {app.platformName()}")
        print(f"QSS theme loaded: {len(app.styleSheet())} characters")
        print(
            f"platform plugins: "
            f"{sorted(p.name for p in (plugins / 'platforms').glob('*'))}"
        )
        print(
            f"qtbase pt_BR translation loaded: {translated} -> 'Cancel' = "
            f"{QCoreApplication.translate('QPlatformTheme', 'Cancel')!r}"
        )
        QTimer.singleShot(0, app.quit)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
