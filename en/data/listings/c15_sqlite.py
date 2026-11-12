"""QtSql with SQLite: connection, DDL, prepared queries, transactions and errors."""

import sys

from PyQt6.QtSql import QSqlDatabase, QSqlError, QSqlQuery
from PyQt6.QtWidgets import QApplication


def execute(q: QSqlQuery, sql: str | None = None) -> None:
    ok = q.exec(sql) if sql is not None else q.exec()
    # never ignore the return value of exec()
    if not ok:
        raise RuntimeError(f"SQL failed: {q.lastError().text()}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    print("available drivers:", QSqlDatabase.drivers())
    db = QSqlDatabase.addDatabase("QSQLITE", "tests")  # connection name
    # a .sqlite file in production
    db.setDatabaseName(":memory:")
    if not db.open():
        sys.exit(db.lastError().text())

    q = QSqlQuery(db)
    execute(
        q,
        """CREATE TABLE test (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       tag TEXT NOT NULL UNIQUE,
                       pressure_bar REAL NOT NULL CHECK (pressure_bar > 0),
                       passed INTEGER NOT NULL)""",
    )

    rows = [("BOP-01", 345.0, 1), ("BOP-02", 310.5, 0), ("XT-07", 690.0, 1)]
    db.transaction()  # all or nothing
    q.prepare("INSERT INTO test (tag, pressure_bar, passed) VALUES (:tag, :p, :a)")
    for tag, p, a in rows:
        # parameters: no SQL injection
        q.bindValue(":tag", tag)
        q.bindValue(":p", p)
        q.bindValue(":a", a)
        execute(q)
    db.commit()
    print("last inserted id:", q.lastInsertId())

    q.prepare("SELECT tag, pressure_bar FROM test WHERE pressure_bar >= ? ORDER BY tag")
    q.addBindValue(340.0)  # positional parameter
    execute(q)
    while q.next():
        print(f"  {q.value(0):8} {q.value('pressure_bar'):7.1f} bar")

    db.transaction()
    q.prepare("INSERT INTO test (tag, pressure_bar, passed) VALUES ('BOP-01', 300, 1)")
    if not q.exec():  # violates UNIQUE(tag)
        error = q.lastError()
        print("error:", error.type().name, "|", error.databaseText())
        db.rollback()
    q.exec("SELECT COUNT(*) FROM test")
    q.next()
    print("records after rollback:", q.value(0))
    q.finish()
    db.close()
    del q, db
    # only after releasing the objects
    QSqlDatabase.removeDatabase("tests")
