# runner: ticks=40 env=TESTS_LIMITS__ALLOWABLE_DROP_PCT:0.3
"""Dependency injection: typed configuration, composition root and replaceable
services."""

import os
import sqlite3
import sys
import tempfile
import tomllib
from dataclasses import dataclass
from typing import Protocol

HERE = os.path.dirname(os.path.abspath(__file__))


@dataclass(frozen=True)
class Config:
    name: str
    pressure_unit: str
    backend: str
    file: str
    allowable_drop_pct: float

    @classmethod
    def load(cls, path: str, environment: dict[str, str]) -> "Config":
        with open(path, "rb") as f:
            data = tomllib.load(f)
        for key, value in environment.items():  # TESTS_SECTION__FIELD=value
            if key.startswith("TESTS_") and "__" in key:
                section, field = key[len("TESTS_") :].lower().split("__", 1)
                kind = type(data[section][field])  # keeps the type from the file
                data[section][field] = kind(value)
        return cls(
            data["application"]["name"],
            data["application"]["pressure_unit"],
            data["persistence"]["backend"],
            data["persistence"]["file"],
            data["limits"]["allowable_drop_pct"],
        )


class TestRepository(Protocol):
    def save(self, code: str, drop_pct: float) -> None: ...
    def list_all(self) -> list[tuple[str, float]]: ...


class MemoryRepository:
    def __init__(self) -> None:
        self._data: list[tuple[str, float]] = []

    def save(self, code: str, drop_pct: float) -> None:
        self._data.append((code, drop_pct))

    def list_all(self) -> list[tuple[str, float]]:
        return list(self._data)


class SQLiteRepository:
    def __init__(self, path: str) -> None:
        self._con = sqlite3.connect(path)
        self._con.execute("CREATE TABLE IF NOT EXISTS test (code TEXT, drop_pct REAL)")

    def save(self, code: str, drop_pct: float) -> None:
        with self._con:  # transaction
            self._con.execute("INSERT INTO test VALUES (?, ?)", (code, drop_pct))

    def list_all(self) -> list[tuple[str, float]]:
        return self._con.execute("SELECT code, drop_pct FROM test").fetchall()


class TestService:
    """Business rule: receives ready-made dependencies; never creates or looks them up."""

    def __init__(self, repo: TestRepository, limit_pct: float) -> None:
        self.repo, self.limit = repo, limit_pct

    def record(self, code: str, p0: float, p1: float) -> bool:
        drop = 100.0 * (p0 - p1) / p0
        self.repo.save(code, drop)
        return drop <= self.limit


def compose(config: Config, data_folder: str) -> TestService:
    """Composition root: the only place that knows the concrete implementations."""
    if config.backend == "sqlite":
        repo: TestRepository = SQLiteRepository(
            os.path.join(data_folder, config.file)
        )
    elif config.backend == "memory":
        repo = MemoryRepository()
    else:
        raise ValueError(f"unknown backend: {config.backend!r}")
    return TestService(repo, config.allowable_drop_pct)


def main() -> int:
    config = Config.load(os.path.join(HERE, "c27_config.toml"), dict(os.environ))
    print("Config:", config)
    folder = tempfile.mkdtemp()
    for backend in ("memory", "sqlite"):
        cfg = Config(**{**config.__dict__, "backend": backend})
        service = compose(cfg, folder)
        r1 = service.record("TH-01", 345.0, 344.0)
        r2 = service.record("TH-02", 345.0, 343.5)
        print(
            f"[{backend:<6}] {type(service.repo).__name__}: passed = {[r1, r2]}; "
            f"records = {[(c, round(q, 3)) for c, q in service.repo.list_all()]}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
