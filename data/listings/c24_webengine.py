# runner: ticks=150 env=QTWEBENGINE_CHROMIUM_FLAGS:--no-sandbox
"""QWebEngineView e QWebEnginePage: conteúdo HTML, JavaScript, console, navegação e
PDF."""

import os
import sys
import tempfile

from PyQt6.QtCore import QTimer, QUrl
from PyQt6.QtWebEngineCore import QWebEnginePage, QWebEngineSettings
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QApplication

HTML = """<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><title>Relatório TH-01</title>
<style>body{font-family:sans-serif;margin:24px}
td,th{border:1px solid #999;padding:4px 10px}</style></head><body>
<h1>Relatório do ensaio TH-01</h1>
<table><tr><th>Etapa</th><th>Pressão (bar)</th></tr>
<tr><td>Pressurização</td><td>345,0</td></tr>
<tr><td>Estabilização</td><td>344,2</td></tr></table>
<p><a id="externo" href="https://example.com/">Link externo</a></p>
<script>
console.log("página carregada: " + document.querySelectorAll("tr").length + " linhas");
</script></body></html>"""


class PaginaControlada(QWebEnginePage):
    """Registra o console JavaScript e bloqueia navegação para fora do conteúdo local."""

    def javaScriptConsoleMessage(self, nivel, mensagem, linha, origem) -> None:
        print(f"  [console {nivel.name}] {mensagem}")

    def acceptNavigationRequest(self, url: QUrl, tipo, principal: bool) -> bool:
        if url.scheme() in ("http", "https"):
            print(f"  navegação bloqueada: {url.toString()} ({tipo.name})")
            return False
        return super().acceptNavigationRequest(url, tipo, principal)


def main() -> int:
    app = QApplication(sys.argv)
    vista = QWebEngineView()
    pagina = PaginaControlada(
        vista
    )  # usa o perfil padrão (QWebEngineProfile.defaultProfile)
    vista.setPage(pagina)
    ajustes = pagina.settings()
    ajustes.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
    ajustes.setAttribute(
        QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, False
    )
    destino_pdf = os.path.join(tempfile.mkdtemp(), "relatorio.pdf")

    def carregado(ok: bool) -> None:
        print(f"loadFinished: {ok}; título: {pagina.title()!r}")
        if not ok:  # uma navegação recusada também emite loadFinished(False)
            return
        pagina.loadFinished.disconnect(carregado)
        pagina.runJavaScript(
            "document.querySelectorAll('td')[3].textContent",
            lambda valor: print(f"runJavaScript -> {valor!r}"),
        )
        pagina.runJavaScript("document.getElementById('externo').click()")
        QTimer.singleShot(500, lambda: pagina.printToPdf(destino_pdf))

    def pdf_pronto(caminho: str, sucesso: bool) -> None:
        with open(caminho, "rb") as f:
            cabecalho = f.read(5)
        print(
            f"printToPdf: sucesso={sucesso}, {os.path.getsize(caminho)} bytes, "
            f"cabeçalho {cabecalho!r}"
        )
        app.quit()

    pagina.loadFinished.connect(carregado)
    pagina.pdfPrintingFinished.connect(pdf_pronto)
    vista.setHtml(HTML, QUrl("file:///relatorios/"))  # baseUrl para recursos relativos
    vista.resize(800, 500)
    vista.show()
    QTimer.singleShot(12_000, app.quit)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
