# runner: ticks=100
"""HTTP com QNetworkAccessManager: GET/POST JSON, cabeçalhos, timeout, erros e
progresso."""

import json
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from PyQt6.QtCore import QByteArray, QUrl
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PyQt6.QtWidgets import QApplication


class ServidorDemo(BaseHTTPRequestHandler):
    """API mínima local, apenas para que o exemplo rode sem acesso à internet."""

    def _responder(
        self,
        status: int,
        corpo: bytes,
        tipo: str = "application/json",
        extras: dict[str, str] | None = None,
    ) -> None:
        self.send_response(status)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(corpo)))
        for k, v in (extras or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(corpo)

    def do_GET(self) -> None:
        if self.path == "/api/pocos/7":
            dados = {"poco": "7-ABC-001", "lamina_dagua_m": 1350.0, "fluido": "óleo"}
            self._responder(200, json.dumps(dados).encode())
        elif self.path == "/lento":
            time.sleep(2.0)
            self._responder(200, b"{}")
        elif (
            self.path == "/arquivo"
        ):  # 256 KiB enviados em blocos, para haver progresso
            self.send_response(200)
            self.send_header("Content-Type", "application/octet-stream")
            self.send_header("Content-Length", str(256 * 1024))
            self.end_headers()
            for _ in range(16):
                self.wfile.write(bytes(16 * 1024))
                self.wfile.flush()
                time.sleep(0.02)
        else:
            self._responder(404, b'{"erro": "recurso inexistente"}')

    def do_POST(self) -> None:
        tamanho = int(self.headers.get("Content-Length", 0))
        recebido = json.loads(self.rfile.read(tamanho))
        recebido["id"] = 42
        self._responder(
            201, json.dumps(recebido).encode(), extras={"Location": "/api/ensaios/42"}
        )

    def log_message(self, *args) -> None:  # silencia o log do servidor
        pass


class ClienteAPI:
    def __init__(self, base: str) -> None:
        self.base = base
        self.nam = QNetworkAccessManager()
        self.nam.setTransferTimeout(5000)  # padrão para todas as requisições (ms)

    def requisicao(self, caminho: str) -> QNetworkRequest:
        req = QNetworkRequest(QUrl(self.base + caminho))
        req.setRawHeader(b"Accept", b"application/json")
        req.setHeader(QNetworkRequest.KnownHeaders.UserAgentHeader, "ManualPyQt6/1.0")
        return req

    @staticmethod
    def descrever(reply: QNetworkReply) -> str:
        status = reply.attribute(QNetworkRequest.Attribute.HttpStatusCodeAttribute)
        erro = reply.error()
        texto = f"HTTP {status}, erro = {erro.name}"
        if erro != QNetworkReply.NetworkError.NoError:
            texto += f" ({reply.errorString()})"
        return texto


def main() -> int:
    app = QApplication(sys.argv)
    servidor = ThreadingHTTPServer(("127.0.0.1", 0), ServidorDemo)
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    api = ClienteAPI(f"http://127.0.0.1:{servidor.server_address[1]}")
    etapas = []

    def proxima() -> None:
        if etapas:
            etapas.pop(0)()
        else:
            servidor.shutdown()
            app.quit()

    def get_json() -> None:
        reply = api.nam.get(api.requisicao("/api/pocos/7"))

        def fim() -> None:
            print("GET /api/pocos/7 ->", api.descrever(reply))
            print(
                "  Content-Type:",
                reply.header(QNetworkRequest.KnownHeaders.ContentTypeHeader),
            )
            dados = json.loads(bytes(reply.readAll()).decode("utf-8"))
            print("  JSON:", dados)
            reply.deleteLater()
            proxima()

        reply.finished.connect(fim)

    def post_json() -> None:
        req = api.requisicao("/api/ensaios")
        req.setHeader(
            QNetworkRequest.KnownHeaders.ContentTypeHeader, "application/json"
        )
        corpo = json.dumps({"ensaio": "TH-01", "pressao_bar": 345.0}).encode()
        reply = api.nam.post(req, QByteArray(corpo))

        def fim() -> None:
            print("POST /api/ensaios ->", api.descrever(reply))
            print("  Location:", bytes(reply.rawHeader(b"Location")).decode())
            print("  JSON:", json.loads(bytes(reply.readAll())))
            reply.deleteLater()
            proxima()

        reply.finished.connect(fim)

    def get_404() -> None:
        reply = api.nam.get(api.requisicao("/nao/existe"))

        def fim() -> None:
            print("GET /nao/existe ->", api.descrever(reply))
            print("  corpo de erro:", bytes(reply.readAll()).decode())
            reply.deleteLater()
            proxima()

        reply.finished.connect(fim)

    def get_timeout() -> None:
        req = api.requisicao("/lento")
        req.setTransferTimeout(300)  # sobrepõe o padrão do gerenciador
        reply = api.nam.get(req)

        def fim() -> None:
            print("GET /lento (timeout 300 ms) ->", api.descrever(reply))
            reply.deleteLater()
            proxima()

        reply.finished.connect(fim)

    def download() -> None:
        reply = api.nam.get(api.requisicao("/arquivo"))
        marcos: list[int] = []

        def progresso(recebidos: int, total: int) -> None:
            if total > 0:
                pct = 100 * recebidos // total
                if (
                    not marcos
                    or pct >= marcos[-1] + 25
                    or (pct == 100 and marcos[-1] != 100)
                ):
                    marcos.append(pct)

        def fim() -> None:
            dados = reply.readAll()
            print(
                f"GET /arquivo -> {api.descrever(reply)}; {dados.size()} bytes; "
                f"marcos de progresso (%): {marcos}"
            )
            reply.deleteLater()
            proxima()

        reply.downloadProgress.connect(progresso)
        reply.finished.connect(fim)

    etapas.extend([get_json, post_json, get_404, get_timeout, download])
    proxima()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
