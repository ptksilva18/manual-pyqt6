"""Modelo de tabela personalizado: leitura, edição, papéis e inserção/remoção."""

import sys
from dataclasses import dataclass

from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt6.QtGui import QColor
from PyQt6.QtTest import QAbstractItemModelTester
from PyQt6.QtWidgets import QApplication, QTableView

R = Qt.ItemDataRole


@dataclass
class Ensaio:
    tag: str
    pressao_bar: float
    aprovado: bool


class ModeloEnsaios(QAbstractTableModel):
    COLUNAS = ("Tag", "Pressão (bar)", "Aprovado")

    def __init__(self, ensaios: list[Ensaio], parent=None) -> None:
        super().__init__(parent)
        self._dados = ensaios

    # ---------------------------------------------------- leitura (obrigatória) --
    def rowCount(self, parent=QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self._dados)  # tabela: sem filhos

    def columnCount(self, parent=QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self.COLUNAS)

    def data(self, index: QModelIndex, role: int = R.DisplayRole):
        if not index.isValid():
            return None
        e, col = self._dados[index.row()], index.column()
        if role == R.DisplayRole:
            return (e.tag, f"{e.pressao_bar:.1f}", "Sim" if e.aprovado else "Não")[col]
        if role == R.EditRole:
            return (e.tag, e.pressao_bar, e.aprovado)[col]
        if role == R.TextAlignmentRole and col == 1:
            return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        if role == R.ForegroundRole and not e.aprovado:
            return QColor("#C00000")  # reprovados em vermelho
        return None

    def headerData(
        self, secao: int, orientacao: Qt.Orientation, role: int = R.DisplayRole
    ):
        if role == R.DisplayRole and orientacao == Qt.Orientation.Horizontal:
            return self.COLUNAS[secao]
        return None

    # ------------------------------------------------------------------- edição --
    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        base = super().flags(index)
        return base | Qt.ItemFlag.ItemIsEditable if index.isValid() else base

    def setData(self, index: QModelIndex, valor, role: int = R.EditRole) -> bool:
        if role != R.EditRole or not index.isValid():
            return False
        e, col = self._dados[index.row()], index.column()
        if col == 0:
            e.tag = str(valor).strip().upper()
        elif col == 1:
            if float(valor) <= 0:
                return False  # recusa valores inválidos
            e.pressao_bar = float(valor)
        else:
            e.aprovado = bool(valor)
        # 'aprovado' muda a cor da linha
        if col == 2:
            fim = self.index(index.row(), self.columnCount() - 1)
            self.dataChanged.emit(self.index(index.row(), 0), fim)
        # demais: só a célula editada
        else:
            self.dataChanged.emit(index, index, [R.DisplayRole, R.EditRole])
        return True

    # ------------------------------------------------------- inserção/remoção --
    def insertRows(self, linha: int, n: int, parent=QModelIndex()) -> bool:
        self.beginInsertRows(parent, linha, linha + n - 1)
        for _ in range(n):
            self._dados.insert(linha, Ensaio("NOVO", 1.0, False))
        self.endInsertRows()
        return True

    def removeRows(self, linha: int, n: int, parent=QModelIndex()) -> bool:
        self.beginRemoveRows(parent, linha, linha + n - 1)
        del self._dados[linha : linha + n]
        self.endRemoveRows()
        return True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    modelo = ModeloEnsaios(
        [Ensaio("BOP-01", 345.0, True), Ensaio("BOP-02", 310.5, False)]
    )
    testador = QAbstractItemModelTester(
        modelo, QAbstractItemModelTester.FailureReportingMode.Fatal
    )
    vista = QTableView()
    vista.setModel(modelo)
    vista.show()

    modelo.dataChanged.connect(
        lambda a, b: print(f"dataChanged linhas {a.row()}..{b.row()}")
    )
    print("célula (1,1) exibida:", modelo.index(1, 1).data())
    print("edição -10 aceita?", modelo.setData(modelo.index(1, 1), -10))
    print("edição 320 aceita?", modelo.setData(modelo.index(1, 1), 320))
    modelo.insertRows(2, 1)
    modelo.setData(modelo.index(2, 0), " bop-03 ")
    print("linhas:", [modelo.index(r, 0).data() for r in range(modelo.rowCount())])
    modelo.removeRows(0, 1)
    print(
        "após remover a 1ª:",
        [modelo.index(r, 0).data() for r in range(modelo.rowCount())],
    )
    sys.exit(app.exec())
