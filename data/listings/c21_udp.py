# runner: ticks=40
"""UDP com QUdpSocket: datagramas independentes, sem conexão e sem garantia de entrega."""

import struct
import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtNetwork import QHostAddress, QNetworkDatagram, QUdpSocket
from PyQt6.QtWidgets import QApplication

FORMATO = "<4sId"  # tag (4 bytes), sequência (uint32), valor (double) — little-endian


def main() -> int:
    app = QApplication(sys.argv)
    receptor = QUdpSocket()
    if not receptor.bind(QHostAddress(QHostAddress.SpecialAddress.LocalHost), 0):
        print("bind falhou:", receptor.errorString())
        return 1
    porta = receptor.localPort()
    recebidos: list[tuple[str, int, float]] = []

    def ler() -> None:
        while receptor.hasPendingDatagrams():
            dg: QNetworkDatagram = receptor.receiveDatagram()
            tag, seq, valor = struct.unpack(FORMATO, bytes(dg.data()))
            recebidos.append((tag.decode(), seq, valor))
            print(
                f"datagrama de {dg.senderAddress().toString()}: "
                f"{tag.decode()} #{seq} = {valor:.3f} ({dg.data().size()} bytes)"
            )

    receptor.readyRead.connect(ler)
    emissor = QUdpSocket()
    for seq, valor in enumerate([101.325, 101.410, 101.388]):
        dados = struct.pack(FORMATO, b"PB01", seq, valor)
        enviados = emissor.writeDatagram(dados, QHostAddress("127.0.0.1"), porta)
        assert enviados == struct.calcsize(FORMATO)

    def fim() -> None:
        print(
            f"{len(recebidos)} datagramas recebidos; tamanho de cada um = "
            f"{struct.calcsize(FORMATO)} bytes"
        )
        app.quit()

    QTimer.singleShot(300, fim)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
