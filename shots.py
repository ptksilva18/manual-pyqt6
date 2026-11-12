# -*- coding: utf-8 -*-
"""
Capturas de tela REAIS das listagens (QWidget.grab() em modo offscreen, escala 2x).
As janelas são as próprias classes das listagens testadas (fonte única).
Uso: QT_QPA_PLATFORM=offscreen QT_SCALE_FACTOR=2 python shots.py
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

HERE = os.path.dirname(os.path.abspath(__file__))
LST = os.path.join(HERE, "data", "listings")
FIG = os.path.join(HERE, "data", "figs")
TMP = "/tmp/shots"
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
    """Moldura de janela neutra (genérica) em torno da área cliente capturada."""
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
    """Retângulos numerados + legenda à direita."""
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


# --- Figura 4.1: primeira aplicação -------------------------------------------
m = mod("c04_primeira.py")
from PyQt6.QtWidgets import QLabel  # noqa: E402
lab = QLabel("Olá, PyQt6!")
lab.setAlignment(Qt.AlignmentFlag.AlignCenter)
lab.resize(320, 120)
framed(grab(lab, "f41"), "Primeira aplicação", "f4_1_primeira.png")

# --- Figura 6.1: galeria -------------------------------------------------------
g = mod("c06_galeria.py")["Galeria"]()
g.resize(740, 440)
framed(grab(g, "f61"), "Galeria de widgets", "f6_1_galeria.png")

# --- Figura 7.1: box layouts em dois tamanhos ----------------------------------
Editor = mod("c07_caixas.py")["Editor"]
e1, e2 = Editor(), Editor()
e1.resize(420, 300)
e2.resize(420, 420)
a = framed(grab(e1, "f71a"), "Janela com 300 px de altura")
b = framed(grab(e2, "f71b"), "Janela com 420 px de altura")
can = Image.new("RGB", (a.width + b.width + 40, max(a.height, b.height)), "white")
can.paste(a, (0, (can.height - a.height)))
can.paste(b, (a.width + 40, 0))
can.save(os.path.join(FIG, "f7_1_caixas.png"), dpi=(300, 300))

# --- Figura 7.2: composição aninhada --------------------------------------------
c = mod("c07_composicao.py")["CalculoTubo"]()
c.resize(520, 430)
framed(grab(c, "f72"), "Verificação de tubo — layouts aninhados", "f7_2_composicao.png")

# --- Figura 8.1: QMainWindow anotada -------------------------------------------
from PyQt6.QtCore import QSettings  # noqa: E402
QSettings("Engenharia", "DiarioEnsaios").clear()
J = mod("c08_janela_principal.py")["JanelaPrincipal"]
j = J()
j.resize(720, 420)
j.abas.currentWidget().setPlainText("Teste hidrostático do BOP\n345 bar por 15 min — aprovado")
p = grab(j, "f81")
QSettings("Engenharia", "DiarioEnsaios").clear()
dpr = j.devicePixelRatioF()
img = Image.open(p).convert("RGB")
from PyQt6.QtWidgets import QDockWidget, QToolBar  # noqa: E402
boxes = [
    (geo(j.menuBar(), j, dpr, (0, 0)), "Barra de menus (QMenuBar)"),
    (geo(j.findChild(QToolBar), j, dpr, (0, 0)), "Barra de ferramentas (QToolBar)"),
    (geo(j.findChild(QDockWidget), j, dpr, (0, 0)), "Painel acoplável (QDockWidget)"),
    (geo(j.centralWidget(), j, dpr, (0, 0)), "Widget central (QTabWidget)"),
    (geo(j.statusBar(), j, dpr, (0, 0)), "Barra de status (QStatusBar)"),
]
annotate(img, boxes, "f8_1_mainwindow.png", anchors={4: "c"})

# --- Figura 9.1: mosaico de diálogos padrão -------------------------------------
shots = []
mb = QMessageBox(QMessageBox.Icon.Warning, "Alterações não salvas", "O documento foi modificado.",
                 QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard
                 | QMessageBox.StandardButton.Cancel)
mb.setInformativeText("Deseja salvar as alterações?")
shots.append(framed(grab(mb, "d1"), "QMessageBox"))
ind = QInputDialog()
ind.setInputMode(QInputDialog.InputMode.DoubleInput)
ind.setLabelText("Fator de segurança:")
ind.setDoubleDecimals(2)
ind.setDoubleValue(1.5)
shots.append(framed(grab(ind, "d2"), "QInputDialog"))
pd = QProgressDialog("Processando arquivos…", "Cancelar", 0, 100)
pd.setValue(60)
shots.append(framed(grab(pd, "d3"), "QProgressDialog"))
cd = QColorDialog(QColor("#2E75B6"))
cd.setOption(QColorDialog.ColorDialogOption.DontUseNativeDialog, True)
shots.append(framed(grab(cd, "d4"), "QColorDialog"))
from PyQt6.QtGui import QFont  # noqa: E402
fd = QFontDialog(QFont("DejaVu Sans", 11))
fd.setOption(QFontDialog.FontDialogOption.DontUseNativeDialog, True)
shots.append(framed(grab(fd, "d5"), "QFontDialog"))
fdl = QFileDialog(None, "Abrir ensaio", "/usr/share", "Ensaios (*.json *.csv);;Todos (*)")
fdl.setOption(QFileDialog.Option.DontUseNativeDialog, True)
fdl.resize(700, 420)
shots.append(framed(grab(fdl, "d6"), "QFileDialog"))
# layout: 3 colunas x 2 linhas, cada célula reduzida a largura comum
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
mos.save(os.path.join(FIG, "f9_1_dialogos.png"), dpi=(300, 300))
print("capturas geradas:", sorted(f for f in os.listdir(FIG) if f.startswith("f")))
