"""Impressão em PDF (QPrinter), QPdfWriter, QSvgGenerator e QSvgRenderer."""

import sys
import tempfile
from pathlib import Path

from PyQt6.QtCore import QMarginsF, QRectF, QSize, Qt
from PyQt6.QtGui import (
    QColor,
    QFont,
    QImage,
    QPageLayout,
    QPageSize,
    QPainter,
    QPdfWriter,
)
from PyQt6.QtPrintSupport import QPrinter
from PyQt6.QtSvg import QSvgGenerator, QSvgRenderer
from PyQt6.QtWidgets import QApplication

PASTA = Path(tempfile.mkdtemp())


def pagina(p: QPainter, largura: int, titulo: str) -> None:
    p.setFont(QFont("DejaVu Sans", 16, QFont.Weight.Bold))
    p.drawText(QRectF(0, 0, largura, 60), Qt.AlignmentFlag.AlignCenter, titulo)
    p.setPen(QColor("#2E75B6"))
    p.drawRect(QRectF(0, 80, largura, 200))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    impressora = QPrinter(QPrinter.PrinterMode.HighResolution)
    # "imprime" em arquivo
    impressora.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
    impressora.setOutputFileName(str(PASTA / "via_qprinter.pdf"))
    impressora.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
    p = QPainter(impressora)
    pagina(p, impressora.width(), "Relatório via QPrinter")
    p.end()

    pdf = QPdfWriter(str(PASTA / "via_qpdfwriter.pdf"))
    pdf.setPageLayout(
        QPageLayout(
            QPageSize(QPageSize.PageSizeId.A4),
            QPageLayout.Orientation.Portrait,
            QMarginsF(15, 15, 15, 15),
            QPageLayout.Unit.Millimeter,
        )
    )
    pdf.setResolution(300)
    print("área útil a 300 dpi com margens de 15 mm:", pdf.width(), "x", pdf.height())
    pdf.setTitle("Relatório de ensaio")
    p = QPainter(pdf)
    pagina(p, pdf.width(), "Relatório via QPdfWriter")
    p.end()
    for nome in ("via_qprinter.pdf", "via_qpdfwriter.pdf"):
        cab = (PASTA / nome).read_bytes()[:5]
        print(f"{nome}: {(PASTA / nome).stat().st_size} bytes | cabeçalho {cab!r}")

    svg = QSvgGenerator()
    svg.setFileName(str(PASTA / "esquema.svg"))
    svg.setSize(QSize(200, 120))
    svg.setViewBox(QRectF(0, 0, 200, 120))
    p = QPainter(svg)
    p.setBrush(QColor("#EAF1FA"))
    p.drawRoundedRect(QRectF(10, 10, 180, 100), 10, 10)
    p.end()
    rend = QSvgRenderer(str(PASTA / "esquema.svg"))
    img = QImage(400, 240, QImage.Format.Format_ARGB32)
    img.fill(QColor("white"))
    p = QPainter(img)
    # SVG escala sem perda
    rend.render(p)
    p.end()
    print(
        "SVG válido?",
        rend.isValid(),
        "| viewBox:",
        rend.viewBoxF().width(),
        "x",
        rend.viewBoxF().height(),
        "| pixel central:",
        img.pixelColor(200, 120).name(),
    )
