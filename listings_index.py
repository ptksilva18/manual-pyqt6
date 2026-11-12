# -*- coding: utf-8 -*-
"""Gera o índice das listagens (Markdown) a partir da estrutura do manual.

Uso:  MANUAL_LANG=pt python listings_index.py   ->  data/listings/INDICE.md
      MANUAL_LANG=en python listings_index.py   ->  en/data/listings/INDEX.md

A numeração segue as mesmas regras do build.py (capítulo.n; anexo letra.n). Com --check, compara a
numeração e os títulos com o meta.json de um build (ex.: build/s4b.docx.meta.json) e falha se houver
qualquer diferença.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from i18n import DATA_DIR, LANG  # noqa: E402

if LANG == "en":
    sys.path.insert(0, os.path.join(HERE, "en"))
import outline as O  # noqa: E402

T = {
    "pt": dict(
        out="INDICE.md",
        head=["# Índice das listagens do MAN-PYQT6-001", "",
              "Correspondência entre o número de cada listagem no manual e o arquivo neste diretório.", "",
              "- **✔ executada** — rodada por [`runner.py`](../../runner.py); a saída real fica em "
              "`../outputs/<nome>.txt`.",
              "- **✔ (indireta)** — arquivo carregado ou executado por outra listagem, conforme a nota.",
              "- **⚠** — não executada no ambiente de teste (Linux): exige Windows.",
              "- **apoio** — arquivo de apoio (modelo de configuração, interface `.ui` ou tradução `.ts`) "
              "mostrado no manual; quando outra listagem o usa, o capítulo indica.", "",
              "| Listagem | Título | Arquivo | Verificação |", "|---|---|---|---|"],
        run="✔ executada", ind="✔ (indireta): ", sup="apoio", cap="Listagem"),
    "en": dict(
        out="INDEX.md",
        head=["# Index of the listings of MAN-PYQT6-001 (English edition)", "",
              "Correspondence between the number of each listing in the manual and the file in this folder.",
              "",
              "- **✔ run** — run by [`runner.py`](../../../runner.py) (`MANUAL_LANG=en`); the actual output "
              "is in `../outputs/<name>.txt`.",
              "- **✔ (indirect)** — file loaded or executed by another listing, as stated in the note.",
              "- **⚠** — not run in the test environment (Linux): requires Windows.",
              "- **support** — support file (configuration template, `.ui` interface or `.ts` translation) "
              "shown in the manual; when another listing uses it, the chapter says so.", "",
              "| Listing | Title | File | Verification |", "|---|---|---|---|"],
        run="✔ run", ind="✔ (indirect): ", sup="support", cap="Listing"),
}[LANG]


def first_sentence(text: str) -> str:
    text = text.strip()
    i = text.find(". ")
    text = text[:i] if i >= 0 else text
    return text[:-1] if text.endswith(".") else text


def listings():
    chapter, annex, n = 0, None, 0
    for b in list(O.BODY) + list(O.ANNEXES):
        if b["k"] == "h" and b["lvl"] == 1:
            chapter, annex, n = chapter + 1, None, 0
        elif b["k"] == "ha" and b["lvl"] == 1:
            annex = chr(ord(annex) + 1) if annex else "A"
            n = 0
        elif b["k"] == "code":
            n += 1
            yield f"{annex or chapter}.{n}", b


def verification(b) -> str:
    nota = b.get("nota")
    if b["tested"]:
        return T["run"]
    if nota is None:
        return T["sup"]
    if nota.startswith("✔"):
        return T["ind"] + first_sentence(nota[1:])
    if nota.startswith("⚠"):
        return "⚠ " + first_sentence(nota[1:])
    raise ValueError(f"nota sem marcador: {nota!r}")


def main() -> int:
    rows = list(listings())
    if "--check" in sys.argv:
        meta = json.load(open(sys.argv[sys.argv.index("--check") + 1], encoding="utf-8"))
        caps = dict(meta["caps"])[T["cap"]]
        expected = [re.match(r"\S+ (\S+) — (.*)$", t).groups() for t, _ in caps]
        got = [(num, b["t"]) for num, b in rows]
        if expected != got:
            for e, g in zip(expected, got):
                if e != g:
                    print("DIFERENÇA:", e, g)
            print(f"meta: {len(expected)} | índice: {len(got)}")
            return 1
        print(f"numeração e títulos conferem com o meta.json: {len(got)} listagens")
    lines = list(T["head"])
    for num, b in rows:
        lines.append(f"| {num} | {b['t']} | [`{b['src']}`]({b['src']}) | {verification(b)} |")
    path = os.path.join(DATA_DIR, "listings", T["out"])
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("gravado:", os.path.relpath(path, HERE), f"({len(rows)} listagens)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
