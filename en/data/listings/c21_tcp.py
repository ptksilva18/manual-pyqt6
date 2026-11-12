# runner: ticks=60
"""TCP with QTcpServer/QTcpSocket: line protocol, framing and disconnection."""

import sys

from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from PyQt6.QtNetwork import QHostAddress, QTcpServer, QTcpSocket
from PyQt6.QtWidgets import QApplication

READINGS = {"PT-101": 123.4, "PT-102": 98.7, "TT-201": 61.2}


class InstrumentServer(QObject):
    """Answers 'READ <tag>' with '<tag> <value>' — one message per line."""

    def __init__(self) -> None:
        super().__init__()
        self.server = QTcpServer(self)
        self.server.newConnection.connect(self._new_connection)

    def listen(self) -> int:
        if not self.server.listen(
            QHostAddress(QHostAddress.SpecialAddress.LocalHost), 0
        ):
            raise RuntimeError(self.server.errorString())
        return self.server.serverPort()

    def _new_connection(self) -> None:
        while self.server.hasPendingConnections():
            sock = self.server.nextPendingConnection()
            sock.readyRead.connect(lambda s=sock: self._read(s))
            sock.disconnected.connect(sock.deleteLater)

    def _read(self, sock: QTcpSocket) -> None:
        while sock.canReadLine():  # TCP is a stream: the line is the message unit
            line = bytes(sock.readLine()).decode("utf-8").strip()
            cmd, _, tag = line.partition(" ")
            if cmd == "READ" and tag in READINGS:
                answer = f"{tag} {READINGS[tag]}"
            else:
                answer = f"ERROR invalid command: {line!r}"
            sock.write((answer + "\n").encode("utf-8"))


class Client(QObject):
    answer = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        self.sock = QTcpSocket(self)
        self._buffer = bytearray()
        self.sock.readyRead.connect(self._read)
        self.sock.errorOccurred.connect(lambda e: print("socket error:", e.name))
        self.sock.stateChanged.connect(lambda s: print("  state:", s.name))

    def _read(self) -> None:
        self._buffer += bytes(self.sock.readAll())
        while b"\n" in self._buffer:  # reassembles fragmented messages
            line, _, self._buffer = self._buffer.partition(b"\n")
            self.answer.emit(line.decode("utf-8"))


def main() -> int:
    app = QApplication(sys.argv)
    server = InstrumentServer()
    port = server.listen()
    print(
        f"Server listening on 127.0.0.1:<{'ephemeral port' if port > 1024 else port}>"
    )
    client = Client()
    answers: list[str] = []

    def on_answer(text: str) -> None:
        answers.append(text)
        print("answer:", text)
        if len(answers) == 4:
            client.sock.disconnectFromHost()

    client.answer.connect(on_answer)
    client.sock.disconnected.connect(lambda: QTimer.singleShot(0, app.quit))
    client.sock.connectToHost("127.0.0.1", port)
    if not client.sock.waitForConnected(2000):  # acceptable only in scripts and tests
        print("failure:", client.sock.errorString())
        return 1
    # Two messages in a single write and one in two pieces: framing takes care of it.
    client.sock.write(b"READ PT-101\nREAD TT-201\n")
    client.sock.write(b"READ PT-1")
    client.sock.write(b"02\nRESET\n")
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
