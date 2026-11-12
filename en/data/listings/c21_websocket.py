# runner: ticks=60
"""WebSockets: QWebSocketServer and QWebSocket exchanging text (JSON) and binary data."""

import json
import struct
import sys

from PyQt6.QtCore import QTimer, QUrl
from PyQt6.QtNetwork import QHostAddress
from PyQt6.QtWebSockets import QWebSocket, QWebSocketProtocol, QWebSocketServer
from PyQt6.QtWidgets import QApplication


def main() -> int:
    app = QApplication(sys.argv)
    server = QWebSocketServer("Telemetry", QWebSocketServer.SslMode.NonSecureMode)
    if not server.listen(QHostAddress(QHostAddress.SpecialAddress.LocalHost), 0):
        print("listen failed:", server.errorString())
        return 1
    clients: list[QWebSocket] = []

    def new_connection() -> None:
        ws = server.nextPendingConnection()
        clients.append(ws)
        print(f"server: client connected (origin {ws.origin()!r})")

        def text(msg: str) -> None:
            request = json.loads(msg)
            samples = [100.0 + 0.5 * i for i in range(request["n"])]
            ws.sendTextMessage(json.dumps({"tag": request["tag"], "n": len(samples)}))
            ws.sendBinaryMessage(struct.pack(f"<{len(samples)}d", *samples))

        ws.textMessageReceived.connect(text)
        ws.disconnected.connect(lambda: (clients.remove(ws), ws.deleteLater()))

    server.newConnection.connect(new_connection)
    client = QWebSocket(origin="http://app.local")

    def connected() -> None:
        print(
            "client: connected ->", server.serverUrl().scheme(), "| sending request"
        )
        client.sendTextMessage(json.dumps({"tag": "PT-101", "n": 5}))

    def binary(data) -> None:
        values = struct.unpack(f"<{len(data) // 8}d", bytes(data))
        print("client: binary with", len(data), "bytes ->", values)
        client.close(QWebSocketProtocol.CloseCode.CloseCodeNormal, "end of collection")

    client.connected.connect(connected)
    client.textMessageReceived.connect(lambda m: print("client: text ->", m))
    client.binaryMessageReceived.connect(binary)
    client.disconnected.connect(
        lambda: (
            print(
                "client: disconnected; code",
                client.closeCode().name,
                f"reason {client.closeReason()!r}",
            ),
            QTimer.singleShot(100, app.quit),
        )
    )
    client.open(QUrl(f"ws://127.0.0.1:{server.serverPort()}"))
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
