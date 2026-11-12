# runner: ticks=60
"""TCP com QTcpServer/QTcpSocket: protocolo de linhas, enquadramento e desconexão."""

import sys

from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from PyQt6.QtNetwork import QHostAddress, QTcpServer, QTcpSocket
from PyQt6.QtWidgets import QApplication

LEITURAS = {"PT-101": 123.4, "PT-102": 98.7, "TT-201": 61.2}


class ServidorInstrumentos(QObject):
    """Responde 'LER <tag>' com '<tag> <valor>' — uma mensagem por linha."""

    def __init__(self) -> None:
        super().__init__()
        self.servidor = QTcpServer(self)
        self.servidor.newConnection.connect(self._nova_conexao)

    def escutar(self) -> int:
        if not self.servidor.listen(
            QHostAddress(QHostAddress.SpecialAddress.LocalHost), 0
        ):
            raise RuntimeError(self.servidor.errorString())
        return self.servidor.serverPort()

    def _nova_conexao(self) -> None:
        while self.servidor.hasPendingConnections():
            sock = self.servidor.nextPendingConnection()
            sock.readyRead.connect(lambda s=sock: self._ler(s))
            sock.disconnected.connect(sock.deleteLater)

    def _ler(self, sock: QTcpSocket) -> None:
        while sock.canReadLine():  # TCP é um fluxo: a linha é a unidade de mensagem
            linha = bytes(sock.readLine()).decode("utf-8").strip()
            cmd, _, tag = linha.partition(" ")
            if cmd == "LER" and tag in LEITURAS:
                resposta = f"{tag} {LEITURAS[tag]}"
            else:
                resposta = f"ERRO comando invalido: {linha!r}"
            sock.write((resposta + "\n").encode("utf-8"))


class Cliente(QObject):
    resposta = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        self.sock = QTcpSocket(self)
        self._buffer = bytearray()
        self.sock.readyRead.connect(self._ler)
        self.sock.errorOccurred.connect(lambda e: print("erro de socket:", e.name))
        self.sock.stateChanged.connect(lambda s: print("  estado:", s.name))

    def _ler(self) -> None:
        self._buffer += bytes(self.sock.readAll())
        while b"\n" in self._buffer:  # remonta mensagens fragmentadas
            linha, _, self._buffer = self._buffer.partition(b"\n")
            self.resposta.emit(linha.decode("utf-8"))


def main() -> int:
    app = QApplication(sys.argv)
    servidor = ServidorInstrumentos()
    porta = servidor.escutar()
    print(
        f"Servidor escutando em 127.0.0.1:<porta {'efêmera' if porta > 1024 else porta}>"
    )
    cliente = Cliente()
    respostas: list[str] = []

    def ao_responder(texto: str) -> None:
        respostas.append(texto)
        print("resposta:", texto)
        if len(respostas) == 4:
            cliente.sock.disconnectFromHost()

    cliente.resposta.connect(ao_responder)
    cliente.sock.disconnected.connect(lambda: QTimer.singleShot(0, app.quit))
    cliente.sock.connectToHost("127.0.0.1", porta)
    if not cliente.sock.waitForConnected(2000):  # aceitável só em scripts e testes
        print("falha:", cliente.sock.errorString())
        return 1
    # Duas mensagens em um único write e uma em dois pedaços: o enquadramento resolve.
    cliente.sock.write(b"LER PT-101\nLER TT-201\n")
    cliente.sock.write(b"LER PT-1")
    cliente.sock.write(b"02\nRESET\n")
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
