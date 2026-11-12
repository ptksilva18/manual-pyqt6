# runner: ticks=100
"""OAuth 2.0 (Authorization Code + PKCE) with QOAuth2AuthorizationCodeFlow.

A minimal authorization provider runs locally and the "browser" is simulated by an
HTTP request, so that the full flow executes without network or interaction.
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

REQUESTS: dict[str, dict[str, str]] = {}


class Provider(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # authorization endpoint
        q = {k: v[0] for k, v in parse_qs(urlparse(self.path).query).items()}
        print("provider: /authorize with", sorted(q))
        REQUESTS["code-123"] = q
        target = (
            q["redirect_uri"]
            + "?"
            + urlencode({"code": "code-123", "state": q["state"]})
        )
        self.send_response(302)
        self.send_header("Location", target)
        self.end_headers()

    def do_POST(self) -> None:  # token endpoint
        body = self.rfile.read(int(self.headers["Content-Length"])).decode()
        f = {k: v[0] for k, v in parse_qs(body).items()}
        request = REQUESTS.get(f.get("code", ""), {})
        digest = hashlib.sha256(f.get("code_verifier", "").encode()).digest()
        challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode()
        pkce_ok = request.get("code_challenge") == challenge
        print(
            f"provider: /token grant_type={f.get('grant_type')}, PKCE verified = "
            f"{pkce_ok}"
        )
        if not pkce_ok:
            self.send_response(400)
            self.end_headers()
            return
        answer = json.dumps(
            {
                "access_token": "tok-abc",
                "token_type": "Bearer",
                "expires_in": 3600,
                "refresh_token": "ref-xyz",
                "scope": request.get("scope", ""),
            }
        ).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(answer)))
        self.end_headers()
        self.wfile.write(answer)

    def log_message(self, *args) -> None:
        pass


def main() -> int:
    app = QApplication(sys.argv)
    provider = ThreadingHTTPServer(("127.0.0.1", 0), Provider)
    threading.Thread(target=provider.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{provider.server_address[1]}"

    flow = QOAuth2AuthorizationCodeFlow()
    flow.setAuthorizationUrl(QUrl(base + "/authorize"))
    flow.setTokenUrl(QUrl(base + "/token"))
    flow.setClientIdentifier("test-app")
    flow.setRequestedScopeTokens({b"read", b"write"})
    handler = QOAuthHttpServerReplyHandler(0)  # listens on localhost, free port
    flow.setReplyHandler(handler)
    print("local redirect_uri listening:", handler.isListening())

    browser = (
        QNetworkAccessManager()
    )  # replaces QDesktopServices.openUrl in this test

    def open_browser(url: QUrl) -> None:
        req = QNetworkRequest(url)
        req.setAttribute(
            QNetworkRequest.Attribute.RedirectPolicyAttribute,
            QNetworkRequest.RedirectPolicy.NoLessSafeRedirectPolicy,
        )
        resp = browser.get(req)
        resp.finished.connect(resp.deleteLater)

    flow.authorizeWithBrowser.connect(open_browser)
    flow.statusChanged.connect(lambda s: print("flow status:", s.name))

    def granted() -> None:
        print("access token :", flow.token())
        print("refresh token:", flow.refreshToken())
        print(
            "granted scope:",
            sorted(bytes(t).decode() for t in flow.grantedScopeTokens()),
        )
        print(
            "expires in (s) ~",
            round(
                flow.expirationAt().toSecsSinceEpoch()
                - flow.expirationAt().currentSecsSinceEpoch(),
                -2,
            ),
        )
        provider.shutdown()
        app.quit()

    def failed(error: QAbstractOAuth.Error) -> None:
        print("failure:", error.name)
        provider.shutdown()
        app.quit()

    flow.granted.connect(granted)
    flow.requestFailed.connect(failed)
    flow.grant()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
