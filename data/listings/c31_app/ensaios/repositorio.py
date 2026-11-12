"""Persistência em SQLite (biblioteca padrão): ensaios, critérios e leituras."""

import json
import sqlite3
from dataclasses import asdict
from pathlib import Path

from .dominio import Criterio, Leitura

ESQUEMA = """
CREATE TABLE IF NOT EXISTS ensaio (
    id INTEGER PRIMARY KEY, codigo TEXT UNIQUE NOT NULL, descricao TEXT NOT NULL,
    criterio TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS leitura (
    ensaio_id INTEGER NOT NULL REFERENCES ensaio(id) ON DELETE CASCADE,
    t_min REAL NOT NULL, p_bar REAL NOT NULL, temp_c REAL NOT NULL);
"""


class Repositorio:
    def __init__(self, caminho: str | Path) -> None:
        self.con = sqlite3.connect(str(caminho))
        self.con.execute("PRAGMA foreign_keys = ON")
        self.con.executescript(ESQUEMA)

    def criar_ensaio(self, codigo: str, descricao: str, criterio: Criterio) -> int:
        with self.con:  # transação: grava tudo ou nada
            cur = self.con.execute(
                "INSERT INTO ensaio (codigo, descricao, criterio) VALUES (?, ?, ?)",
                (codigo, descricao, json.dumps(asdict(criterio))),
            )
        return cur.lastrowid

    def listar(self) -> list[tuple[int, str, str]]:
        return self.con.execute(
            "SELECT id, codigo, descricao FROM ensaio ORDER BY codigo"
        ).fetchall()

    def criterio(self, ensaio_id: int) -> Criterio:
        (txt,) = self.con.execute(
            "SELECT criterio FROM ensaio WHERE id = ?", (ensaio_id,)
        ).fetchone()
        return Criterio(**json.loads(txt))

    def substituir_leituras(self, ensaio_id: int, leituras: list[Leitura]) -> None:
        with self.con:
            self.con.execute("DELETE FROM leitura WHERE ensaio_id = ?", (ensaio_id,))
            self.con.executemany(
                "INSERT INTO leitura VALUES (?, ?, ?, ?)",
                [(ensaio_id, lt.t_min, lt.p_bar, lt.temp_c) for lt in leituras],
            )

    def leituras(self, ensaio_id: int) -> list[Leitura]:
        linhas = self.con.execute(
            "SELECT t_min, p_bar, temp_c FROM leitura WHERE ensaio_id = ? ORDER BY t_min",
            (ensaio_id,),
        ).fetchall()
        return [Leitura(*ln) for ln in linhas]

    def fechar(self) -> None:
        self.con.close()
