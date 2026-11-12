"""Internacionalização: tr(), QTranslator da aplicação e traduções do próprio Qt."""

import sys
from pathlib import Path

from PyQt6.QtCore import QCoreApplication, QLibraryInfo, QLocale, QTranslator
from PyQt6.QtWidgets import QApplication, QDialogButtonBox, QLabel, QWidget

AQUI = Path(__file__).resolve().parent


class Painel(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.titulo = QLabel()
        self.retraduzir()

    def retraduzir(self) -> None:
        self.setWindowTitle(self.tr("Pipe check"))
        self.titulo.setText(self.tr("Test pressure: %1 bar").replace("%1", "345"))


def mensagem_fora_de_classe() -> str:
    return QCoreApplication.translate("Relatorio", "Report generated")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    p = Painel()
    print(
        "antes:", p.windowTitle(), "|", p.titulo.text(), "|", mensagem_fora_de_classe()
    )

    trad_app = QTranslator()  # traduções da aplicação (.qm próprio)
    print("app carregada?", trad_app.load(str(AQUI / "c13_calceng_pt_BR.qm")))
    trad_qt = QTranslator()  # traduções dos textos internos do Qt
    pasta_qt = QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)
    print("qtbase carregada?", trad_qt.load(QLocale("pt_BR"), "qtbase", "_", pasta_qt))
    app.installTranslator(trad_app)
    app.installTranslator(trad_qt)

    p.retraduzir()  # textos precisam ser refeitos
    print(
        "depois:", p.windowTitle(), "|", p.titulo.text(), "|", mensagem_fora_de_classe()
    )
    caixa = QDialogButtonBox(
        QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
    )
    print("botões do Qt:", [b.text() for b in caixa.buttons()])
