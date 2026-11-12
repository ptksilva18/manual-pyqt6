# -*- coding: utf-8 -*-
"""Idioma do documento gerado e textos fixos da interface do documento.

O idioma vem da variavel de ambiente MANUAL_LANG ("pt", padrao, ou "en").
- pt: conteudo em part*.py/front.py (raiz) e dados em data/
- en: conteudo em en/*.py e dados em en/data/
"""
import os

LANG = os.environ.get("MANUAL_LANG", "pt")
if LANG not in ("pt", "en"):
    raise SystemExit(f"MANUAL_LANG invalido: {LANG!r} (use 'pt' ou 'en')")

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = HERE if LANG == "pt" else os.path.join(HERE, "en")
DATA_DIR = os.path.join(CONTENT_DIR, "data")

_S = {
    "pt": {
        "fig": "Figura", "tab": "Tabela", "lst": "Listagem", "FIG": "FIGURA",
        "part": "PARTE", "annex": "ANEXO",
        "toc": "SUMÁRIO", "lof": "LISTA DE FIGURAS", "lot": "LISTA DE TABELAS", "lol": "LISTA DE LISTAGENS",
        "no_entries": "Nenhuma entrada.",
        "objectives": "Objetivos do capítulo", "level": "Nível",
        "levels": {2: "Básico", 3: "Intermediário", 4: "Avançado", 5: "Consolidação"},
        "verified": "✔ Código executado e verificado com PyQt6 6.12.0 / Qt 6.12.0 / Python 3.13.",
        "output": "Saída",
        "cat_caption": "Classes do módulo {m}{note} ({n})", "win_only": " (exclusivo Windows)",
        "cat_functions": "Funções de nível de módulo ({n}): ",
        "revision": "Revisão", "doc_code": "Código do documento", "date": "Data",
        "ref_version": "Versão de referência", "classification": "Classificação",
        "classification_v": "Manual técnico-didático", "author": "Autor",
        "cover_alt_t": "Ilustração da capa",
        "cover_alt_d": "Ilustração genérica de uma janela de aplicação desktop com gráfico, formulário e trecho "
                       "de código PyQt6.",
        "control": "CONTROLE DO DOCUMENTO", "code": "Código", "title": "Título", "subtitle": "Subtítulo",
        "cur_rev": "Revisão atual", "status": "Status", "status_v": "Emitido", "prepared": "Elaborado por",
        "checked": "Verificado por", "approved": "Aprovado por",
        "na": "Não aplicável — publicação independente",
        "history": "HISTÓRICO DE REVISÕES",
        "hist_head": ["Rev.", "Data", "Descrição", "Situação"], "issued": "Emitida",
        "header": "Manual de Python com Interface Gráfica — PyQt6", "page": "Página ",
        "doc_lang": "pt-BR",
        "st_titlelist": "Título de Lista", "st_sublist": "Subtítulo de Lista", "st_code": "Código",
        "st_out": "Saída de Terminal", "st_marker": "Marcador de Conteúdo", "st_tabtext": "Tabela Texto",
        "st_tabhead": "Tabela Cabeçalho", "st_after": "Após Tabela", "st_inline": "Código em Linha",
        "st_fig": "Figura",
        "placeholder": "[Conteúdo a desenvolver]",
    },
    "en": {
        "fig": "Figure", "tab": "Table", "lst": "Listing", "FIG": "FIGURE",
        "part": "PART", "annex": "ANNEX",
        "toc": "CONTENTS", "lof": "LIST OF FIGURES", "lot": "LIST OF TABLES", "lol": "LIST OF LISTINGS",
        "no_entries": "No entries.",
        "objectives": "Chapter objectives", "level": "Level",
        "levels": {2: "Basic", 3: "Intermediate", 4: "Advanced", 5: "Consolidation"},
        "verified": "✔ Code run and verified with PyQt6 6.12.0 / Qt 6.12.0 / Python 3.13.",
        "output": "Output",
        "cat_caption": "Classes in module {m}{note} ({n})", "win_only": " (Windows only)",
        "cat_functions": "Module-level functions ({n}): ",
        "revision": "Revision", "doc_code": "Document code", "date": "Date",
        "ref_version": "Reference versions", "classification": "Classification",
        "classification_v": "Technical training manual", "author": "Author",
        "cover_alt_t": "Cover illustration",
        "cover_alt_d": "Generic illustration of a desktop application window with a chart, a form and a "
                       "snippet of PyQt6 code.",
        "control": "DOCUMENT CONTROL", "code": "Code", "title": "Title", "subtitle": "Subtitle",
        "cur_rev": "Current revision", "status": "Status", "status_v": "Issued", "prepared": "Prepared by",
        "checked": "Checked by", "approved": "Approved by",
        "na": "Not applicable — independent publication",
        "history": "REVISION HISTORY",
        "hist_head": ["Rev.", "Date", "Description", "Status"], "issued": "Issued",
        "header": "Python GUI Manual — PyQt6", "page": "Page ",
        "doc_lang": "en-US",
        "st_titlelist": "List Title", "st_sublist": "List Subtitle", "st_code": "Code",
        "st_out": "Terminal Output", "st_marker": "Content Marker", "st_tabtext": "Table Text",
        "st_tabhead": "Table Header", "st_after": "After Table", "st_inline": "Inline Code",
        "st_fig": "Figure",
        "placeholder": "[Content to be developed]",
    },
}
S = _S[LANG]

# Cores dos quadros de destaque (os dois idiomas)
NOTE_COLORS = {
    "NOTA": ("2E75B6", "EAF1FA"), "DICA": ("548235", "EEF5E9"), "ATENÇÃO": ("C55A11", "FBEFE6"),
    "IMPORTANTE": ("C00000", "FBE9E9"),
    "NOTE": ("2E75B6", "EAF1FA"), "TIP": ("548235", "EEF5E9"), "WARNING": ("C55A11", "FBEFE6"),
    "IMPORTANT": ("C00000", "FBE9E9"),
}
