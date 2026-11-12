# runner: ticks=40 env=ENSAIOS_LIMITES__QUEDA_ADMISSIVEL_PCT:0.3
"""Injeção de dependências: configuração tipada, raiz de composição e serviços
substituíveis."""

import os
import sqlite3
import sys
import tempfile
import tomllib
from dataclasses import dataclass
from typing import Protocol

AQUI = os.path.dirname(os.path.abspath(__file__))


@dataclass(frozen=True)
class Config:
    nome: str
    unidade_pressao: str
    backend: str
    arquivo: str
    queda_admissivel_pct: float

    @classmethod
    def carregar(cls, caminho: str, ambiente: dict[str, str]) -> "Config":
        with open(caminho, "rb") as f:
            dados = tomllib.load(f)
        for chave, valor in ambiente.items():  # ENSAIOS_SECAO__CAMPO=valor
            if chave.startswith("ENSAIOS_") and "__" in chave:
                secao, campo = chave[len("ENSAIOS_") :].lower().split("__", 1)
                tipo = type(dados[secao][campo])  # mantém o tipo do arquivo
                dados[secao][campo] = tipo(valor)
        return cls(
            dados["aplicacao"]["nome"],
            dados["aplicacao"]["unidade_pressao"],
            dados["persistencia"]["backend"],
            dados["persistencia"]["arquivo"],
            dados["limites"]["queda_admissivel_pct"],
        )


class RepositorioEnsaios(Protocol):
    def salvar(self, codigo: str, queda_pct: float) -> None: ...
    def listar(self) -> list[tuple[str, float]]: ...


class RepositorioMemoria:
    def __init__(self) -> None:
        self._dados: list[tuple[str, float]] = []

    def salvar(self, codigo: str, queda_pct: float) -> None:
        self._dados.append((codigo, queda_pct))

    def listar(self) -> list[tuple[str, float]]:
        return list(self._dados)


class RepositorioSQLite:
    def __init__(self, caminho: str) -> None:
        self._con = sqlite3.connect(caminho)
        self._con.execute("CREATE TABLE IF NOT EXISTS ensaio (codigo TEXT, queda REAL)")

    def salvar(self, codigo: str, queda_pct: float) -> None:
        with self._con:  # transação
            self._con.execute("INSERT INTO ensaio VALUES (?, ?)", (codigo, queda_pct))

    def listar(self) -> list[tuple[str, float]]:
        return self._con.execute("SELECT codigo, queda FROM ensaio").fetchall()


class ServicoEnsaios:
    """Regra de negócio: recebe dependências prontas; não as cria nem as procura."""

    def __init__(self, repo: RepositorioEnsaios, limite_pct: float) -> None:
        self.repo, self.limite = repo, limite_pct

    def registrar(self, codigo: str, p0: float, p1: float) -> bool:
        queda = 100.0 * (p0 - p1) / p0
        self.repo.salvar(codigo, queda)
        return queda <= self.limite


def compor(config: Config, pasta_dados: str) -> ServicoEnsaios:
    """Raiz de composição: o único lugar que conhece as implementações concretas."""
    if config.backend == "sqlite":
        repo: RepositorioEnsaios = RepositorioSQLite(
            os.path.join(pasta_dados, config.arquivo)
        )
    elif config.backend == "memoria":
        repo = RepositorioMemoria()
    else:
        raise ValueError(f"backend desconhecido: {config.backend!r}")
    return ServicoEnsaios(repo, config.queda_admissivel_pct)


def main() -> int:
    config = Config.carregar(os.path.join(AQUI, "c27_config.toml"), dict(os.environ))
    print("Config:", config)
    pasta = tempfile.mkdtemp()
    for backend in ("memoria", "sqlite"):
        cfg = Config(**{**config.__dict__, "backend": backend})
        servico = compor(cfg, pasta)
        r1 = servico.registrar("TH-01", 345.0, 344.0)
        r2 = servico.registrar("TH-02", 345.0, 343.5)
        print(
            f"[{backend:<7}] {type(servico.repo).__name__}: aprovados = {[r1, r2]}; "
            f"registros = {[(c, round(q, 3)) for c, q in servico.repo.listar()]}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
