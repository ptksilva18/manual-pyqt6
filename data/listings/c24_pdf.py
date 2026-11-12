# runner: ticks=150 env=QTWEBENGINE_CHROMIUM_FLAGS:--no-sandbox
"""Exibição de PDF sem QtPdf: visualizador embutido do Chromium no QWebEngineView."""

import os
import sys
import tempfile

from PyQt6.QtCore import QMarginsF, QTimer, QUrl
from PyQt6.QtGui import QFont, QPageLayout, QPageSize, QPainter, QPdfWriter
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QApplication


def gerar_pdf(caminho: str, paginas: int = 3) -> None:
    escritor = QPdfWriter(caminho)
    escritor.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
    escritor.setPageMargins(QMarginsF(20, 20, 20, 20), QPageLayout.Unit.Millimeter)
    escritor.setTitle("Relatório de ensaio")
    pintor = QPainter(escritor)
    pintor.setFont(QFont("DejaVu Sans", 14))
    for n in range(1, paginas + 1):
        pintor.drawText(200, 400, f"Relatório de ensaio — página {n} de {paginas}")
        if n < paginas:
            escritor.newPage()
    pintor.end()


def main() -> int:
    app = QApplication(sys.argv)
    caminho = os.path.join(tempfile.mkdtemp(), "relatorio.pdf")
    gerar_pdf(caminho)
    print(f"PDF gerado: {os.path.getsize(caminho)} bytes")
    vista = QWebEngineView()
    ajustes = vista.settings()
    ajustes.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
    ajustes.setAttribute(QWebEngineSettings.WebAttribute.PdfViewerEnabled, True)
    print(
        "PdfViewerEnabled:",
        ajustes.testAttribute(QWebEngineSettings.WebAttribute.PdfViewerEnabled),
    )

    def carregado(ok: bool) -> None:
        print(
            f"loadFinished: {ok}; URL: {vista.url().fileName()}; título: "
            f"{vista.title()!r}"
        )
        app.quit()

    vista.loadFinished.connect(carregado)
    vista.load(QUrl.fromLocalFile(caminho))
    vista.resize(800, 600)
    vista.show()
    QTimer.singleShot(12_000, app.quit)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
