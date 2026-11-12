"""CSV with the csv module and with pandas, shown in a QTableView by a generic model."""

import csv
import io
import sys

import pandas as pd
from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt6.QtWidgets import QApplication, QTableView

CSV = "tag;pressure_bar;date\nBOP-01;345,0;2026-11-10\nBOP-02;310,5;2026-11-11\n"


class DataFrameModel(QAbstractTableModel):
    """Read-only model for any DataFrame."""

    def __init__(self, df: pd.DataFrame, parent=None) -> None:
        super().__init__(parent)
        self._df = df

    def rowCount(self, parent=QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self._df)

    def columnCount(self, parent=QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self._df.columns)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid() and role == Qt.ItemDataRole.DisplayRole:
            return str(self._df.iat[index.row(), index.column()])
        return None

    def headerData(self, s, o, role=Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        return (
            str(self._df.columns[s]) if o == Qt.Orientation.Horizontal else str(s + 1)
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    rows = list(csv.DictReader(io.StringIO(CSV), delimiter=";"))
    print("csv.DictReader:", [(r["tag"], r["pressure_bar"]) for r in rows])

    df = pd.read_csv(io.StringIO(CSV), sep=";", decimal=",", parse_dates=["date"])
    print("pandas dtypes:", {c: str(t) for c, t in df.dtypes.items()})
    print("mean pressure:", df["pressure_bar"].mean())
    view = QTableView()
    view.setModel(DataFrameModel(df, view))
    m = view.model()
    print("model:", m.rowCount(), "x", m.columnCount(), "| (1, 1):", m.index(1, 1).data())
