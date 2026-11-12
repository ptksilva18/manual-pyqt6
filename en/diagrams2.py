# -*- coding: utf-8 -*-
"""Teaching diagrams of Parts III to V — English edition (helpers of ../diagrams.py, 2x)."""
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import diagrams as D  # noqa: E402  (helpers: box, arrow, label, save, colors)

D.FIG = os.path.join(HERE, "data", "figs")      # save() writes to en/data/figs
os.makedirs(D.FIG, exist_ok=True)
box, arrow, label, save = D.box, D.arrow, D.label, D.save
NAVY, BLUE, GREEN, ORANGE, GREY = D.NAVY, D.BLUE, D.GREEN, D.ORANGE, D.GREY


def fig_20_1():
    W, H = 2000, 1080
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((20, 20, 860, 980), 24, outline=BLUE, width=4)
    d.rounded_rectangle((1140, 20, 1980, 980), 24, outline=GREEN, width=4)
    label(d, (440, 66), "GUI thread (main)", 38, NAVY, bold=True)
    label(d, (1560, 66), "QThread (own event loop)", 38, GREEN, bold=True)
    box(d, (70, 130, 810, 310), ["Window / Controller", "creates QThread and worker; moveToThread()"], "blue")
    box(d, (70, 400, 810, 560), ["GUI slots", "on_progress, on_result, error → label"], "blue")
    box(d, (70, 650, 810, 810), ["requestInterruption()", "quit() + wait() on shutdown"], "orange")
    box(d, (1190, 130, 1930, 310), ["Worker (QObject)", "work(): loop with checks"], "green")
    box(d, (1190, 400, 1930, 560), ["Signals emitted", "progress, result, error, done"], "green")
    box(d, (1190, 650, 1930, 810), ["isInterruptionRequested()", "ends the loop safely"], "orange")
    arrow(d, (814, 220), (1186, 220))
    label(d, (1000, 186), "started → work", 28, GREY)
    arrow(d, (1186, 480), (814, 480), GREEN)
    label(d, (1000, 446), "queued connection", 28, GREEN)
    arrow(d, (814, 730), (1186, 730), ORANGE, dashed=True)
    label(d, (1000, 696), "stop request", 28, ORANGE)
    label(d, (W / 2, 900), "Event queue of the receiving thread", 30, GREY)
    label(d, (W / 2, 1040), "Golden rule: widgets are accessed only in the GUI thread; "
          "data crosses threads through signals.", 32, NAVY)
    save(im, "f20_1_worker.png")


def fig_21_1():
    W, H = 2000, 820
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    stages = [(["Instrument", "RS-232/485 or USB"], "grey"),
              (["QSerialPort", "readyRead (non-blocking)"], "blue"),
              (["Framing", "canReadLine + parse"], "green"),
              (["Model / buffer", "deque or numpy"], "purple"),
              (["Real-time chart", "pyqtgraph / QtGraphs"], "orange")]
    x, w, g = 20, 330, 72
    for i, (txt, kind) in enumerate(stages):
        box(d, (x, 230, x + w, 450), txt, kind, sz=27)
        if i:
            arrow(d, (x - g + 4, 340), (x - 4, 340))
        x += w + g
    d.rounded_rectangle((398, 140, 1178, 520), 26, outline=BLUE, width=3)
    label(d, (788, 110), "acquisition thread (optional, for high rates)", 28, BLUE)
    label(d, (1400, 610), "sample(seq, p, T) signal — queued connection", 28, GREEN)
    arrow(d, (1180, 565), (1620, 565), GREEN, dashed=True)
    label(d, (W / 2, 740), "Acquisition never blocks the interface; port errors arrive through "
          "errorOccurred.", 32, NAVY)
    save(im, "f21_1_serial.png")


def fig_24_1():
    W, H = 2000, 900
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((20, 40, 900, 760), 24, outline=BLUE, width=4)
    d.rounded_rectangle((1100, 40, 1980, 760), 24, outline=ORANGE, width=4)
    label(d, (460, 86), "Python process (PyQt6)", 36, NAVY, bold=True)
    label(d, (1540, 86), "Web page (Chromium)", 36, ORANGE, bold=True)
    box(d, (70, 150, 850, 330), ["Python QObject", "pyqtProperty, pyqtSlot, pyqtSignal"], "green")
    box(d, (70, 430, 850, 600), ["QWebChannel", "registerObject(\"bridge\", obj)"], "blue")
    box(d, (1150, 150, 1930, 330), ["Page JavaScript", "bridge.pressure(z, callback)"], "orange")
    box(d, (1150, 430, 1930, 600), ["qwebchannel.js", "new QWebChannel(qt.webChannelTransport, …)"],
        "orange", sz=30)
    arrow(d, (460, 334), (460, 426))
    arrow(d, (1540, 426), (1540, 334))
    arrow(d, (854, 490), (1146, 490))
    arrow(d, (1146, 545), (854, 545))
    label(d, (1000, 456), "JSON messages", 28, GREY)
    label(d, (1000, 640), "QWebEnginePage.setWebChannel()", 28, GREY)
    label(d, (W / 2, 840), "Slot calls are asynchronous in JavaScript: the result arrives "
          "through a callback.", 32, NAVY)
    save(im, "f24_1_webchannel.png")


def fig_27_1():
    W, H = 2000, 1180
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    layers = [(["Presentation — Views", "widgets, .ui files, QML; no business rules"], "blue"),
              (["Presenters / ViewModels", "screen state, commands, input validation"], "teal"),
              (["Application services", "use cases, orchestration, threads, undo"], "green"),
              (["Domain", "pure entities and calculations in Python (no Qt)"], "orange"),
              (["Infrastructure", "files, database, network, instruments"], "grey")]
    y = 30
    for i, (txt, kind) in enumerate(layers):
        box(d, (260, y, 1740, y + 170), txt, kind, sz=36)
        if i:
            arrow(d, (1000, y - 50), (1000, y - 4))
        y += 220
    label(d, (130, 560), "depends on ↓", 30, GREY)
    label(d, (1870, 560), "testable", 30, GREEN)
    label(d, (1870, 600), "headless", 30, GREEN)
    label(d, (W / 2, 1140), "Dependencies point inward: the domain neither imports PyQt6 "
          "nor knows the interface.", 32, NAVY)
    save(im, "f27_1_layers.png")


def fig_31_1():
    W, H = 2000, 1240
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    box(d, (40, 40, 1960, 220), ["window.py — MainWindow (QMainWindow)",
                                 "actions, QTableView, QTabWidget, pyqtgraph, QDockWidget, QSettings"],
        "blue", sz=34)
    box(d, (40, 300, 620, 480), ["models.py", "TestListModel, ReadingsModel"], "teal", sz=32)
    box(d, (710, 300, 1290, 480), ["services.py", "AnalysisService (QThreadPool)"], "green", sz=32)
    box(d, (1380, 300, 1960, 480), ["report.py", "QTextDocument → QPdfWriter"], "green", sz=32)
    box(d, (700, 580, 1600, 760), ["domain.py — Reading, Criterion, Result, analyze()",
                                   "pure Python: regression, thermal compensation, acceptance"],
        "orange", sz=34)
    box(d, (40, 860, 620, 1040), ["repository.py", "SQLite (sqlite3)"], "grey", sz=32)
    box(d, (710, 860, 1290, 1040), ["csv_import.py", "CSV (; or , and decimal comma)"], "grey",
        sz=30)
    box(d, (1380, 860, 1960, 1040), ["app.py", "composition, self-test, QStandardPaths"], "purple",
        sz=30)
    for x in (330, 1000, 1670):
        arrow(d, (x, 224), (x, 296))
    arrow(d, (1000, 484), (1000, 576))
    arrow(d, (1670, 484), (1500, 576))
    arrow(d, (665, 224), (560, 856), GREY, dashed=True)
    arrow(d, (1000, 224), (1000, 296))
    arrow(d, (900, 856), (900, 764))
    arrow(d, (520, 484), (720, 600))
    arrow(d, (540, 856), (760, 764))
    d.line([(1960, 950), (1985, 950), (1985, 130)], fill=BLUE, width=4)
    arrow(d, (1985, 130), (1964, 130), BLUE)
    label(d, (W / 2, 1150), "Arrows: main dependencies (who imports whom). The domain does not import "
          "PyQt6; app.py composes everything.", 32, NAVY)
    save(im, "f31_1_capstone.png")


PART34_FIGS = (fig_20_1, fig_21_1, fig_24_1, fig_27_1, fig_31_1)

if __name__ == "__main__":
    for fn in PART34_FIGS:
        fn()
    print("diagrams (Parts III to V) generated:", len(PART34_FIGS))
