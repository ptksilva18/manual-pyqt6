"""Modelos Model/View que expõem os dados do repositório à interface."""

from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt

from .dominio import Leitura


class ModeloEnsaios(QAbstractTableModel):
    CABECALHO = ("Código", "Descrição")

    def __init__(self) -> None:
        super().__init__()
        self._linhas: list[tuple[int, str, str]] = []

    def recarregar(self, linhas: list[tuple[int, str, str]]) -> None:
        self.beginResetModel()
        self._linhas = list(linhas)
        self.endResetModel()

    def ensaio_id(self, linha: int) -> int:
        return self._linhas[linha][0]

    def rowCount(self, parent=QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self._linhas)

    def columnCount(self, parent=QModelIndex()) -> int:
        return 0 if parent.isValid() else 2

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid() and role == Qt.ItemDataRole.DisplayRole:
            return self._linhas[index.row()][index.column() + 1]
        return None

    def headerData(self, secao, orientacao, role=Qt.ItemDataRole.DisplayRole):
        if (
            role == Qt.ItemDataRole.DisplayRole
            and orientacao == Qt.Orientation.Horizontal
        ):
            return self.CABECALHO[secao]
        return None


class ModeloLeituras(QAbstractTableModel):
    CABECALHO = ("Tempo (min)", "Pressão (bar)", "Temperatura (°C)")
    FORMATOS = ("{:.1f}", "{:.3f}", "{:.2f}")

    def __init__(self) -> None:
        super().__init__()
        self._leituras: list[Leitura] = []

    def definir(self, leituras: list[Leitura]) -> None:
        self.beginResetModel()
        self._leituras = list(leituras)
        self.endResetModel()

    def leituras(self) -> list[Leitura]:
        return list(self._leituras)

    def rowCount(self, parent=QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self._leituras)

    def columnCount(self, parent=QModelIndex()) -> int:
        return 0 if parent.isValid() else 3

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        valor = (
            self._leituras[index.row()].t_min,
            self._leituras[index.row()].p_bar,
            self._leituras[index.row()].temp_c,
        )[index.column()]
        if role == Qt.ItemDataRole.DisplayRole:
            return self.FORMATOS[index.column()].format(valor)
        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        return None

    def headerData(self, secao, orientacao, role=Qt.ItemDataRole.DisplayRole):
        if (
            role == Qt.ItemDataRole.DisplayRole
            and orientacao == Qt.Orientation.Horizontal
        ):
            return self.CABECALHO[secao]
        return None
