# -*- coding: utf-8 -*-
"""Part I — Fundamentals (Chapters 1 to 10), English edition."""
from blocks import ST_BAS, flat, part
from part1_a import CAP01, CAP02, CAP03
from part1_b import CAP04, CAP05, CAP06, CAP07
from part1_c import CAP08, CAP09, CAP10

PART1 = flat(
    part("I", "FUNDAMENTALS", "From the development environment to the first complete application", ST_BAS,
         "Chapters 1 to 10 · Basic level"),
    CAP01, CAP02, CAP03, CAP04, CAP05, CAP06, CAP07, CAP08, CAP09, CAP10,
)
