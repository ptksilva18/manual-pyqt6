# runner: ticks=40
"""Desktop integration: system tray, QDesktopServices and permissions."""

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


class EngAppHandler(QObject):
    """Receives URLs of the engapp:// scheme opened by QDesktopServices.openUrl()."""

    @pyqtSlot(QUrl)
    def open_url(self, url: QUrl) -> None:
        print(
            f"  internal handler: host={url.host()!r}, path={url.path()!r}, "
            f"query={url.query()!r}"
        )


def main() -> int:
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # tray applications live without windows

    available = QSystemTrayIcon.isSystemTrayAvailable()
    print(
        f"System tray available: {available}; "
        f"messages supported: {QSystemTrayIcon.supportsMessages()}"
    )
    icon = app.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxInformation)
    tray = QSystemTrayIcon(QIcon(icon))
    tray.setToolTip("Test monitor")
    menu = QMenu()
    act_quit = QAction("Quit", menu)
    act_quit.triggered.connect(app.quit)
    menu.addAction(act_quit)
    tray.setContextMenu(menu)
    if available:
        tray.show()
        tray.showMessage(
            "Test TH-01",
            "Pressure stabilized",
            QSystemTrayIcon.MessageIcon.Information,
            5000,
        )
    else:
        print(
            "  no tray: use an ordinary window or notifications in the interface itself"
        )

    handler = EngAppHandler()
    QDesktopServices.setUrlHandler("engapp", handler, "open_url")
    print(
        "openUrl(engapp://...) ->",
        QDesktopServices.openUrl(QUrl("engapp://tests/TH-01?tab=charts")),
    )
    QDesktopServices.unsetUrlHandler("engapp")

    for permission in (
        QCameraPermission(),
        QMicrophonePermission(),
        QLocationPermission(),
    ):
        print(f"{type(permission).__name__:<22} {app.checkPermission(permission).name}")
    location = QLocationPermission()
    location.setAccuracy(QLocationPermission.Accuracy.Precise)
    app.requestPermission(
        location,
        lambda p: print("requestPermission(location, precise) ->", p.status().name),
    )
    app.processEvents()
    return 0


if __name__ == "__main__":
    sys.exit(main())
