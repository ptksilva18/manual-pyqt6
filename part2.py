# -*- coding: utf-8 -*-
"""Parte II — Interface profissional (Capítulos 11 a 19), desenvolvida no Step 3 (Rev. 0C)."""
from blocks import ST_INT, flat, part
from part2_a import CAP11, CAP12, CAP13, CAP14
from part2_b import CAP15, CAP16, CAP17, CAP18, CAP19

PART2 = flat(
    part("II", "INTERFACE PROFISSIONAL", "Design, estilo, dados e gráficos 2D", ST_INT,
         "Capítulos 11 a 19 · Nível Intermediário"),
    CAP11, CAP12, CAP13, CAP14, CAP15, CAP16, CAP17, CAP18, CAP19,
)
