# runner: ticks=150 env=QTWEBENGINE_CHROMIUM_FLAGS:--no-sandbox
"""QWebChannel: objeto Python acessível pelo JavaScript (slots, sinais e propriedades)."""

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

AQUI = os.path.dirname(os.path.abspath(__file__))


class Ponte(QObject):
    alerta = pyqtSignal(str)
    paginaPronta = pyqtSignal()

    @pyqtProperty(str, constant=True)
    def unidade(self) -> str:
        return "bar"

    @pyqtSlot(float, result=float)
    def pressao(self, profundidade_m: float) -> float:
        p = 1030.0 * 9.80665 * profundidade_m / 1e5 + 1.01325
        print(f"  Python: pressao({profundidade_m}) = {p:.4f}")
        if p > 100.0:
            self.alerta.emit(f"{p:.1f} bar excede 100 bar")
        return p

    @pyqtSlot()
    def pronto(self) -> None:
        print("  Python: página conectada ao canal")
        self.paginaPronta.emit()


def script_qwebchannel() -> QWebEngineScript:
    arquivo = QFile(
        ":/qtwebchannel/qwebchannel.js"
    )  # recurso embutido no Qt WebChannel
    arquivo.open(QIODevice.OpenModeFlag.ReadOnly)
    script = QWebEngineScript()
    script.setSourceCode(bytes(arquivo.readAll()).decode("utf-8"))
    script.setName("qwebchannel.js")
    script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentCreation)
    script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
    return script


def main() -> int:
    app = QApplication(sys.argv)
    vista = QWebEngineView()
    pagina = vista.page()
    pagina.scripts().insert(script_qwebchannel())
    ponte = Ponte()
    canal = QWebChannel(pagina)
    canal.registerObject("ponte", ponte)
    pagina.setWebChannel(canal)

    def ler_dom() -> None:
        js = (
            "['resultado','unidade','alerta'].map("
            "id => id + '=' + document.getElementById(id).textContent).join('; ')"
        )
        pagina.runJavaScript(js, lambda texto: (print("DOM:", texto), app.quit()))

    def pagina_pronta() -> None:  # simula o clique do usuário no botão Calcular
        pagina.runJavaScript("document.getElementById('calcular').click()")
        QTimer.singleShot(800, ler_dom)

    ponte.paginaPronta.connect(pagina_pronta)
    vista.load(QUrl.fromLocalFile(os.path.join(AQUI, "c24_webchannel.html")))
    vista.resize(640, 400)
    vista.show()
    QTimer.singleShot(12_000, app.quit)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
