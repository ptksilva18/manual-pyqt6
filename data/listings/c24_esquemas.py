# runner: ticks=150 env=QTWEBENGINE_CHROMIUM_FLAGS:--no-sandbox
"""Perfil próprio, esquema de URL engapp://, interceptação de requisições e downloads."""

import os
import sys
import tempfile

from PyQt6.QtCore import QBuffer, QByteArray, QIODevice, QTimer, QUrl
from PyQt6.QtWebEngineCore import (
    QWebEngineDownloadRequest,
    QWebEnginePage,
    QWebEngineProfile,
    QWebEngineUrlRequestInfo,
    QWebEngineUrlRequestInterceptor,
    QWebEngineUrlRequestJob,
    QWebEngineUrlScheme,
    QWebEngineUrlSchemeHandler,
)
from PyQt6.QtWidgets import QApplication

# Esquemas próprios devem ser registrados ANTES de criar a QApplication.
ESQUEMA = QWebEngineUrlScheme(b"engapp")
ESQUEMA.setSyntax(QWebEngineUrlScheme.Syntax.Host)
ESQUEMA.setFlags(
    QWebEngineUrlScheme.Flag.SecureScheme | QWebEngineUrlScheme.Flag.LocalScheme
)
QWebEngineUrlScheme.registerScheme(ESQUEMA)

PAGINAS = {
    "/indice": b"<html><head><title>Ajuda interna</title></head><body>"
    b"<a id='csv' href='engapp://docs/dados.csv' download='ensaio.csv'>CSV</a>"
    b"<img src='engapp://docs/rastreio.gif'></body></html>",
    "/dados.csv": b"tempo_min;pressao_bar\n0;345.0\n30;344.2\n60;344.0\n",
}


class ConteudoInterno(QWebEngineUrlSchemeHandler):
    """Serve conteúdo gerado pelo Python (banco, cálculos, arquivos empacotados)."""

    def requestStarted(self, job: QWebEngineUrlRequestJob) -> None:
        caminho = job.requestUrl().path()
        if caminho not in PAGINAS:
            job.fail(QWebEngineUrlRequestJob.Error.UrlNotFound)
            return
        tipo = b"text/csv" if caminho.endswith(".csv") else b"text/html"
        buf = QBuffer(parent=job)  # o job é dono do buffer
        buf.setData(PAGINAS[caminho])
        buf.open(QIODevice.OpenModeFlag.ReadOnly)
        job.reply(QByteArray(tipo), buf)


class Filtro(QWebEngineUrlRequestInterceptor):
    """Executa fora da thread da GUI: apenas decide e ajusta a requisição."""

    def interceptRequest(self, info: QWebEngineUrlRequestInfo) -> None:
        url = info.requestUrl()
        tipo = info.resourceType().name
        if "rastreio" in url.path():
            info.block(True)
            print(f"  interceptor: BLOQUEADO {url.path()} ({tipo})")
        else:
            info.setHttpHeader(b"X-App", b"ManualPyQt6")
            print(f"  interceptor: liberado {url.path()} ({tipo})")


def main() -> int:
    app = QApplication(sys.argv)
    perfil = (
        QWebEngineProfile()
    )  # sem nome: perfil "off-the-record" (nada vai para o disco)
    print("Perfil off-the-record:", perfil.isOffTheRecord())
    tratador, filtro = ConteudoInterno(), Filtro()
    perfil.installUrlSchemeHandler(b"engapp", tratador)
    perfil.setUrlRequestInterceptor(filtro)
    pasta = tempfile.mkdtemp()

    def download(req: QWebEngineDownloadRequest) -> None:
        req.setDownloadDirectory(pasta)
        print(f"  download solicitado: {req.downloadFileName()} ({req.mimeType()})")
        req.isFinishedChanged.connect(lambda: concluido(req))
        req.accept()  # sem accept(), o download é cancelado

    def concluido(req: QWebEngineDownloadRequest) -> None:
        caminho = os.path.join(req.downloadDirectory(), req.downloadFileName())
        with open(caminho, encoding="utf-8") as f:
            linhas = f.read().splitlines()
        print(
            f"  download {req.state().name}: {len(linhas)} linhas; última = "
            f"{linhas[-1]!r}"
        )
        QTimer.singleShot(0, app.quit)

    perfil.downloadRequested.connect(download)
    pagina = QWebEnginePage(perfil)

    def carregado(ok: bool) -> None:
        print(f"loadFinished: {ok}; título: {pagina.title()!r}")
        pagina.runJavaScript("document.getElementById('csv').click()")

    pagina.loadFinished.connect(carregado)
    pagina.load(QUrl("engapp://docs/indice"))
    QTimer.singleShot(12_000, app.quit)
    codigo = app.exec()
    del pagina  # a página deve ser destruída antes do seu perfil
    return codigo


if __name__ == "__main__":
    sys.exit(main())
