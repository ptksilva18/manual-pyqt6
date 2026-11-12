"""Modelos prontos: QStringListModel e QStandardItemModel."""

import sys

from PyQt6.QtCore import QStringListModel
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import QApplication, QListView, QTreeView

if __name__ == "__main__":
    app = QApplication(sys.argv)

    nomes = QStringListModel(["Hidrostático", "Funcional"])
    QListView().setModel(nomes)
    nomes.insertRows(nomes.rowCount(), 1)
    nomes.setData(nomes.index(2), "Estanqueidade")
    print("QStringListModel:", nomes.stringList())

    arvore = QStandardItemModel()
    arvore.setHorizontalHeaderLabels(["Sistema", "Itens"])
    controle = [QStandardItem("Controle submarino"), QStandardItem("2")]
    controle[0].appendRow([QStandardItem("SCM"), QStandardItem("1")])
    controle[0].appendRow([QStandardItem("HPU"), QStandardItem("1")])
    arvore.appendRow(controle)
    QTreeView().setModel(arvore)
    raiz = arvore.index(0, 0)
    print(
        "QStandardItemModel: filhos de",
        raiz.data(),
        "=",
        [arvore.index(i, 0, raiz).data() for i in range(arvore.rowCount(raiz))],
    )
