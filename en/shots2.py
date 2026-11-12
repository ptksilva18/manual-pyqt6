# -*- coding: utf-8 -*-
"""Part II figures — English edition: real screenshots (offscreen, 2x) and easing-curve chart."""
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
import shots  # noqa: E402,F401  (en/shots.py: reuses framed/annotate; creates the QApplication)
from shots import FONT, FONT_B, annotate, framed, grab  # noqa: E402

app = QApplication.instance()


def mod(name):
    return runpy.run_path(os.path.join(LST, name), run_name="listing")


# 11.1 Qt Designer (screenshot taken under Xvfb; see the text) ---------------
des = Image.open(os.path.join(FIG, "raw_designer_xvfb.png")).convert("RGB").crop((0, 0, 1000, 680))
des = des.resize((2000, 1360), Image.LANCZOS)
annotate(des, [((0, 116, 516, 1356), "Widget box"),
               ((524, 116, 968, 1356), "Form editor"),
               ((976, 116, 2000, 500), "Object inspector"),
               ((976, 512, 2000, 936), "Property editor"),
               ((976, 944, 2000, 1356), "Signals/slots, actions and resources")],
         "f11_1_designer.png")

# 12.1 light and dark themes ----------------------------------------------------
m12 = mod("c12_themes.py")
app.setStyle("Fusion")
light, dark = m12["Form"](), m12["Form"]()
light.apply_theme(m12["LIGHT"])
dark.apply_theme(m12["DARK"])
for w in (light, dark):
    w.resize(430, 300)
a = framed(grab(light, "t_light"), "Light theme")
b = framed(grab(dark, "t_dark"), "Dark theme")
can = Image.new("RGB", (a.width + b.width + 40, max(a.height, b.height)), "white")
can.paste(a, (0, 0))
can.paste(b, (a.width + 40, 0))
can.save(os.path.join(FIG, "f12_1_themes.png"), dpi=(300, 300))

# 14.2 table with model and delegate --------------------------------------------
m14 = mod("c14_delegate.py")
model = m14["TestModel"]([m14["PressureTest"]("BOP-01", 345.0, True), m14["PressureTest"]("BOP-02", 310.5, False),
                          m14["PressureTest"]("XT-07", 690.0, True)])
view = QTableView()
view.setModel(model)
view.setItemDelegateForColumn(1, m14["PressureDelegate"](1035.0, view))
view.setAlternatingRowColors(True)
view.resize(420, 170)
view.horizontalHeader().setStretchLastSection(True)
framed(grab(view, "t_table"), "QTableView + TestModel + PressureDelegate", "f14_2_table.png")

# 17.1 primitives and gauge --------------------------------------------------------
from PyQt6.QtGui import QImage  # noqa: E402
m17 = mod("c17_primitives.py")
img = QImage(800, 640, QImage.Format.Format_ARGB32_Premultiplied)
img.setDevicePixelRatio(2.0)
m17["draw"](img)
img.save(os.path.join(FIG, "f17_1_primitives.png"))
Gauge = mod("c17_gauge.py")["Gauge"]
m1, m2 = Gauge(690.0), Gauge(15.0, "ksi")
m1.value, m2.value = 345.0, 14.2
for m in (m1, m2):
    m.resize(300, 300)
a = framed(grab(m1, "gauge1"), "Gauge(690 bar)")
b = framed(grab(m2, "gauge2"), "Gauge(15 ksi)")
can = Image.new("RGB", (a.width + b.width + 40, max(a.height, b.height)), "white")
can.paste(a, (0, 0))
can.paste(b, (a.width + 40, 0))
can.save(os.path.join(FIG, "f17_2_gauge.png"), dpi=(300, 300))

# 18.1 scene with two views ---------------------------------------------------------
m18 = mod("c18_scene.py")
from PyQt6.QtGui import QPainter  # noqa: E402
from PyQt6.QtWidgets import QGraphicsView, QHBoxLayout, QWidget  # noqa: E402
scene = m18["build_scene"]()
v1, v2 = m18["ZoomView"](scene), QGraphicsView(scene)
for v in (v1, v2):
    v.setRenderHint(QPainter.RenderHint.Antialiasing)
v2.scale(0.6, 0.6)
v2.rotate(-8)
next(i for i in scene.items() if getattr(i, "tag", "") == "XV-102").setSelected(True)
j = QWidget()
lay = QHBoxLayout(j)
lay.addWidget(v1, 3)
lay.addWidget(v2, 2)
j.resize(900, 320)
framed(grab(j, "scene"), "A QGraphicsScene shown by two QGraphicsView", "f18_1_scene.png")

# 19.1 easing curves (values computed by QEasingCurve itself) ----------------------
import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
kinds = ["Linear", "InOutQuad", "OutCubic", "OutBounce", "InOutElastic", "OutBack"]
fig, axes = plt.subplots(2, 3, figsize=(9, 5.2), dpi=200, sharex=True, sharey=True)
t = [i / 200 for i in range(201)]
for ax, name in zip(axes.flat, kinds):
    c = QEasingCurve(getattr(QEasingCurve.Type, name))
    ax.plot(t, [c.valueForProgress(x) for x in t], color="#2E75B6", lw=2)
    ax.plot([0, 1], [0, 1], color="#BFBFBF", lw=1, ls="--")
    ax.set_title(f"QEasingCurve.Type.{name}", fontsize=9)
    ax.grid(alpha=0.3)
    ax.set_ylim(-0.45, 1.45)
for ax in axes[1]:
    ax.set_xlabel("time progress")
for ax in axes[:, 0]:
    ax.set_ylabel("value")
fig.tight_layout()
fig.savefig(os.path.join(FIG, "f19_1_easing.png"))
print("Part II figures generated")
