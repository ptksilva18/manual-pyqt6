# -*- coding: utf-8 -*-
"""Figuras das Partes III e IV: executa as listagens com CAPTURA=<arquivo> em escala 2x.

Listagens com OpenGL/RHI (QtGraphs, Qt Quick 3D, QOpenGLWidget) rodam sob Xvfb (xcb);
as demais na plataforma offscreen. A moldura de janela é a mesma das Partes I e II.
"""
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
LST = os.path.join(HERE, "data", "listings")
FIG = os.path.join(HERE, "data", "figs")
TMP = "/tmp/shots3"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

CAPTURAS = [  # listagem, arquivo final, título da moldura, plataforma
    ("c22_graphs2d.py", "f22_1_graphs2d.png", "QtGraphs 2D — GraphsView", "xcb"),
    ("c22_graphs3d.py", "f22_2_graphs3d.png", "QtGraphs 3D — Q3DSurfaceWidgetItem", "xcb"),
    ("c22_qtcharts.py", "f22_3_qtcharts.png", "QtCharts", "offscreen"),
    ("c22_matplotlib.py", "f22_4_matplotlib.png", "Resposta ao degrau — Matplotlib + PyQt6", "offscreen"),
    ("c25_opengl.py", "f25_1_opengl.png", "QOpenGLWidget — OpenGL 4.1 Core", "xcb"),
    ("c25_quick3d.py", "f25_2_quick3d.png", "Qt Quick 3D em QQuickWidget", "xcb"),
    ("c26_qquickwidget.py", "f26_1_qquickwidget.png", "Widgets + QML", "offscreen"),
]


def framed(path: str, title: str, out: str) -> None:
    im = Image.open(path).convert("RGB")
    w, h = im.size
    bar, border = 56, 2
    W, H = w + 2 * border, h + bar + border
    fr = Image.new("RGB", (W + 24, H + 24), (255, 255, 255))
    d = ImageDraw.Draw(fr)
    d.rounded_rectangle((14, 16, 14 + W + 6, 16 + H + 6), radius=14, fill=(205, 210, 218))
    d.rounded_rectangle((8, 8, 8 + W, 8 + H), radius=12, fill=(232, 236, 242), outline=(170, 178, 190),
                        width=2)
    d.text((8 + 24, 8 + 14), title, font=ImageFont.truetype(FONT, 24), fill=(40, 40, 40))
    for i in range(3):
        cx = 8 + W - 40 - i * 40
        d.ellipse((cx - 9, 8 + 19, cx + 9, 8 + 37), outline=(120, 128, 140), width=2)
    fr.paste(im, (8 + border, 8 + bar))
    fr.save(os.path.join(FIG, out), dpi=(300, 300))


def main() -> int:
    os.makedirs(TMP, exist_ok=True)
    from runner import _ensure_xvfb  # inicia (ou reinicia) o Xvfb :99 se necessário

    _ensure_xvfb()
    falhas = 0
    for nome, final, titulo, plat in CAPTURAS:
        bruto = os.path.join(TMP, final)
        if os.path.exists(bruto):
            os.remove(bruto)
        env = dict(os.environ, CAPTURA=bruto, QT_SCALE_FACTOR="2", QT_QPA_PLATFORM=plat,
                   DISPLAY=":99", QT_AUDIO_BACKEND="pulseaudio")
        subprocess.run([sys.executable, os.path.join(LST, nome)], cwd=LST, env=env,
                       capture_output=True, text=True, timeout=120)
        if not os.path.exists(bruto):
            print("FALHA na captura:", nome)
            falhas += 1
            continue
        framed(bruto, titulo, final)
        print(f"{final}: {Image.open(os.path.join(FIG, final)).size}")
    return falhas


if __name__ == "__main__":
    sys.exit(main())
