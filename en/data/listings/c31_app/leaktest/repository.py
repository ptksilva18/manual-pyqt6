"""Persistence in SQLite (standard library): tests, criteria and readings."""

import json
import sqlite3
from dataclasses import asdict
from pathlib import Path

from .domain import Criterion, Reading

SCHEMA = """
CREATE TABLE IF NOT EXISTS test (
    id INTEGER PRIMARY KEY, code TEXT UNIQUE NOT NULL, description TEXT NOT NULL,
    criterion TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS reading (
    test_id INTEGER NOT NULL REFERENCES test(id) ON DELETE CASCADE,
    t_min REAL NOT NULL, p_bar REAL NOT NULL, temp_c REAL NOT NULL);
"""


class Repository:
    def __init__(self, path: str | Path) -> None:
        self.con = sqlite3.connect(str(path))
        self.con.execute("PRAGMA foreign_keys = ON")
        self.con.executescript(SCHEMA)

    def create_test(self, code: str, description: str, criterion: Criterion) -> int:
        with self.con:  # transaction: writes everything or nothing
            cur = self.con.execute(
                "INSERT INTO test (code, description, criterion) VALUES (?, ?, ?)",
                (code, description, json.dumps(asdict(criterion))),
            )
        return cur.lastrowid

    def list_tests(self) -> list[tuple[int, str, str]]:
        return self.con.execute(
            "SELECT id, code, description FROM test ORDER BY code"
        ).fetchall()

    def criterion(self, test_id: int) -> Criterion:
        (txt,) = self.con.execute(
            "SELECT criterion FROM test WHERE id = ?", (test_id,)
        ).fetchone()
        return Criterion(**json.loads(txt))

    def replace_readings(self, test_id: int, readings: list[Reading]) -> None:
        with self.con:
            self.con.execute("DELETE FROM reading WHERE test_id = ?", (test_id,))
            self.con.executemany(
                "INSERT INTO reading VALUES (?, ?, ?, ?)",
                [(test_id, rd.t_min, rd.p_bar, rd.temp_c) for rd in readings],
            )

    def readings(self, test_id: int) -> list[Reading]:
        rows = self.con.execute(
            "SELECT t_min, p_bar, temp_c FROM reading WHERE test_id = ? ORDER BY t_min",
            (test_id,),
        ).fetchall()
        return [Reading(*row) for row in rows]

    def close(self) -> None:
        self.con.close()
