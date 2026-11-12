# -*- coding: utf-8 -*-
"""
REAL screenshots of the listings — English edition (QWidget.grab() offscreen, 2x scale).
The windows are the very classes of the tested listings (single source).
Usage: QT_QPA_PLATFORM=offscreen QT_SCALE_FACTOR=2 python en/shots.py
"""
import os
import runpy
import sys

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QT_SCALE_FACTOR", "2")

from PIL import Image, ImageDraw, ImageFont  # noqa: E402
from PyQt6.QtCore import QDate, Qt  # noqa: E402
from PyQt6.QtGui import QColor  # noqa: E402
from PyQt6.QtWidgets import (  # noqa: E402
    QApplication, QColorDialog, QFileDialog, QFontDialog, QInputDialog, QMessageBox,
    QProgressDialog, QWidget,
)

HERE = os.path.dirname(os.path.abspath(__file__))      # en/
LST = os.path.join(HERE, "data", "listings")
FIG = os.path.join(HERE, "data", "figs")
TMP = "/tmp/shots_en"
os.makedirs(FIG, exist_ok=True)
os.makedirs(TMP, exist_ok=True)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

app = QApplication(sys.argv)


def mod(name):
    return runpy.run_path(os.path.join(LST, name), run_name="listing")


def grab(w: QWidget, name: str) -> str:
    w.show()
    for _ in range(5):
        app.processEvents()
    path = os.path.join(TMP, name + ".png")
    w.grab().save(path)
    return path


def framed(path: str, title: str, out: str | None = None) -> Image.Image:
    """Neutral (generic) window frame around the captured client area."""
    im = Image.open(path).convert("RGB")
    w, h = im.size
    bar, border = 56, 2
    W, H = w + 2 * border, h + bar + border
    fr = Image.new("RGB", (W + 24, H + 24), (255, 255, 255))
    d = ImageDraw.Draw(fr)
    d.rounded_rectangle((14, 16, 14 + W + 6, 16 + H + 6), radius=14, fill=(205, 210, 218))   # sombra
    d.rounded_rectangle((8, 8, 8 + W, 8 + H), radius=12, fill=(232, 236, 242), outline=(170, 178, 190), width=2)
    f = ImageFont.truetype(FONT, 24)
    d.text((8 + 24, 8 + 14), title, font=f, fill=(40, 40, 40))
    for i in range(3):
        cx = 8 + W - 40 - i * 40
        d.ellipse((cx - 9, 8 + 19, cx + 9, 8 + 37), outline=(120, 128, 140), width=2)
    fr.paste(im, (8 + border, 8 + bar))
    if out:
        fr.save(os.path.join(FIG, out), dpi=(300, 300))
    return fr


def annotate(img: Image.Image, boxes, out: str, anchors=None) -> None:
    """Numbered rectangles + legend on the right."""
    pad = 560
    W, H = img.size
    can = Image.new("RGB", (W + pad, H), (255, 255, 255))
    can.paste(img, (0, 0))
    d = ImageDraw.Draw(can)
    cores = [(192, 0, 0), (46, 117, 182), (84, 130, 53), (197, 90, 17), (112, 48, 160), (0, 128, 128)]
    fl = ImageFont.truetype(FONT_B, 26)
    ft = ImageFont.truetype(FONT, 25)
    y = 40
    for i, (rect, texto) in enumerate(boxes):
        c = cores[i % len(cores)]
        x0, y0, x1, y1 = rect
        d.rectangle((x0, y0, x1, y1), outline=c, width=5)
        anc = (anchors or {}).get(i, "r")
        cy = (y0 + y1) / 2
        cx = x1 - 34 if anc == "r" else (x0 + x1) / 2
        d.ellipse((cx - 20, cy - 20, cx + 20, cy + 20), fill=c)
        d.text((cx, cy), str(i + 1), font=fl, fill="white", anchor="mm")
        d.ellipse((W + 30, y, W + 70, y + 40), fill=c)
        d.text((W + 50, y + 20), str(i + 1), font=fl, fill="white", anchor="mm")
        d.text((W + 85, y + 6), texto, font=ft, fill=(30, 30, 30))
        y += 64
    can.save(os.path.join(FIG, out), dpi=(300, 300))


def geo(w: QWidget, root: QWidget, dpr: float, off) -> tuple:
    p = w.mapTo(root, w.rect().topLeft())
    return (off[0] + p.x() * dpr, off[1] + p.y() * dpr,
            off[0] + (p.x() + w.width()) * dpr - 1, off[1] + (p.y() + w.height()) * dpr - 1)


# --- Figure 4.1: first application --------------------------------------------
m = mod("c04_first.py")
from PyQt6.QtWidgets import QLabel  # noqa: E402
lab = QLabel("Hello, PyQt6!")
lab.setAlignment(Qt.AlignmentFlag.AlignCenter)
lab.resize(320, 120)
framed(grab(lab, "f41"), "First application", "f4_1_first.png")

# --- Figure 6.1: gallery -------------------------------------------------------
g = mod("c06_gallery.py")["Gallery"]()
g.resize(740, 440)
framed(grab(g, "f61"), "Widget gallery", "f6_1_gallery.png")

# --- Figure 7.1: box layouts in two sizes ----------------------------------
Editor = mod("c07_boxes.py")["Editor"]
e1, e2 = Editor(), Editor()
e1.resize(420, 300)
e2.resize(420, 420)
a = framed(grab(e1, "f71a"), "Window 300 px high")
b = framed(grab(e2, "f71b"), "Window 420 px high")
can = Image.new("RGB", (a.width + b.width + 40, max(a.height, b.height)), "white")
can.paste(a, (0, (can.height - a.height)))
can.paste(b, (a.width + 40, 0))
can.save(os.path.join(FIG, "f7_1_boxes.png"), dpi=(300, 300))

# --- Figure 7.2: nested composition --------------------------------------------
c = mod("c07_composition.py")["PipeCheck"]()
c.resize(520, 430)
framed(grab(c, "f72"), "Pipe check — nested layouts", "f7_2_composition.png")

# --- Figure 8.1: annotated QMainWindow -------------------------------------------
from PyQt6.QtCore import QSettings  # noqa: E402
QSettings("Engineering", "TestLog").clear()
J = mod("c08_main_window.py")["MainWindow"]
j = J()
j.resize(720, 420)
j.tabs.currentWidget().setPlainText("BOP hydrostatic test\n345 bar for 15 min — passed")
p = grab(j, "f81")
QSettings("Engineering", "TestLog").clear()
dpr = j.devicePixelRatioF()
img = Image.open(p).convert("RGB")
from PyQt6.QtWidgets import QDockWidget, QToolBar  # noqa: E402
boxes = [
    (geo(j.menuBar(), j, dpr, (0, 0)), "Menu bar (QMenuBar)"),
    (geo(j.findChild(QToolBar), j, dpr, (0, 0)), "Toolbar (QToolBar)"),
    (geo(j.findChild(QDockWidget), j, dpr, (0, 0)), "Dock widget (QDockWidget)"),
    (geo(j.centralWidget(), j, dpr, (0, 0)), "Central widget (QTabWidget)"),
    (geo(j.statusBar(), j, dpr, (0, 0)), "Status bar (QStatusBar)"),
]
annotate(img, boxes, "f8_1_mainwindow.png", anchors={4: "c"})

# --- Figure 9.1: mosaic of standard dialogs -------------------------------------
shots = []
mb = QMessageBox(QMessageBox.Icon.Warning, "Unsaved changes", "The document has been modified.",
                 QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard
                 | QMessageBox.StandardButton.Cancel)
mb.setInformativeText("Do you want to save your changes?")
shots.append(framed(grab(mb, "d1"), "QMessageBox"))
ind = QInputDialog()
ind.setInputMode(QInputDialog.InputMode.DoubleInput)
ind.setLabelText("Safety factor:")
ind.setDoubleDecimals(2)
ind.setDoubleValue(1.5)
shots.append(framed(grab(ind, "d2"), "QInputDialog"))
pd = QProgressDialog("Processing files…", "Cancel", 0, 100)
pd.setValue(60)
shots.append(framed(grab(pd, "d3"), "QProgressDialog"))
cd = QColorDialog(QColor("#2E75B6"))
cd.setOption(QColorDialog.ColorDialogOption.DontUseNativeDialog, True)
shots.append(framed(grab(cd, "d4"), "QColorDialog"))
from PyQt6.QtGui import QFont  # noqa: E402
fd = QFontDialog(QFont("DejaVu Sans", 11))
fd.setOption(QFontDialog.FontDialogOption.DontUseNativeDialog, True)
shots.append(framed(grab(fd, "d5"), "QFontDialog"))
fdl = QFileDialog(None, "Open test", "/usr/share", "Tests (*.json *.csv);;All (*)")
fdl.setOption(QFileDialog.Option.DontUseNativeDialog, True)
fdl.resize(700, 420)
shots.append(framed(grab(fdl, "d6"), "QFileDialog"))
# layout: 3 columns x 2 rows, each cell scaled down to a common width
cw = 900
cells = []
for s in shots:
    r = cw / s.width
    cells.append(s.resize((cw, int(s.height * r)), Image.LANCZOS) if s.width > cw else s)
order = [cells[0], cells[1], cells[2], cells[5], cells[3], cells[4]]
rows = [order[0:2], order[2:4], order[4:6]]
H = sum(max(c.height for c in row) for row in rows) + 60
W = 2 * cw + 30
mos = Image.new("RGB", (W, H), "white")
y = 0
for row in rows:
    x = 0
    for c_ in row:
        mos.paste(c_, (x + (cw - c_.width) // 2, y))
        x += cw + 30
    y += max(c_.height for c_ in row) + 30
mos.save(os.path.join(FIG, "f9_1_dialogs.png"), dpi=(300, 300))
print("screenshots generated:", sorted(f for f in os.listdir(FIG) if f.startswith("f")))
