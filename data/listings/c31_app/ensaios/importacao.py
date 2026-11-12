"""Importação de leituras de arquivos CSV exportados por registradores de pressão."""

import csv
from pathlib import Path

from .dominio import ErroDados, Leitura


def numero(texto: str) -> float:
    return float(texto.strip().replace(",", "."))  # aceita vírgula decimal


def ler_csv(caminho: str | Path) -> list[Leitura]:
    """Colunas: tempo_min; pressao_bar; temperatura_c (separador ';' ou ',')."""
    texto = Path(caminho).read_text(encoding="utf-8-sig")
    dialeto = csv.Sniffer().sniff(texto.splitlines()[0], delimiters=";,")
    leituras = []
    for n, linha in enumerate(csv.reader(texto.splitlines(), dialeto), start=1):
        if n == 1 or not any(c.strip() for c in linha):  # cabeçalho ou linha vazia
            continue
        try:
            t, p, temp = (numero(c) for c in linha[:3])
        except (ValueError, TypeError) as exc:
            raise ErroDados(f"linha {n} inválida: {linha!r}") from exc
        leituras.append(Leitura(t, p, temp))
    return leituras
