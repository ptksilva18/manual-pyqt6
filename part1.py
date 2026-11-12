# -*- coding: utf-8 -*-
"""Parte I — Fundamentos (Capítulos 1 a 10), desenvolvida no Step 2 (Rev. 0B)."""
from blocks import ST_BAS, flat, part
from part1_a import CAP01, CAP02, CAP03
from part1_b import CAP04, CAP05, CAP06, CAP07
from part1_c import CAP08, CAP09, CAP10

PART1 = flat(
    part("I", "FUNDAMENTOS", "Do ambiente de desenvolvimento à primeira aplicação completa", ST_BAS,
         "Capítulos 1 a 10 · Nível Básico"),
    CAP01, CAP02, CAP03, CAP04, CAP05, CAP06, CAP07, CAP08, CAP09, CAP10,
)
