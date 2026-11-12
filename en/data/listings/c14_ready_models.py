"""Ready-made models: QStringListModel and QStandardItemModel."""

import sys

from PyQt6.QtCore import QStringListModel
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import QApplication, QListView, QTreeView

if __name__ == "__main__":
    app = QApplication(sys.argv)

    names = QStringListModel(["Hydrostatic", "Functional"])
    QListView().setModel(names)
    names.insertRows(names.rowCount(), 1)
    names.setData(names.index(2), "Leak test")
    print("QStringListModel:", names.stringList())

    tree = QStandardItemModel()
    tree.setHorizontalHeaderLabels(["System", "Items"])
    control = [QStandardItem("Subsea control"), QStandardItem("2")]
    control[0].appendRow([QStandardItem("SCM"), QStandardItem("1")])
    control[0].appendRow([QStandardItem("HPU"), QStandardItem("1")])
    tree.appendRow(control)
    QTreeView().setModel(tree)
    root = tree.index(0, 0)
    print(
        "QStandardItemModel: children of",
        root.data(),
        "=",
        [tree.index(i, 0, root).data() for i in range(tree.rowCount(root))],
    )
