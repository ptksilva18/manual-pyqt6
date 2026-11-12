# -*- coding: utf-8 -*-
"""Part I — Chapters 4 to 7 (English edition)."""
from blocks import ST_BAS, bl, ch, flat, h2, h3, h4, img, lst, nl, note, out, p, snip, tab

CAP04 = flat(
    ch("First application with PyQt6", ST_BAS, [
        "Write, run and understand the smallest possible PyQt6 application.",
        "Understand the application object and the event loop.",
        "Evolve to a window based on a QMainWindow subclass.",
    ]),
    h2("Minimal anatomy of an application"),
    p("Every PyQt6 application with a graphical interface follows the same four steps, numbered in the comments of "
      "Listing 4.1: create the application object, create at least one window, show it and enter the "
      "*event loop*."),
    lst("c04_first.py", "First PyQt6 application"),
    img("Window produced by the first application", "f4_1_first.png", width_cm=8.0),
    nl("`QApplication(sys.argv)` creates the application object, which initializes Qt, loads the platform plugin "
       "and processes command-line arguments. There must be **exactly one** per process, created before any "
       "widget.",
       "A widget created **without a parent** becomes a top-level window; here, a `QLabel` serves as the window.",
       "`show()` schedules the display. Nothing appears on screen yet: painting happens when the event loop runs.",
       "`app.exec()` enters the event loop and returns only when the application ends; its return value is the "
       "exit code, passed on to `sys.exit()`."),
    note("WARNING", "Creating a widget before the `QApplication` produces the fatal error *QWidget: Must construct a "
                    "QApplication before a QWidget*, which ends the process."),
    h3("QApplication, QGuiApplication and QCoreApplication"),
    tab("Qt application classes", ["Class", "Module", "When to use"],
        [["QCoreApplication", "QtCore", "Programs without a graphical interface that use the event loop (servers, services, command-line tools with timers and networking)"],
         ["QGuiApplication", "QtGui", "Graphical applications without widgets, such as Qt Quick/QML applications (Chapter 26)"],
         ["QApplication", "QtWidgets", "Applications with widgets — the case of this whole manual up to Chapter 25"]],
        [2300, 1500, 5271]),
    p("The three form a hierarchy (`QApplication` inherits from `QGuiApplication`, which inherits from "
      "`QCoreApplication`). The single instance can be obtained anywhere in the program with "
      "`QApplication.instance()`."),
    h3("sys.argv and command-line arguments"),
    p("The constructor receives the argument list so that Qt recognizes its own options, such as `-style` or "
      "`-platform`. PyQt6 **removes from the list** the options that Qt consumed, leaving the others to the "
      "program."),
    lst("c04_arguments.py", "Command-line arguments: Qt consumes the options it recognizes"),
    out("c04_arguments"),
    p("To parse the remaining arguments robustly, use Python's `argparse` or Qt's `QCommandLineParser` "
      "(Chapter 16)."),
    h3("The event loop"),
    p("A graphical application spends most of its time **waiting**: for a click, a key, a timer, data from the "
      "network. The event loop is the loop, started by `exec()`, that waits for the next event, delivers it to the "
      "target object, runs the corresponding handlers and slots and repaints what changed. Figure 4.2 summarizes "
      "the complete life cycle."),
    img("Life cycle of a PyQt6 application and the event loop", "f4_2_lifecycle.png"),
    note("IMPORTANT", "While a slot is running, the event loop is stopped: the window does not repaint and does not "
                      "respond to the user. All slot code must be fast. Long calculations go to another thread "
                      "(Chapter 20) or are split into steps with `QTimer` (Chapter 5)."),

    h2("QWidget as a top-level window"),
    p("Any widget without a parent is displayed as a window, with a frame and title bar provided by the operating "
      "system. For simple windows — utilities, custom dialogs, prototypes —, a `QWidget` subclass with a layout is "
      "enough. The window type and decoration are controlled by *window flags*:"),
    snip('''from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget

panel = QWidget()
panel.setWindowTitle("Monitor")
panel.setWindowFlags(Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint)
panel.setMinimumSize(320, 200)
panel.show()'''),
    p("Note that `setWindowFlags()` must be called before `show()`; calling it on a window that is already visible "
      "hides it, and `show()` must be called again."),

    h2("QMainWindow subclass"),
    p("`QMainWindow` is the class meant for the main window of applications: it already reserves areas for a menu "
      "bar, toolbars, dock widgets, a status bar and a **central widget** (Chapter 8). The professional pattern is "
      "to create a subclass and build the interface in `__init__`, keeping the `if __name__ == \"__main__\"` block "
      "only for start-up."),
    lst("c04_mainwindow.py", "Main window as a QMainWindow subclass"),
    p("A `main()` function returning the exit code makes testing easier and allows its use as an *entry point* in "
      "`pyproject.toml` (Listing 2.2)."),

    h2("Shutting down the application"),
    h3("sys.exit(app.exec()) and exit codes"),
    p("`app.exec()` returns the value passed to `app.exit(code)`; `app.quit()` is equivalent to `exit(0)`. Passing "
      "this value on to `sys.exit()` lets scripts and schedulers detect failures (convention: 0 = success). To end "
      "with an error after showing a message, use `QApplication.exit(1)`."),
    h3("quitOnLastWindowClosed and aboutToQuit"),
    p("By default, the application ends when the last visible window is closed (`quitOnLastWindowClosed()` equal "
      "to `True`). Applications that live in the system tray (Chapter 23) disable this behavior with "
      "`app.setQuitOnLastWindowClosed(False)`. The `aboutToQuit` signal is emitted just before `exec()` returns — "
      "the right place to save settings and release resources."),
    lst("c04_lifecycle.py", "Metadata, aboutToQuit and quitOnLastWindowClosed"),
    out("c04_lifecycle"),

    h2("Application metadata: name, organization, version and icon"),
    p("The metadata set in Listing 4.4 are not decorative: `organizationName` and `applicationName` determine where "
      "`QSettings` stores the preferences (Chapter 8) and where `QStandardPaths` locates data folders (Chapter 13); "
      "`applicationDisplayName` is appended to window titles on some platforms; `applicationVersion` feeds *About* "
      "dialogs and `QCommandLineParser`. The default icon of all windows is set once on the application:"),
    snip('''from PyQt6.QtGui import QIcon

app.setWindowIcon(QIcon("resources/icon.svg"))     # SVG scales well on High-DPI screens
app.setDesktopFileName("eng-calc")                 # Linux/Wayland: .desktop file'''),

    h2("Chapter exercises"),
    nl("Modify Listing 4.1 to show a `QPushButton` as the window and connect `clicked` to `app.quit`.",
       "Run Listing 4.2 with the `-style windows` option on the command line and compare the appearance.",
       "Change Listing 4.4 so that the application keeps running after the window is closed; end it with a `QTimer`.",
       "Create the `main()` function of a project with the structure of Figure 2.1, called by `__main__.py`."),
)

CAP05 = flat(
    ch("QObject, signals and slots", ST_BAS, [
        "Understand QObject, the object tree and memory management.",
        "Connect, create and disconnect signals and slots safely.",
        "Use properties, meta-objects and timers.",
    ]),
    h2("QObject: Qt's base class"),
    p("`QObject` is the root of almost every Qt class that has an identity (widgets, timers, models, sockets). It "
      "provides four fundamental services: the parent–child **object tree**, **signals and slots**, "
      "**properties** and **events**. Value classes, such as `QPoint` or `QColor`, do not inherit from "
      "`QObject`."),
    h3("Parent–child hierarchy and memory ownership"),
    p("Every `QObject` can have a parent, passed in the constructor or through `setParent()`. The parent **owns** "
      "its children: when destroyed, it destroys all of them recursively. For widgets, the relationship has a second "
      "effect: a child widget is drawn inside the parent's area, and a widget without a parent is a window."),
    img("Parent–child object tree of a window", "f5_1_tree.png"),
    h3("objectName, findChild() and findChildren()"),
    p("`objectName` identifies an object within the tree. It is used by `findChild()` and `findChildren()`, by "
      "style sheets (the `#name` selector), by Qt Designer and by the main window's `saveState()`."),
    lst("c05_tree.py", "Object tree: parent-child, objectName, findChild/findChildren and destroyed"),
    out("c05_tree"),
    p("Three details of the output deserve attention: the layout appears as a child of the window (it was created "
      "with `QVBoxLayout(window)`); the widgets added to the layout were **reparented** to the window; and each "
      "`QLineEdit` has an internal unnamed child, created by Qt itself — that is why searches should filter by type "
      "and name, not by position in the list."),
    h3("deleteLater() and the C++ versus Python life cycle"),
    p("To destroy a Qt object, use `deleteLater()`: destruction happens in the next cycle of the event loop, when "
      "it is safe (for example, after the slot that is handling a signal from that object has finished). The "
      "`destroyed` signal reports when the C++ object no longer exists."),
    p("Since each object has a Python part and a C++ part, the Python variable may keep existing after the parent "
      "destroyed the C++ object. Any access then raises `RuntimeError`; the `PyQt6.sip` module lets you detect "
      "this situation."),
    lst("c05_cpp_lifetime.py", "C++ x Python life cycle: a reference to a C++ object already destroyed"),
    out("c05_cpp_lifetime"),
    note("WARNING", "The opposite problem also occurs: a widget **without a parent** kept only in a local variable is "
                    "destroyed by Python's garbage collector at the end of the function — the window \"flashes\" and "
                    "disappears. Keep windows in attributes (`self.data_window = ...`) or give them a parent."),

    h2("Signals and slots"),
    p("Signals and slots are Qt's mechanism for communication between objects. A **signal** is emitted when "
      "something happens (a button was clicked, a value changed); a **slot** is any callable connected to it. The "
      "emitter does not know who is connected, which reduces the coupling between parts of the application."),
    img("Signals and slots mechanism", "f5_2_signals.png"),
    h3("Connecting built-in signals"),
    p("Qt widgets already declare dozens of signals. Connection uses the syntax `object.signal.connect(callable)`; "
      "the signal's arguments are passed to the callable, which may accept fewer arguments than the signal sends."),
    snip('''button.clicked.connect(self.calculate)               # clicked(bool) -> calculate()
field.textChanged.connect(self.validate)              # textChanged(str) -> validate(text)
spin.valueChanged.connect(bar.setValue)               # slot of another widget
combo.currentIndexChanged.connect(lambda i: print(i))'''),
    h3("Custom signals with pyqtSignal"),
    h4("Declaration as a class attribute"),
    p("Custom signals are declared with `pyqtSignal(types...)` **in the class body**, never inside `__init__`, and "
      "only in `QObject` subclasses. Each instance automatically receives its *bound signal*, with the methods "
      "`connect()`, `disconnect()` and `emit()`."),
    h4("Signals with arguments and overloads"),
    p("The declared types define the signature: `pyqtSignal(str, float)` emits two arguments. An overloaded signal "
      "accepts lists of types (`pyqtSignal([int], [str])`), and the desired variant is chosen by indexing: "
      "`signal[int]`."),
    lst("c05_signals.py", "Custom signals: declaration, arguments, overloads and connections"),
    out("c05_signals"),
    p("The repeated reading (250.0) did not cause an emission because the method only emits when the value changes "
      "— a recommended practice to avoid update loops. After the `disconnect`, only the *log* kept receiving."),
    h3("Slots with @pyqtSlot"),
    p("Any callable works as a slot, but decorating methods with `@pyqtSlot(types)` brings advantages: the method "
      "is registered in the meta-object (reachable through `QMetaObject.invokeMethod` and from QML), the connection "
      "is slightly more efficient and, in cross-thread connections, the slot runs in the receiver object's thread "
      "(Chapter 20)."),
    h3("Passing extra arguments (lambda and functools.partial)"),
    p("When the slot needs information that the signal does not send — for example, which button was clicked —, "
      "use `lambda` or `functools.partial`, watching out for the `checked` argument pitfall shown in Listing 3.4."),
    h3("Connection types"),
    p("The second argument of `connect()` defines how the slot is called."),
    tab("Values of Qt.ConnectionType", ["Value", "Behavior"],
        [["AutoConnection", "Default. Direct if emitter and receiver are in the same thread; queued otherwise."],
         ["DirectConnection", "The slot runs immediately, in the emitter's thread."],
         ["QueuedConnection", "The slot runs in the event loop of the receiver's thread."],
         ["BlockingQueuedConnection", "Like QueuedConnection, but the emitter blocks until the slot returns (never in the same thread)."],
         ["UniqueConnection", "Combinable flag: prevents duplicate connections."],
         ["SingleShotConnection", "Combinable flag: the connection is removed after the first emission."]],
        [2600, 6471]),
    lst("c05_connections.py", "Connection types, UniqueConnection, SingleShotConnection and signal blocking"),
    out("c05_connections"),
    h3("Disconnecting, blockSignals() and QSignalBlocker"),
    p("`signal.disconnect(slot)` removes a specific connection; `signal.disconnect()` removes all of them. To "
      "suppress signals temporarily — for example, when filling a form from saved data without triggering "
      "validations —, prefer `QSignalBlocker` in a `with` block over calling `blockSignals(True)` and "
      "`blockSignals(False)` manually: the block is undone even if an exception occurs."),

    h2("Properties: pyqtProperty and dynamic properties"),
    p("Properties declared with `pyqtProperty` (as a decorator or a function) enter the meta-object, with a type, "
      "*getter*, *setter* and notification signal. **Dynamic properties**, created with `setProperty()` on any "
      "object, need no declaration — they are useful to tag widgets (for example, `dangerous=True`) and style them "
      "with style-sheet selectors (Chapter 12)."),
    lst("c05_meta.py", "Dynamic properties and introspection with QMetaObject"),
    out("c05_meta"),

    h2("Meta-object system and introspection"),
    p("The **QMetaObject** describes, at run time, the name of the class, its properties, signals, slots and enums. "
      "It is what allows Qt to connect signals by name, Qt Designer to list editable properties and QML to access "
      "Python objects. In Listing 5.5, the loops start at `propertyOffset()` and `methodOffset()` to list only what "
      "the class itself declared, excluding what was inherited from `QObject`."),

    h2("Timers: QTimer, QBasicTimer and QElapsedTimer"),
    p("`QTimer` emits `timeout` periodically or a single time (`QTimer.singleShot`). It depends on the event loop: "
      "the interval is a minimum, not a real-time guarantee. `QBasicTimer` is a lightweight alternative without "
      "signals, handled in `timerEvent()`. `QElapsedTimer` measures intervals with a monotonic clock."),
    lst("c05_timers.py", "QTimer (periodic and singleShot), QElapsedTimer and QBasicTimer"),
    out("c05_timers"),
    p("The exact number of periodic readings may vary by ±1 depending on the machine load — a direct consequence of "
      "the timer depending on the event loop. The timer type (`Qt.TimerType.PreciseTimer`, `CoarseTimer` or "
      "`VeryCoarseTimer`) tunes the desired accuracy and the power consumption."),
    note("TIP", "`QTimer.singleShot(0, function)` schedules `function` right after the event loop processes the "
                "pending events — useful to complete initialization after the window appears."),

    h2("QtCore value types: QPoint, QSize, QRect, QDate, QDateTime, QUrl"),
    p("QtCore provides value types used throughout the API: integer geometry (`QPoint`, `QSize`, `QRect`) and "
      "floating-point geometry (`QPointF`, `QSizeF`, `QRectF`), dates and times (`QDate`, `QTime`, `QDateTime`, "
      "`QTimeZone`) and addresses (`QUrl`)."),
    lst("c05_types.py", "QtCore value types: geometry, dates and URLs"),
    out("c05_types"),
    note("WARNING", "For historical reasons, for an integer `QRect` `right() = left() + width() - 1` (199 for a width "
                    "of 200), and the center is rounded down. In precise geometric calculations, use `QRectF`, "
                    "where `right() = left() + width()`."),

    h2("Chapter exercises"),
    nl("Add to Listing 5.3 a `backToNormal` signal emitted when the value drops back below the limit.",
       "Create an object with a `temperature` `pyqtProperty` and connect its notification signal to a `QLCDNumber`.",
       "Using `findChildren`, write a function that clears every `QLineEdit` of a form.",
       "Show with `QTimer.singleShot` that a `QueuedConnection` slot runs only after the current code returns.",
       "Using `QDate`, compute how many working days (Monday to Friday) there are between two given dates."),
)

CAP06 = flat(
    ch("Fundamental widgets", ST_BAS, [
        "Know the properties common to all widgets.",
        "Use display widgets, buttons and data-entry widgets.",
        "Associate each widget with its most relevant signals.",
    ]),
    h2("QWidget: common properties and methods"),
    p("All visual elements inherit from `QWidget`. That is why the properties in this section apply to any widget "
      "in the chapter. In PyQt6, Qt properties can be passed directly as keyword arguments to the constructor — "
      "`QSpinBox(minimum=0, maximum=100, suffix=\" %\")` —, a feature used in several listings."),
    h3("Geometry, minimum/maximum size and visibility"),
    p("`resize()`, `move()` and `setGeometry()` position windows; inside layouts, the layout decides the geometry "
      "(Chapter 7), respecting `setMinimumSize()`, `setMaximumSize()` and `setFixedSize()`. `show()`, `hide()` and "
      "`setVisible()` control visibility; `isVisible()` reports the effective state."),
    h3("Enabling, focus, tooltip, status tip and cursor"),
    snip('''button.setEnabled(False)                         # also disables the children
field.setFocus()                                 # receives keyboard focus
field.setToolTip("Gauge pressure, in bar")       # balloon when the mouse rests on it
action.setStatusTip("Saves the current record")  # text in the status bar (Ch. 8)
area.setCursor(Qt.CursorShape.CrossCursor)'''),
    h3("Window flags and states (Qt.WindowType, Qt.WindowState)"),
    p("For windows, `Qt.WindowType` defines the type and decoration (`Dialog`, `Tool`, `FramelessWindowHint`, "
      "`WindowStaysOnTopHint`) and `Qt.WindowState` the state (`WindowMaximized`, `WindowMinimized`, "
      "`WindowFullScreen`), also reachable through `showMaximized()` and `showFullScreen()`."),
    img("Gallery of the fundamental widgets", "f6_1_gallery.png", width_cm=14.0),
    p("Figure 6.1 is the screenshot of Listing 6.1, which gathers the widgets described in the next sections."),
    lst("c06_gallery.py", "Gallery of the fundamental widgets"),

    h2("Display widgets"),
    h3("QLabel: text, rich text, images and links"),
    p("`QLabel` displays plain text, *rich text* (a subset of HTML) or an image (`setPixmap`). With "
      "`setOpenExternalLinks(True)`, `<a href>` links open in the browser; with `setBuddy(field)`, the label's `&` "
      "shortcut moves the focus to the associated field (Chapter 7). `setWordWrap(True)` wraps long lines."),
    h3("QLCDNumber"),
    p("Displays numbers with the look of a seven-segment display. `display()` accepts `int`, `float` or `str`; "
      "`setDigitCount()` sets the number of digits and `setMode()` the base (decimal, hexadecimal, octal, binary)."),
    h3("QProgressBar"),
    p("Shows the progress of an operation between `minimum()` and `maximum()`. With minimum and maximum both 0, it "
      "enters indeterminate mode (continuous animation), useful when the total is unknown. `setFormat(\"%v of %m\")` "
      "customizes the text."),

    h2("Buttons"),
    h3("QAbstractButton and QPushButton"),
    p("`QAbstractButton` defines the common behavior: text, icon, shortcut, checkable state and the signals "
      "`clicked(bool)`, `pressed`, `released` and `toggled(bool)`. `QPushButton` is the standard command button; "
      "`setDefault(True)` makes it triggerable with the Enter key in dialogs."),
    h3("QToolButton and QCommandLinkButton"),
    p("`QToolButton` is the compact toolbar button; it can show a menu (`setMenu`) with the opening mode defined by "
      "`ToolButtonPopupMode` (`DelayedPopup`, `MenuButtonPopup`, `InstantPopup`). `QCommandLinkButton` is a large "
      "button with descriptive text, used in wizards."),
    h3("QCheckBox and QRadioButton"),
    p("`QCheckBox` represents an on/off option, with an optional third state (`setTristate`); the "
      "`checkStateChanged(Qt.CheckState)` signal reports the complete state. `QRadioButton` represents an exclusive "
      "choice: buttons with the same parent are automatically mutually exclusive."),
    h3("QButtonGroup and exclusivity"),
    p("`QButtonGroup` groups buttons logically (with no visual effect), associates an integer identifier with each "
      "one and emits `idClicked(int)`. It is the recommended way to handle a set of options with a single slot."),
    lst("c06_buttons.py", "Checkable buttons, exclusive QButtonGroup and QDialogButtonBox"),
    out("c06_buttons"),
    h3("QDialogButtonBox"),
    p("Arranges standard buttons (OK, Cancel, Apply, Save…) in the **correct order and position for each "
      "platform** — on Windows, OK is to the left of Cancel; on macOS, to the right. It emits `accepted` and "
      "`rejected` according to the button's role. Its use in dialogs is detailed in Chapter 9."),

    h2("Text entry"),
    h3("QLineEdit"),
    p("A single-line field, the most used entry widget. Its signals distinguish the origin of the change: "
      "`textEdited` is emitted only by user editing; `textChanged` also by code (`setText`); `editingFinished` when "
      "Enter is pressed or the focus is lost with acceptable content; `returnPressed` when Enter is pressed."),
    lst("c06_lineedit.py", "QLineEdit: validators, input mask, echo mode and autocompletion"),
    out("c06_lineedit"),
    h4("Echo modes and placeholder"),
    p("`EchoMode` defines what is displayed: `Normal`, `NoEcho`, `Password` and `PasswordEchoOnEdit`. The real text "
      "is still available in `text()`; `displayText()` returns what appears on screen. `placeholderText` shows a "
      "hint while the field is empty."),
    h4("Input masks (inputMask)"),
    p("The mask restricts the input character by character: `9` requires a digit, `A` requires a letter, `>` "
      "converts to upper case, and the part after `;` defines the fill character. `hasAcceptableInput()` reports "
      "whether the mask is complete."),
    h4("Validators: QIntValidator, QDoubleValidator, QRegularExpressionValidator"),
    p("A validator classifies the text into three states: `Acceptable` (valid), `Intermediate` (may become valid "
      "with more typing — for example, `700` above the maximum) and `Invalid` (blocked while typing). While the "
      "state is not `Acceptable`, `editingFinished` is not emitted."),
    note("WARNING", "`QDoubleValidator` follows the **locale**: in pt-BR, the decimal separator is the comma and "
                    "`345.5` is classified as `Intermediate`, while `345,5` is `Acceptable` (verified with the pt-BR "
                    "`QLocale`). That is why Listing 6.3 sets `QLocale.c()`. Decide consciously which convention "
                    "your application adopts and convert with `QLocale.toDouble()`."),
    h4("Autocompletion with QCompleter"),
    p("`QCompleter` suggests values from a list or a model (Chapter 14). Configure case sensitivity "
      "(`setCaseSensitivity`), filter mode (`setFilterMode`, for example `Qt.MatchFlag.MatchContains`) and "
      "presentation mode (`setCompletionMode`)."),
    h3("QTextEdit and QTextBrowser"),
    p("`QTextEdit` edits multi-line formatted text (*rich text*), based on `QTextDocument`. Use "
      "`toPlainText()`/`setPlainText()` for plain text and `toHtml()`/`setHtml()` or `toMarkdown()`/`setMarkdown()` "
      "for formatted content. `QTextBrowser` is the read-only variant with link navigation — suitable for help "
      "screens."),
    h3("QPlainTextEdit"),
    p("A plain-text editor optimized for large volumes: logs, data files, code. It is significantly more efficient "
      "than `QTextEdit` for thousands of lines; `setMaximumBlockCount(n)` limits the number of lines kept, ideal for "
      "continuous log windows."),

    h2("Numeric and range entry"),
    h3("QSpinBox and QDoubleSpinBox"),
    p("Numeric fields with arrows, limits (`minimum`, `maximum`), step (`singleStep`), prefix and suffix (unit). "
      "`QDoubleSpinBox` adds `decimals`. With `setStepType(QAbstractSpinBox.StepType.AdaptiveDecimalStepType)`, the "
      "step adapts to the order of magnitude of the value. `setKeyboardTracking(False)` makes `valueChanged` be "
      "emitted only when the edit is confirmed, not at every key."),
    h3("QSlider, QDial and QScrollBar"),
    p("All three derive from `QAbstractSlider` and work with **integers**. For real quantities, map the scale, as "
      "in Listing 6.4, which synchronizes a 0–1000 slider with a 0.0–100.0 % spin box. `sliderMoved` is emitted "
      "only while dragging; `valueChanged`, at every change of value."),
    lst("c06_numeric.py", "Synchronizing QSlider and QDoubleSpinBox; QComboBox with associated data"),
    out("c06_numeric"),
    p("The two-way synchronization does not enter an infinite loop because Qt widgets emit `valueChanged` only when "
      "the value actually changes."),

    h2("Selection in lists: QComboBox and QFontComboBox"),
    p("`QComboBox` presents a drop-down list. Each item has a text, an optional icon and **associated data** "
      "(`addItem(text, data)`, `itemData(i)`, `currentData()`), which separates what the user sees from the value "
      "used by the program — like the conversion factors of Listing 6.4. With `setEditable(True)`, it accepts free "
      "typing. `QFontComboBox` is a specialization that lists the installed fonts."),

    h2("Date and time: QDateEdit, QTimeEdit, QDateTimeEdit and QCalendarWidget"),
    p("Date and time editors work with `QDate`, `QTime` and `QDateTime`. Configure `displayFormat` (for example, "
      "`\"yyyy-MM-dd\"`), limits (`setMinimumDate`, `setMaximumDate`) and `calendarPopup=True` to open a calendar. "
      "`QCalendarWidget` is the full calendar, embeddable in any layout."),

    h2("Grouping widgets and frames: QGroupBox, QFrame, QToolBox and QTabWidget"),
    p("`QGroupBox` groups widgets with a frame and a title — and can be checkable, enabling or disabling all of its "
      "content. `QFrame` draws lines and frames (`setFrameShape`). `QToolBox` organizes pages into expandable "
      "sections and `QTabWidget` into tabs; both allow long forms without scrolling."),

    h2("Capturing shortcuts: QKeySequenceEdit"),
    p("`QKeySequenceEdit` captures a key combination typed by the user and makes it available as a `QKeySequence` — "
      "the widget used in screens for configuring custom shortcuts."),
    tab("Fundamental widgets and their main signals", ["Widget", "Main signals", "Typical use"],
        [["QPushButton", "clicked, pressed, released, toggled", "Trigger an action: calculate, save, open"],
         ["QLineEdit", "textChanged, textEdited, editingFinished, returnPressed", "Short text: tags, names, validated values"],
         ["QSpinBox", "valueChanged, textChanged", "Bounded integers: quantities, counts"],
         ["QComboBox", "currentIndexChanged, currentTextChanged, activated", "Choice from a closed list: material, unit"],
         ["QSlider", "valueChanged, sliderMoved, sliderReleased", "Continuous visual adjustment: opening, zoom"],
         ["QCheckBox", "checkStateChanged, toggled", "On/off option: include safety margin"]],
        [2200, 4371, 2500]),

    h2("Chapter exercises"),
    nl("Create a tag field in the format `AA-9999` with `QRegularExpressionValidator` and conversion to upper case.",
       "Implement a pressure-unit converter with `QDoubleSpinBox` and `QComboBox` using `currentData()`.",
       "Use `QButtonGroup` to select the design code among three options and show the choice in a `QLabel`.",
       "Build a log window with `QPlainTextEdit` limited to 500 lines, fed by a `QTimer`.",
       "Explain, with an example, the difference between the `textChanged` and `textEdited` signals."),
)

CAP07 = flat(
    ch("Layouts and geometry management", ST_BAS, [
        "Replace absolute positioning with layout managers.",
        "Combine nested layouts for responsive interfaces.",
        "Control resizing with QSizePolicy, stretch and QSplitter.",
    ]),
    h2("Why use layouts"),
    p("Positioning widgets with fixed coordinates (`move`, `setGeometry`) breaks easily: larger fonts, translation "
      "into another language, High-DPI scaling or simply resizing the window leave texts cut off and space wasted. "
      "**Layout managers** compute the geometry automatically from the preferred size of each widget (`sizeHint`), "
      "its size policies and the available space, and recompute everything whenever something changes."),
    note("TIP", "Installing a layout on a widget is simple: pass the widget to the layout's constructor "
                "(`QVBoxLayout(self)`) or call `self.setLayout(layout)`. Widgets added to the layout are "
                "automatically reparented to the widget that owns it."),

    h2("Box layouts: QHBoxLayout and QVBoxLayout"),
    p("`QHBoxLayout` lines items up horizontally and `QVBoxLayout` vertically. Items can be widgets (`addWidget`), "
      "other layouts (`addLayout`), fixed spaces (`addSpacing`) or elastic ones (`addStretch`)."),
    lst("c07_boxes.py", "QHBoxLayout and QVBoxLayout: margins, spacing, stretch and alignment"),
    out("c07_boxes"),
    h3("Margins, spacing and alignment"),
    p("`setContentsMargins(left, top, right, bottom)` defines the space between the widget's border and the items; "
      "`setSpacing()` the space between items. The `alignment` parameter of `addWidget` aligns an item inside its "
      "cell without stretching it — like the `Rev. 0` label, kept to the right."),
    h3("Stretch factors and QSpacerItem"),
    p("The *stretch* factor distributes extra space proportionally. In Listing 7.1, the `QTextEdit` has stretch 1 "
      "and the other items 0: all additional vertical space goes to it, as the output shows — when the window grew "
      "by 200 px, the editor grew by exactly 200 px. An `addStretch()` before the buttons creates an elastic "
      "`QSpacerItem` that pushes them to the right."),
    img("Behavior of QHBoxLayout and QVBoxLayout", "f7_1_boxes.png"),

    h2("QGridLayout"),
    p("Arranges items in rows and columns. `addWidget(w, row, column)` places an item in a cell and "
      "`addWidget(w, row, column, rowSpan, colSpan)` merges cells."),
    lst("c07_grid.py", "QGridLayout: numeric keypad with merged cells (row/column span)"),
    out("c07_grid"),
    h3("Rows, columns and merged cells (span)"),
    p("The display takes the whole of row 0 (1 row × 4 columns) and the `0` button takes two columns of the last "
      "row. `getItemPosition()` returns the position and *spans* of any item, useful in interfaces generated by "
      "code."),
    h3("Row and column stretch"),
    p("`setColumnStretch(c, factor)` and `setRowStretch(r, factor)` control how extra space is distributed among "
      "columns and rows; `setColumnMinimumWidth()` guarantees a minimum width."),

    h2("QFormLayout"),
    p("A two-column layout specialized in forms: labels on the left, fields on the right. `addRow(text, field)` "
      "creates the label and associates it with the field as a **buddy** — the `&` in the text defines an "
      "Alt+letter shortcut that moves the focus to the field. In addition, `QFormLayout` automatically adopts the "
      "label alignment expected on each platform."),
    lst("c07_form.py", "QFormLayout: aligned labels and fields, with wrapping and growth policies"),
    out("c07_form"),
    h3("Row wrapping and field growth policies"),
    p("`RowWrapPolicy` decides when the label goes above the field (`DontWrapRows`, `WrapLongRows`, `WrapAllRows`) — "
      "useful on narrow screens. `FieldGrowthPolicy` decides which fields stretch (`FieldsStayAtSizeHint`, "
      "`ExpandingFieldsGrow`, `AllNonFixedFieldsGrow`)."),

    h2("QStackedLayout and QStackedWidget"),
    p("They stack several pages and show one at a time (`setCurrentIndex`). They provide no navigation of their own: "
      "combine them with a list, a `QComboBox` or buttons. `QStackedWidget` is the ready-made widget that uses a "
      "`QStackedLayout` internally; it is the basis of settings screens and custom wizards."),

    h2("Nested layouts"),
    p("Real interfaces combine layouts: each `QGroupBox` has its own layout, and an outer layout arranges them. "
      "Listing 7.4 builds a pipe-check screen with four levels: main column (`QVBoxLayout`), input form "
      "(`QFormLayout`), results grid (`QGridLayout`) and row of buttons (`QHBoxLayout`)."),
    lst("c07_composition.py", "Composition with nested layouts"),
    out("c07_composition"),
    img("Example of composition with nested layouts", "f7_2_composition.png", width_cm=10.5),
    p("The results shown are calculated by the listing itself — D/t, inside diameter and the Barlow pressure "
      "P = 2·SMYS·t/OD with the input values (OD = 273.1 mm, t = 12.7 mm, SMYS = 448 MPa) —, and the output confirms "
      "that the labels are consistent with the calculation. In Chapter 8, these values are recalculated at every "
      "change of a field."),

    h2("Size policies"),
    h3("sizeHint() and minimumSizeHint()"),
    p("Each widget tells the layout its preferred size (`sizeHint()`) and the smallest reasonable size "
      "(`minimumSizeHint()`). In custom widgets, override these methods so that the layout sizes them correctly."),
    h3("QSizePolicy"),
    p("The size policy tells the layout how to interpret the `sizeHint` in each direction, and the policy's "
      "*stretch factor* breaks ties between widgets that want to grow."),
    tab("Values of QSizePolicy.Policy", ["Policy", "Behavior"],
        [["Fixed", "sizeHint() is the only acceptable size."],
         ["Minimum", "sizeHint() is the minimum; it may grow, with no benefit in growing."],
         ["Maximum", "sizeHint() is the maximum; it may shrink."],
         ["Preferred", "sizeHint() is the preferred size; it may grow or shrink."],
         ["MinimumExpanding", "sizeHint() is the minimum; it takes advantage of extra space."],
         ["Expanding", "sizeHint() is sensible; it wants as much space as possible."],
         ["Ignored", "sizeHint() is ignored; it receives as much space as possible."]],
        [2600, 6471]),
    snip('''from PyQt6.QtWidgets import QSizePolicy

chart.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)'''),

    h2("QSplitter"),
    p("`QSplitter` divides the space between widgets with handles that the user drags. `setStretchFactor()` defines "
      "how extra space is shared when resizing, `setSizes()` sets initial sizes and `saveState()`/`restoreState()` "
      "let you remember the split chosen by the user between sessions (Chapter 8)."),
    lst("c07_stack_splitter.py", "QStackedWidget, QSplitter and QScrollArea"),
    out("c07_stack_splitter"),

    h2("QScrollArea"),
    p("Wraps a widget larger than the available space, adding scroll bars. Use `setWidget()` with a widget that "
      "already has its layout and, almost always, `setWidgetResizable(True)`, so that the content follows the width "
      "of the area. Without this call, the content keeps the size of its `sizeHint` at the moment it was inserted."),

    h2("Chapter exercises"),
    nl("Reproduce Figure 7.1 and change the stretch so that the editor and the top label share the extra space 3:1.",
       "Complete the keypad of Listing 7.2 by evaluating the expression when `=` is clicked (use `ast` to evaluate "
       "safely).",
       "Adapt Listing 7.4 to recalculate the results at every `valueChanged` of the fields.",
       "Create a settings screen with `QListWidget` + `QStackedWidget` in a `QSplitter` whose split is saved with "
       "`QSettings`."),
)
