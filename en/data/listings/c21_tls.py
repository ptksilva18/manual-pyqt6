# runner: ticks=60
"""TLS with QSslServer/QSslSocket: server certificate, verification and errors."""

import os
import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtNetwork import (
    QHostAddress,
    QSsl,
    QSslCertificate,
    QSslConfiguration,
    QSslKey,
    QSslServer,
    QSslSocket,
)
from PyQt6.QtWidgets import QApplication

CN = QSslCertificate.SubjectInfo.CommonName

HERE = os.path.dirname(os.path.abspath(__file__))
CRT = os.path.join(HERE, "resources", "tls", "server.crt")
KEY = os.path.join(HERE, "resources", "tls", "server.key")


def server_config() -> QSslConfiguration:
    conf = QSslConfiguration.defaultConfiguration()
    with open(CRT, "rb") as f:
        conf.setLocalCertificate(QSslCertificate(f.read(), QSsl.EncodingFormat.Pem))
    with open(KEY, "rb") as f:
        conf.setPrivateKey(
            QSslKey(f.read(), QSsl.KeyAlgorithm.Rsa, QSsl.EncodingFormat.Pem)
        )
    conf.setProtocol(QSsl.SslProtocol.TlsV1_2OrLater)
    return conf


def main() -> int:
    app = QApplication(sys.argv)
    print(
        "TLS support:",
        QSslSocket.supportsSsl(),
        "| backend:",
        QSslSocket.activeBackend(),
        "|",
        QSslSocket.sslLibraryVersionString(),
    )
    server = QSslServer()
    server.setSslConfiguration(server_config())
    server.pendingConnectionAvailable.connect(
        lambda: serve(server.nextPendingConnection())
    )
    server.listen(QHostAddress(QHostAddress.SpecialAddress.LocalHost), 0)
    port = server.serverPort()

    def serve(sock: QSslSocket) -> None:
        sock.readyRead.connect(lambda: sock.write(b"ACK " + bytes(sock.readAll())))
        sock.disconnected.connect(sock.deleteLater)

    def client(
        trust_certificate: bool, expected_name: str, label: str
    ) -> QSslSocket:
        sock = QSslSocket()
        sock.setPeerVerifyName(expected_name)  # name checked against the certificate
        if (
            trust_certificate
        ):  # own CA: trusts only the server's certificate
            conf = sock.sslConfiguration()
            conf.setCaCertificates(QSslCertificate.fromPath(CRT))
            sock.setSslConfiguration(conf)
        sock.encrypted.connect(
            lambda: (
                print(
                    f"[{label}] encrypted channel: {sock.sessionProtocol().name}, "
                    f"{sock.sessionCipher().name()}; peer = "
                    f"{sock.peerCertificate().subjectInfo(CN)}"
                ),
                sock.write(b"PING"),
            )
        )
        sock.readyRead.connect(
            lambda: (
                print(f"[{label}] received: {bytes(sock.readAll()).decode()}"),
                sock.disconnectFromHost(),
            )
        )
        sock.sslErrors.connect(
            lambda errors: print(
                f"[{label}] sslErrors: {[e.error().name for e in errors]}"
            )
        )
        sock.errorOccurred.connect(lambda e: print(f"[{label}] error: {e.name}"))
        sock.connectToHostEncrypted("127.0.0.1", port)
        return sock

    s1 = client(False, "localhost", "no CA  ")  # unknown self-signed certificate
    QTimer.singleShot(
        400, lambda: setattr(app, "_s2", client(True, "localhost", "with CA"))
    )
    QTimer.singleShot(
        800, lambda: setattr(app, "_s3", client(True, "scada.example", "other name"))
    )
    QTimer.singleShot(1300, app.quit)
    del s1
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
