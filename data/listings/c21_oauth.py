# runner: ticks=100
"""OAuth 2.0 (Authorization Code + PKCE) com QOAuth2AuthorizationCodeFlow.

Um provedor de autorização mínimo roda localmente e o "navegador" é simulado por
uma requisição HTTP, para que o fluxo completo execute sem rede nem interação.
"""

import base64
import hashlib
import json
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlencode, urlparse

from PyQt6.QtCore import QUrl
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt6.QtNetworkAuth import (
    QAbstractOAuth,
    QOAuth2AuthorizationCodeFlow,
    QOAuthHttpServerReplyHandler,
)
from PyQt6.QtWidgets import QApplication

PEDIDOS: dict[str, dict[str, str]] = {}


class Provedor(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # endpoint de autorização
        q = {k: v[0] for k, v in parse_qs(urlparse(self.path).query).items()}
        print("provedor: /authorize com", sorted(q))
        PEDIDOS["codigo-123"] = q
        destino = (
            q["redirect_uri"]
            + "?"
            + urlencode({"code": "codigo-123", "state": q["state"]})
        )
        self.send_response(302)
        self.send_header("Location", destino)
        self.end_headers()

    def do_POST(self) -> None:  # endpoint de token
        corpo = self.rfile.read(int(self.headers["Content-Length"])).decode()
        f = {k: v[0] for k, v in parse_qs(corpo).items()}
        pedido = PEDIDOS.get(f.get("code", ""), {})
        digest = hashlib.sha256(f.get("code_verifier", "").encode()).digest()
        desafio = base64.urlsafe_b64encode(digest).rstrip(b"=").decode()
        pkce_ok = pedido.get("code_challenge") == desafio
        print(
            f"provedor: /token grant_type={f.get('grant_type')}, PKCE conferido = "
            f"{pkce_ok}"
        )
        if not pkce_ok:
            self.send_response(400)
            self.end_headers()
            return
        resposta = json.dumps(
            {
                "access_token": "tok-abc",
                "token_type": "Bearer",
                "expires_in": 3600,
                "refresh_token": "ref-xyz",
                "scope": pedido.get("scope", ""),
            }
        ).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(resposta)))
        self.end_headers()
        self.wfile.write(resposta)

    def log_message(self, *args) -> None:
        pass


def main() -> int:
    app = QApplication(sys.argv)
    provedor = ThreadingHTTPServer(("127.0.0.1", 0), Provedor)
    threading.Thread(target=provedor.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{provedor.server_address[1]}"

    fluxo = QOAuth2AuthorizationCodeFlow()
    fluxo.setAuthorizationUrl(QUrl(base + "/authorize"))
    fluxo.setTokenUrl(QUrl(base + "/token"))
    fluxo.setClientIdentifier("app-ensaios")
    fluxo.setRequestedScopeTokens({b"leitura", b"escrita"})
    retorno = QOAuthHttpServerReplyHandler(0)  # escuta em localhost, porta livre
    fluxo.setReplyHandler(retorno)
    print("redirect_uri local escutando:", retorno.isListening())

    navegador = (
        QNetworkAccessManager()
    )  # substitui QDesktopServices.openUrl neste teste

    def abrir_navegador(url: QUrl) -> None:
        req = QNetworkRequest(url)
        req.setAttribute(
            QNetworkRequest.Attribute.RedirectPolicyAttribute,
            QNetworkRequest.RedirectPolicy.NoLessSafeRedirectPolicy,
        )
        resp = navegador.get(req)
        resp.finished.connect(resp.deleteLater)

    fluxo.authorizeWithBrowser.connect(abrir_navegador)
    fluxo.statusChanged.connect(lambda s: print("status do fluxo:", s.name))

    def concedido() -> None:
        print("token de acesso:", fluxo.token())
        print("refresh token :", fluxo.refreshToken())
        print(
            "escopo concedido:",
            sorted(bytes(t).decode() for t in fluxo.grantedScopeTokens()),
        )
        print(
            "expira em (s) ~",
            round(
                fluxo.expirationAt().toSecsSinceEpoch()
                - fluxo.expirationAt().currentSecsSinceEpoch(),
                -2,
            ),
        )
        provedor.shutdown()
        app.quit()

    def falhou(erro: QAbstractOAuth.Error) -> None:
        print("falha:", erro.name)
        provedor.shutdown()
        app.quit()

    fluxo.granted.connect(concedido)
    fluxo.requestFailed.connect(falhou)
    fluxo.grant()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
