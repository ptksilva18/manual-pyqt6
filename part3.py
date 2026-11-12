# -*- coding: utf-8 -*-
"""Parte III — Desenvolvimento avançado (Capítulos 20 a 26), desenvolvida no Step 4 (Rev. 0D)."""
from blocks import ST_AVA, flat, part
from part3_a import CAP20, CAP21, CAP22
from part3_b import CAP23, CAP24, CAP25, CAP26

PART3 = flat(
    part("III", "DESENVOLVIMENTO AVANÇADO", "Concorrência, comunicação, visualização, mídia, Web, 3D e QML",
         ST_AVA, "Capítulos 20 a 26 · Nível Avançado"),
    CAP20, CAP21, CAP22, CAP23, CAP24, CAP25, CAP26,
)
