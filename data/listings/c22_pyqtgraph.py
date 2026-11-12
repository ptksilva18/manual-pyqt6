# runner: ticks=60
"""pyqtgraph: gráfico em tempo real com buffer circular numpy e QTimer."""

import os
import sys
import time

import numpy as np
import pyqtgraph as pg
from PyQt6.QtCore import QElapsedTimer, QTimer
from PyQt6.QtWidgets import QApplication


class Osciloscopio(pg.PlotWidget):
    def __init__(self, n_pontos: int = 2_000, taxa_hz: float = 1_000.0) -> None:
        super().__init__(background="w")
        self.n, self.dt = n_pontos, 1.0 / taxa_hz
        self.t = np.arange(-n_pontos, 0) * self.dt
        self.y = np.zeros(n_pontos)
        self.fase = 0.0
        self.setLabel("bottom", "Tempo", units="s")
        self.setLabel("left", "Aceleração", units="g")
        self.showGrid(x=True, y=True, alpha=0.3)
        self.setYRange(-1.5, 1.5)
        self.curva = self.plot(self.t, self.y, pen=pg.mkPen("#2E75B6", width=1.5))
        self.curva.setClipToView(True)  # desenha só o trecho visível
        self.curva.setDownsampling(
            auto=True, method="peak"
        )  # preserva picos ao reduzir
        self.quadros = 0
        self.relogio = QElapsedTimer()
        self.relogio.start()

    def novas_amostras(self, k: int) -> np.ndarray:
        tt = self.fase + np.arange(1, k + 1) * self.dt
        self.fase = tt[-1]
        return 0.8 * np.sin(2 * np.pi * 12.0 * tt) + 0.2 * np.sin(2 * np.pi * 95.0 * tt)

    def atualizar(self) -> None:
        k = 20  # 20 amostras por quadro de 20 ms = 1 kHz
        self.y = np.roll(self.y, -k)
        self.y[-k:] = self.novas_amostras(k)
        self.t = self.t + k * self.dt
        self.curva.setData(self.t, self.y)  # substitui os dados; sem recriar itens
        self.quadros += 1


def main() -> int:
    pg.setConfigOptions(antialias=False)  # mais rápido para sinais densos
    app = QApplication(sys.argv)
    osc = Osciloscopio()
    osc.resize(800, 360)
    osc.show()
    timer = QTimer()
    timer.setInterval(20)
    timer.timeout.connect(osc.atualizar)
    timer.start()

    def fim() -> None:
        timer.stop()
        seg = osc.relogio.elapsed() / 1000.0
        print(
            f"pyqtgraph {pg.__version__}: {osc.quadros} quadros em {seg:.1f} s "
            f"(~{osc.quadros / seg:.0f} quadros/s; alvo 50)"
        )
        print(
            f"Janela de dados: {osc.n} pontos, t = [{osc.t[0]:.3f}; {osc.t[-1]:.3f}] s"
        )
        destino = os.environ.get("CAPTURA")
        if destino:
            osc.grab().save(destino)
        app.quit()

    QTimer.singleShot(3000, fim)
    t0 = time.perf_counter()
    codigo = app.exec()
    print(f"Tempo total no event loop: {time.perf_counter() - t0:.1f} s")
    return codigo


if __name__ == "__main__":
    sys.exit(main())
