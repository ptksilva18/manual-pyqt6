"""CSV com o módulo csv e com pandas, exibido em QTableView por um modelo genérico."""

import csv
import io
import sys

import pandas as pd
from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt6.QtWidgets import QApplication, QTableView

CSV = "tag;pressao_bar;data\nBOP-01;345,0;2026-11-10\nBOP-02;310,5;2026-11-11\n"


class ModeloDataFrame(QAbstractTableModel):
    """Modelo somente leitura para qualquer DataFrame."""

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
    linhas = list(csv.DictReader(io.StringIO(CSV), delimiter=";"))
    print("csv.DictReader:", [(l["tag"], l["pressao_bar"]) for l in linhas])

    df = pd.read_csv(io.StringIO(CSV), sep=";", decimal=",", parse_dates=["data"])
    print("tipos pandas:", {c: str(t) for c, t in df.dtypes.items()})
    print("média de pressão:", df["pressao_bar"].mean())
    vista = QTableView()
    vista.setModel(ModeloDataFrame(df, vista))
    m = vista.model()
    print(
        "modelo:", m.rowCount(), "x", m.columnCount(), "| (1, 1):", m.index(1, 1).data()
    )
