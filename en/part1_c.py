# -*- coding: utf-8 -*-
"""Part I — Chapters 8 to 10 (English edition)."""
from blocks import ST_BAS, bl, ch, flat, h2, h3, img, lst, nl, note, out, p, snip, tab

CAP08 = flat(
    ch("Main window: QMainWindow", ST_BAS, [
        "Build the complete structure of a main window.",
        "Create reusable actions in menus, toolbars and shortcuts.",
        "Persist the window's geometry and state between sessions.",
    ]),
    p("This chapter is built around a single listing — a test log with every area of the main window. Each section "
      "comments on a part of it."),
    lst("c08_main_window.py", "Complete main window: actions, menus, toolbar, docks and QSettings"),
    out("c08_main_window"),

    h2("Anatomy of QMainWindow"),
    p("`QMainWindow` has its own layout, with reserved regions. That is why **you do not install a layout on it**: "
      "the content goes into the central widget (`setCentralWidget`), and the other elements are added through "
      "specific methods."),
    img("Areas of QMainWindow", "f8_1_mainwindow.png"),
    p("Figure 8.1 is the screenshot of Listing 8.1. The menu bar and status bar are created on demand at the first "
      "call to `menuBar()` and `statusBar()`."),

    h2("Actions: QAction and QActionGroup"),
    p("An **action** represents a user command regardless of where it appears. The same `QAction` can be in the "
      "menu, in the toolbar and in a context menu: text, icon, shortcut, enabled state and checked state stay "
      "synchronized everywhere. Its main signal is `triggered(bool)`."),
    h3("Text, icon, tooltip and status tip"),
    p("The `&` in the text defines the access key in the menu (Alt+N for `&New`). In Listing 8.1, the icons come "
      "from `QStyle.standardIcon()`, available on any platform; in real applications, use your own SVG icons or, on "
      "Qt 6.7 or later, theme icons through `QIcon.fromTheme(QIcon.ThemeIcon.DocumentOpen)`. The `statusTip` "
      "appears in the status bar when the mouse passes over the action."),
    h3("Shortcuts with QKeySequence and QShortcut"),
    p("Prefer `QKeySequence.StandardKey` (`New`, `Open`, `Save`, `Copy`, `Undo`…): Qt translates it to the "
      "conventional shortcut of each platform (Ctrl+S on Windows/Linux, ⌘S on macOS). For shortcuts without a "
      "visible action, use `QShortcut(QKeySequence(\"Ctrl+Shift+D\"), self, self.debug)`."),
    h3("Checkable actions and exclusive groups"),
    p("With `checkable=True`, the action keeps an on/off state and emits `toggled(bool)` — like *Word wrap*. A "
      "`QActionGroup` (exclusive by default) makes a set of checkable actions behave like radio buttons, and its "
      "`triggered(QAction)` signal tells which one was chosen — like the *Units* submenu."),

    h2("Menus: QMenuBar and QMenu"),
    h3("Submenus and separators"),
    p("`menuBar().addMenu(\"&File\")` creates a menu; `addAction`/`addActions` inserts actions; `addSeparator()` "
      "groups them visually; `menu.addMenu(...)` creates submenus. The *Panels* menu receives the "
      "`toggleViewAction()` of each dock: a ready-made, checkable action that shows and hides the panel."),
    h3("Context menus"),
    p("There are two ways to offer a context menu (right click): set `ContextMenuPolicy.ActionsContextMenu` and add "
      "actions to the widget, or — more flexible — `CustomContextMenu` and handle the "
      "`customContextMenuRequested(QPoint)` signal, building a `QMenu` according to the clicked item. The position "
      "received is in the widget's coordinates and must be converted to global coordinates (`mapToGlobal`) before "
      "`menu.exec()`."),

    h2("Toolbars: QToolBar"),
    p("`QToolBar` shows actions as buttons. The user can move it between the allowed areas (`setAllowedAreas`), "
      "detach it (`setFloatable`) or it can be pinned (`setMovable(False)`). `setToolButtonStyle()` chooses between "
      "icon only, text only or both. Every toolbar must have an `objectName` so that `saveState()` can store its "
      "position."),

    h2("Status bar: QStatusBar"),
    p("Temporary messages are shown with `showMessage(text, ms)`. Permanent widgets (`addPermanentWidget`) stay on "
      "the right and are not covered by messages — like the line counter of the listing. `addWidget` inserts normal "
      "widgets on the left."),

    h2("Dock widgets: QDockWidget"),
    p("Docks are panels that the user can move between the edges of the window, stack in tabs, detach as floating "
      "windows or close. `setAllowedAreas()` restricts the allowed edges; `setFeatures()` controls whether it can be "
      "moved, closed or float; the window's `setDockOptions()` enables nesting and tabs (`AllowNestedDocks`, "
      "`AllowTabbedDocks`). Like toolbars, each dock needs an `objectName`."),

    h2("Central widget, tabs and MDI"),
    h3("QTabWidget as the central area"),
    p("A `QTabWidget` as the central widget is the typical arrangement of applications with several documents. In "
      "the listing, `documentMode=True` gives a cleaner look and `tabsClosable=True` shows the close button, whose "
      "`tabCloseRequested(int)` signal is connected to `removeTab`."),
    h3("QMdiArea and QMdiSubWindow"),
    p("The classic alternative is the multiple-document interface (MDI): `QMdiArea` as the central widget and each "
      "document in a `QMdiSubWindow`, with internal windows that can be tiled (`tileSubWindows`) or cascaded "
      "(`cascadeSubWindows`). Useful when the user needs to compare documents side by side."),
    snip('''from PyQt6.QtWidgets import QMdiArea, QTextEdit

area = QMdiArea()
self.setCentralWidget(area)
sub = area.addSubWindow(QTextEdit())
sub.setWindowTitle("Test 1")
sub.show()
area.tileSubWindows()'''),

    h2("Persisting state with QSettings"),
    p("`QSettings` stores key–value pairs in the standard location of each platform: the Windows Registry, `.plist` "
      "files on macOS and INI files in `~/.config` on Linux. The organization/application pair identifies the set "
      "of settings. Listing 8.1 stores them in `closeEvent` and restores them in the constructor, and the output "
      "proves the cycle: on the first opening there is no state; after closing, the second opening restores "
      "geometry and state."),
    h3("saveGeometry() and restoreGeometry()"),
    p("They store the window's size, position, maximized state and screen. `restoreGeometry()` adjusts the window "
      "if the original screen no longer exists (for example, a disconnected monitor)."),
    h3("saveState() and restoreState()"),
    p("They store the arrangement of toolbars and docks. The optional `version` parameter lets you discard states "
      "saved by older versions of the interface, when the dock structure changes."),
    note("WARNING", "Without an `objectName` on each `QToolBar` and `QDockWidget`, Qt prints a warning and cannot "
                    "restore the position of these elements."),

    h2("Splash screen: QSplashScreen"),
    p("Applications that take time to start should show a splash screen. `showMessage()` displays the progress, "
      "`app.processEvents()` keeps the screen updated during synchronous work, and `finish(window)` closes the "
      "splash when the main window appears."),
    lst("c08_splash.py", "QSplashScreen during start-up"),
    out("c08_splash"),

    h2("Chapter exercises"),
    nl("Add to Listing 8.1 the *Open* action (`StandardKey.Open`) with a `QFileDialog` and a *Help → About* menu.",
       "Create a second dock with a `QTextEdit` for remarks and allow it to be stacked in tabs with the first one.",
       "Store in `QSettings` the unit system chosen in the `QActionGroup` and restore it at start-up.",
       "Replace the central `QTabWidget` with a `QMdiArea` and add actions to arrange the subwindows."),
)

CAP09 = flat(
    ch("Dialogs", ST_BAS, [
        "Distinguish modal and modeless dialogs.",
        "Use Qt's standard dialogs.",
        "Create custom dialogs and wizards with validation.",
    ]),
    h2("QDialog: modal and modeless"),
    p("A **dialog** is a secondary window for a short task: confirm, choose, fill in data. A **modal** dialog blocks "
      "interaction with the other windows until it is closed; a **modeless** one coexists with the main window (for "
      "example, a *Find* box)."),
    h3("exec(), open() and show()"),
    tab("Ways of showing a QDialog", ["Method", "Modality", "Return"],
        [["exec()", "Application modal; starts a local event loop", "Blocks the code until closed and returns the result code"],
         ["open()", "Modal to the parent window (window modal)", "Returns immediately; the result arrives through the finished(int) signal"],
         ["show()", "Modeless (by default)", "Returns immediately; the dialog coexists with the main window"]],
        [1600, 3471, 4000]),
    p("`exec()` is the simplest to use, since the code continues only after the answer. `open()` is preferable in "
      "applications with several windows: it does not create a nested event loop and, on macOS, shows the dialog as "
      "a *sheet* attached to the parent window."),
    h3("accept(), reject() and the result code"),
    p("`accept()` closes the dialog with the result `QDialog.DialogCode.Accepted` (1) and `reject()` with `Rejected` "
      "(0); the Esc key and the close button call `reject()`. The `accepted`, `rejected` and `finished(int)` signals "
      "report the closing."),

    h2("QMessageBox"),
    p("Standard message box to inform, warn, confirm or report errors."),
    lst("c09_messagebox.py", "QMessageBox: static methods and a customized box"),
    out("c09_messagebox"),
    h3("Static methods: information, question, warning, critical, about"),
    p("The static methods create, show and destroy the box in one line, returning the chosen button "
      "(`QMessageBox.StandardButton`). In destructive operations, make the **safe** option the default "
      "(`defaultButton=No`), so that an accidental Enter does not erase data. Closing the box with Esc is equivalent "
      "to the escape button — in the listing, `No`."),
    h3("Standard and custom buttons"),
    p("For full control, create the instance: main text, informative text, icon, detailed (expandable) text and "
      "standard or custom buttons (`addButton(text, role)`). Listing 9.1 simulates the click on *Discard* with a "
      "`QTimer` only so that the example runs without intervention."),
    note("NOTE", "The texts of the standard buttons (OK, Cancel, Save…) and of Qt's dialogs appear in English unless "
                 "Qt's own translations are loaded with `QTranslator` — the topic of Chapter 13. Figure 9.1 shows the "
                 "dialogs untranslated."),

    h2("Standard dialogs"),
    img("Qt standard dialogs", "f9_1_dialogs.png", width_cm=15.0),
    h3("QFileDialog"),
    p("Selection of files and folders. The static methods `getOpenFileName`, `getOpenFileNames`, `getSaveFileName` "
      "and `getExistingDirectory` return a tuple `(path, chosen_filter)` — an empty path if the user cancels. By "
      "default, Qt uses the system's **native** dialog; the `DontUseNativeDialog` option forces Qt's own dialog "
      "(Figure 9.1), which can be customized."),
    snip('''path, _ = QFileDialog.getOpenFileName(
    self, "Open test", str(Path.home()), "Tests (*.json *.csv);;All (*)")
if path:                         # empty string = canceled
    self.load(Path(path))'''),
    h3("QColorDialog and QFontDialog"),
    p("`QColorDialog.getColor(initial, parent)` returns a `QColor` (check `isValid()`, false if canceled). "
      "`QFontDialog.getFont(initial, parent)` returns the tuple `(QFont, ok)`."),
    h3("QInputDialog"),
    p("Collects a single value: `getText`, `getInt`, `getDouble`, `getItem` (list) and `getMultiLineText`. All of "
      "them return `(value, ok)`; `getDouble` accepts minimum, maximum, decimals and step."),
    h3("QProgressDialog"),
    p("Shows the progress of a long operation with a cancel button. `setMinimumDuration(ms)` avoids showing the "
      "dialog for quick operations; `wasCanceled()` tells whether the user canceled. With `autoReset` on (the "
      "default), when the maximum is reached the dialog is reset and `value()` goes back to −1 — behavior visible "
      "in the output of Listing 9.2."),
    lst("c09_standard.py", "Standard dialogs: QInputDialog, QProgressDialog and QFileDialog (non-native)"),
    out("c09_standard"),
    note("WARNING", "The loop in Listing 9.2 calls `processEvents()` to keep the dialog responsive, but the work still "
                    "runs in the interface thread. For really long tasks, use a worker thread (Chapter 20) and update "
                    "the progress through signals."),
    h3("QErrorMessage"),
    p("An error dialog with the *Show this message again* check box: messages the user chose to hide do not appear "
      "again during the session. Useful for repetitive, non-critical warnings."),

    h2("Custom dialogs"),
    h3("Composition with QDialogButtonBox"),
    p("A custom dialog is a `QDialog` subclass with a layout of fields and a `QDialogButtonBox`, whose `accepted` "
      "and `rejected` signals are connected to `accept()` and `reject()`. After `exec()`, the caller reads the data "
      "through a method of the dialog — preferably returning a data object (`dataclass`), not the widgets."),
    lst("c09_dialog.py", "Custom dialog with QDialogButtonBox and validation before accept()"),
    out("c09_dialog"),
    note("TIP", "Do not name the data method `result()`: `QDialog` already has a `result()` method, which returns "
                "the result code. That is why the listing uses `result_data()`."),
    h3("Validating data before accept()"),
    p("Reimplementing `accept()` is the most robust way to validate: the dialog closes only with valid data, "
      "regardless of how the user confirmed (button, Enter). In the listing, the first attempt without a tag keeps "
      "the dialog open and shows the message; the second, valid one closes it and delivers the `PressureTest` "
      "object. A complementary alternative is to disable the OK button while the form is incomplete."),

    h2("Wizards: QWizard and QWizardPage"),
    p("`QWizard` guides the user through a sequence of pages (`QWizardPage`) with Back/Next/Finish buttons. "
      "`registerField(\"name*\", widget)` registers a field accessible on every page through `field(\"name\")`; the "
      "asterisk makes the field mandatory, disabling *Next* while it is empty. `initializePage()` is called when "
      "entering each page — the place to build summaries."),
    lst("c09_wizard.py", "QWizard with registered fields (registerField) and chained pages"),
    out("c09_wizard"),

    h2("Chapter exercises"),
    nl("Create a *Preferences* dialog with `QDialogButtonBox` (OK, Cancel, Apply) that applies the changes only when "
       "OK or Apply is clicked.",
       "Modify Listing 9.3 to disable OK while the tag is empty, without reimplementing `accept()`.",
       "Use `QFileDialog.getSaveFileName` to save the result of the test dialog as JSON.",
       "Add to the wizard of Listing 9.4 a conditional page shown only when the units are *Imperial* (`nextId()`)."),
)

CAP10 = flat(
    ch("Events", ST_BAS, [
        "Understand how events are generated, dispatched and propagated.",
        "Reimplement event handlers and install filters.",
        "Implement drag and drop and use of the clipboard.",
    ]),
    h2("The event system"),
    p("Signals report that *something happened in an object*; **events** are the low-level raw material those "
      "signals come from: a click is a `QMouseEvent` delivered to the button, which, when handling it, emits "
      "`clicked`. Handling events directly is necessary when you create your own widget, when you want to change "
      "the default behavior of a widget or react to something for which there is no signal."),
    h3("QEvent and event types"),
    p("Every event is an object of a `QEvent` subclass with a type (`QEvent.Type`): `MouseButtonPress`, `KeyPress`, "
      "`Resize`, `Paint`, `Close`, `FocusIn`, `Timer`… They are produced by the operating system (through the "
      "platform plugin), by Qt itself (timers, repainting) or by the application (`postEvent`, `sendEvent`)."),
    h3("Propagation, accept() and ignore()"),
    p("Every event carries an acceptance flag. Input events (mouse, keyboard, wheel) that a widget **ignores** are "
      "sent again to the parent widget, going up the tree until someone accepts them. When overriding a handler, "
      "call the base-class implementation for what you do not handle — it decides correctly between accepting and "
      "propagating."),
    img("Path of an event from the operating system to the widget", "f10_1_events.png"),

    h2("Reimplementing handlers"),
    p("Each event type has a virtual method in `QWidget` that can be overridden. Listing 10.1 implements several of "
      "them and uses the `QtTest` module to generate real mouse and keyboard events — the same technique as the "
      "automated tests of Chapter 28."),
    lst("c10_handlers.py", "Reimplementing event handlers (mouse, keyboard, window)"),
    out("c10_handlers"),
    h3("Mouse: mousePressEvent, mouseMoveEvent, mouseReleaseEvent, wheelEvent"),
    p("`event.position()` returns the position in the widget's coordinates as a `QPointF` (use `globalPosition()` "
      "for screen coordinates); `button()` gives the button that caused the event and `buttons()` all the buttons "
      "pressed at that moment. By default, `mouseMoveEvent` is received only with a button pressed; to receive free "
      "movements, turn on `setMouseTracking(True)`. `wheelEvent` reports the rotation in `angleDelta()` (units of "
      "1/8 degree; a typical step is 120)."),
    h3("Keyboard: keyPressEvent and keyReleaseEvent"),
    p("Only the widget with **focus** receives keyboard events; custom widgets need `setFocusPolicy()`. "
      "`event.key()` returns a `Qt.Key`, `event.modifiers()` the modifier keys and `event.text()` the generated "
      "text. Unhandled keys must be passed on to `super().keyPressEvent(e)`, so that shortcuts and navigation keep "
      "working."),
    h3("Window: resizeEvent, moveEvent, showEvent and closeEvent"),
    p("`resizeEvent` reports the old and the new size (the first one, before the window is shown, has the invalid "
      "old size −1×−1, as in the output). `closeEvent` is the place to confirm closing: `event.ignore()` keeps the "
      "window open and makes `close()` return `False`."),
    h3("Focus and hover: focusInEvent, enterEvent and leaveEvent"),
    p("`focusInEvent`/`focusOutEvent` follow the keyboard focus (useful to validate when leaving the field). "
      "`enterEvent` (which in Qt 6 receives a `QEnterEvent`, with a position) and `leaveEvent` follow the cursor "
      "entering and leaving, the basis for *hover* effects in custom widgets."),

    h2("Event filters: installEventFilter()"),
    p("An **event filter** is an object that intercepts the events meant for another one, before the latter "
      "receives them, without the need for a subclass. `eventFilter(obj, ev)` returns `True` to **consume** the "
      "event or `False` to let it continue. A single filter can watch several objects, and a filter installed on "
      "the `QApplication` itself sees every event of every object (use sparingly, because of the cost)."),
    lst("c10_filter.py", "Event filter: one object watches and intercepts the events of another"),
    out("c10_filter"),
    note("TIP", "To restrict characters in text fields, a validator (Chapter 6) is usually the simplest solution. "
                "Filters are suited to cross-cutting behaviors: global shortcuts, activity logging, temporary "
                "blocking of interaction."),

    h2("Custom events: postEvent() and sendEvent()"),
    p("The application can create its own event types, numbered from `QEvent.Type.User` onwards with "
      "`QEvent.registerEventType()`, which guarantees an unused identifier. `postEvent()` **queues** the event "
      "(delivered by the event loop, asynchronously and safely across threads); `sendEvent()` delivers it "
      "**immediately**, synchronously. The output of Listing 10.3 shows the difference in the order of execution."),
    lst("c10_custom_event.py", "Custom events: registerEventType, postEvent (asynchronous) and sendEvent"),
    out("c10_custom_event"),
    p("In most cases, custom signals handle communication between objects with less code; custom events are useful "
      "when you want to take advantage of Qt's event queue, filters and event compression."),

    h2("Drag and drop"),
    h3("QDrag and QMimeData"),
    p("The dragged content is packed in `QMimeData`, which can hold several formats at once (text, HTML, file URLs, "
      "images, custom formats). To **start** a drag from a custom widget, create a `QDrag` with the `QMimeData` in "
      "`mouseMoveEvent` (after the mouse has moved more than `QApplication.startDragDistance()`) and call "
      "`drag.exec(actions)`. View widgets (lists, trees, tables) already come with built-in drag support."),
    h3("dragEnterEvent, dragMoveEvent and dropEvent"),
    p("To **receive**, the widget calls `setAcceptDrops(True)` and handles `dragEnterEvent` (accept or refuse the "
      "content), optionally `dragMoveEvent` (accept only in certain regions) and `dropEvent` (process). Listing 10.4 "
      "accepts only `.csv` files and, to be runnable without interaction, generates the same events the system "
      "would send in a real drag."),
    lst("c10_drag_drop.py", "Drag and drop: a target that accepts only .csv files"),
    out("c10_drag_drop"),

    h2("Clipboard: QClipboard"),
    p("`QApplication.clipboard()` gives access to the system clipboard. `setText()`/`text()` cover the common case; "
      "`setMimeData()` publishes several formats at once, letting the target application choose the richest one it "
      "understands (for example, HTML in a text editor and plain text in a terminal). The `dataChanged` signal "
      "reports when the content changes."),
    lst("c10_clipboard.py", "Clipboard: text, MIME data and change notification"),
    out("c10_clipboard"),
    note("NOTE", "On Linux/X11 there is also the *selection* (selected text, pasted with the middle button), "
                 "accessible with `clipboard.text(QClipboard.Mode.Selection)`."),

    h2("Chapter exercises"),
    nl("Create a widget that draws a dot where the user clicks (store the positions and call `update()`; painting "
       "is detailed in Chapter 17).",
       "Modify Listing 10.1 to show the mouse coordinates in a `QLabel` using `setMouseTracking(True)`.",
       "Implement an event filter that logs every `FocusIn` of the fields of a form.",
       "Allow `.json` files to be dropped on the window of Listing 8.1 to open them in a new tab.",
       "Create a *Copy results* action that publishes plain text (CSV) and HTML (table) to the clipboard."),
)
