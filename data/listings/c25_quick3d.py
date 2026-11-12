# runner: ticks=40 xcb
"""Qt Quick 3D controlado pelo Python: cena QML em QQuickWidget, propriedades e nós 3D."""

import os
import sys

from PyQt6.QtCore import QTimer, QUrl
from PyQt6.QtQuick3D import QQuick3DObject
from PyQt6.QtQuickWidgets import QQuickWidget
from PyQt6.QtWidgets import QApplication

AQUI = os.path.dirname(os.path.abspath(__file__))


def main() -> int:
    app = QApplication(sys.argv)
    vista = QQuickWidget()
    vista.setResizeMode(QQuickWidget.ResizeMode.SizeRootObjectToView)
    vista.setSource(QUrl.fromLocalFile(os.path.join(AQUI, "c25_quick3d.qml")))
    if vista.status() != QQuickWidget.Status.Ready:
        print([e.toString() for e in vista.errors()])
        return 1
    raiz = vista.rootObject()  # o View3D (um QQuickItem)
    tampa = raiz.findChild(QQuick3DObject, "tampa")
    print(
        f"Raiz: {raiz.metaObject().className()}; nó 'tampa': "
        f"{tampa.metaObject().className()}"
    )
    print("Posição da tampa:", tampa.property("position"))
    vista.resize(520, 360)
    vista.show()
    passos = [0]

    def animar() -> None:
        passos[0] += 1
        raiz.setProperty(
            "anguloTampa", 10.0 * passos[0]
        )  # binding em QML atualiza a cena

    timer = QTimer()
    timer.timeout.connect(animar)
    timer.start(40)

    def fim() -> None:
        timer.stop()
        img = vista.grabFramebuffer()
        print(
            f"anguloTampa = {raiz.property('anguloTampa'):.0f}°; "
            f"captura {img.width()}x{img.height()}, centro "
            f"{img.pixelColor(260, 200).name()}"
        )
        if os.environ.get("CAPTURA"):
            img.save(os.environ["CAPTURA"])
        app.quit()

    QTimer.singleShot(1200, fim)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
