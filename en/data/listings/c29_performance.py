# runner: ticks=600 timeout=180
"""Measurement and optimization: cProfile, QElapsedTimer, cached model, batch inserts."""

import cProfile
import io
import math
import pstats
import sys

from PyQt6.QtCore import QAbstractTableModel, QElapsedTimer, QLocale, QModelIndex, Qt
from PyQt6.QtWidgets import QApplication, QHeaderView, QTableView

N_ROWS, N_COLUMNS = 20_000, 6


def value(row: int, column: int) -> float:
    return math.sin(row * 0.001 + column) * 1000.0


class SlowModel(QAbstractTableModel):
    """Computes and formats on every call to data() — called thousands of times per
    paint."""

    def __init__(self) -> None:
        super().__init__()
        self.locale = QLocale(QLocale.Language.English, QLocale.Country.UnitedStates)

    def rowCount(self, parent=QModelIndex()) -> int:
        return 0 if parent.isValid() else N_ROWS

    def columnCount(self, parent=QModelIndex()) -> int:
        return 0 if parent.isValid() else N_COLUMNS

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            return self.locale.toString(value(index.row(), index.column()), "f", 3)
        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        return None


class FastModel(SlowModel):
    """Pre-formats once and answers only the roles used; constant alignment."""

    ALIGNMENT = Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter

    def __init__(self) -> None:
        super().__init__()
        self.cache = [
            [self.locale.toString(value(r, c), "f", 3) for c in range(N_COLUMNS)]
            for r in range(N_ROWS)
        ]

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            return self.cache[index.row()][index.column()]
        if role == Qt.ItemDataRole.TextAlignmentRole:
            return self.ALIGNMENT
        return None


def measure_painting(model, fit_columns: bool) -> float:
    view = QTableView()
    view.setModel(model)
    view.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
    view.resize(900, 600)
    view.show()
    QApplication.processEvents()
    clock = QElapsedTimer()
    clock.start()
    if fit_columns:
        # Measures the text of up to resizeContentsPrecision() rows per column
        # (default: 1000).
        view.resizeColumnsToContents()
    for _ in range(20):
        view.viewport().repaint()
    ms = clock.nsecsElapsed() / 1e6
    view.close()
    return ms


def main() -> int:
    app = QApplication(sys.argv)  # noqa: F841
    profile = cProfile.Profile()
    profile.enable()
    t_slow = measure_painting(SlowModel(), fit_columns=True)
    profile.disable()
    clock = QElapsedTimer()
    clock.start()
    fast = FastModel()
    t_cache = clock.nsecsElapsed() / 1e6
    t_fast = measure_painting(fast, fit_columns=False)
    print(f"Slow model + resizeColumnsToContents: {t_slow:8.1f} ms")
    print(
        f"Cached model, fixed widths          : {t_fast:8.1f} ms "
        f"(~{t_slow / t_fast:.0f}x faster)"
    )
    table = (
        QTableView()
    )  # keep the reference: the header belongs to the table (Section 29.4)
    print(
        f"One-off cost of pre-formatting {N_ROWS * N_COLUMNS} cells: {t_cache:.1f} ms; "
        f"resizeColumnsToContents precision: "
        f"{table.horizontalHeader().resizeContentsPrecision()} rows"
    )
    output = io.StringIO()
    pstats.Stats(profile, stream=output).sort_stats("cumulative").print_stats(
        "data|value", 3
    )
    print("cProfile — most expensive Python functions (filter 'data|value'):")
    for line in output.getvalue().splitlines():
        if "ncalls" in line or ("c29_performance.py" in line and "(" in line):
            print("  " + line.replace(__file__, "c29_performance.py").strip())
    return 0


if __name__ == "__main__":
    sys.exit(main())
