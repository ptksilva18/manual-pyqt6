"""SQL models: QSqlQueryModel, QSqlTableModel (editing) and QSqlRelationalTableModel."""

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
    db = QSqlDatabase.addDatabase("QSQLITE")  # default connection (no name)
    db.setDatabaseName(":memory:")
    db.open()
    q = QSqlQuery()
    q.exec("CREATE TABLE kind (id INTEGER PRIMARY KEY, name TEXT)")
    q.exec("INSERT INTO kind VALUES (1, 'Hydrostatic'), (2, 'Functional')")
    q.exec(
        "CREATE TABLE test "
        "(id INTEGER PRIMARY KEY, tag TEXT, pressure REAL, kind_id INT)"
    )
    q.exec("INSERT INTO test VALUES (1,'BOP-01',345,1), (2,'BOP-02',310.5,2)")

    query = QSqlQueryModel()  # read-only
    query.setQuery("SELECT tag, pressure FROM test ORDER BY pressure DESC")
    print(
        "QSqlQueryModel:",
        [query.index(r, 0).data() for r in range(query.rowCount())],
    )

    table = QSqlTableModel()
    table.setTable("test")
    table.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
    table.select()
    table.setData(table.index(1, 2), 315.0)  # edits in memory
    print("pending changes?", table.isDirty())
    # writes to the database (transaction)
    print("submitAll:", table.submitAll())
    q.exec("SELECT pressure FROM test WHERE id = 2")
    q.next()
    print("value in the database:", q.value(0))

    rel = QSqlRelationalTableModel()
    rel.setTable("test")
    rel.setRelation(3, QSqlRelation("kind", "id", "name"))  # kind_id -> kind.name
    rel.setHeaderData(3, Qt.Orientation.Horizontal, "Type")
    rel.select()
    view = QTableView()
    view.setModel(rel)
    # editor = combo with the names
    view.setItemDelegate(QSqlRelationalDelegate(view))
    print(
        "relational:",
        [
            (rel.index(r, 1).data(), rel.index(r, 3).data())
            for r in range(rel.rowCount())
        ],
    )
