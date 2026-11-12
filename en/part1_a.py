# -*- coding: utf-8 -*-
"""Part I — Chapters 1 to 3 (English edition)."""
from blocks import (ST_BAS, bl, ch, code, fig, flat, h2, h3, h4, img, lst, nl, note, out, p, part,
                    snip, tab)
import outline_data as D

CAP01 = flat(
    ch("Introduction to PyQt6 and the Qt ecosystem", ST_BAS, [
        "Understand what Qt and PyQt6 are and how the bindings work.",
        "Know the complete map of PyQt6 6.12 modules and the status of each one.",
        "Identify the practical differences between PyQt5, PyQt6 and PySide6.",
    ]),
    h2("Purpose and audience of the manual"),
    p("This manual teaches how to build **professional desktop applications** in Python using PyQt6. The starting "
      "point is zero: no previous experience with graphical interfaces is required, only basic programming "
      "knowledge. The end point is a complete application — with a main window, data persistence, charts, "
      "background processing, automated tests and an installer — built with the same practices used in everyday "
      "engineering tools."),
    p("The audience includes engineers, scientists and analysts who already write Python scripts and need to "
      "turn them into tools with a graphical interface that other people can use, as well as developers coming "
      "from other toolkits (Tkinter, wxPython, PyQt5) who want to master PyQt6 in depth."),
    p("Three principles guide the text:"),
    bl("**Verifiable accuracy**: every listing marked with ✔ was run with PyQt6 6.12.0 and Qt 6.12.0; the outputs "
       "shown in the *Output* blocks are the real outputs of those runs, and the figures showing windows are "
       "screenshots of the listings themselves.",
       "**No gaps in the progression**: every concept is introduced before it is used and revisited in richer "
       "contexts in the following chapters.",
       "**Professional practice from the start**: project structure, type hints, error handling and separation "
       "between interface and logic already appear in Part I, not as an appendix."),

    h2("Organization of the manual"),
    p("The manual is divided into five Parts, each corresponding to a level of depth, followed by reference "
      "annexes. Each chapter opens with a box of objectives and ends with exercises."),
    h3("Parts, levels and learning paths"),
    tab("Parts of the manual and reading paths", ["Part", "Level", "Prerequisite", "For whom"],
        [["I — Fundamentals (Ch. 1–10)", "Basic", "Basic Python", "All readers, in sequence"],
         ["II — Professional interface (Ch. 11–19)", "Intermediate", "Part I", "Those who will build real applications"],
         ["III — Advanced development (Ch. 20–26)", "Advanced", "Parts I and II", "Pick the chapters according to the project"],
         ["IV — Quality and distribution (Ch. 27–30)", "Advanced", "Parts I and II", "Those who will maintain and distribute software"],
         ["V — Capstone project (Ch. 31)", "Consolidation", "Parts I to IV", "Hands-on review of all the content"]],
        [3171, 1500, 1700, 2700]),
    p("The **minimum path** to produce a useful tool is: Chapters 1 to 10, 11 (Qt Designer), 14 (Model/View), "
      "20 (concurrency) and 30 (packaging). The **complete path** goes through all chapters in order."),
    h3("Cross-cutting capstone project"),
    p("Throughout the manual, the examples converge on a single technical application — an engineering calculator "
      "with a test log. In Part I it takes shape: a minimal window (Chapter 4), forms with validation (Chapters 6 "
      "and 7), a main window with menus, panels and state persistence (Chapter 8), data-entry dialogs (Chapter 9) "
      "and event handling (Chapter 10). The following Parts add a database, charts, threads, tests and an "
      "installer, culminating in Chapter 31."),
    h3("Typographic and code conventions"),
    p("The conventions below are used throughout the document."),
    tab("Typographic conventions adopted in the manual", ["Element", "Formatting", "Use"], D.CONVENTIONS, [2600, 2900, 3571]),
    note("NOTE", "NOTE boxes bring complementary information that does not interrupt the main line of reasoning."),
    note("TIP", "TIP boxes bring good practices and productivity shortcuts."),
    note("WARNING", "WARNING boxes alert to common mistakes, memory pitfalls and portability problems."),
    p("In the listings, colors follow the pattern of modern editors: keywords in blue, *strings* in dark red, "
      "comments in green and numbers in teal. Short snippets without a caption are illustrative fragments; "
      "complete programs receive a numbered caption (Listing N.M)."),

    h2("What Qt and PyQt6 are"),
    p("**Qt** is a cross-platform framework written in C++ for building applications with a graphical interface "
      "and also services without one. It offers widgets, 2D and 3D graphics, networking, databases, multimedia, "
      "internationalization, threads and much more, with the same source code on Windows, macOS and Linux. "
      "**PyQt6** is the set of *bindings* that exposes this API to Python: each Qt C++ class appears as a Python "
      "class with the same method names."),
    h3("Brief history: Qt, PyQt4, PyQt5, PyQt6 and PySide6"),
    p("Qt had its first public release in 1995, created by the Norwegian company Trolltech; since then it passed "
      "through Nokia and is now developed by The Qt Company, with contributions from the Qt Project community. "
      "Riverbank Computing has published PyQt since 1998, following the major Qt generations: PyQt4 (Qt 4), PyQt5 "
      "(Qt 5) and PyQt6 (Qt 6). Qt 6.0 was released in December 2020, and PyQt6 followed it."),
    p("In parallel there is **PySide**, started by Nokia in 2009 and now maintained by The Qt Company itself under "
      "the official name *Qt for Python* (package **PySide6** for Qt 6). PyQt6 and PySide6 cover essentially the "
      "same Qt API; the differences lie in licensing and in some naming details, discussed in Section 1.3.4."),
    h3("Architecture of the bindings: SIP, PyQt6-sip and PyQt6-Qt6"),
    p("The PyQt6 modules are compiled extensions (`.pyd` files on Windows and `.so` on Linux/macOS) generated by "
      "the **SIP** tool, also from Riverbank. Running `pip install PyQt6` installs three packages: **PyQt6** (the "
      "extension modules and the `pyuic6` and `pylupdate6` tools), **PyQt6-sip** (the support module `PyQt6.sip`, "
      "which manages the correspondence between Python and C++ objects) and **PyQt6-Qt6** (the compiled Qt "
      "libraries, including the platform plugins). There is no need to install Qt separately."),
    img("Layered architecture of a PyQt6 application", "f1_1_architecture.png"),
    p("Figure 1.1 shows the run-time flow: Python code calls methods of the bindings, which call the C++ "
      "libraries; in the opposite direction, operating-system events reach Qt through the **platform plugin** and "
      "come back to Python as calls to overridden methods and to *slots* connected to signals."),
    note("NOTE", "Every Qt object created in Python has two parts: the Python *wrapper* and the C++ object. "
                 "Chapter 5 shows why this duality matters for memory management."),
    h3("Licensing: GPL v3, commercial license and distribution implications"),
    p("PyQt6 is distributed under **two licenses**: GPL v3 and a commercial license sold by Riverbank Computing. "
      "Under the GPL v3, whoever **distributes** an application that uses PyQt6 must also distribute it under a "
      "GPL-compatible license, making the source code available to the recipients. Internal use without "
      "distribution to third parties does not trigger this distribution obligation. Proprietary software that is "
      "distributed requires the commercial PyQt6 license."),
    p("PySide6, in turn, is available under LGPL v3 (as well as GPL and a commercial license), which allows "
      "proprietary applications as long as the LGPL conditions are respected. The topic is revisited in Chapter 30, "
      "in the context of packaging."),
    note("IMPORTANT", "This manual is not legal advice. Before distributing software, read the license texts and, "
                      "if necessary, consult your organization's legal department."),
    h3("PyQt6 versus PySide6"),
    h4("API differences: pyqtSignal/Signal, pyqtSlot/Slot, pyqtProperty/Property"),
    p("Most code is identical between the two bindings; changing the imported package is enough. The most frequent "
      "differences are summarized below."),
    tab("Frequent differences between PyQt6 and PySide6", ["Feature", "PyQt6", "PySide6"],
        [["Signal declaration", "`pyqtSignal(...)`", "`Signal(...)`"],
         ["Slot decorator", "`@pyqtSlot(...)`", "`@Slot(...)`"],
         ["Qt property", "`pyqtProperty(...)`", "`Property(...)`"],
         ["Loading .ui at run time", "`uic.loadUi()`", "`QUiLoader` (QtUiTools module)"],
         ["Code generator from .ui", "`pyuic6`", "`pyside6-uic`"],
         ["Resource compiler (.qrc)", "Not included", "`pyside6-rcc`"],
         ["Licenses", "GPL v3 or commercial", "LGPL v3, GPL or commercial"],
         ["Maintainer", "Riverbank Computing", "The Qt Company"]],
        [2900, 2900, 3271]),
    h4("Selection criteria for professional projects"),
    p("Technically, both are mature and follow the Qt releases. The choice is usually decided by three factors: "
      "(1) **license** — distributing proprietary software favors PySide6 (LGPL) or the commercial PyQt6 license; "
      "(2) **existing code base** — projects and teams already using PyQt5 migrate to PyQt6 with less friction; "
      "(3) **ecosystem** — third-party libraries sometimes support only one of the bindings. This manual uses PyQt6, "
      "but the concepts apply fully to PySide6."),

    h2("Map of PyQt6 6.12 modules"),
    p("The following table lists all extension modules distributed in the official wheels of PyQt6 6.12.0 and of "
      "the add-on packages, with the `pip` package that provides them and the status of each module in Qt 6.12. "
      "The chapters shown in the last column cover each module."),
    tab("PyQt6 6.12 modules and add-on packages", ["Module", "pip package", "Purpose", "Status", "Ch."],
        D.MODULE_ROWS, [2050, 1500, 3021, 1800, 700], font=16),
    note("NOTE", "QtPdf and QtPdfWidgets appear in Riverbank's module documentation, but they are not present in the "
                 "PyQt6 6.12.0 or PyQt6-WebEngine 6.140.0 wheels published on PyPI (verified for Linux, Windows and "
                 "macOS). The topic is covered in Chapter 24 with this caveat."),
    img("Map of PyQt6 modules grouped by domain", "f1_2_module_map.png"),
    p("In practice, nearly all desktop applications use only three modules — **QtCore**, **QtGui** and "
      "**QtWidgets** —, which are the focus of Part I. The others are added as the project needs them."),

    h2("Main changes from PyQt5 to PyQt6"),
    p("Those coming from PyQt5 will find the same architecture, but with changes that break source-code "
      "compatibility. The table summarizes the most frequent ones."),
    tab("Main differences between PyQt5 and PyQt6", ["Topic", "PyQt5", "PyQt6"], D.PYQT5_TO_6, [1900, 2900, 4271], font=17),
    h3("Mandatory scoped enums"),
    p("In PyQt6, Qt enums are Python enums (`enum.Enum` and `enum.Flag`) and must be written with their full name: "
      "the name of the enum is part of the path. The PyQt5 shortcut no longer exists."),
    snip('''from PyQt6.QtCore import Qt

label.setAlignment(Qt.AlignmentFlag.AlignCenter)           # PyQt6
# label.setAlignment(Qt.AlignCenter)               # PyQt5: AttributeError in PyQt6
button = Qt.MouseButton.LeftButton
flags = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter   # Flag combination'''),
    note("TIP", "To find the name of the enum, look at the method signature in the stubs (`.pyi`) installed with "
                "PyQt6 — the editor shows the expected type, for example `Qt.AlignmentFlag`."),
    h3("exec() instead of exec_()"),
    p("Since `exec` is no longer a reserved word in Python 3, PyQt6 removed the `exec_()` aliases. Use "
      "`app.exec()`, `dialog.exec()` and `menu.exec(...)`."),
    h3("Classes relocated between modules"),
    p("In Qt 6, some classes that do not depend on widgets moved from QtWidgets to QtGui: `QAction`, "
      "`QActionGroup`, `QShortcut`, `QUndoCommand`, `QUndoStack`, `QUndoGroup` and `QFileSystemModel`. Likewise, "
      "`QOpenGLWidget` moved to QtOpenGLWidgets and `QSvgWidget` to QtSvgWidgets. The typical symptom in migrated "
      "code is an `ImportError` on the import line."),
    h3("Removed APIs and their replacements"),
    bl("`QDesktopWidget` → `QScreen`, obtained with `QGuiApplication.primaryScreen()` or `screens()`.",
       "`QRegExp` → `QRegularExpression` (and `QRegExpValidator` → `QRegularExpressionValidator`).",
       "`QFontMetrics.width()` → `QFontMetrics.horizontalAdvance()`.",
       "`event.pos()` in mouse events still exists but is obsolete: prefer `event.position()`, which returns "
       "`QPointF`.",
       "High-DPI attributes (`AA_EnableHighDpiScaling`) are no longer needed: scaling is always on.",
       "`pyrcc5` has no equivalent in PyQt6; resources are covered in Chapter 13."),

    h2("Chapter exercises"),
    nl("List the three packages installed by `pip install PyQt6` and explain the role of each one.",
       "Under which conditions does the GPL v3 require the source code of a PyQt6 application to be made available?",
       "Rewrite for PyQt6: `label.setAlignment(Qt.AlignRight | Qt.AlignTop)` and `app.exec_()`.",
       "Using Table 1.5, identify the module that provides `QAction` in PyQt6 and explain the reason for the change.",
       "Look at Table 1.4 and state which modules you would use for an application that reads a serial port, "
       "stores the data in SQLite and plots 2D charts."),
)

CAP02 = flat(
    ch("Setting up the development environment", ST_BAS, [
        "Install Python, PyQt6 and add-ons in an isolated virtual environment.",
        "Configure the IDE, type checking and Qt Designer.",
        "Organize a project with a professional structure and pyproject.toml.",
    ]),
    h2("System requirements"),
    h3("Supported Python versions (PyQt6 6.12 requires Python ≥ 3.10)"),
    p("PyQt6 6.12.0 declares `Requires-Python >= 3.10`. The wheels are of the **abi3** type (stable CPython ABI): "
      "a single wheel serves every Python version from 3.10 onwards, without recompilation. Preferably use a recent, "
      "supported version of Python 3 (the examples in this manual were run with Python 3.13)."),
    h3("Platforms: Windows, Linux and macOS"),
    tab("PyQt6 6.12.0 wheels published on PyPI", ["System", "Architecture", "Minimum requirement of the wheel"],
        [["Windows", "x86-64 (win_amd64)", "64-bit Windows supported by Qt 6.12"],
         ["Windows", "ARM64 (win_arm64)", "Windows on ARM"],
         ["Linux", "x86-64", "glibc ≥ 2.34 (manylinux_2_34 tag)"],
         ["Linux", "ARM64 (aarch64)", "glibc ≥ 2.39 (manylinux_2_39 tag)"],
         ["macOS", "universal2 (Intel and Apple Silicon)", "macOS 14 or later (macosx_14_0 tag)"]],
        [1700, 3200, 4171]),
    p("On platforms without a compatible wheel, `pip` tries to build from source, which requires Qt to be installed "
      "and a compiler — a scenario to be avoided in ordinary projects."),
    note("WARNING", "On minimal Linux distributions, the application may fail to open with the message *Could not "
                    "load the Qt platform plugin \"xcb\"*. Since Qt 6.5, the xcb plugin requires the **xcb-cursor** "
                    "library (package `libxcb-cursor0` on Debian/Ubuntu). Run with the environment variable "
                    "`QT_DEBUG_PLUGINS=1` to see which dependency is missing."),

    h2("Virtual environments and package management"),
    p("A **virtual environment** (venv) is an isolated copy of the interpreter with its own package directory. "
      "Every project should have its own: this way, different PyQt6 versions coexist on the same machine and the "
      "project declares exactly what it depends on."),
    h3("Creating and activating a venv"),
    h4("Windows (PowerShell and cmd)"),
    snip('''# PowerShell, in the project folder
py -3.13 -m venv .venv
.venv\\Scripts\\Activate.ps1          # the prompt now shows (.venv)

# cmd.exe
.venv\\Scripts\\activate.bat

deactivate                            # leaves the virtual environment''', lang="text"),
    note("TIP", "If PowerShell refuses activation because of the execution policy, allow local scripts for your "
                "user with `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`."),
    h4("Linux and macOS"),
    snip('''python3 -m venv .venv                 # Debian/Ubuntu: requires the python3-venv package
source .venv/bin/activate
python -c "import sys; print(sys.prefix)"   # must point to .../.venv''', lang="text"),
    h3("Installing PyQt6 and the add-on packages"),
    snip('''python -m pip install --upgrade pip
python -m pip install PyQt6                       # core + other standard modules
python -m pip install PyQt6-Charts PyQt6-Graphs   # add-ons: install only what you need
python -m pip install PyQt6-WebEngine''', lang="text"),
    tab("PyQt6 packages distributed by Riverbank Computing on PyPI",
        ["pip package", "Modules provided", "Verified version"],
        [["PyQt6", "Core: 32 modules (+ QAxContainer on Windows), uic, lupdate, sip", "6.12.0"],
         ["PyQt6-Charts", "QtCharts", "6.12.0"],
         ["PyQt6-Graphs", "QtGraphs, QtGraphsWidgets", "6.12.0"],
         ["PyQt6-DataVisualization", "QtDataVisualization", "6.12.0"],
         ["PyQt6-3D", "Qt3DAnimation, Qt3DCore, Qt3DExtras, Qt3DInput, Qt3DLogic, Qt3DRender", "6.12.0"],
         ["PyQt6-NetworkAuth", "QtNetworkAuth", "6.12.0"],
         ["PyQt6-WebEngine", "QtWebEngineCore, QtWebEngineQuick, QtWebEngineWidgets", "6.140.0"]],
        [2400, 4971, 1700]),
    note("NOTE", "Always use `python -m pip` instead of `pip`: it guarantees that the package is installed in the "
                 "active interpreter (the venv's), and not in another Python that comes first in the PATH."),
    h3("Pinning versions and reproducibility (requirements.txt, pip freeze, lock files)"),
    p("PyQt6 6.12.0 depends on `PyQt6-Qt6 >= 6.12.0, < 6.13.0` and on `PyQt6-sip >= 13.13, < 14`: the bindings "
      "package and the package with the Qt libraries must have the same *minor* version. So that all developers and "
      "the continuous-integration server use exactly the same environment, record the versions:"),
    snip('''python -m pip freeze > requirements.txt     # records the exact versions of this venv
python -m pip install -r requirements.txt    # reproduces the venv on another machine

# typical excerpt of requirements.txt
PyQt6==6.12.0
PyQt6-Qt6==6.12.0
PyQt6-sip==13.13.0''', lang="text"),
    p("Lock tools (for example, `pip-tools`, `uv` or `poetry`) automate this process and also record file "
      "*hashes*, which strengthens supply-chain security."),

    h2("Development tools"),
    h3("Configuring VS Code and PyCharm"),
    p("In **VS Code**, install the Python extension (Microsoft) and select the venv interpreter with the command "
      "*Python: Select Interpreter*; debugging then uses that environment. In **PyCharm**, set the interpreter in "
      "*Settings → Project → Python Interpreter* pointing to `.venv`. In both, check that autocompletion shows the "
      "methods of `QWidget` — a sign that the PyQt6 stubs were found."),
    h3("Type hints and PyQt6 .pyi files (mypy and pyright)"),
    p("PyQt6 installs stub files (`QtCore.pyi`, `QtWidgets.pyi` etc.) and the `py.typed` marker. This enables static "
      "type checking with `mypy` or `pyright` and precise autocompletion, including enum names. Annotating your own "
      "classes (`def __init__(self, parent: QWidget | None = None) -> None`) takes advantage of this and documents "
      "the intent of the code."),
    h3("Obtaining and running Qt Designer"),
    p("**Qt Designer** — the visual form editor used in Chapter 11 — is not part of the PyQt6 wheels. The most "
      "common alternatives are: (1) the official Qt installer, which includes Qt Designer and Qt Creator; (2) the "
      "Linux distribution packages; (3) the `pyside6-designer` executable that comes with the PySide6 package — "
      "install it in a separate venv so as not to mix the bindings. The `.ui` files produced are plain XML and do "
      "not depend on the binding that will load them."),

    h2("Verifying the installation"),
    p("The following script confirms the PyQt6 and Qt versions and checks which add-on packages are present."),
    lst("c02_check.py", "Script that verifies the installation of PyQt6 and the add-ons"),
    out("c02_check"),
    p("`PYQT_VERSION_STR` is the version of the bindings; `QT_VERSION_STR` is the Qt version at run time, and "
      "`QLibraryInfo.version()` is the Qt version the bindings were built against. A mismatch between them "
      "indicates a mix of packages of different versions."),

    h2("Professional project structure"),
    h3("Directory layout (src layout)"),
    img("Recommended directory structure for a PyQt6 project", "f2_1_structure.png"),
    p("The **src layout** puts the package inside `src/`, which forces the tests to import the installed package "
      "(and not loose files in the folder), revealing packaging problems early. The split into `ui/`, `models/` and "
      "`services/` anticipates the architecture of Chapter 27: calculations in `services/` do not import Qt and can "
      "be tested and reused independently of the interface."),
    h3("The pyproject.toml file"),
    lst("c02_pyproject.toml", "pyproject.toml template for a PyQt6 application", lang="toml"),
    p("The `[project.gui-scripts]` section creates, at installation, an `eng-calc` executable that calls the "
      "`main()` function of the `eng_calc.__main__` module; on Windows, *gui* scripts start without opening a "
      "console window. With the project installed in editable mode (`python -m pip install -e .[dev]`), changes to "
      "the code take effect immediately. The template in Listing 2.2 was validated by building a wheel with "
      "`pip wheel`."),
    snip('''# src/eng_calc/__main__.py
import sys


def main() -> int:
    from eng_calc.app import run                   # deferred import
    return run(sys.argv)


if __name__ == "__main__":                         # allows: python -m eng_calc
    sys.exit(main())'''),

    h2("Chapter exercises"),
    nl("Create a venv, install PyQt6 and run Listing 2.1. Write down the versions shown.",
       "Generate the `requirements.txt` of your environment and explain why `PyQt6` and `PyQt6-Qt6` must have the "
       "same minor version.",
       "Build the structure of Figure 2.1 with the `pyproject.toml` of Listing 2.2 and install it with "
       "`pip install -e .`.",
       "Configure `mypy` in the project and check a file that calls `QLabel.setAlignment` with an invalid argument."),
)

CAP03 = flat(
    ch("Essential Python for interface programming", ST_BAS, [
        "Review the Python features most used in PyQt6 code.",
        "Master classes, inheritance, callables and decorators in the GUI context.",
        "Apply type hints, dataclasses and enum in interface code.",
    ]),
    p("This chapter is not a Python course: it reviews, with PyQt6 examples, the language features that appear in "
      "practically every graphical application. Those who already master object orientation can read only "
      "sections 3.1.3, 3.2 and 3.5, which deal with PyQt particularities."),
    h2("Object-oriented programming"),
    h3("Classes, instances and the __init__ method"),
    p("In PyQt6, practically every window is a **class** that inherits from a Qt widget. The `__init__` method "
      "builds the interface (creates widgets, layouts and connections) and stores in attributes (`self.field`, "
      "`self.button`) the widgets that will need to be accessed later. Widgets used only during construction can "
      "stay in local variables, because Qt keeps them alive through the parent–child relationship (Chapter 5)."),
    h3("Inheritance and super() in widget subclasses"),
    p("When inheriting from a Qt class, call `super().__init__(...)` **before** using any feature of the base "
      "class: this call is what creates the C++ object. By convention, the last parameter of the constructor is "
      "`parent`, passed on to the base."),
    lst("c03_inheritance.py", "Inheritance and super(): a QWidget subclass with its own parameters"),
    out("c03_inheritance"),
    p("The method resolution order (MRO) shows the chain: `ResultPanel → TitledPanel → QWidget → QObject`. Qt "
      "methods can be overridden like any Python method — this is how events are handled in Chapter 10."),
    h3("Multiple inheritance, mixins and restrictions with QObject"),
    p("A Python class can inherit from **only one Qt class**, but it can combine as many pure-Python *mixins* as "
      "needed. PyQt6 supports cooperative multiple inheritance: each `__init__` must accept and pass on "
      "`*args, **kwargs` so that the `super()` chain reaches the Qt class."),
    lst("c03_mixin.py", "Pure-Python mixin combined with a single Qt class"),
    out("c03_mixin"),
    note("WARNING", "Inheriting from two Qt classes at the same time (for example, `class X(QLabel, QPushButton)`) is "
                    "not supported. To combine widget behaviors, use composition: a widget that contains others."),
    h3("Python's @property versus pyqtProperty"),
    p("Python's `@property` creates computed attributes visible only to Python code. `pyqtProperty`, on the other "
      "hand, registers the property in Qt's **meta-object system**, making it reachable through `property()`/"
      "`setProperty()`, by animations (Chapter 19), by QML (Chapter 26) and by style sheets."),
    lst("c03_property.py", "@property (Python) versus pyqtProperty (visible to the meta-object system)"),
    out("c03_property"),
    p("Note that `setProperty('level', 80.0)` went through the *setter* and was clamped to the capacity (50.0), and "
      "that the `levelChanged` signal was emitted on both changes. `property('capacity')`, however, returns "
      "`None`: an ordinary `@property` does not exist for Qt."),

    h2("Functions as objects"),
    h3("Callables, lambdas and closures"),
    p("Connecting a signal means handing Qt a **callable**: a function, a method, a `lambda`, an object with "
      "`__call__` or a `functools.partial`. Lambdas are handy to adapt arguments, but they have a well-known pitfall "
      "when created in loops and connected to signals that send arguments, such as `clicked(bool)`."),
    lst("c03_lambda.py", "Classic pitfall: a lambda in a loop connected to clicked(bool)"),
    out("c03_lambda"),
    p("In the wrong form, PyQt passes the signal's `checked` argument (False) to the lambda's first parameter, "
      "overwriting the default value `i` — every button logs `False`. The fix is to reserve the first parameter "
      "for the signal argument (`lambda checked=False, i=i: ...`) or to use `partial`."),
    h3("functools.partial to pass arguments to slots"),
    p("`partial(function, arg1)` creates a new callable with arguments fixed at creation time. It is more readable "
      "than a lambda when the goal is just to pre-fill arguments, and the fixed value does not depend on variables "
      "that change later (the *late binding* problem of closures)."),

    h2("Decorators"),
    p("Decorators wrap a function to add behavior. In PyQt6, the most used decorator is `@pyqtSlot`, which "
      "declares the C++ signature of the slot. Custom decorators — to measure time, log or handle errors — can be "
      "combined with it."),
    lst("c03_decorator.py", "Decorators: a custom decorator stacked with @pyqtSlot"),
    out("c03_decorator"),
    note("TIP", "Always use `functools.wraps` in custom decorators (it preserves the function's name and metadata) and "
                "keep `@pyqtSlot` as the outermost decorator, so that the slot declaration is applied to the final "
                "function."),

    h2("Type hints, dataclasses and enum"),
    p("`dataclass` is ideal for the **data** the interface displays and edits (a test, a pipe, a well); `Enum` "
      "represents closed sets of options (materials, units, states). A `QComboBox` can store, alongside each text, "
      "an arbitrary Python object in the `userData` parameter — including an enum member."),
    lst("c03_dataclass_enum.py", "dataclass + Enum feeding a QComboBox (associated data via userData)"),
    out("c03_dataclass_enum"),
    p("`frozen=True` makes the instance immutable — useful for values that travel between the interface and the "
      "calculation layer without risk of accidental change."),

    h2("Exceptions and context managers"),
    p("This is a point where PyQt6 differs from ordinary Python: an **unhandled** exception inside a slot or a "
      "method called by Qt makes PyQt call `qFatal()`, which **ends the process** abruptly. In everyday tools, this "
      "means losing the user's work. The solution is to install your own `sys.excepthook`, which PyQt6 calls "
      "instead of terminating."),
    lst("c03_exceptions.py", "Exceptions in slots: a global excepthook keeps the application alive"),
    out("c03_exceptions"),
    p("Without the line `sys.excepthook = global_handler`, the same program ends with the *traceback* and the "
      "*Aborted* signal (exit code 134 on Linux) — behavior verified with the same PyQt6 version. In real "
      "applications, the handler writes the error to a log and shows a friendly message (Chapter 27)."),
    p("**Context managers** (`with`) guarantee that resources are released even when an exception occurs. Besides "
      "files, several PyQt6 classes support `with`: `QSignalBlocker` (temporarily blocks signals, Chapter 5) and "
      "`QMutexLocker` (thread lock, Chapter 20)."),
    snip('''from PyQt6.QtCore import QSignalBlocker

with QSignalBlocker(spin):        # changes below do not emit valueChanged
    spin.setValue(0.0)
# when the block ends, signals are emitted normally again'''),

    h2("Modules, packages and imports"),
    p("Import explicitly the classes you use — this makes clear which module each class comes from and avoids name "
      "clashes. Never use `from PyQt6.QtWidgets import *`."),
    snip('''# Style 1: explicit classes (the most common in this manual)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow

# Style 2: modules (useful when many classes are used)
from PyQt6 import QtCore, QtWidgets
window = QtWidgets.QMainWindow()

# Inside the package itself (src/eng_calc/ui/window.py)
from ..services.pipes import barlow_pressure    # relative import'''),

    h2("Chapter exercises"),
    nl("Create the class `AlarmPanel(ResultPanel)` that paints the value red when it exceeds a limit.",
       "Modify Listing 3.4 to use `partial` instead of a lambda and confirm the output.",
       "Write a `@log_call` decorator that prints the arguments received by a slot and test it with `@pyqtSlot(int)`.",
       "Run Listing 3.7 with the `excepthook` line commented out and observe the exit code of the process.",
       "Create an `Enum` of pressure units and fill a `QComboBox` with `userData` holding the conversion factor."),
)
