# -*- coding: utf-8 -*-
"""Part V — Capstone project (Chapter 31), references and glossary (English edition)."""
from blocks import ST_FIN, bl, ch, flat, h2, img, lst, nl, note, out, p, part, snip, tab

APP_NOTE = "✔ Executed by Listing 31.13 (tests, self-test of the source code and of the frozen executable)."

CAP31 = flat(
    ch("Capstone project: a technical engineering application", ST_FIN, [
        "Apply, in a single project, the concepts of all the Parts.",
        "Document requirements, architecture and technical decisions.",
        "Deliver the application tested, packaged and documented.",
    ]),
    p("This chapter brings the manual together in a complete application: the **Leak Test Monitor**, a tool to "
      "record, analyze and document pressure tests of lines, vessels and equipment. The code (about 900 lines, "
      "including tests) is organized as a professional Python package and was verified end to end: automated "
      "tests, scripted non-interactive execution (*self-test*), generation of the PDF report, packaging with "
      "PyInstaller and re-execution of the frozen executable (Listing 31.13)."),

    h2("Requirements and scope"),
    tab("Requirements of the Leak Test Monitor", ["ID", "Requirement", "Where it is met"],
        [["RF-01", "Register tests with a unique code, description and acceptance criterion",
          "repository.py, window.py"],
         ["RF-02", "Import readings (time, pressure, temperature) from CSV with ';' or ',' and decimal comma",
          "csv_import.py"],
         ["RF-03", "Compute pressure drop, percentage drop and rate of drop by linear regression",
          "domain.py"],
         ["RF-04", "Compensate the thermal variation of the trapped fluid (dp/dT given in the criterion)",
          "domain.py"],
         ["RF-05", "Pass or fail the test, listing every reason for failure", "domain.py"],
         ["RF-06", "Show readings in a table and a chart, and the result in a dockable panel", "window.py"],
         ["RF-07", "Issue a PDF report with result, criterion, chart and readings", "report.py"],
         ["RNF-01", "The interface must not freeze during the analysis", "services.py (QThreadPool)"],
         ["RNF-02", "Calculation rules testable without the interface and checked against an independent "
          "reference", "tests/test_domain.py (NumPy)"],
         ["RNF-03", "Data persisted in the user's data folder; window state restored",
          "app.py (QStandardPaths), QSettings"],
         ["RNF-04", "Executable independent of a Python installation", "leak_test_monitor.spec"]],
        [1000, 5300, 2771], font=17),
    p("Out of scope for this version: manual editing of readings, multiple simultaneous users and direct "
      "acquisition from the instrument — the latter can be added with the `QSerialPort` of Chapter 21, feeding "
      "the same readings model."),
    note("WARNING", "The acceptance criterion of the example (minimum duration, maximum percentage drop and rate, "
                    "dp/dT coefficient) is illustrative. In real use, the values and the thermal compensation "
                    "method must come from the test procedure and from the standard applicable to the "
                    "equipment."),

    h2("Solution architecture"),
    p("The application follows the layers of Chapter 27. The **domain** (`domain.py`) is pure Python; "
      "**infrastructure** (`repository.py`, `csv_import.py`) deals with SQLite and files; **services** "
      "(`services.py`, `report.py`) run the analysis in the background and produce the PDF; the "
      "**presentation** (`models.py`, `window.py`) uses Model/View, actions and signals. The `app.py` module "
      "is the **composition root**: it creates the `QApplication`, chooses the database, injects repository "
      "and service into the window and offers the `--selftest` mode."),
    img("Architecture of the capstone project", "f31_1_capstone.png", 15.5),
    tab("Modules of the capstone project and reference chapters", ["Module", "Content", "Chapters"],
        [["domain.py", "dataclasses, linear regression, thermal compensation, criterion", "3, 27"],
         ["csv_import.py", "csv.Sniffer, decimal comma conversion, errors per line", "16"],
         ["repository.py", "SQLite with transactions and a foreign key", "15, 27"],
         ["models.py", "QAbstractTableModel, roles and headers", "14"],
         ["services.py", "QThreadPool, QRunnable and signals between threads", "20"],
         ["report.py", "QTextDocument, QPdfWriter, Matplotlib", "17, 22"],
         ["window.py", "QMainWindow, QAction, QSplitter, QDockWidget, pyqtgraph", "7, 8, 9, 22"],
         ["app.py", "composition, QStandardPaths, QSettings, self-test", "4, 13, 27"],
         ["tests/", "pytest and pytest-qt", "28"],
         ["leak_test_monitor.spec", "PyInstaller (onedir)", "30"]],
        [2300, 4900, 1871], font=17),
    lst("c31_app/leaktest/app.py", "app.py — composition root, data folders and self-test", nota=APP_NOTE),
    p("The package also has `leaktest/__init__.py` (version) and `leaktest/__main__.py`, which allows running it "
      "with `python -m leaktest`:"),
    snip(["import sys", "", "from .app import main", "", "sys.exit(main(sys.argv))"]),
    p("In `--selftest` mode, the SQLite database and the configuration file (`QSettings` in INI format) go to "
      "the given folder — the test never touches the user's real data."),

    h2("Main interface"),
    p("The window combines what was seen in Parts I and II: actions with standard shortcuts "
      "(`QKeySequence.StandardKey.New`), menu and toolbar sharing the same `QAction`s, a `QSplitter` with the "
      "list of tests and the chart and readings tabs, and a `QDockWidget` with the result. The enabled state of "
      "the actions follows the state (`_update_actions`): it is not possible to analyze without readings or to "
      "issue a report without a result. The dialogs (`QInputDialog`, `QFileDialog`, `QMessageBox`) only appear "
      "when the arguments are not supplied — which allows the actions to be tested without interaction."),
    lst("c31_app/leaktest/window.py", "window.py — main window, actions and integration of the components",
        nota=APP_NOTE),
    img("Main window of the Leak Test Monitor after the self-test", "f31_2_window.png", 15.5),
    p("Note `_on_completed()`: if the user switched tests while the analysis was running, the result that "
      "arrives is discarded. This care is indispensable whenever an asynchronous task finishes after the "
      "context that requested it has changed."),

    h2("Data model and persistence"),
    p("The readings come from pressure recorders in CSV. The example file contains a 60 min hold at 345 bar "
      "with 0.57 °C of fluid heating:"),
    lst("c31_app/data/TH-01.csv", "data/TH-01.csv — example readings", lang="text",
        nota="✔ Read by the self-test and by the tests of Listing 31.11."),
    p("The domain defines three immutable objects (`Reading`, `Criterion`, `Result`) and the `analyze()` "
      "function. The final pressure is corrected to the initial temperature by p_corr = p − k·(T − T0), where k "
      "is the dp/dT coefficient of the criterion; the rate of drop comes from the slope of the least-squares "
      "line over the corrected pressures, which makes it less sensitive to a single noisy reading than the "
      "difference between the end points. All the failures of the criterion are accumulated in `reasons`, so "
      "that the report says **why** the test failed."),
    lst("c31_app/leaktest/domain.py", "domain.py — analysis rules in pure Python", nota=APP_NOTE),
    lst("c31_app/leaktest/csv_import.py", "csv_import.py — reading CSV with separator detection",
        nota=APP_NOTE),
    p("Persistence uses the standard library's `sqlite3`, with transactions (`with self.con`) and cascading "
      "deletion of the readings. The criterion is stored as JSON from the *dataclass* — adding a field to the "
      "criterion requires no schema migration. For screens centered on editable tables, Qt's SQL models "
      "(Chapter 15) would be an equally valid alternative."),
    lst("c31_app/leaktest/repository.py", "repository.py — persistence in SQLite", nota=APP_NOTE),
    lst("c31_app/leaktest/models.py", "models.py — table models for tests and readings",
        nota=APP_NOTE),

    h2("Background computation and charts"),
    p("Analyzing one test is fast, but the pattern has to hold for long computations (thousands of readings, "
      "nonlinear fits). The service hands the task to a `QThreadPool` and returns the result through a signal: "
      "the signals object lives in the GUI thread, so the emissions made in the pool thread arrive queued and "
      "the slots can update widgets safely (Chapter 20). The list of readings is copied before it goes to the "
      "pool, so that the thread shares no mutable state with the interface."),
    lst("c31_app/leaktest/services.py", "services.py — analysis in a QThreadPool with the result by signal",
        nota=APP_NOTE),
    p("The window's chart is a pyqtgraph `PlotWidget`, updated with `setData()` whenever the test changes; in "
      "the report, the same series is drawn with Matplotlib, which produces a print-quality image "
      "(Chapter 22)."),

    h2("PDF reports"),
    p("The report is assembled in HTML — tables, colors and lists — and converted to PDF by `QTextDocument`, "
      "which paginates the content automatically to the printable area of the A4 sheet defined in the "
      "`QPdfWriter`. The Matplotlib chart is generated in memory (PNG) and registered in the document with "
      "`addResource()` under the URL `chart://pressure`, referenced by the `<img>` tag. No temporary file is "
      "needed."),
    lst("c31_app/leaktest/report.py", "report.py — HTML + Matplotlib → QTextDocument → PDF",
        nota=APP_NOTE),
    img("First page of the PDF report generated by the self-test", "f31_3_report.png", 12.0),

    h2("Testing, packaging and delivery"),
    p("The domain tests check values computed by hand and compare the linear regression with NumPy's "
      "(`numpy.polyfit`) — an independent cross-check. The interface tests exercise the full workflow with "
      "pytest-qt, including waiting for the signal from the pool thread, and the error paths, replacing the "
      "message boxes with functions that record the text (`monkeypatch`)."),
    lst("c31_app/tests/test_domain.py", "tests/test_domain.py — tests of the domain and of the import",
        nota=APP_NOTE),
    lst("c31_app/tests/test_window.py", "tests/test_window.py — interface tests with pytest-qt",
        nota=APP_NOTE),
    p("A three-line `conftest.py` adds the project root to `sys.path`, allowing `import leaktest` without "
      "installing the package. The executable is generated from the `.spec`:"),
    lst("c31_app/leak_test_monitor.spec", "leak_test_monitor.spec — packaging with PyInstaller",
        nota=APP_NOTE),
    p("Listing 31.13 is the delivery script, equivalent to what a continuous integration server would run: "
      "tests with coverage, self-test from the source code, packaging and self-test of the frozen executable. "
      "The delivery is approved only if all four stages pass."),
    lst("c31_delivery.py", "Delivery script: tests, self-test, packaging and retest of the executable"),
    out("c31_delivery"),
    p("The result agrees with the manual calculation: the final pressure of 344.918 bar, corrected for 0.57 °C "
      "of heating with dp/dT = 0.25 bar/°C, is 344.918 − 0.25 × 0.57 = 344.776 bar; the drop is 0.224 bar "
      "(0.065 % of 345 bar), within the 0.5 % limit. The coverage of `app.py` shows as 0 % because the "
      "self-test runs in another process, outside pytest-cov's measurement; it is verified by stages 2 and 4."),

    h2("Lessons learned and next steps"),
    p("The problems found while developing the capstone project are typical of real applications and show why "
      "each verification stage exists:"),
    bl("**The frozen executable failed on the first attempt** (\"The 'platformdirs' package is required\"): the "
       "runtime hook of `pkg_resources`, pulled in indirectly by dependencies, broke the program. Only the "
       "self-test of the executable — not the tests of the source code — revealed the problem. The fix "
       "(excluding `pkg_resources` and `setuptools` in the `.spec`) also reduced the package from 515 MB to "
       "364 MB.",
       "**Isolate the test state**: the self-test redirects the database and `QSettings` to a temporary folder; "
       "without this, running the check would change the user's data.",
       "**Asynchronous results can arrive late**: checking the test identifier in `_on_completed()` avoids "
       "showing the result of one test on the screen of another.",
       "**Separating the domain paid off several times**: the rules were tested in milliseconds, compared "
       "with NumPy and reused unchanged in the report and in the self-test."),
    p("Natural evolutions of the project, each supported by a chapter of the manual:"),
    nl("Direct acquisition from the recorder through a serial port or the network (Chapter 21), with a "
       "real-time chart (Chapter 22).",
       "Editing of readings with undo/redo (`QUndoStack`, Chapter 27).",
       "Translated interface (`QTranslator`, Chapter 13) and dark theme (Chapter 12).",
       "Code signing and installer (Inno Setup, DMG or AppImage, Chapter 30).",
       "Continuous integration with the system matrix of Chapter 28 and automatic publication of the "
       "executables."),
    note("TIP", "Use this project as a template for your own tools: replace the domain (for example, sizing or "
                "fatigue calculations) and keep the layer structure, the tests and the delivery script."),
)

REFERENCES = flat(
    dict(k="hu", t="References"),
    p("Official documentation and standards consulted in preparing this manual (accessed on 11 Nov 2026). The "
      "reference versions are given in the Preface."),
    bl("BATCHELDER, N. *Coverage.py documentation*. Available at: https://coverage.readthedocs.io/.",
       "CX_FREEZE. *cx_Freeze documentation*. Available at: https://cx-freeze.readthedocs.io/.",
       "FOWLER, M. *Presentation Model*. 2004. Available at: "
       "https://martinfowler.com/eaaDev/PresentationModel.html.",
       "FREE SOFTWARE FOUNDATION. *GNU General Public License, version 3*. 2007. Available at: "
       "https://www.gnu.org/licenses/gpl-3.0.html.",
       "GAMMA, E.; HELM, R.; JOHNSON, R.; VLISSIDES, J. *Design Patterns: Elements of Reusable "
       "Object-Oriented Software*. Reading: Addison-Wesley, 1994.",
       "IETF. *RFC 6455 — The WebSocket Protocol*. 2011. Available at: https://www.rfc-editor.org/rfc/rfc6455.",
       "IETF. *RFC 6749 — The OAuth 2.0 Authorization Framework*. 2012. Available at: "
       "https://www.rfc-editor.org/rfc/rfc6749.",
       "IETF. *RFC 7636 — Proof Key for Code Exchange by OAuth Public Clients (PKCE)*. 2015. Available at: "
       "https://www.rfc-editor.org/rfc/rfc7636.",
       "JORDAN RUSSELL'S SOFTWARE. *Inno Setup Help*. Available at: https://jrsoftware.org/ishelp/.",
       "KHRONOS GROUP. *OpenGL and Vulkan Registry* (specifications). Available at: "
       "https://registry.khronos.org/.",
       "MATPLOTLIB DEVELOPMENT TEAM. *Matplotlib documentation*. Available at: https://matplotlib.org/stable/.",
       "NATIONAL MARINE ELECTRONICS ASSOCIATION. *NMEA 0183 — Standard for Interfacing Marine Electronic "
       "Devices*.",
       "NUITKA. *Nuitka User Manual*. Available at: https://nuitka.net/.",
       "NUMPY DEVELOPERS. *NumPy documentation*. Available at: https://numpy.org/doc/.",
       "PYINSTALLER DEVELOPMENT TEAM. *PyInstaller Manual*. Available at: https://pyinstaller.org/.",
       "PYQTGRAPH. *PyQtGraph documentation*. Available at: https://pyqtgraph.readthedocs.io/.",
       "PYTEST-DEV. *pytest documentation*. Available at: https://docs.pytest.org/.",
       "PYTEST-DEV. *pytest-qt documentation*. Available at: https://pytest-qt.readthedocs.io/.",
       "PYTHON PACKAGING AUTHORITY. *Python Packaging User Guide*. Available at: https://packaging.python.org/.",
       "PYTHON SOFTWARE FOUNDATION. *Python 3 documentation* (language and standard library). Available at: "
       "https://docs.python.org/3/.",
       "QASYNC. *qasync — Python library for using asyncio in Qt-based applications* (repository). "
       "Available at: https://github.com/CabbageDevelopment/qasync.",
       "RIVERBANK COMPUTING. *PyQt6 Reference Guide*. Available at: "
       "https://www.riverbankcomputing.com/static/Docs/PyQt6/.",
       "RIVERBANK COMPUTING. *PyQt* (product and licensing). Available at: "
       "https://www.riverbankcomputing.com/software/pyqt/.",
       "SUMMERFIELD, M. *Rapid GUI Programming with Python and Qt*. Upper Saddle River: Prentice Hall, 2007.",
       "THE QT COMPANY. *Qt 6 Documentation*. Available at: https://doc.qt.io/qt-6/.",
       "THE QT COMPANY. *Qt Licensing*. Available at: https://www.qt.io/licensing/.",
       "W3C. *Web Content Accessibility Guidelines (WCAG) 2.2*. 2023. Available at: "
       "https://www.w3.org/TR/WCAG22/."),
)

GLOSSARY_TERMS = [
    ("Action (QAction)", "Reusable command with text, icon, shortcut and state, shared by menus, toolbars and "
     "keyboard shortcuts."),
    ("Antialiasing", "Smoothing of the edges of lines and text with intermediate colors in the boundary "
     "pixels."),
    ("Self-test", "Scripted, non-interactive execution of the application that checks the essential "
     "functions; used after packaging."),
    ("Backend", "Specific implementation behind a generic API, such as the audio, database or rendering "
     "plugin in use."),
    ("Binding", "Layer that exposes a library written in one language (C++) to another (Python); PyQt6 is "
     "generated with SIP."),
    ("Blitting", "Redrawing technique that copies an already rendered region and updates only what changed."),
    ("Circular buffer", "Fixed-size structure in which new data replaces the oldest."),
    ("Callback", "Function passed as an argument to be called when an event or operation finishes."),
    ("Coverage", "Proportion of lines or branches of code executed by the tests."),
    ("Queued connection", "Connection in which the slot is executed by the event loop of the receiver's "
     "thread, with the arguments copied into an event."),
    ("Freezing", "Packaging of the Python interpreter, the code and the dependencies into a distributable "
     "executable."),
    ("D-Bus", "Inter-process communication bus used on desktop Linux systems."),
    ("Deadlock", "Permanent blocking in which two or more threads wait for each other."),
    ("Delegate", "Object that paints and edits the items of a Model/View view."),
    ("Downsampling", "Reduction of the number of points of a signal for display, preserving its shape."),
    ("Framing", "Rule that delimits messages in a continuous stream of bytes, such as TCP."),
    ("Entry point", "Record, in the metadata of an installed package, of an object that other applications "
     "can discover and load."),
    ("Event loop", "Loop that receives events from the system and from timers and dispatches them to Qt "
     "objects; started by exec()."),
    ("Fixture", "In pytest, a resource prepared for a test and released at its end (e.g. qtbot)."),
    ("Flag", "Enum whose members can be combined with the | operator (e.g. Qt.AlignmentFlag)."),
    ("GIL", "Global Interpreter Lock: CPython lock that allows only one thread to execute Python bytecode at "
     "a time (in standard CPython, not the free-threaded variant)."),
    ("High-DPI", "High pixel density screens; Qt scales the interface by the devicePixelRatio."),
    ("Hook (PyInstaller)", "Script that tells PyInstaller about the additional files, modules and plugins of a "
     "package."),
    ("i18n / l10n", "Internationalization (preparing the code for translation) and localization (translating "
     "and adapting to a region)."),
    ("Dependency injection", "Technique in which an object receives the dependencies it needs ready-made, "
     "instead of creating them."),
    ("Introspection", "Querying, at run time, the structure of objects, classes and modules."),
    ("Layout", "Manager that positions and sizes widgets automatically."),
    ("Meta-object", "Run-time description of a QObject class: signals, slots, properties and enums."),
    ("Modal", "Window that blocks interaction with other windows until it is closed."),
    ("Model/View", "Qt architecture that separates the data (model) from the presentation (view) and from "
     "editing (delegate)."),
    ("MVP / MVVM", "Presentation patterns: Model-View-Presenter and Model-View-ViewModel."),
    ("Mutex", "Mutual exclusion primitive that guarantees that only one thread executes a critical section."),
    ("NMEA 0183", "Standard of text sentences for navigation equipment, such as GNSS receivers."),
    ("Notarization", "Automated Apple check required to distribute applications outside the App Store on "
     "macOS."),
    ("OAuth 2.0 / PKCE", "Delegated authorization protocol; PKCE protects the authorization code flow in "
     "public applications."),
    ("Offscreen", "Qt platform that creates windows only in memory, without a screen; used in tests."),
    ("Onedir / onefile", "PyInstaller modes: a folder with the executable and libraries, or a single "
     "self-extracting executable."),
    ("Palette (QPalette)", "Set of colors per role and state used by the styles to paint widgets."),
    ("Plugin (Qt)", "Library loaded at run time that extends Qt (platform, images, SQL, multimedia)."),
    ("Property (pyqtProperty)", "Attribute registered in the meta-object, accessible from QML, QSS, "
     "animations and introspection."),
    ("Proxy (model)", "Intermediate model that sorts, filters or transforms another model without copying "
     "the data."),
    ("QML", "Qt Quick's declarative language for describing interfaces and scenes."),
    ("QSS", "Qt Style Sheets: style sheets with a CSS-like syntax applied to widgets."),
    ("Composition root", "Single point of the application that creates and connects the concrete "
     "implementations."),
    ("Visual regression", "Test that compares the current rendering with an approved reference image."),
    ("RHI", "Rendering Hardware Interface: Qt's abstraction over Direct3D, Metal, Vulkan and OpenGL."),
    ("Sandbox", "Isolation of a process with reduced privileges, such as Chromium's in WebEngine."),
    ("Signal / slot", "Qt's communication mechanism: an emitted signal calls the slots connected to it."),
    ("SIP", "Riverbank Computing tool that generates the PyQt6 bindings."),
    ("Thread", "Independent line of execution within a process."),
    ("TLS", "Transport Layer Security: protocol for encryption and authentication of network connections."),
    ("Undo stack", "Stack of commands that allows changes to be undone and redone (QUndoStack)."),
    ("venv", "Isolated Python virtual environment, with its own set of packages."),
    ("Wheel", "Precompiled Python package format (.whl) installed by pip."),
    ("Widget", "Interface element of Qt Widgets; every window and control is a QWidget."),
    ("Worker", "Object that performs work outside the GUI thread and reports results through signals."),
    ("Xvfb", "Virtual X11 server, without a physical screen, used for graphical tests on Linux servers."),
]

GLOSSARY = flat(
    dict(k="hu", t="Glossary"),
    p("Technical terms used in the manual, in alphabetical order."),
    bl(*[f"**{t}** — {d}" for t, d in sorted(GLOSSARY_TERMS, key=lambda x: x[0].lower())]),
)

PART5 = flat(
    part("V", "CAPSTONE PROJECT", "A complete technical application, from requirement to installer", ST_FIN,
         "Chapter 31 · Consolidation"),
    CAP31,
    REFERENCES,
    GLOSSARY,
)
