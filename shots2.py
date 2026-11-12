# -*- coding: utf-8 -*-
"""Figuras da Parte II: capturas reais (offscreen, 2x) e gráfico de curvas de easing."""
import os
import runpy
import sys

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QT_SCALE_FACTOR", "2")

from PIL import Image, ImageDraw, ImageFont  # noqa: E402
from PyQt6.QtCore import QEasingCurve, QPointF  # noqa: E402
from PyQt6.QtWidgets import QApplication, QTableView  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
LST = os.path.join(HERE, "data", "listings")
FIG = os.path.join(HERE, "data", "figs")
sys.path.insert(0, LST)
import shots  # noqa: E402,F401  (reutiliza framed/annotate; já cria a QApplication)
from shots import FONT, FONT_B, annotate, framed, grab  # noqa: E402

app = QApplication.instance()


def mod(name):
    return runpy.run_path(os.path.join(LST, name), run_name="listing")


# 11.1 Qt Designer (captura feita sob Xvfb; ver texto) -------------------------
des = Image.open(os.path.join(FIG, "raw_designer_xvfb.png")).convert("RGB").crop((0, 0, 1000, 680))
des = des.resize((2000, 1360), Image.LANCZOS)
annotate(des, [((0, 116, 516, 1356), "Caixa de widgets"),
               ((524, 116, 968, 1356), "Editor de formulário"),
               ((976, 116, 2000, 500), "Inspetor de objetos"),
               ((976, 512, 2000, 936), "Editor de propriedades"),
               ((976, 944, 2000, 1356), "Sinais/slots, ações e recursos")],
         "f11_1_designer.png")

# 12.1 temas claro e escuro ------------------------------------------------------
m12 = mod("c12_temas.py")
app.setStyle("Fusion")
claro, escuro = m12["Formulario"](), m12["Formulario"]()
claro.aplicar_tema(m12["CLARO"])
escuro.aplicar_tema(m12["ESCURO"])
for w in (claro, escuro):
    w.resize(430, 300)
a = framed(grab(claro, "t_claro"), "Tema claro")
b = framed(grab(escuro, "t_escuro"), "Tema escuro")
can = Image.new("RGB", (a.width + b.width + 40, max(a.height, b.height)), "white")
can.paste(a, (0, 0))
can.paste(b, (a.width + 40, 0))
can.save(os.path.join(FIG, "f12_1_temas.png"), dpi=(300, 300))

# 14.2 tabela com modelo e delegado ---------------------------------------------
m14 = mod("c14_delegado.py")
modelo = m14["ModeloEnsaios"]([m14["Ensaio"]("BOP-01", 345.0, True), m14["Ensaio"]("BOP-02", 310.5, False),
                               m14["Ensaio"]("XT-07", 690.0, True)])
vista = QTableView()
vista.setModel(modelo)
vista.setItemDelegateForColumn(1, m14["DelegadoPressao"](1035.0, vista))
vista.setAlternatingRowColors(True)
vista.resize(420, 170)
vista.horizontalHeader().setStretchLastSection(True)
framed(grab(vista, "t_tabela"), "QTableView + ModeloEnsaios + DelegadoPressao", "f14_2_tabela.png")

# 17.1 primitivas e manômetro ------------------------------------------------------
from PyQt6.QtGui import QImage  # noqa: E402
m17 = mod("c17_primitivas.py")
img = QImage(800, 640, QImage.Format.Format_ARGB32_Premultiplied)
img.setDevicePixelRatio(2.0)
m17["desenhar"](img)
img.save(os.path.join(FIG, "f17_1_primitivas.png"))
Man = mod("c17_manometro.py")["Manometro"]
m1, m2 = Man(690.0), Man(15.0, "ksi")
m1.valor, m2.valor = 345.0, 14.2
for m in (m1, m2):
    m.resize(300, 300)
a = framed(grab(m1, "man1"), "Manometro(690 bar)")
b = framed(grab(m2, "man2"), "Manometro(15 ksi)")
can = Image.new("RGB", (a.width + b.width + 40, max(a.height, b.height)), "white")
can.paste(a, (0, 0))
can.paste(b, (a.width + 40, 0))
can.save(os.path.join(FIG, "f17_2_manometro.png"), dpi=(300, 300))

# 18.1 cena com duas visões ---------------------------------------------------------
m18 = mod("c18_cena.py")
from PyQt6.QtGui import QPainter  # noqa: E402
from PyQt6.QtWidgets import QGraphicsView, QHBoxLayout, QWidget  # noqa: E402
cena = m18["montar_cena"]()
v1, v2 = m18["VisaoZoom"](cena), QGraphicsView(cena)
for v in (v1, v2):
    v.setRenderHint(QPainter.RenderHint.Antialiasing)
v2.scale(0.6, 0.6)
v2.rotate(-8)
next(i for i in cena.items() if getattr(i, "tag", "") == "XV-102").setSelected(True)
j = QWidget()
lay = QHBoxLayout(j)
lay.addWidget(v1, 3)
lay.addWidget(v2, 2)
j.resize(900, 320)
framed(grab(j, "cena"), "Uma QGraphicsScene exibida por duas QGraphicsView", "f18_1_cena.png")

# 19.1 curvas de easing (valores calculados pelo próprio QEasingCurve) -------------
import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
tipos = ["Linear", "InOutQuad", "OutCubic", "OutBounce", "InOutElastic", "OutBack"]
fig, eixos = plt.subplots(2, 3, figsize=(9, 5.2), dpi=200, sharex=True, sharey=True)
t = [i / 200 for i in range(201)]
for ax, nome in zip(eixos.flat, tipos):
    c = QEasingCurve(getattr(QEasingCurve.Type, nome))
    ax.plot(t, [c.valueForProgress(x) for x in t], color="#2E75B6", lw=2)
    ax.plot([0, 1], [0, 1], color="#BFBFBF", lw=1, ls="--")
    ax.set_title(f"QEasingCurve.Type.{nome}", fontsize=9)
    ax.grid(alpha=0.3)
    ax.set_ylim(-0.45, 1.45)
for ax in eixos[1]:
    ax.set_xlabel("progresso do tempo")
for ax in eixos[:, 0]:
    ax.set_ylabel("valor")
fig.tight_layout()
fig.savefig(os.path.join(FIG, "f19_1_easing.png"))
print("figuras da Parte II geradas")
