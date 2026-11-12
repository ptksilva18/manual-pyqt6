# runner: ticks=150 env=QTWEBENGINE_CHROMIUM_FLAGS:--no-sandbox
"""QWebChannel: Python object accessible from JavaScript (slots, signals, properties)."""

import os
import sys

from PyQt6.QtCore import (
    QFile,
    QIODevice,
    QObject,
    QTimer,
    QUrl,
    pyqtProperty,
    pyqtSignal,
    pyqtSlot,
)
from PyQt6.QtWebChannel import QWebChannel
from PyQt6.QtWebEngineCore import QWebEngineScript
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QApplication

HERE = os.path.dirname(os.path.abspath(__file__))


class Bridge(QObject):
    alert = pyqtSignal(str)
    pageReady = pyqtSignal()

    @pyqtProperty(str, constant=True)
    def unit(self) -> str:
        return "bar"

    @pyqtSlot(float, result=float)
    def pressure(self, depth_m: float) -> float:
        p = 1030.0 * 9.80665 * depth_m / 1e5 + 1.01325
        print(f"  Python: pressure({depth_m}) = {p:.4f}")
        if p > 100.0:
            self.alert.emit(f"{p:.1f} bar exceeds 100 bar")
        return p

    @pyqtSlot()
    def ready(self) -> None:
        print("  Python: page connected to the channel")
        self.pageReady.emit()


def qwebchannel_script() -> QWebEngineScript:
    js_file = QFile(
        ":/qtwebchannel/qwebchannel.js"
    )  # resource built into Qt WebChannel
    js_file.open(QIODevice.OpenModeFlag.ReadOnly)
    script = QWebEngineScript()
    script.setSourceCode(bytes(js_file.readAll()).decode("utf-8"))
    script.setName("qwebchannel.js")
    script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentCreation)
    script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
    return script


def main() -> int:
    app = QApplication(sys.argv)
    view = QWebEngineView()
    page = view.page()
    page.scripts().insert(qwebchannel_script())
    bridge = Bridge()
    channel = QWebChannel(page)
    channel.registerObject("bridge", bridge)
    page.setWebChannel(channel)

    def read_dom() -> None:
        js = (
            "['result','unit','alert'].map("
            "id => id + '=' + document.getElementById(id).textContent).join('; ')"
        )
        page.runJavaScript(js, lambda text: (print("DOM:", text), app.quit()))

    def page_ready() -> None:  # simulates the user clicking the Compute button
        page.runJavaScript("document.getElementById('compute').click()")
        QTimer.singleShot(800, read_dom)

    bridge.pageReady.connect(page_ready)
    view.load(QUrl.fromLocalFile(os.path.join(HERE, "c24_webchannel.html")))
    view.resize(640, 400)
    view.show()
    QTimer.singleShot(12_000, app.quit)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
