# runner: ticks=40
"""UDP with QUdpSocket: independent datagrams, connectionless, no delivery guarantee."""

import struct
import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtNetwork import QHostAddress, QNetworkDatagram, QUdpSocket
from PyQt6.QtWidgets import QApplication

FORMAT = "<4sId"  # tag (4 bytes), sequence (uint32), value (double) — little-endian


def main() -> int:
    app = QApplication(sys.argv)
    receiver = QUdpSocket()
    if not receiver.bind(QHostAddress(QHostAddress.SpecialAddress.LocalHost), 0):
        print("bind failed:", receiver.errorString())
        return 1
    port = receiver.localPort()
    received: list[tuple[str, int, float]] = []

    def read() -> None:
        while receiver.hasPendingDatagrams():
            dg: QNetworkDatagram = receiver.receiveDatagram()
            tag, seq, value = struct.unpack(FORMAT, bytes(dg.data()))
            received.append((tag.decode(), seq, value))
            print(
                f"datagram from {dg.senderAddress().toString()}: "
                f"{tag.decode()} #{seq} = {value:.3f} ({dg.data().size()} bytes)"
            )

    receiver.readyRead.connect(read)
    sender = QUdpSocket()
    for seq, value in enumerate([101.325, 101.410, 101.388]):
        data = struct.pack(FORMAT, b"PB01", seq, value)
        sent = sender.writeDatagram(data, QHostAddress("127.0.0.1"), port)
        assert sent == struct.calcsize(FORMAT)

    def finish() -> None:
        print(
            f"{len(received)} datagrams received; size of each one = "
            f"{struct.calcsize(FORMAT)} bytes"
        )
        app.quit()

    QTimer.singleShot(300, finish)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
