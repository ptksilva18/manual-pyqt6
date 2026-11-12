# runner: ticks=100
"""QtHelp: registro de documentação .qch, sumário, índice de palavras-chave e busca."""

import os
import shutil
import sys
import tempfile

from PyQt6.QtCore import QTimer, QUrl
from PyQt6.QtHelp import QHelpEngine
from PyQt6.QtWidgets import QApplication, QSplitter, QTextBrowser

AQUI = os.path.dirname(os.path.abspath(__file__))
QCH = os.path.join(AQUI, "resources", "ajuda", "manual.qch")


class NavegadorAjuda(QTextBrowser):
    """QTextBrowser que lê as páginas de dentro do arquivo .qch (URLs qthelp://)."""

    def __init__(self, motor: QHelpEngine) -> None:
        super().__init__()
        self.motor = motor

    def loadResource(self, tipo: int, url: QUrl):
        if url.scheme() == "qthelp":
            return self.motor.fileData(url)
        return super().loadResource(tipo, url)


def main() -> int:
    app = QApplication(sys.argv)
    pasta = tempfile.mkdtemp()
    colecao = os.path.join(pasta, "ajuda.qhc")  # coleção: banco de dados criado pelo Qt
    motor = QHelpEngine(colecao)
    motor.setReadOnly(False)  # padrão True: sem isto, registerDocumentation() falha
    if not motor.setupData():
        print("setupData falhou:", motor.error())
        return 1
    shutil.copy(QCH, pasta)
    ok = motor.registerDocumentation(os.path.join(pasta, "manual.qch"))
    ns = QHelpEngine.namespaceName(os.path.join(pasta, "manual.qch"))
    print(f"registerDocumentation: {ok}; namespace: {ns}")
    print("Documentações registradas:", motor.registeredDocumentations())

    for chave in ("QThread", "estanqueidade"):
        for link in motor.documentsForKeyword(chave):
            print(f"Índice '{chave}' -> {link.title!r}: {link.url.toString()}")
    pagina = motor.documentsForIdentifier("ensaios.qthread")[0].url
    html = bytes(motor.fileData(pagina)).decode("utf-8")
    print(
        "fileData():",
        len(html),
        "bytes; contém 'moveToThread':",
        "moveToThread" in html,
    )

    navegador = NavegadorAjuda(motor)
    navegador.setSource(pagina)
    divisor = QSplitter()
    divisor.addWidget(motor.contentWidget())  # QHelpContentWidget (sumário)
    divisor.addWidget(navegador)
    divisor.resize(800, 400)
    divisor.show()
    print("Título exibido:", navegador.documentTitle())

    busca = motor.searchEngine()

    def indexado() -> None:
        busca.search(
            "pressão"
        )  # Qt 6: a consulta é uma string (sintaxe de busca do QtHelp)

    def buscado() -> None:
        n = busca.searchResultCount()
        print(f"Busca 'pressão': {n} resultado(s)")
        for r in busca.searchResults(0, n):
            print(f"  {r.title()} — {r.url().fileName()}")
        app.quit()

    busca.indexingFinished.connect(indexado)
    busca.searchingFinished.connect(buscado)
    busca.reindexDocumentation()
    QTimer.singleShot(8000, app.quit)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
