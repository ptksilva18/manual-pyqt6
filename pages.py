# -*- coding: utf-8 -*-
"""
Localiza no PDF (renderizado pelo LibreOffice) a pagina de cada titulo/legenda
e grava {bookmark: numero_de_pagina_logico} para pre-preencher o sumario.

Uso: python pages.py doc.pdf doc.docx.meta.json paginas.json
"""
import json
import re
import subprocess
import sys


def norm(s):
    s = s.replace(" ", " ").replace("‑", "-")
    return re.sub(r"\s+", " ", s).strip()


def roman(n):
    vals = [(1000, "m"), (900, "cm"), (500, "d"), (400, "cd"), (100, "c"), (90, "xc"), (50, "l"), (40, "xl"),
            (10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")]
    out = ""
    for v, s in vals:
        while n >= v:
            out += s
            n -= v
    return out


def page_texts(pdf):
    n = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout).group(1))
    txt = subprocess.run(["pdftotext", "-layout", "-enc", "UTF-8", pdf, "-"], capture_output=True, text=True).stdout
    pages = txt.split("\f")[:n]
    return [norm(p) for p in pages]


def main(pdf, meta_path, out_path):
    meta = json.load(open(meta_path, encoding="utf-8"))
    pages = page_texts(pdf)
    # pagina fisica (1-based) do Prefacio: primeira que o contem e nao e pagina de sumario
    first_title = meta["order"][0][1]
    toc_title = meta.get("toc_title", "SUMÁRIO")
    body_start = meta.get("body_start", "PARTE I — FUNDAMENTOS")
    pref = next(i for i, t in enumerate(pages) if first_title in t and toc_title not in t and ". ." not in t
                and not re.search(re.escape(first_title) + r"\s*\.{3,}", t))
    # inicio do corpo: primeira pagina apos o prefacio com o titulo da Parte I
    body = next(i for i in range(pref + 1, len(pages)) if body_start in pages[i])
    result, missing = {}, []
    cur = pref
    for bm, text in meta["order"]:
        key = norm(text)[:48]
        found = None
        for i in range(cur, len(pages)):
            if key in pages[i]:
                found = i
                break
        if found is None:
            missing.append(text)
            continue
        cur = found
        if found < body:
            result[bm] = roman(found)          # capa = pag. fisica 1 sem numero; i = fisica 2
        else:
            result[bm] = str(found - body + 1)
    json.dump(result, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(f"Prefácio/Preface na pág. física {pref + 1}; corpo inicia na pág. física {body + 1}; "
          f"{len(result)} localizados; {len(missing)} não localizados")
    for m in missing[:20]:
        print("  NÃO LOCALIZADO:", m)
    return 0 if not missing else 1


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:4]))
