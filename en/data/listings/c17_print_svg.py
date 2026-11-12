"""Printing to PDF (QPrinter), QPdfWriter, QSvgGenerator and QSvgRenderer."""

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

FOLDER = Path(tempfile.mkdtemp())


def page(p: QPainter, width: int, title: str) -> None:
    p.setFont(QFont("DejaVu Sans", 16, QFont.Weight.Bold))
    p.drawText(QRectF(0, 0, width, 60), Qt.AlignmentFlag.AlignCenter, title)
    p.setPen(QColor("#2E75B6"))
    p.drawRect(QRectF(0, 80, width, 200))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    printer = QPrinter(QPrinter.PrinterMode.HighResolution)
    # "prints" to a file
    printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
    printer.setOutputFileName(str(FOLDER / "via_qprinter.pdf"))
    printer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
    p = QPainter(printer)
    page(p, printer.width(), "Report via QPrinter")
    p.end()

    pdf = QPdfWriter(str(FOLDER / "via_qpdfwriter.pdf"))
    pdf.setPageLayout(
        QPageLayout(
            QPageSize(QPageSize.PageSizeId.A4),
            QPageLayout.Orientation.Portrait,
            QMarginsF(15, 15, 15, 15),
            QPageLayout.Unit.Millimeter,
        )
    )
    pdf.setResolution(300)
    print("printable area at 300 dpi with 15 mm margins:", pdf.width(), "x", pdf.height())
    pdf.setTitle("Test report")
    p = QPainter(pdf)
    page(p, pdf.width(), "Report via QPdfWriter")
    p.end()
    for name in ("via_qprinter.pdf", "via_qpdfwriter.pdf"):
        head = (FOLDER / name).read_bytes()[:5]
        print(f"{name}: {(FOLDER / name).stat().st_size} bytes | header {head!r}")

    svg = QSvgGenerator()
    svg.setFileName(str(FOLDER / "diagram.svg"))
    svg.setSize(QSize(200, 120))
    svg.setViewBox(QRectF(0, 0, 200, 120))
    p = QPainter(svg)
    p.setBrush(QColor("#EAF1FA"))
    p.drawRoundedRect(QRectF(10, 10, 180, 100), 10, 10)
    p.end()
    rend = QSvgRenderer(str(FOLDER / "diagram.svg"))
    img = QImage(400, 240, QImage.Format.Format_ARGB32)
    img.fill(QColor("white"))
    p = QPainter(img)
    # SVG scales without loss
    rend.render(p)
    p.end()
    print(
        "valid SVG?",
        rend.isValid(),
        "| viewBox:",
        rend.viewBoxF().width(),
        "x",
        rend.viewBoxF().height(),
        "| center pixel:",
        img.pixelColor(200, 120).name(),
    )
