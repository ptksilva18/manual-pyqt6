# -*- coding: utf-8 -*-
"""Part IV — Chapters 27 to 30 (English edition)."""
from blocks import ST_AVA, bl, ch, flat, h2, h3, img, lst, nl, note, out, p, part, snip, tab

CAP27 = flat(
    ch("Architecture of PyQt6 applications", ST_AVA, [
        "Separate interface, application logic and domain.",
        "Apply the MVC, MVP and MVVM patterns with PyQt6.",
        "Implement undo/redo and extensibility through plugins.",
    ]),
    h2("Layers and separation of concerns"),
    p("Technical applications live for many years and outlive several interfaces. What guarantees that "
      "longevity is the separation into layers, with dependencies always pointing inward: the interface "
      "depends on the logic, never the other way round. The **domain** — calculations, acceptance rules, "
      "units — is pure Python, with no PyQt6 `import`, and can be tested, reused in scripts and validated "
      "against spreadsheets and standards independently."),
    img("Recommended layered architecture", "f27_1_layers.png", 15.0),
    bl("**Views**: widgets, `.ui` files and QML. They display and capture; they neither compute nor access "
       "files.",
       "**Presenters/ViewModels**: state and behavior of the screen; they translate between the view and the "
       "services.",
       "**Application services**: use cases (\"record test\", \"generate report\"), threads, undo.",
       "**Domain**: entities and pure functions; the most stable and most tested part of the system.",
       "**Infrastructure**: database, files, network, instruments — behind replaceable interfaces."),

    h2("Presentation patterns: MVC, MVP and MVVM"),
    p("The three patterns separate the interface from the logic; they differ in who knows whom. In classic "
      "**MVC**, the controller receives the input and updates the model, and the view observes the model — in "
      "Qt, the Model/View architecture (Chapter 14) merges view and controller. In **MVP**, the view is "
      "passive and exposes a minimal interface; the *presenter* reads the values, calls the domain and tells "
      "the view to display the result. Since the presenter talks to a `Protocol`, it can be tested with a "
      "fake view, without a `QApplication`."),
    lst("c27_mvp.py", "MVP: pure domain, presenter and two views (widget and fake)"),
    out("c27_mvp"),
    p("In **MVVM**, the *ViewModel* exposes observable properties (`pyqtProperty` with `notify`) and the view "
      "binds to them. It is QML's natural model (Chapter 26) and works well with Widgets when the binding is "
      "encapsulated in a function. Listing 27.2 shows a detail that separates prototypes from products: when "
      "the widget is updated from the ViewModel, the widget's signals are blocked (`QSignalBlocker`); "
      "otherwise, the value rounded by the widget (3 decimal places) would go back to the ViewModel, and the "
      "bar ↔ psi conversion would accumulate error on every round trip."),
    lst("c27_mvvm.py", "MVVM: ViewModel with notifiable properties and two-way binding"),
    out("c27_mvvm"),

    h2("Dependency injection and configuration"),
    p("A service that creates its own dependencies (`self.repo = SQLiteRepository(...)`) is stuck with them. "
      "With **dependency injection**, it receives them ready-made in the constructor, and a single point — the "
      "**composition root** — decides the concrete implementations from the configuration. Python needs no "
      "*framework* for this: constructors, `Protocol` and a `compose()` function are enough. The "
      "configuration comes from a TOML file (read with `tomllib`, from the standard library) and can be "
      "overridden by environment variables, which is useful on servers and in tests."),
    lst("c27_config.toml", "Application TOML configuration file", lang="text",
        nota="✔ Read by Listing 27.4 (run and verified)."),
    lst("c27_di.py", "Dependency injection: typed configuration, composition root and repositories"),
    out("c27_di"),
    p("The 0.3 % limit came from the `TESTS_LIMITS__ALLOWABLE_DROP_PCT` environment variable, set in the "
      "test, and not from the file (0.5 %). The same `TestService` worked with both repositories without any "
      "change. **User** preferences (window geometry, recent files) remain in `QSettings` (Chapter 13); the "
      "**application** configuration (backends, limits, addresses) stays in the versioned file."),

    h2("Command pattern: QUndoStack, QUndoCommand and QUndoView"),
    p("Reliable undo/redo requires every change to the document to go through a **command** that knows how to "
      "execute itself (`redo()`) and revert itself (`undo()`). `QUndoStack.push()` executes the command and "
      "stacks it; `id()` and `mergeWith()` merge successive edits (turning a `QDial` should not produce a "
      "hundred steps); `beginMacro()`/`endMacro()` group commands; `setClean()`/`isClean()` mark the saved "
      "point, so that \"save changes?\" is asked only when necessary."),
    lst("c27_undo.py", "QUndoStack: commands, merging, macros, clean state and QUndoView"),
    out("c27_undo"),
    p("The three edits of PT-101 became a single command; undoing the macro restored both pressures at once and "
      "returned the stack to the clean state. `createUndoAction()`/`createRedoAction()` create `QAction`s whose "
      "text and enabled state follow the stack — ready for the Edit menu. `QUndoGroup` coordinates the stacks "
      "of several open documents."),
    note("WARNING", "In PyQt6, `QUndoStack`, `QUndoCommand` and `QUndoGroup` are in `QtGui`; only `QUndoView` "
                    "remains in `QtWidgets` (Table 1.5)."),

    h2("Plugins and extensibility with importlib"),
    p("Plugins let teams add features — exporters, calculations specific to a client, instrument drivers — "
      "without changing the core. The ingredients are: **discovery** (files in a folder, via "
      "`importlib.util`, or installed packages that declare *entry points*, via `importlib.metadata`), a "
      "versioned **contract** (`API_VERSION`, `register` function) and a stable **facade** (`AppAPI`) that "
      "exposes only what the plugin may use."),
    lst("plugins_demo/unit_converter.py", "Example plugin (plugins_demo folder)",
        nota="✔ Loaded and executed by Listing 27.7 (run and verified)."),
    lst("c27_plugins.py", "Discovery, version validation and isolation of plugins"),
    out("c27_plugins"),
    p("An installable package registers its plugins in `pyproject.toml`, in the "
      "`[project.entry-points.\"pyqt6_manual.plugins\"]` section, with lines such as "
      "`converter = my_package.plugin`. Remember that loading a plugin **executes code**: accept only plugins "
      "from a trusted source."),

    h2("Global exception handling (sys.excepthook) and error reports"),
    p("As seen in Chapter 3, an unhandled exception in a slot ends the process when `sys.excepthook` is the "
      "default one. A custom hook turns the error into a *log* record and a message to the user, with details "
      "that can be copied for support, and the application carries on. Exceptions in Python threads go "
      "through `threading.excepthook` (Python 3.8+)."),
    lst("c27_exceptions.py", "sys.excepthook and threading.excepthook with an error report"),
    out("c27_exceptions"),
    note("WARNING", "If the error box is the only open window, closing it triggers `quitOnLastWindowClosed` and "
                    "ends the application — which is what happened in the first version of this listing, before "
                    "the main window was created. In real applications the main window exists, but the detail "
                    "matters in command-line tools and in tests."),

    h2("Chapter exercises"),
    nl("Write `pytest` tests for the `Presenter` of Listing 27.1 using only the `FakeView`.",
       "Add the kPa unit to the ViewModel of Listing 27.2, without changing the view beyond a new field.",
       "Implement a JSON-file repository and select it through the TOML configuration.",
       "Make inserting and removing rows in a `QAbstractTableModel` (Chapter 14) undoable.",
       "Package a plugin as an installable package and discover it through an *entry point*."),
)

CAP28 = flat(
    ch("Automated testing", ST_AVA, [
        "Test widgets, signals and models automatically.",
        "Use QtTest and pytest-qt.",
        "Run GUI tests in continuous integration without a display.",
    ]),
    h2("Testing strategy for GUI applications"),
    p("Interface tests are slower and more fragile than tests of pure functions. The architecture of "
      "Chapter 27 lets you distribute them as a pyramid: many **domain** tests (milliseconds, no Qt), a "
      "moderate number of tests of **presenters, ViewModels and models** (with Qt, no visible windows) and a "
      "few **interface** tests that simulate the user in the critical flows."),
    tab("Testing tools and what each one checks", ["Tool", "Main use", "Execution"],
        [["pytest (or unittest)", "Domain, services, acceptance rules", "No Qt"],
         ["QAbstractItemModelTester", "Contract of Model/View models", "QtTest, no windows"],
         ["QSignalSpy", "Emitted signals and their arguments", "QtTest"],
         ["QTest", "Keyboard, mouse, waits and exposed windows", "QtTest, with widgets"],
         ["pytest-qt (qtbot)", "All of the above with pytest fixtures and waits on signals", "pytest"],
         ["Image comparison", "Visual regression of painted widgets", "Versioned reference"]],
        [2700, 3900, 2471]),
    lst("c28_calculator.py", "Widget under test: hydrostatic pressure calculator"),
    out("c28_calculator"),

    h2("QtTest: QTest, QSignalSpy and QAbstractItemModelTester"),
    p("The `QtTest` module provides the same tools used in Qt's own tests. With the standard library's "
      "`unittest`, they require no external dependency at all:"),
    bl("`QTest.keyClicks()`, `keyClick()`, `mouseClick()` and the like generate real events, which go through "
       "validators, shortcuts and event filters — unlike calling `setText()`.",
       "`QSignalSpy(signal)` records each emission as a list of arguments; `wait(ms)` waits for the next "
       "emission while running the event loop.",
       "`QAbstractItemModelTester` continuously checks whether the model honors the Qt contract (indexes, "
       "counts, insertion and removal signals) while the test manipulates it."),
    lst("c28_qtest.py", "QtTest with unittest: keyboard, mouse, QSignalSpy and QAbstractItemModelTester"),
    out("c28_qtest"),

    h2("pytest-qt and the qtbot fixture"),
    p("The **pytest-qt** plugin (MIT license) integrates Qt with pytest: it creates the `QApplication` only once, "
      "offers the `qtbot` fixture and captures exceptions raised in slots during the test, which would "
      "otherwise go unnoticed. `qtbot.addWidget()` registers widgets for automatic destruction; `waitSignal()` "
      "and `assertNotEmitted()` check signals with a deadline; `waitUntil()` repeats a condition until it is "
      "true — the correct way to wait, instead of `time.sleep()`."),
    lst("c28_test_calculator.py", "Tests with pytest-qt: qtbot, waitSignal, assertNotEmitted and parametrization"),
    out("c28_test_calculator"),
    p("A parametrized test failed on the first run: the expected value for 500 m had been computed by hand as "
      "51.51 bar, when the correct value is 51.52 bar (50.504 + 1.013). It is exactly the kind of error that "
      "automated tests exist to reveal — including in the tests themselves."),

    h2("Simulating mouse and keyboard"),
    bl("For buttons, prefer `mouseClick(button, Qt.MouseButton.LeftButton)`; `button.click()` does not exercise "
       "the event path and therefore tests less.",
       "`keyClicks()` honors validators: in the `test_validator_blocks_text` test, the letters were rejected "
       "by the `QDoubleValidator` — behavior that a `setText()` would not reveal.",
       "Shortcuts and special keys: `keyClick(widget, Qt.Key.Key_S, Qt.KeyboardModifier.ControlModifier)`.",
       "Drag and drop and gestures require `mousePress`/`mouseMove`/`mouseRelease` with coordinates; keep those "
       "tests few in number.",
       "Modal dialogs block the test: inject the dialog (Chapter 27) or close it with a `QTimer` created before "
       "`exec()`."),

    h2("Headless continuous integration (QT_QPA_PLATFORM=offscreen)"),
    p("Continuous integration servers have no display. Qt's `offscreen` platform creates windows only in "
      "memory and is enough for the vast majority of widget tests; for OpenGL, Qt Quick 3D or QtGraphs 3D, use "
      "a virtual X server (Xvfb), as in this manual. On Linux, the PyQt6 wheels depend on system libraries "
      "(EGL, OpenGL, xkbcommon, fontconfig, D-Bus — checked with `ldd` on the `libQt6Gui` library), which must "
      "be installed in the server image."),
    lst("c28_ci.yml", "GitHub Actions: matrix of systems and Python versions with headless tests",
        lang="text", nota="✔ YAML syntax validated with a parser; commands equivalent to those run in this "
                          "chapter."),

    h2("Coverage and visual regression tests"),
    p("**pytest-cov** measures which lines and branches (`--cov-branch`) were executed. Coverage does not prove "
      "correctness, but it points to code that was never exercised. In the report below, the missing lines "
      "(Missing column) are the `if __name__ == \"__main__\"` demonstration block — exclude it from the "
      "measurement with `# pragma: no cover` or with coverage's `exclude_also` setting."),
    lst("c28_coverage.py", "Running the suite with pytest-cov, as in continuous integration"),
    out("c28_coverage"),
    p("**Visual regression** tests compare a widget's rendering with an approved reference image. To make them "
      "reproducible, fix the style (`Fusion`), font, size and scale factor, and use a per-channel tolerance to "
      "absorb antialiasing differences. Font differences between operating systems are unavoidable: keep "
      "references per platform or run these tests on a single server image."),
    lst("c28_visual_regression.py", "Visual regression: comparison with a reference image"),
    out("c28_visual_regression"),

    h2("Chapter exercises"),
    nl("Write the tests of the MVP form of Listing 27.1 with pytest-qt.",
       "Apply `QAbstractItemModelTester` to the hierarchical model of Chapter 14.",
       "Configure coverage to exclude `__main__` blocks and reach 100 % on the calculator module.",
       "Create a visual regression test for the pressure gauge of Chapter 17 with a versioned reference.",
       "Adapt the CI workflow to run the QtGraphs 3D tests under Xvfb on Linux."),
)

CAP29 = flat(
    ch("Performance, debugging and accessibility", ST_AVA, [
        "Measure and remove bottlenecks in painting, models and I/O.",
        "Debug typical PyQt6 problems, including destroyed C++ objects.",
        "Make the application accessible to all users.",
    ]),
    h2("Measuring performance (cProfile, QElapsedTimer)"),
    p("Optimize only what has been measured. `QElapsedTimer` (nanosecond resolution) measures specific "
      "sections; `cProfile`, from the standard library, shows how many times each Python function was called "
      "and how much time it consumed. In interfaces, the usual suspect is the `data()` of models, called "
      "thousands of times on every paint."),
    lst("c29_performance.py", "cProfile and QElapsedTimer: slow model versus cached model"),
    out("c29_performance"),

    h2("Optimizing models, views and painting"),
    bl("**Models**: answer only the roles used, return prebuilt constants and avoid formatting and computation "
       "in `data()`; the listing's cache cost on the order of 100 ms once in order to save on every paint. For "
       "huge tables, load on demand with `canFetchMore()`/`fetchMore()`.",
       "**Notifications**: prefer `beginResetModel()`/`endResetModel()` or block insertions to thousands of "
       "single-row `beginInsertRows()` calls; emit `dataChanged` only for the changed range and with the list "
       "of roles.",
       "**Views**: a fixed row height (`QHeaderView.ResizeMode.Fixed`) and defined widths avoid measuring "
       "content; `resizeColumnsToContents()` measures up to `resizeContentsPrecision()` rows (1000 by "
       "default); in `QListView`, `setUniformItemSizes(True)`.",
       "**Painting**: in `paintEvent()`, draw only the region of `event.rect()`, reuse `QPen`, `QFont` and "
       "`QPainterPath`, and keep static drawings in a `QPixmap` (or use `QPixmapCache`).",
       "**Graphics View**: `setItemIndexMethod()`, `ItemCoordinateCache` on complex items and a "
       "`setViewportUpdateMode()` suited to the update pattern.",
       "**I/O and computation**: always outside the GUI thread (Chapter 20)."),

    h2("Debugging"),
    h3("Qt messages: qDebug, qWarning and QLoggingCategory"),
    p("Qt itself reports usage errors through warning messages — impossible connections, duplicate layouts, "
      "missing plugins. `qInstallMessageHandler()` intercepts all of them, with type and **category**, and "
      "lets you forward them to Python's `logging` (Chapter 13). `QLoggingCategory` organizes the "
      "application's messages into hierarchical categories that can be switched on and off by rules, without "
      "changing the code."),
    lst("c29_debugging.py", "QLoggingCategory, filter rules, message handler and QT_DEBUG_PLUGINS"),
    out("c29_debugging"),
    note("WARNING", "The C++ constructor of `QLoggingCategory` keeps only the pointer to the name. In the test, a "
                    "category created with a temporary `str` ignored the filter rules; created from a `bytes` "
                    "object kept in a module variable (as in Listing 29.2), it obeyed them."),
    h3("Diagnostic environment variables (QT_DEBUG_PLUGINS, QT_LOGGING_RULES)"),
    tab("Useful environment variables for diagnosis", ["Variable", "Effect"],
        [["QT_DEBUG_PLUGINS=1", "Details the search for and loading of plugins (platform, images, SQL...)"],
         ["QT_LOGGING_RULES", "Category rules, e.g. \"qt.qpa.*=true;app.io.debug=false\""],
         ["QT_MESSAGE_PATTERN", "Message format, e.g. \"%{time} %{category} %{message}\""],
         ["QT_FATAL_WARNINGS=1", "Turns warnings into an immediate failure — useful in tests"],
         ["QT_QPA_PLATFORM", "Platform: windows, cocoa, xcb, wayland, offscreen..."],
         ["QT_SCALE_FACTOR", "Global scale factor (High-DPI tests, Chapter 12)"],
         ["QSG_INFO=1", "Information about the Qt Quick scene graph (backend, graphics API)"],
         ["PYTHONFAULTHANDLER=1", "Turns on Python's faulthandler without changing the code"]],
        [2700, 6371]),
    h3("faulthandler and crashes in native code"),
    p("A segmentation fault in C++ code ends the process without a Python *traceback*. The `faulthandler` "
      "module (or `python -X faulthandler`) prints the Python stack of all threads at the moment of the crash, "
      "pointing to the line that called the native code — the first step in isolating the problem. Throughout "
      "this manual, crashes of this kind were documented in `QRangeModel` (Chapter 14), in the audio backend "
      "and in the destruction order of `QAudioEngine` (Chapter 23)."),

    h2("Memory management: pitfalls between Python and C++ (sip.isdeleted)"),
    p("Every Qt object has two parts: the C++ object and the Python *wrapper*. Ownership defines who destroys "
      "whom: objects with a parent are destroyed by the parent (Chapter 5); objects without a parent are "
      "destroyed when the Python wrapper is collected. The pitfalls of Listing 29.3 are the most frequent:"),
    lst("c29_memory.py", "Destroyed C++ objects, temporaries, unreferenced objects and faulthandler"),
    out("c29_memory"),
    bl("**Object destroyed by the parent**: the wrapper still exists and any use raises `RuntimeError: wrapped "
       "C/C++ object ... has been deleted`. `sip.isdeleted(obj)` lets you test before using it.",
       "**Temporary**: in `QTableView().horizontalHeader()`, the table is collected at the end of the "
       "expression and takes the header with it — the error really appeared while preparing Listing 29.1.",
       "**Unreferenced window**: created inside a function and not stored, it disappears when the function "
       "returns. Keep the reference (an attribute) or give it a parent.",
       "**Connections to lambdas** keep the captured objects alive; disconnect them or use "
       "`functools.partial` carefully with short-lived objects.",
       "`deleteLater()` defers destruction to the event loop — the safe way to destroy an object inside one "
       "of its own slots."),

    h2("Accessibility"),
    p("Accessibility is a legal requirement in many contexts and benefits all users: full keyboard operation, "
      "compatibility with screen readers and legibility under any lighting condition. Qt exposes the widget "
      "tree to the system's assistive technologies (UI Automation on Windows, NSAccessibility on macOS, AT-SPI "
      "on Linux)."),
    lst("c29_accessibility.py", "Accessible names, buddies, tab order, contrast and preferences"),
    out("c29_accessibility"),
    h3("Accessible names and descriptions"),
    p("Screen readers announce the name and role of each control. Buttons and labels with text already have a "
      "name; fields and graphical controls need `setAccessibleName()` and, when useful, "
      "`setAccessibleDescription()`. `QLabel.setBuddy()` associates the label with the field and creates the "
      "shortcut with `&` (Alt+T for \"&Tag\")."),
    h3("Keyboard navigation and tab order"),
    p("Every function must be reachable from the keyboard. Define the tab order with `QWidget.setTabOrder()` (or "
      "in Designer, Chapter 11), use a suitable `focusPolicy` and offer shortcuts (`QKeySequence`) for frequent "
      "actions. The listing walks the focus chain with the same rules as the Tab key."),
    h3("Contrast, font size and QAccessibilityHints"),
    p("The WCAG 2.x guidelines require a minimum contrast of 4.5:1 for normal text (level AA). The listing's "
      "`contrast()` function implements the relative luminance formula: gray `#999999` on white (2.85:1) fails; "
      "`#595959` (7.00:1) passes. Use font sizes in points — scalable with the DPI — and do not fix the heights "
      "of widgets that contain text. `QStyleHints.accessibility()` (Qt 6.10+) returns a `QAccessibilityHints` "
      "with the system's contrast and motion preferences, and signals to react when they change."),

    h2("Chapter exercises"),
    nl("Profile opening a 100 000-row CSV in a `QTableView` and optimize it until it takes less than 1 s.",
       "Forward all Qt messages to `logging` with category and source file.",
       "Write a utility that lists the widgets of a window with neither an `accessibleName` nor visible text.",
       "Implement a high-contrast theme activated when `contrastPreference()` indicates `HighContrast`."),
)

CAP30 = flat(
    ch("Packaging and distribution", ST_AVA, [
        "Generate standalone executables for Windows, Linux and macOS.",
        "Include Qt plugins, resources and translations correctly.",
        "Produce installers and honor the license obligations.",
    ]),
    h2("Overview of the packaging tools"),
    p("The end user should not need to install Python or PyQt6. Packaging tools bundle the interpreter, the "
      "code, the Qt libraries, the plugins (platform, styles, image formats, SQL) and the application data. "
      "None of them cross-compiles: build the Windows package on Windows, the macOS one on macOS and the Linux "
      "one on the oldest distribution you intend to support."),
    tab("Packaging tools for PyQt6 applications", ["Tool", "Approach", "Platforms", "Remarks"],
        [["PyInstaller", "Freezes interpreter + dependencies", "Windows, Linux, macOS",
          "The most used; dedicated hooks for PyQt6; onedir and onefile modes (6.22.3 tested in this chapter)"],
         ["Nuitka", "Compiles Python to C and freezes", "Windows, Linux, macOS",
          "Requires a C compiler; the pyqt6 plugin warns that PyQt6 support is not perfect (Qt threads) and "
          "recommends PySide6"],
         ["cx_Freeze", "Freezes interpreter + dependencies", "Windows, Linux, macOS",
          "Hooks for PyQt6; generates MSI, DMG and AppImage through the bdist_* commands (8.7.4 tested)"],
         ["pyqtdeploy (Riverbank)", "Static deployment, incl. mobile", "Desktop and mobile",
          "Up to version 3.3.0, supports only Qt 5/PyQt5: not an option for PyQt6"]],
        [2000, 2500, 1800, 2771], font=16),

    h2("PyInstaller"),
    h3("The .spec file, onedir and onefile modes"),
    p("PyInstaller analyzes the `import`s starting from the main script and gathers what is needed. The "
      "`pyinstaller app.py` command generates a `.spec` file — a Python script that describes the package and "
      "should be versioned and edited for fine-tuning. In **onedir** mode (the default), the result is a "
      "folder with the executable and the dependencies in `_internal`; in **onefile** mode (`--onefile`), a "
      "single executable that unpacks itself into a temporary folder on every run — more practical to "
      "distribute, but slower to start. For installers, prefer onedir."),
    lst("c30_app/monitor_app.py", "Application to be packaged: resources, theme, translation and self-test",
        nota="✔ Packaged and executed by Listing 30.3 (run and verified)."),
    lst("c30_app/monitor_app.spec", "PyInstaller .spec file (onedir, data and exclusions)",
        nota="✔ Used by Listing 30.3 (run and verified)."),
    lst("c30_package.py", "Packaging with PyInstaller and running the frozen result"),
    out("c30_package"),
    h3("Including data, plugins and translations"),
    bl("**Data**: declare it in `datas` in the `.spec` (or `--add-data source:destination`) and locate it at "
       "run time from `sys._MEIPASS`, like the `resource()` function of Listing 30.1 — which also works with "
       "the unpackaged source code.",
       "**Qt plugins and translations**: the PyInstaller hooks for PyQt6 include plugins and translations; the "
       "output confirms the `plugins` and `translations` folders and the `qtbase_pt_BR` translation working in "
       "the frozen executable (\"Cancelar\").",
       "**Size**: the test package took about 235 MB because it includes every Qt library that the hook "
       "considers possible. Use `excludes` for unused modules (WebEngine alone takes hundreds of megabytes) and "
       "check the result by running the self-test.",
       "**Console window**: on Windows and macOS, use `console=False` in the `.spec` (or `--windowed`) for GUI "
       "applications."),
    note("TIP", "Include a self-test option in the executable, such as `--selftest` in Listing 30.1, and run it on "
                "the continuous integration server right after packaging: missing plugins and forgotten data "
                "show up before they reach the user."),

    h2("Nuitka"),
    p("Nuitka translates the Python code to C and compiles it, with the `--standalone` (folder) or `--onefile` "
      "mode. It requires a C compiler (MSVC, MinGW, GCC or Clang) and longer builds; in return, it offers fast "
      "startup and code that is harder to inspect. For PyQt6, the `pyqt6` plugin reports that support is not "
      "perfect — for example, Qt threads — and recommends PySide6; test the compiled application carefully "
      "before adopting it."),
    snip(["python -m nuitka --standalone --enable-plugin=pyqt6 \\",
          "    --include-data-dir=resources=resources \\",
          "    --windows-console-mode=disable monitor_app.py"], lang="text"),

    h2("cx_Freeze"),
    p("cx_Freeze freezes the application in a way similar to PyInstaller and integrates with `setuptools`. Its "
      "`bdist_msi` (Windows), `bdist_dmg`/`bdist_mac` (macOS) and `bdist_appimage` (Linux) commands generate "
      "the distribution formats directly."),
    snip(["cxfreeze --script monitor_app.py --target-name monitor_app \\",
          "    build_exe --include-files=resources"], lang="text"),
    p("The command above was run with cx_Freeze 8.7.4 on the application of Listing 30.1: the generated "
      "executable passed the self-test (theme, plugins and translation). Note that `--include-files` is an "
      "option of the `build_exe` subcommand, and that cx_Freeze places the data next to the executable — hence "
      "the second branch of the `resource()` function."),

    h2("Installers: Inno Setup, MSI, DMG and AppImage"),
    bl("**Windows**: Inno Setup (free) generates `.exe` installers from a script; for MSI — required by many IT "
       "departments for centralized distribution — use the WiX Toolset or cx_Freeze's `bdist_msi`.",
       "**macOS**: distribute the `.app` bundle inside a `.dmg` image (`hdiutil create` or the `create-dmg` "
       "tool), signed and notarized.",
       "**Linux**: AppImage (a single executable file, no installation) with `appimagetool`/`linuxdeploy`, or "
       "Flatpak packages; `.deb`/`.rpm` packages for specific distributions."),
    lst("c30_installer.iss", "Inno Setup script for the folder generated by PyInstaller", lang="text",
        allow_long=True, nota="⚠ Not run in the test environment (Linux): requires Inno Setup 6.3+ on "
                              "Windows. The directives follow the official Inno Setup documentation."),

    h2("Code signing and notarization"),
    p("Unsigned executables trigger Windows SmartScreen warnings and are blocked by macOS Gatekeeper. Signing "
      "requires a code-signing certificate issued by a certificate authority (Windows) or an Apple Developer "
      "account (macOS):"),
    snip(["# Windows (Windows SDK): signature with a timestamp",
          "signtool sign /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 /a monitor_app.exe",
          "",
          "# macOS: signature with hardened runtime, notarization and stapling",
          "codesign --force --options runtime --timestamp \\",
          "    --sign \"Developer ID Application: Company (TEAMID)\" TestMonitor.app",
          "xcrun notarytool submit TestMonitor.dmg --keychain-profile profile --wait",
          "xcrun stapler staple TestMonitor.dmg"], lang="text"),
    p("Sign the internal libraries first and the executable and the bundle last; the timestamp keeps the "
      "signature valid after the certificate expires."),

    h2("Licensing in distribution (GPL v3 versus commercial)"),
    p("PyQt6 is distributed by Riverbank Computing under the **GPL v3** or under a Riverbank **commercial "
      "license**. The practical points, without replacing the advice of your legal department:"),
    bl("When **distributing** an application that uses PyQt6 under the GPL v3, the whole application must be "
       "licensed under terms compatible with the GPL v3, and the source code must be offered to whoever "
       "receives the program. This holds regardless of the Qt libraries being under the LGPL.",
       "To distribute closed-source applications, the commercial PyQt license is required (which also covers "
       "PyQt-Charts, PyQt-Graphs, PyQt-NetworkAuth etc.), used with Qt under the LGPL or under a commercial Qt "
       "license.",
       "Some Qt modules — among them Qt Charts, Qt Data Visualization, Qt Graphs and Qt Network Authentication "
       "— are not available under the LGPL, only under the GPL v3 or commercially.",
       "The distributed package contains third-party components with their own licenses: FFmpeg (LGPL, "
       "Chapter 23), OpenSSL, Chromium (WebEngine) and the Python libraries used. Include the license texts and "
       "the required notices.",
       "In general, GPL obligations are triggered by distribution to third parties; internal use of a tool "
       "without distributing it is treated differently. Confirm how your case is classified with your legal "
       "department."),
    note("WARNING", "This manual is not legal advice. Check the current terms on the licensing pages of "
                    "Riverbank Computing and The Qt Company before distributing any software."),

    h2("Chapter exercises"),
    nl("Generate the onefile version of Listing 30.3 and compare its startup time with the onedir version.",
       "Reduce the size of the package by excluding unused modules and confirm with the self-test.",
       "Create the Inno Setup installer on Windows and test installation, shortcut and uninstallation.",
       "Build a CI workflow that packages, runs the self-test and publishes the artifacts per platform.",
       "List the licenses of all the components included in the generated package."),
)

PART4 = flat(
    part("IV", "QUALITY, ARCHITECTURE AND DISTRIBUTION", "From code that works to a product that lasts",
         ST_AVA, "Chapters 27 to 30 · Advanced level"),
    CAP27, CAP28, CAP29, CAP30,
)
