# runner: ticks=40
"""Integração com o desktop: bandeja do sistema, QDesktopServices e permissões."""

import sys

from PyQt6.QtCore import (
    QCameraPermission,
    QLocationPermission,
    QMicrophonePermission,
    QObject,
    QUrl,
    pyqtSlot,
)
from PyQt6.QtGui import QAction, QDesktopServices, QIcon
from PyQt6.QtWidgets import QApplication, QMenu, QStyle, QSystemTrayIcon


class TratadorEngApp(QObject):
    """Recebe URLs do esquema engapp:// abertos por QDesktopServices.openUrl()."""

    @pyqtSlot(QUrl)
    def abrir(self, url: QUrl) -> None:
        print(
            f"  tratador interno: host={url.host()!r}, caminho={url.path()!r}, "
            f"consulta={url.query()!r}"
        )


def main() -> int:
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # aplicações de bandeja vivem sem janelas

    disponivel = QSystemTrayIcon.isSystemTrayAvailable()
    print(
        f"Bandeja do sistema disponível: {disponivel}; "
        f"mensagens suportadas: {QSystemTrayIcon.supportsMessages()}"
    )
    icone = app.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxInformation)
    bandeja = QSystemTrayIcon(QIcon(icone))
    bandeja.setToolTip("Monitor de ensaios")
    menu = QMenu()
    acao_sair = QAction("Sair", menu)
    acao_sair.triggered.connect(app.quit)
    menu.addAction(acao_sair)
    bandeja.setContextMenu(menu)
    if disponivel:
        bandeja.show()
        bandeja.showMessage(
            "Ensaio TH-01",
            "Pressão estabilizada",
            QSystemTrayIcon.MessageIcon.Information,
            5000,
        )
    else:
        print(
            "  sem bandeja: use uma janela comum ou notificações pela própria interface"
        )

    tratador = TratadorEngApp()
    QDesktopServices.setUrlHandler("engapp", tratador, "abrir")
    print(
        "openUrl(engapp://...) ->",
        QDesktopServices.openUrl(QUrl("engapp://ensaios/TH-01?aba=graficos")),
    )
    QDesktopServices.unsetUrlHandler("engapp")

    for permissao in (
        QCameraPermission(),
        QMicrophonePermission(),
        QLocationPermission(),
    ):
        print(f"{type(permissao).__name__:<22} {app.checkPermission(permissao).name}")
    local = QLocationPermission()
    local.setAccuracy(QLocationPermission.Accuracy.Precise)
    app.requestPermission(
        local, lambda p: print("requestPermission(local, preciso) ->", p.status().name)
    )
    app.processEvents()
    return 0


if __name__ == "__main__":
    sys.exit(main())
