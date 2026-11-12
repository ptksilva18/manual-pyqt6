"""Aplicação mínima a ser empacotada: recursos, tema, tradução do Qt e autoteste."""

import sys
from pathlib import Path

from PyQt6.QtCore import QCoreApplication, QLibraryInfo, QLocale, QTimer, QTranslator
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

VERSAO = "1.0.0"


def recurso(relativo: str) -> Path:
    """Caminho de um arquivo de dados no código-fonte ou na aplicação congelada."""
    if hasattr(
        sys, "_MEIPASS"
    ):  # PyInstaller (onedir: _internal; onefile: pasta temporária)
        base = Path(sys._MEIPASS)
    elif getattr(sys, "frozen", False):  # cx_Freeze: dados ao lado do executável
        base = Path(sys.executable).resolve().parent
    else:  # código-fonte (e Nuitka standalone, que preserva __file__)
        base = Path(__file__).resolve().parent
    return base / relativo


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Monitor de Ensaios")
    app.setApplicationVersion(VERSAO)
    app.setStyleSheet(recurso("recursos/tema.qss").read_text(encoding="utf-8"))
    tradutor = QTranslator(app)
    pasta_tr = QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)
    traduzido = tradutor.load(QLocale("pt_BR"), "qtbase", "_", pasta_tr)
    app.installTranslator(tradutor)

    janela = QWidget()
    titulo = QLabel(f"Monitor de Ensaios {VERSAO}", objectName="titulo")
    QVBoxLayout(janela).addWidget(titulo)
    janela.show()

    if "--autoteste" in sys.argv:  # verificação usada após o empacotamento
        plugins = Path(QLibraryInfo.path(QLibraryInfo.LibraryPath.PluginsPath))
        print(
            f"congelado: {getattr(sys, 'frozen', False)}; PyInstaller: "
            f"{hasattr(sys, '_MEIPASS')}"
        )
        print(f"plataforma Qt: {app.platformName()}")
        print(f"tema QSS carregado: {len(app.styleSheet())} caracteres")
        print(
            f"plugins de plataforma: "
            f"{sorted(p.name for p in (plugins / 'platforms').glob('*'))}"
        )
        print(
            f"tradução qtbase pt_BR carregada: {traduzido} -> 'Cancel' = "
            f"{QCoreApplication.translate('QPlatformTheme', 'Cancel')!r}"
        )
        QTimer.singleShot(0, app.quit)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
