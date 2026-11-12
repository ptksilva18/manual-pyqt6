"""QtSql com SQLite: conexão, DDL, consultas preparadas, transações e erros."""

import sys

from PyQt6.QtSql import QSqlDatabase, QSqlError, QSqlQuery
from PyQt6.QtWidgets import QApplication


def executar(q: QSqlQuery, sql: str | None = None) -> None:
    ok = q.exec(sql) if sql is not None else q.exec()
    # nunca ignore o retorno de exec()
    if not ok:
        raise RuntimeError(f"SQL falhou: {q.lastError().text()}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    print("drivers disponíveis:", QSqlDatabase.drivers())
    db = QSqlDatabase.addDatabase("QSQLITE", "ensaios")  # nome da conexão
    # arquivo .sqlite em produção
    db.setDatabaseName(":memory:")
    if not db.open():
        sys.exit(db.lastError().text())

    q = QSqlQuery(db)
    executar(
        q,
        """CREATE TABLE ensaio (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       tag TEXT NOT NULL UNIQUE,
                       pressao_bar REAL NOT NULL CHECK (pressao_bar > 0),
                       aprovado INTEGER NOT NULL)""",
    )

    dados = [("BOP-01", 345.0, 1), ("BOP-02", 310.5, 0), ("XT-07", 690.0, 1)]
    db.transaction()  # tudo ou nada
    q.prepare("INSERT INTO ensaio (tag, pressao_bar, aprovado) VALUES (:tag, :p, :a)")
    for tag, p, a in dados:
        # parâmetros: sem injeção de SQL
        q.bindValue(":tag", tag)
        q.bindValue(":p", p)
        q.bindValue(":a", a)
        executar(q)
    db.commit()
    print("último id inserido:", q.lastInsertId())

    q.prepare("SELECT tag, pressao_bar FROM ensaio WHERE pressao_bar >= ? ORDER BY tag")
    q.addBindValue(340.0)  # parâmetro posicional
    executar(q)
    while q.next():
        print(f"  {q.value(0):8} {q.value('pressao_bar'):7.1f} bar")

    db.transaction()
    q.prepare(
        "INSERT INTO ensaio (tag, pressao_bar, aprovado) VALUES ('BOP-01', 300, 1)"
    )
    if not q.exec():  # viola UNIQUE(tag)
        erro = q.lastError()
        print("erro:", erro.type().name, "|", erro.databaseText())
        db.rollback()
    q.exec("SELECT COUNT(*) FROM ensaio")
    q.next()
    print("registros após rollback:", q.value(0))
    q.finish()
    db.close()
    del q, db
    # só depois de liberar objetos
    QSqlDatabase.removeDatabase("ensaios")
