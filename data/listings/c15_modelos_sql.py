"""Modelos SQL: QSqlQueryModel, QSqlTableModel (edição) e QSqlRelationalTableModel."""

import sys

from PyQt6.QtCore import Qt
from PyQt6.QtSql import (
    QSqlDatabase,
    QSqlQuery,
    QSqlQueryModel,
    QSqlRelation,
    QSqlRelationalDelegate,
    QSqlRelationalTableModel,
    QSqlTableModel,
)
from PyQt6.QtWidgets import QApplication, QTableView

if __name__ == "__main__":
    app = QApplication(sys.argv)
    db = QSqlDatabase.addDatabase("QSQLITE")  # conexão padrão (sem nome)
    db.setDatabaseName(":memory:")
    db.open()
    q = QSqlQuery()
    q.exec("CREATE TABLE tipo (id INTEGER PRIMARY KEY, nome TEXT)")
    q.exec("INSERT INTO tipo VALUES (1, 'Hidrostático'), (2, 'Funcional')")
    q.exec(
        "CREATE TABLE ensaio "
        "(id INTEGER PRIMARY KEY, tag TEXT, pressao REAL, tipo_id INT)"
    )
    q.exec("INSERT INTO ensaio VALUES (1,'BOP-01',345,1), (2,'BOP-02',310.5,2)")

    consulta = QSqlQueryModel()  # somente leitura
    consulta.setQuery("SELECT tag, pressao FROM ensaio ORDER BY pressao DESC")
    print(
        "QSqlQueryModel:",
        [consulta.index(r, 0).data() for r in range(consulta.rowCount())],
    )

    tabela = QSqlTableModel()
    tabela.setTable("ensaio")
    tabela.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
    tabela.select()
    tabela.setData(tabela.index(1, 2), 315.0)  # edita em memória
    print("alterações pendentes?", tabela.isDirty())
    # grava no banco (transação)
    print("submitAll:", tabela.submitAll())
    q.exec("SELECT pressao FROM ensaio WHERE id = 2")
    q.next()
    print("valor no banco:", q.value(0))

    rel = QSqlRelationalTableModel()
    rel.setTable("ensaio")
    rel.setRelation(3, QSqlRelation("tipo", "id", "nome"))  # tipo_id -> tipo.nome
    rel.setHeaderData(3, Qt.Orientation.Horizontal, "Tipo")
    rel.select()
    vista = QTableView()
    vista.setModel(rel)
    # editor = combo com os nomes
    vista.setItemDelegate(QSqlRelationalDelegate(vista))
    print(
        "relacional:",
        [
            (rel.index(r, 1).data(), rel.index(r, 3).data())
            for r in range(rel.rowCount())
        ],
    )
