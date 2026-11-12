"""Convenience widgets: QListWidget, QTreeWidget and QTableWidget."""

import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QListWidget,
    QListWidgetItem,
    QTableWidget,
    QTableWidgetItem,
    QTreeWidget,
    QTreeWidgetItem,
)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    tags = QListWidget()
    for tag in ("PT-101", "PT-102", "TT-201"):
        item = QListWidgetItem(tag)
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        item.setCheckState(
            Qt.CheckState.Checked if tag.startswith("PT") else Qt.CheckState.Unchecked
        )
        tags.addItem(item)
    checked = [
        tags.item(i).text()
        for i in range(tags.count())
        if tags.item(i).checkState() == Qt.CheckState.Checked
    ]
    print("checked in the list:", checked)

    tree = QTreeWidget()
    tree.setHeaderLabels(["Equipment", "Pressure class"])
    rig = QTreeWidgetItem(tree, ["Rig", ""])
    bop = QTreeWidgetItem(rig, ["BOP", "15 ksi"])
    QTreeWidgetItem(bop, ["Blind ram", "15 ksi"])
    QTreeWidgetItem(rig, ["Riser", "—"])
    tree.expandAll()
    print("children of the rig:", [rig.child(i).text(0) for i in range(rig.childCount())])

    table = QTableWidget(2, 3)
    table.setHorizontalHeaderLabels(["Tag", "Pressure (bar)", "Status"])
    for r, row in enumerate([("BOP-01", 345.0, "OK"), ("BOP-02", 310.5, "Failed")]):
        for c, value in enumerate(row):
            cell = QTableWidgetItem()
            # stores the type (float), not text
            cell.setData(Qt.ItemDataRole.DisplayRole, value)
            table.setItem(r, c, cell)
    table.sortItems(1, Qt.SortOrder.AscendingOrder)  # numeric sorting
    print("sorted by pressure:", [table.item(r, 0).text() for r in range(2)])
