"""Widgets de conveniência: QListWidget, QTreeWidget e QTableWidget."""

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

    lista = QListWidget()
    for tag in ("PT-101", "PT-102", "TT-201"):
        item = QListWidgetItem(tag)
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        item.setCheckState(
            Qt.CheckState.Checked if tag.startswith("PT") else Qt.CheckState.Unchecked
        )
        lista.addItem(item)
    marcados = [
        lista.item(i).text()
        for i in range(lista.count())
        if lista.item(i).checkState() == Qt.CheckState.Checked
    ]
    print("lista marcada:", marcados)

    arvore = QTreeWidget()
    arvore.setHeaderLabels(["Equipamento", "Classe de pressão"])
    sonda = QTreeWidgetItem(arvore, ["Sonda", ""])
    bop = QTreeWidgetItem(sonda, ["BOP", "15 ksi"])
    QTreeWidgetItem(bop, ["Gaveta cega", "15 ksi"])
    QTreeWidgetItem(sonda, ["Riser", "—"])
    arvore.expandAll()
    print(
        "filhos da sonda:", [sonda.child(i).text(0) for i in range(sonda.childCount())]
    )

    tabela = QTableWidget(2, 3)
    tabela.setHorizontalHeaderLabels(["Tag", "Pressão (bar)", "Status"])
    for r, linha in enumerate([("BOP-01", 345.0, "OK"), ("BOP-02", 310.5, "Falha")]):
        for c, valor in enumerate(linha):
            cel = QTableWidgetItem()
            # guarda o tipo (float), não texto
            cel.setData(Qt.ItemDataRole.DisplayRole, valor)
            tabela.setItem(r, c, cel)
    tabela.sortItems(1, Qt.SortOrder.AscendingOrder)  # ordenação numérica
    print("ordenado por pressão:", [tabela.item(r, 0).text() for r in range(2)])
