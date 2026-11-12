# runner: ticks=100
"""QtHelp: registering .qch documentation, table of contents, keyword index and search."""

import os
import shutil
import sys
import tempfile

from PyQt6.QtCore import QTimer, QUrl
from PyQt6.QtHelp import QHelpEngine
from PyQt6.QtWidgets import QApplication, QSplitter, QTextBrowser

HERE = os.path.dirname(os.path.abspath(__file__))
QCH = os.path.join(HERE, "resources", "help", "manual.qch")


class HelpBrowser(QTextBrowser):
    """QTextBrowser that reads the pages from inside the .qch file (qthelp:// URLs)."""

    def __init__(self, engine: QHelpEngine) -> None:
        super().__init__()
        self.engine = engine

    def loadResource(self, kind: int, url: QUrl):
        if url.scheme() == "qthelp":
            return self.engine.fileData(url)
        return super().loadResource(kind, url)


def main() -> int:
    app = QApplication(sys.argv)
    folder = tempfile.mkdtemp()
    collection = os.path.join(folder, "help.qhc")  # collection: database created by Qt
    engine = QHelpEngine(collection)
    engine.setReadOnly(False)  # default True: without this, registerDocumentation() fails
    if not engine.setupData():
        print("setupData failed:", engine.error())
        return 1
    shutil.copy(QCH, folder)
    ok = engine.registerDocumentation(os.path.join(folder, "manual.qch"))
    ns = QHelpEngine.namespaceName(os.path.join(folder, "manual.qch"))
    print(f"registerDocumentation: {ok}; namespace: {ns}")
    print("Registered documentation:", engine.registeredDocumentations())

    for key in ("QThread", "leak test"):
        for link in engine.documentsForKeyword(key):
            print(f"Index '{key}' -> {link.title!r}: {link.url.toString()}")
    page = engine.documentsForIdentifier("tests.qthread")[0].url
    html = bytes(engine.fileData(page)).decode("utf-8")
    print(
        "fileData():",
        len(html),
        "bytes; contains 'moveToThread':",
        "moveToThread" in html,
    )

    browser = HelpBrowser(engine)
    browser.setSource(page)
    splitter = QSplitter()
    splitter.addWidget(engine.contentWidget())  # QHelpContentWidget (table of contents)
    splitter.addWidget(browser)
    splitter.resize(800, 400)
    splitter.show()
    print("Title displayed:", browser.documentTitle())

    search = engine.searchEngine()

    def indexed() -> None:
        search.search(
            "pressure"
        )  # Qt 6: the query is a string (QtHelp search syntax)

    def searched() -> None:
        n = search.searchResultCount()
        print(f"Search 'pressure': {n} result(s)")
        for r in search.searchResults(0, n):
            print(f"  {r.title()} — {r.url().fileName()}")
        app.quit()

    search.indexingFinished.connect(indexed)
    search.searchingFinished.connect(searched)
    search.reindexDocumentation()
    QTimer.singleShot(8000, app.quit)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
