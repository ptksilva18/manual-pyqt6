# runner: ticks=60
"""Visual regression: compares a widget's rendering with a reference image."""

import os
import sys
import tempfile

from PyQt6.QtGui import QColor, QFont, QImage
from PyQt6.QtWidgets import QApplication, QStyleFactory

from c28_calculator import Calculator


def render(extra_style: str = "") -> QImage:
    w = Calculator()
    w.setFont(QFont("DejaVu Sans", 10))  # fixed font: reproducible results
    w.setStyleSheet(extra_style)
    w.resize(320, 120)
    w.entry.setText("1350")
    w.compute()
    img = w.grab().toImage().convertToFormat(QImage.Format.Format_RGB32)
    w.deleteLater()
    return img


def compare(
    current: QImage, reference: QImage, tolerance: int = 8
) -> tuple[int, float]:
    """Counts pixels whose largest per-channel difference exceeds the tolerance."""
    if current.size() != reference.size():
        return -1, 100.0
    different = 0
    for y in range(current.height()):
        for x in range(current.width()):
            a, r = QColor(current.pixel(x, y)), QColor(reference.pixel(x, y))
            if (
                max(
                    abs(a.red() - r.red()),
                    abs(a.green() - r.green()),
                    abs(a.blue() - r.blue()),
                )
                > tolerance
            ):
                different += 1
    return different, 100.0 * different / (current.width() * current.height())


def main() -> int:
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))  # platform-independent style
    folder = tempfile.mkdtemp()
    ref_path = os.path.join(folder, "calculator_ref.png")
    reference = render()
    reference.save(ref_path)  # in a real project: versioned with the code and reviewed
    print(f"Reference {reference.width()}x{reference.height()} saved")

    n, pct = compare(
        render(), QImage(ref_path).convertToFormat(QImage.Format.Format_RGB32)
    )
    print(
        f"Identical rendering: {n} different pixels ({pct:.2f} %) -> "
        f"{'PASSED' if n == 0 else 'FAILED'}"
    )
    n, pct = compare(render("QLabel#result { color: #C00000; }"), reference)
    print(
        f"Result color changed: {n} different pixels ({pct:.2f} %) -> "
        f"{'PASSED' if n == 0 else 'FAILED (regression detected)'}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
