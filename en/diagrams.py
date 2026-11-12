# -*- coding: utf-8 -*-
"""Teaching diagrams — English edition (same drawing helpers as ../diagrams.py, 2x)."""
import math
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import diagrams as D  # noqa: E402  (helpers: box, arrow, label, font, colors)

D.FIG = os.path.join(HERE, "data", "figs")      # save() writes to en/data/figs
os.makedirs(D.FIG, exist_ok=True)
box, arrow, label, font, save = D.box, D.arrow, D.label, D.font, D.save
NAVY, BLUE, GREEN, ORANGE, GREY = D.NAVY, D.BLUE, D.GREEN, D.ORANGE, D.GREY
PALE, EDGE = D.PALE, D.EDGE


# ------------------------------------------------------------------ 1.1 ----
def fig_1_1():
    W, H = 1900, 1160
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    layers = [
        (["Your Python application", "classes, signals and slots, business logic (.py)"], "green"),
        (["PyQt6 — bindings generated with SIP", "extension modules QtCore, QtGui, QtWidgets… + PyQt6-sip"], "blue"),
        (["Qt 6 libraries (C++)", "Qt6Core, Qt6Gui, Qt6Widgets… shipped in the PyQt6-Qt6 package"], "blue"),
        (["Qt platform plugins", "windows · cocoa (macOS) · xcb / wayland (Linux) · offscreen"], "orange"),
        (["Operating system", "Windows · macOS · Linux"], "grey"),
    ]
    x0, x1, h, gap, y = 220, 1610, 170, 52, 40
    for i, (ln, k) in enumerate(layers):
        box(d, (x0, y, x1, y + h), ln, k, sz=36)
        if i < len(layers) - 1:
            arrow(d, ((x0 + x1) / 2, y + h + 4), ((x0 + x1) / 2, y + h + gap - 4))
        y += h + gap
    d.line([(1650, 40), (1680, 40), (1680, 40 + 2 * h + gap), (1650, 40 + 2 * h + gap)], fill=GREEN, width=5)
    label(d, (1790, 40 + h + gap / 2), "Python", 38, GREEN, bold=True)
    yc = 40 + 2 * (h + gap)
    d.line([(1650, yc), (1680, yc), (1680, yc + 2 * h + gap), (1650, yc + 2 * h + gap)], fill=BLUE, width=5)
    label(d, (1790, yc + h + gap / 2), "C++", 38, BLUE, bold=True)
    label(d, (110, 40 + h + gap / 2 - 10), "calls", 32, GREY)
    label(d, (110, 40 + h + gap / 2 + 34), "↓ ↑", 36, GREY)
    label(d, (110, 40 + h + gap / 2 + 80), "signals", 32, GREY)
    save(im, "f1_1_architecture.png")


# ------------------------------------------------------------------ 1.2 ----
def fig_1_2():
    W, H = 1980, 1500
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    groups = [
        ("Core", "green", ["QtCore", "QtGui", "QtWidgets"]),
        ("Data and documents", "blue", ["QtSql", "QtXml", "QtPrintSupport", "QtSvg · QtSvgWidgets"]),
        ("Network and devices", "blue", ["QtNetwork · QtWebSockets", "QtNetworkAuth*", "QtRemoteObjects · QtDBus",
                                         "QtSerialPort", "QtBluetooth · QtNfc"]),
        ("Multimedia and system", "teal", ["QtMultimedia(+Widgets)", "QtSpatialAudio", "QtTextToSpeech",
                                           "QtPositioning · QtSensors"]),
        ("2D/3D graphics", "orange", ["QtOpenGL(+Widgets)", "QtGraphs* · QtGraphsWidgets*", "QtQuick3D",
                                      "QtCharts* (deprecated)", "QtDataVisualization* (deprecated)",
                                      "Qt3D* (deprecated)"]),
        ("Web", "purple", ["QtWebEngineCore*", "QtWebEngineWidgets*", "QtWebEngineQuick*", "QtWebChannel"]),
        ("QML / Qt Quick", "purple", ["QtQml", "QtQuick", "QtQuickWidgets"]),
        ("Tools and quality", "grey", ["QtTest · QtDesigner · QtHelp", "QtStateMachine",
                                       "uic (pyuic6) · lupdate (pylupdate6)", "QAxContainer (Windows)"]),
    ]
    cols, cw, ch_, gx, gy, x_ini, y_ini = 3, 630, 450, 30, 35, 15, 15
    for i, (title, k, mods) in enumerate(groups):
        c, r = i % cols, i // cols
        x0 = x_ini + c * (cw + gx)
        y0 = y_ini + r * (ch_ + gy)
        d.rounded_rectangle((x0, y0, x0 + cw, y0 + ch_), radius=18, fill=PALE[k], outline=EDGE[k], width=4)
        d.rounded_rectangle((x0, y0, x0 + cw, y0 + 76), radius=18, fill=EDGE[k])
        d.rectangle((x0, y0 + 50, x0 + cw, y0 + 76), fill=EDGE[k])
        label(d, (x0 + cw / 2, y0 + 39), title, 34, (255, 255, 255), bold=True)
        yy = y0 + 112
        for m in mods:
            col = (150, 150, 150) if "deprecated" in m else (40, 40, 40)
            label(d, (x0 + 22, yy), m, 32, col, anchor="lm")
            yy += 55
    x0, y0 = x_ini + 2 * (cw + gx), y_ini + 2 * (ch_ + gy)
    d.rounded_rectangle((x0, y0, x0 + cw, y0 + ch_), radius=18, fill="white", outline=(190, 190, 190), width=3)
    for i, t in enumerate(["Legend", "* module of an add-on package", "   (installed separately with pip)",
                           "grey = deprecated in Qt 6", "   (avoid in new code)"]):
        label(d, (x0 + 26, y0 + 60 + i * 62), t, 34 if i == 0 else 31, NAVY if i == 0 else GREY,
              anchor="lm", bold=(i == 0))
    save(im, "f1_2_module_map.png")


# ------------------------------------------------------------------ 2.1 ----
def fig_2_1():
    lines = [
        "eng-calc/",
        "├── pyproject.toml            # metadata, dependencies, entry points",
        "├── README.md",
        "├── src/",
        "│   └── eng_calc/",
        "│       ├── __init__.py",
        "│       ├── __main__.py       # entry point: main()",
        "│       ├── app.py            # creates QApplication and the main window",
        "│       ├── ui/               # windows, dialogs and .ui files",
        "│       ├── models/           # data models (Model/View)",
        "│       ├── services/         # calculations and business rules (no Qt)",
        "│       └── resources/        # icons, .qss style sheets, translations",
        "├── tests/",
        "│   └── test_window.py        # tests (pytest-qt)",
        "└── docs/",
    ]
    f = font(34, mono=True)
    W, H = 1640, 60 + len(lines) * 54 + 40
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((10, 10, W - 10, H - 10), radius=18, fill=(248, 250, 252), outline=BLUE, width=4)
    y = 50
    for ln in lines:
        if "#" in ln:
            a, b = ln.split("#", 1)
            d.text((60, y), a, font=f, fill=(30, 30, 30))
            d.text((60 + d.textlength(a, font=f), y), "#" + b, font=f, fill=(0, 128, 0))
        else:
            d.text((60, y), ln, font=f, fill=NAVY if ln.endswith("/") else (30, 30, 30))
        y += 54
    assert max(d.textlength(ln, font=f) for ln in lines) + 60 < W - 20, "line wider than the figure"
    save(im, "f2_1_structure.png")


# ------------------------------------------------------------------ 4.2 ----
def fig_4_2():
    W, H = 2000, 1180
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    bw, bh, y0 = 600, 170, 30
    xs = [20, 700, 1380]
    top = [(["1. QApplication(sys.argv)", "one object per process"], "green"),
           (["2. Create widgets", "window, layouts, connections"], "blue"),
           (["3. window.show()", "schedules the display"], "blue")]
    for (ln, k), x in zip(top, xs):
        box(d, (x, y0, x + bw, y0 + bh), ln, k, sz=36)
    for i in range(2):
        arrow(d, (xs[i] + bw + 6, y0 + bh / 2), (xs[i + 1] - 6, y0 + bh / 2))
    cx, cy, r = 1000, 600, 210
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=ORANGE, width=8)
    label(d, (cx, cy - 30), "4. app.exec()", 42, ORANGE, bold=True)
    label(d, (cx, cy + 30), "event loop", 36, ORANGE)
    arrow(d, (xs[2] + bw / 2, y0 + bh + 6), (cx + 110, cy - r - 12))
    steps = [("waits for an event", (cx - r - 470, cy - 150)), ("dispatches to the object", (cx + r + 40, cy - 150)),
             ("runs handlers/slots", (cx + r + 40, cy + 80)), ("repaints the screen", (cx - r - 470, cy + 80))]
    for t, (x, y) in steps:
        d.rounded_rectangle((x, y, x + 430, y + 76), radius=14, fill=PALE["orange"], outline=ORANGE, width=3)
        sz = 34
        while d.textlength(t, font=font(sz)) > 400:
            sz -= 1
        label(d, (x + 215, y + 38), t, sz, (60, 60, 60))
    for ang in (-60, 30, 120, 210):
        a0, a1 = math.radians(ang), math.radians(ang + 25)
        arrow(d, (cx + r * math.cos(a0), cy + r * math.sin(a0)),
              (cx + r * math.cos(a1), cy + r * math.sin(a1)), ORANGE, width=6, head=30)
    yb = 970
    bottom = [(["5. quit() / last window", "the loop ends"], "grey"),
              (["6. aboutToQuit signal", "save the settings"], "grey"),
              (["7. sys.exit(code)", "exit code to the OS"], "green")]
    for (ln, k), x in zip(bottom, xs):
        box(d, (x, yb, x + bw, yb + bh), ln, k, sz=36)
    arrow(d, (cx - 110, cy + r + 8), (xs[0] + bw / 2, yb - 6))
    for i in range(2):
        arrow(d, (xs[i] + bw + 6, yb + bh / 2), (xs[i + 1] - 6, yb + bh / 2))
    save(im, "f4_2_lifecycle.png")


# ------------------------------------------------------------------ 5.1 ----
def fig_5_1():
    W, H = 2000, 900
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    root = (720, 30, 1280, 200)
    box(d, root, ["QWidget", "objectName = \"window\""], "green", sz=38)
    children = [(["QVBoxLayout", "mainLayout"], "grey"), (["QLineEdit", "flowField"], "blue"),
                (["QLineEdit", "pressureField"], "blue"), (["QPushButton", "calculateButton"], "blue")]
    bw, gap, y = 465, 25, 420
    x = (W - (4 * bw + 3 * gap)) / 2
    for ln, k in children:
        box(d, (x, y, x + bw, y + 160), ln, k, sz=38)
        arrow(d, ((root[0] + root[2]) / 2, root[3] + 6), (x + bw / 2, y - 6), width=4)
        x += bw + gap
    label(d, (360, 115), "child.parent() → parent", 34, GREY)
    label(d, (1640, 115), "parent.children() → children", 34, GREY)
    label(d, (W / 2, 670), "Destroying the parent automatically destroys all its children.", 38, NAVY)
    label(d, (W / 2, 740), "layout.addWidget(w) reparents w to the widget that owns the layout.", 34, GREY)
    label(d, (W / 2, 805), "Complex widgets have internal children (QLineEdit creates helper objects).", 34, GREY)
    save(im, "f5_1_tree.png")


# ------------------------------------------------------------------ 5.2 ----
def fig_5_2():
    W, H = 2000, 1000
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((20, 120, 660, 880), radius=20, fill=PALE["green"], outline=GREEN, width=4)
    label(d, (340, 180), "Sensor (emitter)", 40, NAVY, bold=True)
    for t, y in (("readingChanged(float)", 370), ("alarm(str, float)", 620)):
        d.rounded_rectangle((60, y - 55, 620, y + 55), radius=14, fill="white", outline=GREEN, width=3)
        label(d, (340, y), t, 36, (40, 40, 40))
    label(d, (340, 800), "self.alarm.emit(tag, v)", 32, GREY)
    targets = [(["Panel.display(v)", "method with @pyqtSlot"], 220, "blue"),
               (["lambda v: print(...)", "any callable"], 480, "blue"),
               (["Panel.log_alarm", "receives (str, float)"], 740, "orange")]
    for ln, y, k in targets:
        box(d, (1260, y - 95, 1980, y + 95), ln, k, sz=36)
    arrow(d, (622, 370), (1254, 220))
    arrow(d, (622, 370), (1254, 480))
    arrow(d, (622, 620), (1254, 740))
    for (x, y) in ((900, 255), (960, 470), (900, 625)):
        label(d, (x, y), "connect()", 32, GREY)
    label(d, (W / 2, 55), "A signal can have several receivers; a slot can receive several signals.", 36, NAVY)
    label(d, (W / 2, 945), "The emitter does not know its receivers: low coupling.", 34, GREY)
    save(im, "f5_2_signals.png")


# ----------------------------------------------------------------- 10.1 ----
def fig_10_1():
    W, H = 2000, 1000
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    l1 = [(["Operating system", "native event"], "grey"), (["Platform plugin", "converts it to a QEvent"], "orange"),
          (["Event queue", "event loop"], "orange"), (["QApplication.notify()", "delivers to the object"], "blue")]
    l2 = [(["Application filters", "app.installEventFilter"], "purple"),
          (["Object filters", "eventFilter()"], "purple"),
          (["QWidget.event()", "general dispatcher"], "blue"), (["Specific handler", "mousePressEvent()…"], "green")]
    bw, bh, gap = 460, 180, 40
    y1, y2 = 40, 450
    xs = [20 + i * (bw + gap) for i in range(4)]
    for (ln, k), x in zip(l1, xs):
        box(d, (x, y1, x + bw, y1 + bh), ln, k, sz=36)
    for (ln, k), x in zip(l2, xs):
        box(d, (x, y2, x + bw, y2 + bh), ln, k, sz=36)
    for i in range(3):
        arrow(d, (xs[i] + bw + 4, y1 + bh / 2), (xs[i + 1] - 4, y1 + bh / 2))
        arrow(d, (xs[i] + bw + 4, y2 + bh / 2), (xs[i + 1] - 4, y2 + bh / 2))
    arrow(d, (xs[3] + bw / 2, y1 + bh + 4), (xs[0] + bw / 2, y2 - 4))
    arrow(d, (xs[1] + bw / 2, y2 + bh + 4), (xs[1] + bw / 2, y2 + bh + 110), (192, 0, 0), dashed=True)
    label(d, (xs[1] + bw / 2, y2 + bh + 150), "returns True: event consumed", 33, (192, 0, 0))
    arrow(d, (xs[3] + bw / 2, y2 + bh + 4), (xs[3] + bw / 2, y2 + bh + 110), GREEN, dashed=True)
    label(d, (xs[3] + bw / 2 - 40, y2 + bh + 150), "ignore(): goes up to the parent", 33, GREEN)
    label(d, (W / 2, H - 45), "Ignored input events go up the widget tree until someone accepts them.", 35, NAVY)
    save(im, "f10_1_events.png")


# ----------------------------------------------------------------- 13.1 ----
def fig_13_1():
    W, H = 2000, 760
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    steps = [(["Source code", "self.tr(\"Pipe check\")"], "green"),
             (["pylupdate6", "extracts the texts"], "orange"),
             ([".ts file (XML)", "translations to fill in"], "blue"),
             (["Qt Linguist", "the translator fills it in"], "orange"),
             (["lrelease", "compiles"], "orange"),
             ([".qm file", "compact binary"], "blue")]
    bw, bh, gap = 600, 170, 70
    pos = [(30, 40), (700, 40), (1370, 40), (1370, 300), (700, 300), (30, 300)]
    for (ln, k), (x, y) in zip(steps, pos):
        box(d, (x, y, x + bw, y + bh), ln, k, sz=36)
    arrow(d, (630 + 4, 125), (700 - 4, 125))
    arrow(d, (1300 + 4, 125), (1370 - 4, 125))
    arrow(d, (1670, 210 + 4), (1670, 300 - 4))
    arrow(d, (1370 - 4, 385), (1300 + 4, 385))
    arrow(d, (700 - 4, 385), (630 + 4, 385))
    box(d, (30, 560, 1300, 720), ["QTranslator.load(\"app_pt_BR.qm\") + app.installTranslator()",
                                  "tr() now returns the translated text at run time"], "green", sz=34)
    arrow(d, (330, 470 + 4), (330, 560 - 4))
    box(d, (1370, 560, 1970, 720), ["qtbase_pt_BR.qm", "Qt's internal texts"], "grey", sz=34)
    arrow(d, (1370 - 4, 640), (1300 + 4, 640))
    save(im, "f13_1_translation.png")


# ----------------------------------------------------------------- 14.1 ----
def fig_14_1():
    W, H = 2000, 980
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    box(d, (20, 330, 380, 530), ["Data", "list, DB, DataFrame"], "grey", sz=38)
    box(d, (500, 330, 900, 530), ["Model", "QAbstractItemModel"], "green", sz=38)
    box(d, (1020, 330, 1440, 530), ["Proxy (optional)", "QSortFilterProxyModel"], "purple", sz=36)
    box(d, (1560, 330, 1980, 530), ["View", "QTableView / QTreeView"], "blue", sz=36)
    arrow(d, (384, 430), (496, 430))
    arrow(d, (904, 410), (1016, 410))
    arrow(d, (1016, 455), (904, 455))
    arrow(d, (1444, 410), (1556, 410))
    arrow(d, (1556, 455), (1444, 455))
    label(d, (960, 300), "data / signals", 28, GREY)
    label(d, (1500, 300), "indexes", 28, GREY)
    box(d, (1560, 40, 1980, 220), ["Delegate", "paints and edits cells"], "orange", sz=36)
    arrow(d, (1770, 224), (1770, 326))
    box(d, (1560, 690, 1980, 870), ["QItemSelectionModel", "selected items"], "teal", sz=34)
    arrow(d, (1770, 534), (1770, 686))
    box(d, (500, 690, 1440, 870), ["Model signals: dataChanged, rowsInserted,",
                                    "rowsRemoved, layoutChanged, modelReset"], "green", sz=34, title_bold=False)
    arrow(d, (700, 534), (700, 686), GREEN, dashed=True)
    label(d, (W / 2, 950), "A single data source can feed several views, each with its own proxy and delegate.",
          32, NAVY)
    save(im, "f14_1_modelview.png")


PART1_FIGS = (fig_1_1, fig_1_2, fig_2_1, fig_4_2, fig_5_1, fig_5_2, fig_10_1)
PART2_FIGS = (fig_13_1, fig_14_1)

if __name__ == "__main__":
    figs = PART1_FIGS + PART2_FIGS
    for fn in figs:
        fn()
    print("diagrams generated:", len(figs))
