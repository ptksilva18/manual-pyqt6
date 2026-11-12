# -*- coding: utf-8 -*-
"""Geracao das imagens do documento: capa e placeholders de figuras."""
import math
import textwrap

from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_M = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

NAVY = (31, 56, 100)
BLUE = (46, 117, 182)
LIGHT = (234, 241, 250)
GREY = (120, 120, 120)

PH_W, PH_H = 1800, 780       # 15,0 cm x 6,5 cm
COVER_W, COVER_H = 1920, 1000  # 16,0 cm x 8,33 cm


def _dashed_rect(d, box, color, width=4, dash=24, gap=14):
    x0, y0, x1, y1 = box
    for (a, b, horiz, fixed) in ((x0, x1, True, y0), (x0, x1, True, y1), (y0, y1, False, x0), (y0, y1, False, x1)):
        pos = a
        while pos < b:
            end = min(pos + dash, b)
            if horiz:
                d.line([(pos, fixed), (end, fixed)], fill=color, width=width)
            else:
                d.line([(fixed, pos), (fixed, end)], fill=color, width=width)
            pos = end + gap


def placeholder(path, label, title, desc, step_text):
    img = Image.new("RGB", (PH_W, PH_H), (247, 249, 252))
    d = ImageDraw.Draw(img)
    _dashed_rect(d, (14, 14, PH_W - 15, PH_H - 15), BLUE, width=5)
    # icone generico de imagem (moldura + montanha + sol)
    cx, cy = PH_W // 2, 170
    d.rounded_rectangle((cx - 90, cy - 62, cx + 90, cy + 62), radius=12, outline=BLUE, width=6)
    d.polygon([(cx - 70, cy + 45), (cx - 20, cy - 15), (cx + 10, cy + 20), (cx + 35, cy - 2), (cx + 72, cy + 45)], fill=(180, 205, 232))
    d.ellipse((cx + 28, cy - 45, cx + 58, cy - 15), fill=(180, 205, 232))
    f_lab = ImageFont.truetype(FONT_B, 46)
    f_tit = ImageFont.truetype(FONT_B, 40)
    f_desc = ImageFont.truetype(FONT, 32)
    f_step = ImageFont.truetype(FONT, 28)
    y = 270
    for text, font, color, gap in ((label, f_lab, NAVY, 16),):
        w = d.textlength(text, font=font)
        d.text(((PH_W - w) / 2, y), text, font=font, fill=color)
        y += font.size + gap
    for line in textwrap.wrap(title, 62):
        w = d.textlength(line, font=f_tit)
        d.text(((PH_W - w) / 2, y), line, font=f_tit, fill=NAVY)
        y += 52
    y += 14
    for line in textwrap.wrap(desc, 88)[:5]:
        w = d.textlength(line, font=f_desc)
        d.text(((PH_W - w) / 2, y), line, font=f_desc, fill=(70, 70, 70))
        y += 44
    w = d.textlength(step_text, font=f_step)
    d.text(((PH_W - w) / 2, PH_H - 80), step_text, font=f_step, fill=GREY)
    img.save(path, dpi=(300, 300))


def cover(path):
    """Ilustracao original e generica de uma janela de aplicacao desktop."""
    W, H = COVER_W, COVER_H
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    # fundo em gradiente vertical
    for yy in range(H):
        t = yy / H
        c = tuple(int(NAVY[i] * (1 - t) + (16, 30, 56)[i] * t) for i in range(3))
        d.line([(0, yy), (W, yy)], fill=c)
    # grade tecnica sutil
    for x in range(0, W, 48):
        d.line([(x, 0), (x, H)], fill=(40, 68, 116), width=1)
    for yy in range(0, H, 48):
        d.line([(0, yy), (W, yy)], fill=(40, 68, 116), width=1)
    # janela principal
    x0, y0, x1, y1 = 300, 110, 1620, 900
    d.rounded_rectangle((x0 + 14, y0 + 18, x1 + 14, y1 + 18), radius=22, fill=(10, 20, 40))
    d.rounded_rectangle((x0, y0, x1, y1), radius=22, fill=(245, 247, 250))
    d.rounded_rectangle((x0, y0, x1, y0 + 64), radius=22, fill=(222, 228, 237))
    d.rectangle((x0, y0 + 40, x1, y0 + 64), fill=(222, 228, 237))
    for i, col in enumerate(((150, 160, 175), (150, 160, 175), (150, 160, 175))):
        d.ellipse((x1 - 150 + i * 42, y0 + 20, x1 - 126 + i * 42, y0 + 44), fill=col)
    # barra de menus e ferramentas
    d.rectangle((x0, y0 + 64, x1, y0 + 110), fill=(236, 240, 246))
    for i in range(6):
        d.rounded_rectangle((x0 + 24 + i * 120, y0 + 76, x0 + 120 + i * 120, y0 + 98), radius=6, fill=(205, 214, 228))
    # painel lateral (arvore)
    d.rectangle((x0, y0 + 110, x0 + 330, y1 - 40), fill=(232, 237, 245))
    for i in range(10):
        ind = 30 if i % 3 else 0
        d.rounded_rectangle((x0 + 24 + ind, y0 + 140 + i * 52, x0 + 290, y0 + 166 + i * 52), radius=6,
                            fill=BLUE if i == 4 else (200, 210, 226))
    # area de grafico
    gx0, gy0, gx1, gy1 = x0 + 370, y0 + 140, x1 - 40, y0 + 520
    d.rounded_rectangle((gx0, gy0, gx1, gy1), radius=10, fill=(255, 255, 255), outline=(205, 214, 228), width=3)
    for k in range(1, 6):
        yy = gy0 + k * (gy1 - gy0) / 6
        d.line([(gx0 + 20, yy), (gx1 - 20, yy)], fill=(232, 236, 242), width=2)
    pts = []
    for k in range(0, 101):
        xx = gx0 + 30 + k * (gx1 - gx0 - 60) / 100
        val = 0.5 + 0.28 * math.sin(k / 9.0) * math.exp(-k / 140) + 0.12 * math.sin(k / 3.1)
        pts.append((xx, gy1 - 30 - val * (gy1 - gy0 - 60)))
    d.line(pts, fill=BLUE, width=6, joint="curve")
    pts2 = [(xx, yy + 40 + 25 * math.cos(i / 7)) for i, (xx, yy) in enumerate(pts)]
    d.line(pts2, fill=(237, 125, 49), width=5, joint="curve")
    # formulario: rotulos, campos, slider, botoes
    fy = y0 + 560
    for i in range(3):
        d.rounded_rectangle((gx0, fy + i * 62, gx0 + 200, fy + i * 62 + 34), radius=6, fill=(200, 210, 226))
        d.rounded_rectangle((gx0 + 230, fy + i * 62, gx0 + 640, fy + i * 62 + 34), radius=6, fill=(255, 255, 255),
                            outline=(180, 192, 210), width=3)
    sx0, sx1, sy = gx0 + 700, gx1 - 30, fy + 18
    d.line([(sx0, sy), (sx1, sy)], fill=(190, 200, 216), width=8)
    d.line([(sx0, sy), (sx0 + (sx1 - sx0) * 0.62, sy)], fill=BLUE, width=8)
    d.ellipse((sx0 + (sx1 - sx0) * 0.62 - 16, sy - 16, sx0 + (sx1 - sx0) * 0.62 + 16, sy + 16), fill=(255, 255, 255),
              outline=BLUE, width=5)
    for i, col in enumerate((BLUE, (205, 214, 228))):
        d.rounded_rectangle((sx0, fy + 62 + i * 62, sx1, fy + 106 + i * 62), radius=10, fill=col)
    # barra de status
    d.rectangle((x0, y1 - 40, x1, y1), fill=(222, 228, 237))
    d.rounded_rectangle((x0, y1 - 40, x1, y1), radius=22, fill=(222, 228, 237))
    d.rectangle((x0, y1 - 40, x1, y1 - 20), fill=(222, 228, 237))
    d.rounded_rectangle((x0 + 24, y1 - 30, x0 + 300, y1 - 12), radius=5, fill=(200, 210, 226))
    # prompt de codigo sobreposto
    cx0, cy0 = 70, 560
    d.rounded_rectangle((cx0 + 10, cy0 + 12, cx0 + 680, cy0 + 352), radius=16, fill=(5, 12, 25))
    d.rounded_rectangle((cx0, cy0, cx0 + 670, cy0 + 340), radius=16, fill=(24, 32, 48))
    fm = ImageFont.truetype(FONT_M, 30)
    kw, tx, ok = (198, 120, 221), (220, 223, 228), (152, 195, 121)
    lines = [("import", kw, " sys", tx),
             ("from", kw, " PyQt6.QtWidgets ", tx, "import", kw, " (", tx),
             ("    QApplication, QMainWindow)", tx),
             ("app = QApplication(sys.argv)", tx),
             ("win = QMainWindow()", tx),
             ("win.show()", tx),
             ("sys.exit(app.exec())", ok)]
    yy = cy0 + 30
    for ln in lines:
        xx = cx0 + 28
        for j in range(0, len(ln), 2):
            d.text((xx, yy), ln[j], font=fm, fill=ln[j + 1])
            xx += d.textlength(ln[j], font=fm)
        yy += 40
    img.save(path, dpi=(300, 300))


if __name__ == "__main__":
    import os
    aqui = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
    cover(os.path.join(aqui, "cover.png"))
    placeholder(os.path.join(aqui, "ph_test.png"), "FIGURA 1.1", "Arquitetura em camadas de uma aplicação PyQt6",
                "Diagrama: código Python → PyQt6 (extensões SIP) → bibliotecas Qt 6 (C++) → plataforma.",
                "Espaço reservado · imagem a produzir no Step 2 — Básico")
