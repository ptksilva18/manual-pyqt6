# runner: ticks=600 timeout=120
"""Custo por atualização (dados + pintura) de pyqtgraph, QtCharts e Matplotlib."""

import sys
import time

import numpy as np
import pyqtgraph as pg
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtWidgets import QApplication, QGraphicsView

N_PONTOS, N_QUADROS = 20_000, 30


def medir(nome: str, preparar, atualizar, widget) -> float:
    widget.resize(800, 400)
    widget.show()
    preparar()
    QApplication.processEvents()
    tempos = []
    for k in range(N_QUADROS):
        t0 = time.perf_counter()
        atualizar(k)
        # Pintura síncrona para medir o ciclo completo. Em QGraphicsView (pyqtgraph e
        # QtCharts) a cena é desenhada no viewport: repaint() da moldura não basta.
        alvo = widget.viewport() if isinstance(widget, QGraphicsView) else widget
        alvo.repaint()
        tempos.append(time.perf_counter() - t0)
    widget.close()
    mediana = 1000.0 * float(np.median(tempos))
    print(
        f"{nome:<34} mediana {mediana:7.1f} ms/quadro  (~{1000.0 / mediana:5.0f} "
        "quadros/s)"
    )
    return mediana


def main() -> int:
    app = QApplication(sys.argv)
    x = np.linspace(0.0, 10.0, N_PONTOS)

    def sinal(k: int) -> np.ndarray:
        return np.sin(2 * np.pi * (x + 0.05 * k)) + 0.1 * np.cos(40.0 * x)

    pw = pg.PlotWidget()
    curva = pw.plot(pen="b")
    medir("pyqtgraph setData", lambda: None, lambda k: curva.setData(x, sinal(k)), pw)

    chart = QChart()
    serie = QLineSeries()
    chart.addSeries(serie)
    ax, ay = QValueAxis(), QValueAxis()
    ax.setRange(0, 10)
    ay.setRange(-1.2, 1.2)
    chart.addAxis(ax, Qt.AlignmentFlag.AlignBottom)
    chart.addAxis(ay, Qt.AlignmentFlag.AlignLeft)
    serie.attachAxis(ax)
    serie.attachAxis(ay)
    vista = QChartView(chart)
    medir(
        "QtCharts replace(lista QPointF)",
        lambda: None,
        lambda k: serie.replace([QPointF(a, b) for a, b in zip(x, sinal(k))]),
        vista,
    )

    fig = Figure(figsize=(8, 4))
    canvas = FigureCanvasQTAgg(fig)
    eixo = fig.add_subplot()
    (linha,) = eixo.plot(x, sinal(0))

    def mpl(k: int) -> None:
        linha.set_ydata(sinal(k))
        canvas.draw()  # redesenho completo (sem blitting)

    medir("Matplotlib set_ydata + draw()", lambda: None, mpl, canvas)
    print(
        f"({N_PONTOS} pontos por quadro; valores dependem da máquina e do backend "
        "gráfico)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
