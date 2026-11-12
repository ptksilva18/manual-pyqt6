# -*- coding: utf-8 -*-
"""Opening texts (Preface), structure of the Annexes and catalog groups — English edition."""
from blocks import bl, flat, p  # noqa: F401

FRONT_UNNUMBERED = flat(
    dict(k="hu", t="Preface — How to use this manual"),
    p("This manual takes the reader from the first `import` to the packaging of a professional desktop application "
      "written in Python with PyQt6. The text is progressive: each chapter depends only on the previous ones, and "
      "each Part ends with exercises and an increment of the capstone project."),
    p("Reference versions: **Python ≥ 3.10**, **PyQt6 6.12.0** and **Qt 6.12 (LTS)**. The names of modules and "
      "classes cited in this manual were checked by introspection of the official PyQt6 6.12.0 wheels (PyPI) for "
      "Linux, Windows and macOS."),
    p("**How the code was verified.** Every Python listing marked with ✔ was run with Python 3.13, PyQt6 6.12.0 and "
      "Qt 6.12.0 on Linux, without human interaction: the interface ran on Qt's `offscreen` platform or, when "
      "OpenGL, Vulkan or Qt Quick 3D were involved, under a virtual X server with software rendering. The "
      "\"Output\" blocks reproduce the real output of those runs — times and performance figures vary from machine "
      "to machine. Unexpected behaviors found during the tests are recorded in WARNING boxes, together with the "
      "solution adopted. Listings that require another platform (Windows) are marked with ⚠."),
    p("**About this edition.** This is the English edition of the manual, originally written in Brazilian "
      "Portuguese. The code was localized as well — names, comments, messages and outputs — and every listing was "
      "run again in its English form; the screenshots and diagrams were regenerated from the English code."),
    bl("**Part I — Fundamentals** (Basic level): environment, Python for GUIs, QObject, signals/slots, widgets, "
       "layouts, main window, dialogs and events.",
       "**Part II — Professional interface** (Intermediate level): Qt Designer, styles, resources, Model/View, "
       "databases, files, 2D painting, Graphics View and animation.",
       "**Part III — Advanced development** (Advanced level): concurrency, networking, data visualization, "
       "multimedia, Web, 3D and QML.",
       "**Part IV — Quality, architecture and distribution** (Advanced level): architecture, testing, performance, "
       "accessibility and packaging.",
       "**Part V — Capstone project**: a complete technical application, built end to end.",
       "**Annexes**: complete catalog of PyQt6 6.12 classes, quick references, tools and glossary."),
)

import annex_b as AB  # noqa: E402
import part2_anexos as PA  # noqa: E402

ANNEXES = flat(
    dict(k="ha", lvl=1, t="Catalog of PyQt6 6.12 classes by module"),
    p("This annex was generated automatically by introspection of the stub files (`.pyi`) of the official wheels "
      "PyQt6 6.12.0, PyQt6-Charts 6.12.0, PyQt6-Graphs 6.12.0, PyQt6-DataVisualization 6.12.0, PyQt6-3D 6.12.0, "
      "PyQt6-NetworkAuth 6.12.0 and PyQt6-WebEngine 6.140.0. It lists the module-level classes — including "
      "namespaces (for example, `Qt`) and enums declared at module level — and the module-level functions. Nested "
      "classes and enums internal to classes are not listed separately. The QAxContainer module was extracted from "
      "the Windows wheel."),
    dict(k="catalog"),
    dict(k="ha", lvl=1, t="Quick reference of the Qt namespace and frequent enums"),
    AB.ANNEX_B,
    dict(k="ha", lvl=1, t="Quick reference of Qt Style Sheets"),
    PA.ANEXO_C,
    dict(k="ha", lvl=1, t="Command-line tools"),
    PA.ANEXO_D,
)

CATALOG_GROUPS = [
    ("PyQt6 — core", ["QtCore", "QtGui", "QtWidgets", "QtBluetooth", "QtDBus", "QtDesigner", "QtHelp",
                      "QtMultimedia", "QtMultimediaWidgets", "QtNetwork", "QtNfc", "QtOpenGL", "QtOpenGLWidgets",
                      "QtPositioning", "QtPrintSupport", "QtQml", "QtQuick", "QtQuick3D", "QtQuickWidgets",
                      "QtRemoteObjects", "QtSensors", "QtSerialPort", "QtSpatialAudio", "QtSql", "QtStateMachine",
                      "QtSvg", "QtSvgWidgets", "QtTest", "QtTextToSpeech", "QtWebChannel", "QtWebSockets", "QtXml",
                      "QAxContainer"]),
    ("PyQt6-Charts", ["QtCharts"]),
    ("PyQt6-Graphs", ["QtGraphs", "QtGraphsWidgets"]),
    ("PyQt6-DataVisualization", ["QtDataVisualization"]),
    ("PyQt6-3D", ["Qt3DCore", "Qt3DRender", "Qt3DExtras", "Qt3DInput", "Qt3DLogic", "Qt3DAnimation"]),
    ("PyQt6-NetworkAuth", ["QtNetworkAuth"]),
    ("PyQt6-WebEngine", ["QtWebEngineCore", "QtWebEngineWidgets", "QtWebEngineQuick"]),
]
