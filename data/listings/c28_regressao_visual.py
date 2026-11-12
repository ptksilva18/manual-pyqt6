# runner: ticks=60
"""Regressão visual: compara a renderização de um widget com uma imagem de referência."""

import os
import sys
import tempfile

from PyQt6.QtGui import QColor, QFont, QImage
from PyQt6.QtWidgets import QApplication, QStyleFactory

from c28_calculadora import Calculadora


def renderizar(estilo_extra: str = "") -> QImage:
    w = Calculadora()
    w.setFont(QFont("DejaVu Sans", 10))  # fonte fixa: resultados reprodutíveis
    w.setStyleSheet(estilo_extra)
    w.resize(320, 120)
    w.entrada.setText("1350")
    w.calcular()
    img = w.grab().toImage().convertToFormat(QImage.Format.Format_RGB32)
    w.deleteLater()
    return img


def comparar(
    atual: QImage, referencia: QImage, tolerancia: int = 8
) -> tuple[int, float]:
    """Conta pixels cuja diferença máxima por canal excede a tolerância (0-255)."""
    if atual.size() != referencia.size():
        return -1, 100.0
    diferentes = 0
    for y in range(atual.height()):
        for x in range(atual.width()):
            a, r = QColor(atual.pixel(x, y)), QColor(referencia.pixel(x, y))
            if (
                max(
                    abs(a.red() - r.red()),
                    abs(a.green() - r.green()),
                    abs(a.blue() - r.blue()),
                )
                > tolerancia
            ):
                diferentes += 1
    return diferentes, 100.0 * diferentes / (atual.width() * atual.height())


def main() -> int:
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))  # estilo independente da plataforma
    pasta = tempfile.mkdtemp()
    caminho_ref = os.path.join(pasta, "calculadora_ref.png")
    referencia = renderizar()
    referencia.save(caminho_ref)  # em projeto real: versionada com o código e revisada
    print(f"Referência {referencia.width()}x{referencia.height()} gravada")

    n, pct = comparar(
        renderizar(), QImage(caminho_ref).convertToFormat(QImage.Format.Format_RGB32)
    )
    print(
        f"Renderização idêntica: {n} pixels diferentes ({pct:.2f} %) -> "
        f"{'PASSOU' if n == 0 else 'FALHOU'}"
    )
    n, pct = comparar(renderizar("QLabel#resultado { color: #C00000; }"), referencia)
    print(
        f"Cor do resultado alterada: {n} pixels diferentes ({pct:.2f} %) -> "
        f"{'PASSOU' if n == 0 else 'FALHOU (regressão detectada)'}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
