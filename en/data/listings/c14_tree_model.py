"""Hierarchical model with QAbstractItemModel: index(), parent() and internalPointer."""

import sys
from dataclasses import dataclass, field

from PyQt6.QtCore import QAbstractItemModel, QModelIndex, Qt
from PyQt6.QtTest import QAbstractItemModelTester
from PyQt6.QtWidgets import QApplication, QTreeView


@dataclass(eq=False)
class Node:
    name: str
    kind: str
    parent: "Node | None" = None
    children: list["Node"] = field(default_factory=list)

    def add(self, child: "Node") -> "Node":
        child.parent = self
        self.children.append(child)
        return child

    def row(self) -> int:
        return self.parent.children.index(self) if self.parent else 0


class EquipmentModel(QAbstractItemModel):
    def __init__(self, root: Node, parent=None) -> None:
        super().__init__(parent)
        self._root = root  # invisible node

    def _node(self, index: QModelIndex) -> Node:
        return index.internalPointer() if index.isValid() else self._root

    def index(self, row: int, column: int, parent=QModelIndex()) -> QModelIndex:
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        return self.createIndex(row, column, self._node(parent).children[row])

    def parent(self, index: QModelIndex) -> QModelIndex:
        if not index.isValid():
            return QModelIndex()
        up = self._node(index).parent
        if up is None or up is self._root:
            return QModelIndex()
        return self.createIndex(up.row(), 0, up)

    def rowCount(self, parent=QModelIndex()) -> int:
        if parent.isValid() and parent.column() != 0:
            return 0
        return len(self._node(parent).children)

    def columnCount(self, parent=QModelIndex()) -> int:
        return 2

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if index.isValid() and role == Qt.ItemDataRole.DisplayRole:
            node = self._node(index)
            return node.name if index.column() == 0 else node.kind
        return None

    def headerData(
        self, s: int, o: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole
    ):
        if o == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return ("Equipment", "Type")[s]
        return None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    root = Node("root", "")
    rig = root.add(Node("Rig", "Unit"))
    bop = rig.add(Node('BOP 18¾"', "Pressure"))
    for r in ("Blind ram", "Pipe ram", "Annular"):
        bop.add(Node(r, "Element"))
    rig.add(Node("Riser", "Structure"))
    model = EquipmentModel(root)
    tester = QAbstractItemModelTester(
        model, QAbstractItemModelTester.FailureReportingMode.Fatal
    )
    view = QTreeView()
    view.setModel(model)
    view.expandAll()
    i_bop = model.index(0, 0, model.index(0, 0))
    print("BOP index:", i_bop.data(), "| parent:", i_bop.parent().data())
    print(
        "children of the BOP:",
        [model.index(r, 0, i_bop).data() for r in range(model.rowCount(i_bop))],
    )
    print("model approved by QAbstractItemModelTester")
