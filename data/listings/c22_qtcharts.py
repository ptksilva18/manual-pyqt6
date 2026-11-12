# runner: ticks=40
"""QtCharts (legado): QChart/QChartView com linha, dispersão, barras, eixos e pizza."""

import math
import os
import sys

from PyQt6.QtCharts import (
    QBarCategoryAxis,
    QBarSeries,
    QBarSet,
    QChart,
    QChartView,
    QLineSeries,
    QLogValueAxis,
    QPieSeries,
    QScatterSeries,
    QSplineSeries,
    QValueAxis,
)
from PyQt6.QtCore import QPointF, Qt, QTimer
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QApplication, QGridLayout, QWidget


def grafico_decaimento() -> QChart:
    """Pressão em teste de estanqueidade: medidas (dispersão) e ajuste (spline)."""
    ch = QChart()
    ch.setTitle("Teste de estanqueidade")
    medida, ajuste = QScatterSeries(), QSplineSeries()
    medida.setName("Medida")
    medida.setMarkerSize(8.0)
    ajuste.setName("Ajuste exponencial")
    for t in range(0, 61, 5):
        p = 345.0 - 6.0 * (1.0 - math.exp(-t / 15.0))
        ajuste.append(float(t), p)
        medida.append(float(t), p + (0.6 if t % 10 else -0.5))
    ch.addSeries(ajuste)
    ch.addSeries(medida)
    eixo_x, eixo_y = QValueAxis(), QValueAxis()
    eixo_x.setRange(0, 60)
    eixo_x.setTitleText("Tempo (min)")
    eixo_x.setLabelFormat("%.0f")
    eixo_y.setRange(337, 347)
    eixo_y.setTitleText("Pressão (bar)")
    ch.addAxis(eixo_x, Qt.AlignmentFlag.AlignBottom)
    ch.addAxis(eixo_y, Qt.AlignmentFlag.AlignLeft)
    for s in (ajuste, medida):  # a série precisa estar no gráfico antes de attachAxis
        s.attachAxis(eixo_x)
        s.attachAxis(eixo_y)
    return ch


def grafico_curva_sn() -> QChart:
    ch = QChart()
    ch.setTitle("Curva S-N (escala log)")
    curva = QLineSeries()
    curva.setName("N = 1e12 S^-3")
    curva.replace([QPointF(1e12 * s**-3.0, s) for s in (20, 40, 60, 80, 100, 150, 200)])
    ch.addSeries(curva)
    eixo_n = QLogValueAxis()
    eixo_n.setBase(10.0)
    eixo_n.setRange(1e5, 2e8)
    eixo_n.setLabelFormat("%.0e")
    eixo_n.setTitleText("Ciclos N")
    eixo_s = QValueAxis()
    eixo_s.setRange(0, 220)
    eixo_s.setTitleText("S (MPa)")
    eixo_s.setLabelFormat("%.0f")
    ch.addAxis(eixo_n, Qt.AlignmentFlag.AlignBottom)
    ch.addAxis(eixo_s, Qt.AlignmentFlag.AlignLeft)
    curva.attachAxis(eixo_n)
    curva.attachAxis(eixo_s)
    ch.legend().setVisible(False)
    return ch


def grafico_barras() -> QChart:
    ch = QChart()
    ch.setTitle("Horas de operação por mês")
    serie = QBarSeries()
    for nome, valores in (("Sonda A", [610, 702, 655]), ("Sonda B", [580, 690, 720])):
        conjunto = QBarSet(nome)
        conjunto.append([float(v) for v in valores])
        serie.append(conjunto)
    ch.addSeries(serie)
    eixo_cat = QBarCategoryAxis()
    eixo_cat.append(["Jan", "Fev", "Mar"])
    eixo_v = QValueAxis()
    eixo_v.setRange(0, 800)
    eixo_v.setLabelFormat("%.0f")
    ch.addAxis(eixo_cat, Qt.AlignmentFlag.AlignBottom)
    ch.addAxis(eixo_v, Qt.AlignmentFlag.AlignLeft)
    serie.attachAxis(eixo_cat)
    serie.attachAxis(eixo_v)
    return ch


def grafico_pizza() -> QChart:
    ch = QChart()
    ch.setTitle("Tempo não produtivo por causa")
    pizza = QPieSeries()
    for causa, horas in (
        ("Clima", 42.0),
        ("Equipamento", 31.0),
        ("Logística", 17.0),
        ("Outros", 10.0),
    ):
        pizza.append(causa, horas)
    for fatia in pizza.slices():  # percentage() só é final depois de todas as fatias
        fatia.setLabel(f"{fatia.label()} {fatia.percentage() * 100:.0f}%")
        fatia.setLabelVisible(True)
    pizza.slices()[0].setExploded(True)
    ch.addSeries(pizza)
    ch.legend().setVisible(False)
    return ch


def main() -> int:
    app = QApplication(sys.argv)
    janela = QWidget()
    janela.setWindowTitle("QtCharts")
    grade = QGridLayout(janela)
    graficos = [
        grafico_decaimento(),
        grafico_curva_sn(),
        grafico_barras(),
        grafico_pizza(),
    ]
    for i, ch in enumerate(graficos):
        ch.setAnimationOptions(QChart.AnimationOption.NoAnimation)
        vista = QChartView(ch)
        vista.setRenderHint(QPainter.RenderHint.Antialiasing)
        grade.addWidget(vista, i // 2, i % 2)
        tipos = sorted({type(s).__name__ for s in ch.series()})
        eixos = [type(a).__name__ for a in ch.axes()]
        print(f"{ch.title():<32} séries={tipos} eixos={eixos}")
    print("Rótulos da pizza:", [f.label() for f in graficos[3].series()[0].slices()])
    janela.resize(1100, 760)
    janela.show()

    def capturar() -> None:
        destino = os.environ.get("CAPTURA")
        if destino:
            janela.grab().save(destino)
        app.quit()

    QTimer.singleShot(600, capturar)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
