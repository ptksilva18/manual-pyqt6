# runner: ticks=60
"""WebSockets: QWebSocketServer e QWebSocket trocando texto (JSON) e binário."""

import json
import struct
import sys

from PyQt6.QtCore import QTimer, QUrl
from PyQt6.QtNetwork import QHostAddress
from PyQt6.QtWebSockets import QWebSocket, QWebSocketProtocol, QWebSocketServer
from PyQt6.QtWidgets import QApplication


def main() -> int:
    app = QApplication(sys.argv)
    servidor = QWebSocketServer("Telemetria", QWebSocketServer.SslMode.NonSecureMode)
    if not servidor.listen(QHostAddress(QHostAddress.SpecialAddress.LocalHost), 0):
        print("listen falhou:", servidor.errorString())
        return 1
    clientes: list[QWebSocket] = []

    def nova_conexao() -> None:
        ws = servidor.nextPendingConnection()
        clientes.append(ws)
        print(f"servidor: cliente conectado (origem {ws.origin()!r})")

        def texto(msg: str) -> None:
            pedido = json.loads(msg)
            amostras = [100.0 + 0.5 * i for i in range(pedido["n"])]
            ws.sendTextMessage(json.dumps({"tag": pedido["tag"], "n": len(amostras)}))
            ws.sendBinaryMessage(struct.pack(f"<{len(amostras)}d", *amostras))

        ws.textMessageReceived.connect(texto)
        ws.disconnected.connect(lambda: (clientes.remove(ws), ws.deleteLater()))

    servidor.newConnection.connect(nova_conexao)
    cliente = QWebSocket(origin="http://app.local")

    def conectado() -> None:
        print(
            "cliente: conectado ->", servidor.serverUrl().scheme(), "| enviando pedido"
        )
        cliente.sendTextMessage(json.dumps({"tag": "PT-101", "n": 5}))

    def binario(dados) -> None:
        valores = struct.unpack(f"<{len(dados) // 8}d", bytes(dados))
        print("cliente: binário com", len(dados), "bytes ->", valores)
        cliente.close(QWebSocketProtocol.CloseCode.CloseCodeNormal, "fim da coleta")

    cliente.connected.connect(conectado)
    cliente.textMessageReceived.connect(lambda m: print("cliente: texto ->", m))
    cliente.binaryMessageReceived.connect(binario)
    cliente.disconnected.connect(
        lambda: (
            print(
                "cliente: desconectado; código",
                cliente.closeCode().name,
                f"motivo {cliente.closeReason()!r}",
            ),
            QTimer.singleShot(100, app.quit),
        )
    )
    cliente.open(QUrl(f"ws://127.0.0.1:{servidor.serverPort()}"))
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
