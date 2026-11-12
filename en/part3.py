# -*- coding: utf-8 -*-
"""Part III — Advanced development (Chapters 20 to 26), English edition."""
from blocks import ST_AVA, flat, part
from part3_a import CAP20, CAP21, CAP22
from part3_b import CAP23, CAP24, CAP25, CAP26

PART3 = flat(
    part("III", "ADVANCED DEVELOPMENT", "Concurrency, communication, visualization, media, Web, 3D and QML",
         ST_AVA, "Chapters 20 to 26 · Advanced level"),
    CAP20, CAP21, CAP22, CAP23, CAP24, CAP25, CAP26,
)
