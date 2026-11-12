# runner: ticks=100
"""HTTP with QNetworkAccessManager: GET/POST JSON, headers, timeout, errors and
progress."""

import json
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from PyQt6.QtCore import QByteArray, QUrl
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PyQt6.QtWidgets import QApplication


class DemoServer(BaseHTTPRequestHandler):
    """Minimal local API, only so that the example runs without internet access."""

    def _respond(
        self,
        status: int,
        body: bytes,
        content_type: str = "application/json",
        extras: dict[str, str] | None = None,
    ) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        for k, v in (extras or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path == "/api/wells/7":
            data = {"well": "7-ABC-001", "water_depth_m": 1350.0, "fluid": "oil"}
            self._respond(200, json.dumps(data).encode())
        elif self.path == "/slow":
            time.sleep(2.0)
            self._respond(200, b"{}")
        elif (
            self.path == "/file"
        ):  # 256 KiB sent in blocks, so that there is progress
            self.send_response(200)
            self.send_header("Content-Type", "application/octet-stream")
            self.send_header("Content-Length", str(256 * 1024))
            self.end_headers()
            for _ in range(16):
                self.wfile.write(bytes(16 * 1024))
                self.wfile.flush()
                time.sleep(0.02)
        else:
            self._respond(404, b'{"error": "resource does not exist"}')

    def do_POST(self) -> None:
        size = int(self.headers.get("Content-Length", 0))
        received = json.loads(self.rfile.read(size))
        received["id"] = 42
        self._respond(
            201, json.dumps(received).encode(), extras={"Location": "/api/tests/42"}
        )

    def log_message(self, *args) -> None:  # silences the server log
        pass


class APIClient:
    def __init__(self, base: str) -> None:
        self.base = base
        self.nam = QNetworkAccessManager()
        self.nam.setTransferTimeout(5000)  # default for all requests (ms)

    def request(self, path: str) -> QNetworkRequest:
        req = QNetworkRequest(QUrl(self.base + path))
        req.setRawHeader(b"Accept", b"application/json")
        req.setHeader(QNetworkRequest.KnownHeaders.UserAgentHeader, "PyQt6Manual/1.0")
        return req

    @staticmethod
    def describe(reply: QNetworkReply) -> str:
        status = reply.attribute(QNetworkRequest.Attribute.HttpStatusCodeAttribute)
        error = reply.error()
        text = f"HTTP {status}, error = {error.name}"
        if error != QNetworkReply.NetworkError.NoError:
            text += f" ({reply.errorString()})"
        return text


def main() -> int:
    app = QApplication(sys.argv)
    server = ThreadingHTTPServer(("127.0.0.1", 0), DemoServer)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    api = APIClient(f"http://127.0.0.1:{server.server_address[1]}")
    steps = []

    def next_step() -> None:
        if steps:
            steps.pop(0)()
        else:
            server.shutdown()
            app.quit()

    def get_json() -> None:
        reply = api.nam.get(api.request("/api/wells/7"))

        def done() -> None:
            print("GET /api/wells/7 ->", api.describe(reply))
            print(
                "  Content-Type:",
                reply.header(QNetworkRequest.KnownHeaders.ContentTypeHeader),
            )
            data = json.loads(bytes(reply.readAll()).decode("utf-8"))
            print("  JSON:", data)
            reply.deleteLater()
            next_step()

        reply.finished.connect(done)

    def post_json() -> None:
        req = api.request("/api/tests")
        req.setHeader(
            QNetworkRequest.KnownHeaders.ContentTypeHeader, "application/json"
        )
        body = json.dumps({"test": "TH-01", "pressure_bar": 345.0}).encode()
        reply = api.nam.post(req, QByteArray(body))

        def done() -> None:
            print("POST /api/tests ->", api.describe(reply))
            print("  Location:", bytes(reply.rawHeader(b"Location")).decode())
            print("  JSON:", json.loads(bytes(reply.readAll())))
            reply.deleteLater()
            next_step()

        reply.finished.connect(done)

    def get_404() -> None:
        reply = api.nam.get(api.request("/does/not/exist"))

        def done() -> None:
            print("GET /does/not/exist ->", api.describe(reply))
            print("  error body:", bytes(reply.readAll()).decode())
            reply.deleteLater()
            next_step()

        reply.finished.connect(done)

    def get_timeout() -> None:
        req = api.request("/slow")
        req.setTransferTimeout(300)  # overrides the manager's default
        reply = api.nam.get(req)

        def done() -> None:
            print("GET /slow (timeout 300 ms) ->", api.describe(reply))
            reply.deleteLater()
            next_step()

        reply.finished.connect(done)

    def download() -> None:
        reply = api.nam.get(api.request("/file"))
        marks: list[int] = []

        def progress(received: int, total: int) -> None:
            if total > 0:
                pct = 100 * received // total
                if (
                    not marks
                    or pct >= marks[-1] + 25
                    or (pct == 100 and marks[-1] != 100)
                ):
                    marks.append(pct)

        def done() -> None:
            data = reply.readAll()
            print(
                f"GET /file -> {api.describe(reply)}; {data.size()} bytes; "
                f"progress marks (%): {marks}"
            )
            reply.deleteLater()
            next_step()

        reply.downloadProgress.connect(progress)
        reply.finished.connect(done)

    steps.extend([get_json, post_json, get_404, get_timeout, download])
    next_step()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
