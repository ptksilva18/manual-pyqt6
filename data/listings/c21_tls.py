# runner: ticks=60
"""TLS com QSslServer/QSslSocket: certificado do servidor, verificação e erros."""

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

AQUI = os.path.dirname(os.path.abspath(__file__))
CRT = os.path.join(AQUI, "resources", "tls", "servidor.crt")
KEY = os.path.join(AQUI, "resources", "tls", "servidor.key")


def config_servidor() -> QSslConfiguration:
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
        "Suporte a TLS:",
        QSslSocket.supportsSsl(),
        "| backend:",
        QSslSocket.activeBackend(),
        "|",
        QSslSocket.sslLibraryVersionString(),
    )
    servidor = QSslServer()
    servidor.setSslConfiguration(config_servidor())
    servidor.pendingConnectionAvailable.connect(
        lambda: atender(servidor.nextPendingConnection())
    )
    servidor.listen(QHostAddress(QHostAddress.SpecialAddress.LocalHost), 0)
    porta = servidor.serverPort()

    def atender(sock: QSslSocket) -> None:
        sock.readyRead.connect(lambda: sock.write(b"ACK " + bytes(sock.readAll())))
        sock.disconnected.connect(sock.deleteLater)

    def cliente(
        confiar_no_certificado: bool, nome_esperado: str, rotulo: str
    ) -> QSslSocket:
        sock = QSslSocket()
        sock.setPeerVerifyName(nome_esperado)  # nome conferido contra o certificado
        if (
            confiar_no_certificado
        ):  # CA própria: confia apenas no certificado do servidor
            conf = sock.sslConfiguration()
            conf.setCaCertificates(QSslCertificate.fromPath(CRT))
            sock.setSslConfiguration(conf)
        sock.encrypted.connect(
            lambda: (
                print(
                    f"[{rotulo}] canal cifrado: {sock.sessionProtocol().name}, "
                    f"{sock.sessionCipher().name()}; par = "
                    f"{sock.peerCertificate().subjectInfo(CN)}"
                ),
                sock.write(b"PING"),
            )
        )
        sock.readyRead.connect(
            lambda: (
                print(f"[{rotulo}] recebido: {bytes(sock.readAll()).decode()}"),
                sock.disconnectFromHost(),
            )
        )
        sock.sslErrors.connect(
            lambda erros: print(
                f"[{rotulo}] sslErrors: {[e.error().name for e in erros]}"
            )
        )
        sock.errorOccurred.connect(lambda e: print(f"[{rotulo}] erro: {e.name}"))
        sock.connectToHostEncrypted("127.0.0.1", porta)
        return sock

    s1 = cliente(False, "localhost", "sem CA ")  # certificado autoassinado desconhecido
    QTimer.singleShot(
        400, lambda: setattr(app, "_s2", cliente(True, "localhost", "com CA "))
    )
    QTimer.singleShot(
        800, lambda: setattr(app, "_s3", cliente(True, "scada.exemplo", "outro nome"))
    )
    QTimer.singleShot(1300, app.quit)
    del s1
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
