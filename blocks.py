# -*- coding: utf-8 -*-
"""Construtores de blocos do documento (compartilhados por outline.py e partN.py)."""
import os

from i18n import DATA_DIR, S

_D = DATA_DIR   # data/ (pt) ou en/data/ (en)
ST_BAS, ST_INT, ST_AVA, ST_FIN = 2, 3, 4, 5
STEP_NAME = {1: "Step 1 — Estrutura", 2: "Step 2 — Básico", 3: "Step 3 — Intermediário",
             4: "Step 4 — Avançado", 5: "Step 5 — Consolidação"}
TBD = "[a preencher]"


def part(roman, title, sub, step, chapters_hint):
    return dict(k="part", roman=roman, title=title, sub=sub, step=step, hint=chapters_hint)


def ch(title, step, obj):
    return [dict(k="h", lvl=1, t=title, step=step), dict(k="obj", items=obj)]


def h2(t):
    return dict(k="h", lvl=2, t=t)


def h3(t):
    return dict(k="h", lvl=3, t=t)


def h4(t):
    return dict(k="h", lvl=4, t=t)


def p(t):
    return dict(k="p", t=t)


def bl(*items):
    return dict(k="bl", items=list(items))


def fig(title, desc):
    return dict(k="fig", t=title, desc=desc)


def tab(title, header, rows, widths, font=None):
    return dict(k="tab", t=title, header=header, rows=rows, widths=widths, font=font)


def code(title, lines, tested=False):
    return dict(k="code", t=title, lines=lines, tested=tested)


def note(kind, t):
    return dict(k="note", kind=kind, t=t)


def flat(*items):
    out = []
    for it in items:
        if isinstance(it, list):
            out.extend(it)
        else:
            out.append(it)
    return out



def nl(*items):
    """Lista numerada (reinicia em 1)."""
    return dict(k="nl", items=list(items))


def lst(name, title, lang="python", allow_long=False, nota=None):
    """Listagem lida de data/listings/<name> (codigo testado pelo runner).
    allow_long=True apenas para codigo GERADO por ferramenta (nao reformatavel).
    nota: linha de verificacao alternativa (ex.: arquivo QML carregado por outra listagem,
    ou codigo que exige plataforma indisponivel no ambiente de teste)."""
    path = os.path.join(_D, "listings", name)
    lines = open(path, encoding="utf-8").read().rstrip("\n").split("\n")
    return dict(k="code", t=title, lines=lines, tested=(lang == "python" and nota is None),
                lang=lang, src=name, allow_long=allow_long, nota=nota)


def snip(lines, lang="python"):
    """Trecho curto sem legenda (fragmento ilustrativo)."""
    if isinstance(lines, str):
        lines = lines.strip("\n").split("\n")
    return dict(k="snip", lines=lines, lang=lang)


def out(name, title=None):
    """Saida real capturada pelo runner em data/outputs/<name>.txt."""
    path = os.path.join(_D, "outputs", name + ".txt")
    lines = open(path, encoding="utf-8").read().rstrip("\n").split("\n")
    return dict(k="out", t=title or S["output"], lines=lines)


def img(title, path, width_cm=15.0):
    return dict(k="fig", t=title, img=os.path.join(_D, "figs", path), width=width_cm, desc=title)
