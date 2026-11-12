# runner: ticks=150 env=QTWEBENGINE_CHROMIUM_FLAGS:--no-sandbox
"""QWebEngineView and QWebEnginePage: HTML content, JavaScript, console, navigation and
PDF."""

import os
import sys
import tempfile

from PyQt6.QtCore import QTimer, QUrl
from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineSettings
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QApplication

HTML = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Report TH-01</title>
<style>body{font-family:sans-serif;margin:24px}
td,th{border:1px solid #999;padding:4px 10px}</style></head><body>
<h1>Report of test TH-01</h1>
<table><tr><th>Stage</th><th>Pressure (bar)</th></tr>
<tr><td>Pressurization</td><td>345.0</td></tr>
<tr><td>Stabilization</td><td>344.2</td></tr></table>
<p><a id="external" href="https://example.com/">External link</a></p>
<script>
console.log("page loaded: " + document.querySelectorAll("tr").length + " rows");
</script></body></html>"""


class ControlledPage(QWebEnginePage):
    """Logs the JavaScript console and blocks navigation outside the local content."""

    def javaScriptConsoleMessage(self, level, message, line, source) -> None:
        print(f"  [console {level.name}] {message}")

    def acceptNavigationRequest(self, url: QUrl, nav_type, is_main_frame: bool) -> bool:
        if url.scheme() in ("http", "https"):
            print(f"  navigation blocked: {url.toString()} ({nav_type.name})")
            return False
        return super().acceptNavigationRequest(url, nav_type, is_main_frame)


def main() -> int:
    app = QApplication(sys.argv)
    view = QWebEngineView()
    page = ControlledPage(
        view
    )  # uses the default profile (QWebEngineProfile.defaultProfile)
    view.setPage(page)
    settings = page.settings()
    settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
    settings.setAttribute(
        QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, False
    )
    pdf_target = os.path.join(tempfile.mkdtemp(), "report.pdf")

    def on_loaded(ok: bool) -> None:
        print(f"loadFinished: {ok}; title: {page.title()!r}")
        if not ok:  # a refused navigation also emits loadFinished(False)
            return
        page.loadFinished.disconnect(on_loaded)
        page.runJavaScript(
            "document.querySelectorAll('td')[3].textContent",
            lambda value: print(f"runJavaScript -> {value!r}"),
        )
        page.runJavaScript("document.getElementById('external').click()")
        QTimer.singleShot(500, lambda: page.printToPdf(pdf_target))

    def pdf_ready(path: str, success: bool) -> None:
        with open(path, "rb") as f:
            header = f.read(5)
        print(
            f"printToPdf: success={success}, {os.path.getsize(path)} bytes, "
            f"header {header!r}"
        )
        app.quit()

    page.loadFinished.connect(on_loaded)
    page.pdfPrintingFinished.connect(pdf_ready)
    view.setHtml(HTML, QUrl("file:///reports/"))  # baseUrl for relative resources
    view.resize(800, 500)
    view.show()
    QTimer.singleShot(12_000, app.quit)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
