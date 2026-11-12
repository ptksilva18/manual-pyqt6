# runner: ticks=150 env=QTWEBENGINE_CHROMIUM_FLAGS:--no-sandbox
"""Displaying PDF without QtPdf: Chromium's built-in viewer in QWebEngineView."""

import os
import sys
import tempfile

from PyQt6.QtCore import QMarginsF, QTimer, QUrl
from PyQt6.QtGui import QFont, QPageLayout, QPageSize, QPainter, QPdfWriter
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QApplication


def make_pdf(path: str, pages: int = 3) -> None:
    writer = QPdfWriter(path)
    writer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
    writer.setPageMargins(QMarginsF(20, 20, 20, 20), QPageLayout.Unit.Millimeter)
    writer.setTitle("Test report")
    painter = QPainter(writer)
    painter.setFont(QFont("DejaVu Sans", 14))
    for n in range(1, pages + 1):
        painter.drawText(200, 400, f"Test report — page {n} of {pages}")
        if n < pages:
            writer.newPage()
    painter.end()


def main() -> int:
    app = QApplication(sys.argv)
    path = os.path.join(tempfile.mkdtemp(), "report.pdf")
    make_pdf(path)
    print(f"PDF generated: {os.path.getsize(path)} bytes")
    view = QWebEngineView()
    settings = view.settings()
    settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
    settings.setAttribute(QWebEngineSettings.WebAttribute.PdfViewerEnabled, True)
    print(
        "PdfViewerEnabled:",
        settings.testAttribute(QWebEngineSettings.WebAttribute.PdfViewerEnabled),
    )

    def on_loaded(ok: bool) -> None:
        print(
            f"loadFinished: {ok}; URL: {view.url().fileName()}; title: "
            f"{view.title()!r}"
        )
        app.quit()

    view.loadFinished.connect(on_loaded)
    view.load(QUrl.fromLocalFile(path))
    view.resize(800, 600)
    view.show()
    QTimer.singleShot(12_000, app.quit)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
