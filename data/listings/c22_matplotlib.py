# runner: ticks=40
"""Matplotlib embutido: FigureCanvasQTAgg, NavigationToolbar2QT e redesenho por
parâmetro."""

import os
import sys

import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QApplication,
    QDoubleSpinBox,
    QFormLayout,
    QHBoxLayout,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)


class Canvas(FigureCanvasQTAgg):
    def __init__(self) -> None:
        self.fig = Figure(figsize=(6.0, 4.0), layout="constrained")
        super().__init__(self.fig)  # o canvas É um QWidget
        self.ax = self.fig.add_subplot()


class JanelaResposta(QMainWindow):
    """Resposta de um sistema massa-mola-amortecedor a um degrau unitário."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Resposta ao degrau — Matplotlib + PyQt6")
        self.canvas = Canvas()
        self.zeta = QDoubleSpinBox(
            minimum=0.05, maximum=2.0, singleStep=0.05, value=0.20
        )
        self.wn = QDoubleSpinBox(
            minimum=0.5, maximum=20.0, singleStep=0.5, value=4.0, suffix=" rad/s"
        )
        form = QFormLayout()
        form.addRow("Amortecimento ζ", self.zeta)
        form.addRow("Frequência natural ωn", self.wn)
        painel = QWidget()
        painel.setLayout(form)
        area = QVBoxLayout()
        area.addWidget(
            NavigationToolbar2QT(self.canvas, self)
        )  # zoom, pan, salvar figura
        area.addWidget(self.canvas)
        central = QWidget()
        lay = QHBoxLayout(central)
        lay.addLayout(area, 1)
        lay.addWidget(painel)
        self.setCentralWidget(central)
        (self.linha,) = self.canvas.ax.plot([], [], lw=2, color="#2E75B6")
        self.canvas.ax.axhline(1.0, color="0.5", ls="--", lw=1)
        self.canvas.ax.set_xlabel("t (s)", fontsize=9)
        self.canvas.ax.set_ylabel("x(t)", fontsize=9)
        self.canvas.ax.tick_params(labelsize=8)
        self.canvas.ax.grid(True, alpha=0.3)
        self.zeta.valueChanged.connect(self.atualizar)
        self.wn.valueChanged.connect(self.atualizar)
        self.atualizar()

    @staticmethod
    def resposta(t: np.ndarray, zeta: float, wn: float) -> np.ndarray:
        if zeta < 1.0:
            wd = wn * np.sqrt(1.0 - zeta**2)
            fase = np.arccos(zeta)
            return 1.0 - np.exp(-zeta * wn * t) * np.sin(wd * t + fase) / np.sqrt(
                1.0 - zeta**2
            )
        if zeta == 1.0:
            return 1.0 - np.exp(-wn * t) * (1.0 + wn * t)
        s1 = -wn * (zeta - np.sqrt(zeta**2 - 1.0))
        s2 = -wn * (zeta + np.sqrt(zeta**2 - 1.0))
        return 1.0 + (s2 * np.exp(s1 * t) - s1 * np.exp(s2 * t)) / (s1 - s2)

    def atualizar(self) -> None:
        t = np.linspace(0.0, 6.0, 600)
        x = self.resposta(t, self.zeta.value(), self.wn.value())
        self.linha.set_data(t, x)
        self.canvas.ax.relim()
        self.canvas.ax.autoscale_view()
        self.canvas.ax.set_title(
            f"ζ = {self.zeta.value():.2f}, ωn = {self.wn.value():.1f} rad/s"
            f" — sobressinal {100 * (x.max() - 1):.1f} %",
            fontsize=9,
        )
        self.canvas.draw_idle()  # agenda o redesenho; não bloqueia a cada mudança


def main() -> int:
    app = QApplication(sys.argv)
    janela = JanelaResposta()
    janela.resize(980, 500)
    janela.show()
    teorico = 100 * np.exp(-np.pi * 0.2 / np.sqrt(1 - 0.2**2))
    print(f"Título: {janela.canvas.ax.get_title()}")
    print(f"Sobressinal teórico para ζ = 0.20: {teorico:.1f} %")
    janela.zeta.setValue(0.70)
    print(f"Após ζ = 0.70: {janela.canvas.ax.get_title()}")
    janela.zeta.setValue(0.20)

    def capturar() -> None:
        destino = os.environ.get("CAPTURA")
        if destino:
            janela.grab().save(destino)
        app.quit()

    QTimer.singleShot(800, capturar)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
