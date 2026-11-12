"""Proxy models: sorting/filtering, transposition and concatenation."""

import sys

from PyQt6.QtCore import (
    QConcatenateTablesProxyModel,
    QRegularExpression,
    QSortFilterProxyModel,
    Qt,
    QTransposeProxyModel,
)
from PyQt6.QtWidgets import QApplication, QTableView

from c14_table_model import PressureTest, TestModel


def tags(model) -> list[str]:
    return [model.index(r, 0).data() for r in range(model.rowCount())]


class PressureFilter(QSortFilterProxyModel):
    """Filters by tag text AND by minimum pressure (custom filter)."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.min_pressure = 0.0

    def filterAcceptsRow(self, row: int, parent) -> bool:
        source = self.sourceModel()
        p = source.index(row, 1, parent).data(Qt.ItemDataRole.EditRole)
        return p >= self.min_pressure and super().filterAcceptsRow(row, parent)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    base = TestModel(
        [
            PressureTest("BOP-02", 310.5, False),
            PressureTest("BOP-01", 345.0, True),
            PressureTest("XT-07", 690.0, True),
        ]
    )

    proxy = PressureFilter()
    proxy.setSourceModel(base)
    proxy.setSortRole(Qt.ItemDataRole.EditRole)  # sorts by the numeric value
    proxy.setFilterKeyColumn(0)
    view = QTableView()
    view.setModel(proxy)
    view.setSortingEnabled(True)

    proxy.sort(1, Qt.SortOrder.DescendingOrder)
    print("sorted by pressure (desc):", tags(proxy))
    proxy.setFilterRegularExpression(QRegularExpression("^BOP"))
    print("filter ^BOP:", tags(proxy))
    proxy.min_pressure = 320.0
    # reapplies the custom filter
    proxy.invalidateRowsFilter()
    print("^BOP and >= 320 bar:", tags(proxy))
    source = proxy.mapToSource(proxy.index(0, 0))
    print("proxy row 0 = row", source.row(), "of the source model")

    transposed = QTransposeProxyModel()
    transposed.setSourceModel(base)
    print(
        "transposed:",
        transposed.rowCount(),
        "x",
        transposed.columnCount(),
        "| row 0:",
        [transposed.index(0, c).data() for c in range(transposed.columnCount())],
    )

    extra = TestModel([PressureTest("MPD-01", 100.0, True)])
    joined = QConcatenateTablesProxyModel()
    joined.addSourceModel(base)
    joined.addSourceModel(extra)
    print("concatenated:", tags(joined))
