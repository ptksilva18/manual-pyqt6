"""Modelo hierárquico com QAbstractItemModel: index(), parent() e internalPointer."""

import sys
from dataclasses import dataclass, field

from PyQt6.QtCore import QAbstractItemModel, QModelIndex, Qt
from PyQt6.QtTest import QAbstractItemModelTester
from PyQt6.QtWidgets import QApplication, QTreeView


@dataclass(eq=False)
class No:
    nome: str
    tipo: str
    pai: "No | None" = None
    filhos: list["No"] = field(default_factory=list)

    def adicionar(self, filho: "No") -> "No":
        filho.pai = self
        self.filhos.append(filho)
        return filho

    def linha(self) -> int:
        return self.pai.filhos.index(self) if self.pai else 0


class ModeloEquipamentos(QAbstractItemModel):
    def __init__(self, raiz: No, parent=None) -> None:
        super().__init__(parent)
        self._raiz = raiz  # nó invisível

    def _no(self, index: QModelIndex) -> No:
        return index.internalPointer() if index.isValid() else self._raiz

    def index(self, linha: int, coluna: int, parent=QModelIndex()) -> QModelIndex:
        if not self.hasIndex(linha, coluna, parent):
            return QModelIndex()
        return self.createIndex(linha, coluna, self._no(parent).filhos[linha])

    def parent(self, index: QModelIndex) -> QModelIndex:
        if not index.isValid():
            return QModelIndex()
        pai = self._no(index).pai
        if pai is None or pai is self._raiz:
            return QModelIndex()
        return self.createIndex(pai.linha(), 0, pai)

    def rowCount(self, parent=QModelIndex()) -> int:
        if parent.isValid() and parent.column() != 0:
            return 0
        return len(self._no(parent).filhos)

    def columnCount(self, parent=QModelIndex()) -> int:
        return 2

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if index.isValid() and role == Qt.ItemDataRole.DisplayRole:
            no = self._no(index)
            return no.nome if index.column() == 0 else no.tipo
        return None

    def headerData(
        self, s: int, o: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole
    ):
        if o == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return ("Equipamento", "Tipo")[s]
        return None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    raiz = No("raiz", "")
    sonda = raiz.adicionar(No("Sonda", "Unidade"))
    bop = sonda.adicionar(No('BOP 18¾"', "Pressão"))
    for g in ("Gaveta cega", "Gaveta de tubo", "Anular"):
        bop.adicionar(No(g, "Elemento"))
    sonda.adicionar(No("Riser", "Estrutura"))
    modelo = ModeloEquipamentos(raiz)
    testador = QAbstractItemModelTester(
        modelo, QAbstractItemModelTester.FailureReportingMode.Fatal
    )
    vista = QTreeView()
    vista.setModel(modelo)
    vista.expandAll()
    i_bop = modelo.index(0, 0, modelo.index(0, 0))
    print("índice do BOP:", i_bop.data(), "| pai:", i_bop.parent().data())
    print(
        "filhos do BOP:",
        [modelo.index(r, 0, i_bop).data() for r in range(modelo.rowCount(i_bop))],
    )
    print("modelo aprovado pelo QAbstractItemModelTester")
