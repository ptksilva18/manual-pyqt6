"""Model/View models that expose the repository data to the interface."""

from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt

from .domain import Reading


class TestListModel(QAbstractTableModel):
    HEADER = ("Code", "Description")

    def __init__(self) -> None:
        super().__init__()
        self._rows: list[tuple[int, str, str]] = []

    def reload(self, rows: list[tuple[int, str, str]]) -> None:
        self.beginResetModel()
        self._rows = list(rows)
        self.endResetModel()

    def test_id(self, row: int) -> int:
        return self._rows[row][0]

    def rowCount(self, parent=QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self._rows)

    def columnCount(self, parent=QModelIndex()) -> int:
        return 0 if parent.isValid() else 2

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid() and role == Qt.ItemDataRole.DisplayRole:
            return self._rows[index.row()][index.column() + 1]
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if (
            role == Qt.ItemDataRole.DisplayRole
            and orientation == Qt.Orientation.Horizontal
        ):
            return self.HEADER[section]
        return None


class ReadingsModel(QAbstractTableModel):
    HEADER = ("Time (min)", "Pressure (bar)", "Temperature (°C)")
    FORMATS = ("{:.1f}", "{:.3f}", "{:.2f}")

    def __init__(self) -> None:
        super().__init__()
        self._readings: list[Reading] = []

    def set_readings(self, readings: list[Reading]) -> None:
        self.beginResetModel()
        self._readings = list(readings)
        self.endResetModel()

    def readings(self) -> list[Reading]:
        return list(self._readings)

    def rowCount(self, parent=QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self._readings)

    def columnCount(self, parent=QModelIndex()) -> int:
        return 0 if parent.isValid() else 3

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        value = (
            self._readings[index.row()].t_min,
            self._readings[index.row()].p_bar,
            self._readings[index.row()].temp_c,
        )[index.column()]
        if role == Qt.ItemDataRole.DisplayRole:
            return self.FORMATS[index.column()].format(value)
        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if (
            role == Qt.ItemDataRole.DisplayRole
            and orientation == Qt.Orientation.Horizontal
        ):
            return self.HEADER[section]
        return None
