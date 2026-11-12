"""Widget personalizado: manômetro analógico desenhado com QPainter."""

import math
import sys

from PyQt6.QtCore import QPointF, QRectF, QSize, Qt, pyqtProperty, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QPainter, QPen, QPolygonF
from PyQt6.QtWidgets import QApplication, QSizePolicy, QWidget


class Manometro(QWidget):
    valorChanged = pyqtSignal(float)

    def __init__(
        self, maximo: float = 690.0, unidade: str = "bar", parent=None
    ) -> None:
        super().__init__(parent)
        self._valor, self.maximo, self.unidade = 0.0, maximo, unidade
        self.faixas = [
            (0.0, 0.7, "#70AD47"),
            (0.7, 0.9, "#FFC000"),
            (0.9, 1.0, "#C00000"),
        ]
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def sizeHint(self) -> QSize:
        return QSize(260, 260)

    def minimumSizeHint(self) -> QSize:
        return QSize(120, 120)

    def _get_valor(self) -> float:
        return self._valor

    def _set_valor(self, v: float) -> None:
        v = max(0.0, min(v, self.maximo))
        if v != self._valor:
            self._valor = v
            self.valorChanged.emit(v)
            # agenda repintura (não pinta já)
            self.update()

    valor = pyqtProperty(float, _get_valor, _set_valor, notify=valorChanged)

    def paintEvent(self, evento) -> None:
        lado = min(self.width(), self.height())
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.translate(self.width() / 2, self.height() / 2)
        # coordenadas lógicas: -100..100
        p.scale(lado / 200.0, lado / 200.0)
        # ângulos em graus (sentido horário)
        ini, varr = 225.0, -270.0

        p.setPen(QPen(QColor("#595959"), 3))
        p.setBrush(QColor("#FAFAFA"))
        p.drawEllipse(QPointF(0, 0), 95, 95)
        arco = QRectF(-80, -80, 160, 160)
        for a, b, cor in self.faixas:  # faixas operacionais
            p.setPen(QPen(QColor(cor), 10, cap=Qt.PenCapStyle.FlatCap))
            p.drawArc(arco, int((ini + varr * a) * 16), int(varr * (b - a) * 16))

        p.setPen(QPen(QColor("#1E1E1E"), 2))
        p.setFont(QFont("DejaVu Sans", 7))
        for i in range(11):  # marcas e números da escala
            ang = math.radians(ini + varr * i / 10)
            c, s = math.cos(ang), -math.sin(ang)
            p.drawLine(QPointF(70 * c, 70 * s), QPointF(86 * c, 86 * s))
            # 1.5 não vira "2" por arredondamento
            txt = f"{self.maximo * i / 10:g}"
            p.drawText(
                QRectF(58 * c - 15, 58 * s - 7, 30, 14),
                Qt.AlignmentFlag.AlignCenter,
                txt,
            )

        p.setFont(QFont("DejaVu Sans", 11, QFont.Weight.Bold))
        p.drawText(
            QRectF(-50, 58, 100, 20),
            Qt.AlignmentFlag.AlignCenter,
            f"{self._valor:.1f} {self.unidade}",
        )

        ang = ini + varr * self._valor / self.maximo  # ponteiro
        p.rotate(-ang)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor("#C00000"))
        p.drawPolygon(QPolygonF([QPointF(0, -4), QPointF(78, 0), QPointF(0, 4)]))
        p.setBrush(QColor("#1F3864"))
        p.drawEllipse(QPointF(0, 0), 7, 7)
        p.end()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    m = Manometro(maximo=690.0)
    m.valorChanged.connect(lambda v: print(f"valorChanged -> {v:.1f}"))
    m.valor = 345.0
    m.setProperty("valor", 900.0)  # limitado ao máximo
    m.resize(m.sizeHint())
    m.show()
    imagem = m.grab()  # renderiza o paintEvent
    print(
        "renderizado:", imagem.width(), "x", imagem.height(), "| nulo?", imagem.isNull()
    )
    sys.exit(app.exec())
