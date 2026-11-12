# runner: ticks=40 xcb
"""QtGraphs 2D: GraphsView (QML) dentro de uma aplicação Widgets, alimentado pelo
Python."""

import os
import sys

from PyQt6.QtCore import QPointF, QTimer, QUrl
from PyQt6.QtGraphs import QLineSeries, QScatterSeries, QValueAxis
from PyQt6.QtQuickWidgets import QQuickWidget
from PyQt6.QtWidgets import QApplication

AQUI = os.path.dirname(os.path.abspath(__file__))
RHO_FLUIDO = 1030.0  # kg/m3 (água do mar)
G = 9.80665  # m/s2


def pressao_bar(prof_m: float) -> float:
    return RHO_FLUIDO * G * prof_m / 1e5 + 1.01325


def main() -> int:
    app = QApplication(sys.argv)
    vista = QQuickWidget()
    vista.setResizeMode(QQuickWidget.ResizeMode.SizeRootObjectToView)
    vista.setSource(QUrl.fromLocalFile(os.path.join(AQUI, "c22_graphs2d.qml")))
    if vista.status() != QQuickWidget.Status.Ready:
        for erro in vista.errors():
            print(erro.toString())
        return 1
    raiz = vista.rootObject()
    linha = raiz.findChild(QLineSeries, "hidrostatica")
    pontos = raiz.findChild(QScatterSeries, "medida")
    eixo_y = raiz.findChild(QValueAxis, "eixoY")
    print("Séries encontradas:", type(linha).__name__, type(pontos).__name__)

    linha.replace(
        [QPointF(z, pressao_bar(z)) for z in range(0, 3001, 100)]
    )  # 1 só sinal
    medidas = [(800.0, 84.1), (1500.0, 155.9), (2200.0, 228.6), (2900.0, 301.0)]
    for z, p in medidas:
        pontos.append(z, p)
    eixo_y.setMax(350.0)
    print(
        f"Pontos: linha = {linha.count()}, medidas = {pontos.count()}; "
        f"eixo Y até {eixo_y.max():.0f} bar"
    )
    print(f"p(2900 m) teórica = {pressao_bar(2900):.1f} bar")

    vista.resize(760, 440)
    vista.show()

    def capturar() -> None:
        destino = os.environ.get("CAPTURA")
        if destino:
            vista.grabFramebuffer().save(destino)
        app.quit()

    QTimer.singleShot(1200, capturar)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
