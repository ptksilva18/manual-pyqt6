"""Custom table model: reading, editing, roles and insertion/removal."""

import sys
from dataclasses import dataclass

from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt6.QtGui import QColor
from PyQt6.QtTest import QAbstractItemModelTester
from PyQt6.QtWidgets import QApplication, QTableView

R = Qt.ItemDataRole


@dataclass
class PressureTest:
    tag: str
    pressure_bar: float
    passed: bool


class TestModel(QAbstractTableModel):
    COLUMNS = ("Tag", "Pressure (bar)", "Passed")

    def __init__(self, tests: list[PressureTest], parent=None) -> None:
        super().__init__(parent)
        self._data = tests

    # ------------------------------------------------------ reading (mandatory) --
    def rowCount(self, parent=QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self._data)  # table: no children

    def columnCount(self, parent=QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self.COLUMNS)

    def data(self, index: QModelIndex, role: int = R.DisplayRole):
        if not index.isValid():
            return None
        t, col = self._data[index.row()], index.column()
        if role == R.DisplayRole:
            return (t.tag, f"{t.pressure_bar:.1f}", "Yes" if t.passed else "No")[col]
        if role == R.EditRole:
            return (t.tag, t.pressure_bar, t.passed)[col]
        if role == R.TextAlignmentRole and col == 1:
            return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        if role == R.ForegroundRole and not t.passed:
            return QColor("#C00000")  # failed tests in red
        return None

    def headerData(
        self, section: int, orientation: Qt.Orientation, role: int = R.DisplayRole
    ):
        if role == R.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.COLUMNS[section]
        return None

    # ------------------------------------------------------------------ editing --
    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        base = super().flags(index)
        return base | Qt.ItemFlag.ItemIsEditable if index.isValid() else base

    def setData(self, index: QModelIndex, value, role: int = R.EditRole) -> bool:
        if role != R.EditRole or not index.isValid():
            return False
        t, col = self._data[index.row()], index.column()
        if col == 0:
            t.tag = str(value).strip().upper()
        elif col == 1:
            if float(value) <= 0:
                return False  # rejects invalid values
            t.pressure_bar = float(value)
        else:
            t.passed = bool(value)
        # 'passed' changes the color of the row
        if col == 2:
            last = self.index(index.row(), self.columnCount() - 1)
            self.dataChanged.emit(self.index(index.row(), 0), last)
        # others: only the edited cell
        else:
            self.dataChanged.emit(index, index, [R.DisplayRole, R.EditRole])
        return True

    # ------------------------------------------------------ insertion/removal --
    def insertRows(self, row: int, n: int, parent=QModelIndex()) -> bool:
        self.beginInsertRows(parent, row, row + n - 1)
        for _ in range(n):
            self._data.insert(row, PressureTest("NEW", 1.0, False))
        self.endInsertRows()
        return True

    def removeRows(self, row: int, n: int, parent=QModelIndex()) -> bool:
        self.beginRemoveRows(parent, row, row + n - 1)
        del self._data[row : row + n]
        self.endRemoveRows()
        return True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    model = TestModel(
        [PressureTest("BOP-01", 345.0, True), PressureTest("BOP-02", 310.5, False)]
    )
    tester = QAbstractItemModelTester(
        model, QAbstractItemModelTester.FailureReportingMode.Fatal
    )
    view = QTableView()
    view.setModel(model)
    view.show()

    model.dataChanged.connect(
        lambda a, b: print(f"dataChanged rows {a.row()}..{b.row()}")
    )
    print("cell (1,1) displayed:", model.index(1, 1).data())
    print("edit -10 accepted?", model.setData(model.index(1, 1), -10))
    print("edit 320 accepted?", model.setData(model.index(1, 1), 320))
    model.insertRows(2, 1)
    model.setData(model.index(2, 0), " bop-03 ")
    print("rows:", [model.index(r, 0).data() for r in range(model.rowCount())])
    model.removeRows(0, 1)
    print(
        "after removing the 1st:",
        [model.index(r, 0).data() for r in range(model.rowCount())],
    )
    sys.exit(app.exec())
