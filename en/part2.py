# -*- coding: utf-8 -*-
"""Part II — Professional interface (Chapters 11 to 19), English edition."""
from blocks import ST_INT, flat, part
from part2_a import CAP11, CAP12, CAP13, CAP14
from part2_b import CAP15, CAP16, CAP17, CAP18, CAP19

PART2 = flat(
    part("II", "PROFESSIONAL INTERFACE", "Design, style, data and 2D graphics", ST_INT,
         "Chapters 11 to 19 · Intermediate level"),
    CAP11, CAP12, CAP13, CAP14, CAP15, CAP16, CAP17, CAP18, CAP19,
)
