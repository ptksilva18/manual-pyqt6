# -*- coding: utf-8 -*-
"""Part II — Chapters 15 to 19 (English edition)."""
from blocks import ST_INT, bl, ch, flat, h2, h3, h4, img, lst, nl, note, out, p, snip, tab

CAP15 = flat(
    ch("Databases with QtSql", ST_INT, [
        "Connect to SQLite, PostgreSQL, MySQL and ODBC databases.",
        "Run safe queries with parameters and transactions.",
        "Display and edit tables with the SQL models.",
    ]),
    h2("QSqlDatabase and drivers"),
    p("QtSql offers a single API for several databases, through **drivers** (plugins). `QSqlDatabase.drivers()` "
      "lists the available ones; `addDatabase(driver, name)` creates a named connection. SQLite requires no server "
      "or external library — it is the natural choice for the local data of desktop tools."),
    tab("Qt SQL drivers and availability", ["Driver", "Database", "Plugin in the PyQt6-Qt6 6.12.0 wheels",
                                            "Remark"],
        [["QSQLITE", "SQLite 3", "Linux and Windows", "Built in; requires no external library"],
         ["QPSQL", "PostgreSQL", "Linux and Windows", "Requires the libpq client library"],
         ["QMYSQL / QMARIADB", "MySQL / MariaDB", "Linux (missing from the Windows wheel)", "Requires the MySQL/MariaDB client library"],
         ["QODBC", "ODBC sources (SQL Server etc.)", "Linux and Windows", "Requires a configured ODBC driver"],
         ["QOCI", "Oracle", "Linux and Windows", "Requires Oracle Instant Client"],
         ["QIBASE", "Firebird / InterBase", "Linux and Windows", "Requires the client library"],
         ["QMIMER", "Mimer SQL", "Linux and Windows", "Requires the client library"]],
        [1700, 2000, 2571, 2800]),
    p("The availability column was verified by inspecting the `plugins/sqldrivers` folders of the PyQt6-Qt6 6.12.0 "
      "wheels for Linux x86-64 and Windows x64. A plugin that is present still depends on the database's client "
      "library being installed on the system; otherwise, `open()` fails and `lastError()` explains why."),
    lst("c15_sqlite.py", "QtSql with SQLite: connection, DDL, prepared queries, transactions and errors"),
    out("c15_sqlite"),

    h2("QSqlQuery"),
    h3("Prepared queries and parameters (bindValue)"),
    p("Never build SQL by concatenating text typed by the user: use `prepare()` with named (`:tag`) or positional "
      "(`?`) placeholders and `bindValue()`/`addBindValue()`. Besides preventing SQL injection, prepared queries "
      "are faster when repeated in a loop. Always check the return value of `exec()` — the listing centralizes this "
      "in the `execute()` function."),
    h3("Transactions"),
    p("`transaction()`, `commit()` and `rollback()` group operations: either all of them are written, or none. "
      "Besides consistency, inserting thousands of rows inside a transaction is orders of magnitude faster in "
      "SQLite."),
    h3("Error handling with QSqlError"),
    p("`lastError()` returns a `QSqlError` with the type, the driver's text (`driverText`), the database's text "
      "(`databaseText`) and the native code (`nativeErrorCode`). The type classification varies between drivers — "
      "in the output, the `UNIQUE` violation in SQLite was classified as `ConnectionError` —, so, to decide what to "
      "do, rely on the native code and on the database's text."),
    note("WARNING", "To close a named connection, finish and discard every query and the `QSqlDatabase` object "
                    "before calling `QSqlDatabase.removeDatabase(name)`, as at the end of Listing 15.1; otherwise, Qt "
                    "warns that the connection is still in use."),

    h2("SQL models"),
    lst("c15_sql_models.py", "SQL models: QSqlQueryModel, QSqlTableModel (editing) and QSqlRelationalTableModel"),
    out("c15_sql_models"),
    h3("QSqlQueryModel"),
    p("A read-only model for the result of any `SELECT`, ready for a `QTableView`. For computed columns or "
      "formatting, combine it with a proxy (Chapter 14)."),
    h3("QSqlTableModel and edit strategies"),
    p("An editable model of a table. The **edit strategy** defines when the changes go to the database: "
      "`OnFieldChange` (at every field), `OnRowChange` (when the row changes) or `OnManualSubmit` (only on "
      "`submitAll()`, with `revertAll()` to discard). The last one is the best fit for forms with *Save*/*Cancel* "
      "buttons. `setFilter()` and `setSort()` restrict and order the query."),
    h3("QSqlRelationalTableModel and QSqlRelationalDelegate"),
    p("Resolves foreign keys: `setRelation(column, QSqlRelation(table, key, display))` makes the `kind_id` column "
      "show the name of the kind, and `QSqlRelationalDelegate` offers a `QComboBox` with the valid options while "
      "editing."),

    h2("Database integration through an ORM (SQLAlchemy) versus QtSql"),
    p("Libraries such as **SQLAlchemy** map tables to Python classes, generate portable SQL and handle schema "
      "migrations (with Alembic), but they do not talk directly to Qt's views. **QtSql** integrates natively with "
      "Model/View, but works in SQL and with Qt types. A rule of thumb: for screens centered on editable tables, "
      "QtSql; for complex business rules, many relationships and code shared with services without an interface, an "
      "ORM in the services layer, exposed to the interface through your own models (Chapter 14)."),

    h2("Chapter exercises"),
    nl("Create an SQLite database in a file (in `QStandardPaths.StandardLocation.AppDataLocation`) with the test and "
       "kind tables.",
       "Implement a search by tag with a prepared query and `LIKE`, showing the result in a `QSqlQueryModel`.",
       "Build a screen with `QSqlTableModel` in `OnManualSubmit` and *Save* and *Discard* buttons.",
       "Measure the time to insert 10,000 rows with and without a transaction and explain the difference."),
)

CAP16 = flat(
    ch("Files, data and processes", ST_INT, [
        "Read and write text and binary files safely.",
        "Work with JSON, XML and CSV.",
        "Watch files and run external processes.",
    ]),
    h2("QFile, QTextStream, QDataStream and QSaveFile"),
    p("Python already offers `open()` and `pathlib`, which are enough in most cases. The Qt classes are useful when "
      "you want integration with the rest of the API (search prefixes, `QIODevice` for networking and processes) or "
      "specific features, such as the **atomic saving** of `QSaveFile`: the data goes to a temporary file and "
      "replaces the original only on `commit()` — a power failure in the middle of the write does not corrupt the "
      "existing file."),
    lst("c16_files.py", "QSaveFile + QTextStream (text) and QDataStream (versioned binary)"),
    out("c16_files"),
    p("Two details of the output: `QTextStream` wrote `345.0` as `345`, since by default it uses the shortest "
      "notation — format numbers explicitly when the format matters; and the binary file has exactly 48 bytes (4 "
      "for the magic number, 16 for the UTF-16 string with its length prefix, 4 for the count and 3 × 8 for the "
      "`double` values). Pinning `setVersion()` guarantees that files written today will be read by future Qt "
      "versions."),

    h2("JSON: QJsonDocument versus the json module"),
    p("For JSON, Python's `json` module is the simplest and most idiomatic choice. `QJsonDocument` is of interest "
      "when the JSON arrives as a `QByteArray` from a network reply (Chapter 21) or must be handed to Qt APIs."),
    lst("c16_json_xml.py", "JSON (json module and QJsonDocument) and XML (QXmlStreamWriter/Reader and QtXml DOM)"),
    out("c16_json_xml"),

    h2("XML"),
    h3("QXmlStreamReader and QXmlStreamWriter (QtCore)"),
    p("Sequential (*streaming*) reading and writing: they use little memory and suit large files. They are the API "
      "recommended by Qt for XML."),
    h3("DOM with the QtXml module"),
    p("`QDomDocument` loads the whole tree into memory and allows free navigation and modification — convenient for "
      "small configuration files. For new reading code, prefer the stream reader."),

    h2("CSV and integration with pandas"),
    p("The `csv` module handles simple files. For analysis, **pandas** reads and converts types in one go — including "
      "decimals with a comma (`decimal=\",\"`, common in European and Brazilian files) and dates — and a generic "
      "model of a few lines shows any `DataFrame` in a `QTableView`."),
    lst("c16_csv_pandas.py", "CSV with the csv module and with pandas, shown in a QTableView by a generic model"),
    out("c16_csv_pandas"),
    p("With the `csv` module, the values arrive as text (`'345,0'`); with pandas, already as `float64` and "
      "`datetime64`. The output was obtained with pandas 3.0.5, in which text columns have the `str` type."),

    h2("QFileSystemWatcher"),
    p("Watches files and folders and emits `fileChanged`/`directoryChanged` when they change — useful to reload "
      "parameters edited externally or to detect new acquisition files. Some editors save by creating a new file and "
      "renaming it; in that case, the file is no longer watched and must be added again in the slot."),
    lst("c16_watcher_process.py", "QFileSystemWatcher and QProcess (synchronous and asynchronous execution)"),
    out("c16_watcher_process"),

    h2("QProcess: running external programs"),
    h3("Synchronous and asynchronous execution"),
    p("`QProcess` runs external programs — solvers, converters, scripts. The **synchronous** mode "
      "(`waitForFinished()`) blocks the event loop and is acceptable only for quick commands. The **asynchronous** "
      "mode keeps the interface responsive: the output arrives through `readyReadStandardOutput` and the end through "
      "`finished(code, status)`. Pass the program and the arguments separately (`setProgram`/`setArguments`), "
      "without building command lines from user text."),
    h3("Capturing stdout/stderr and exit codes"),
    p("`readAllStandardOutput()` and `readAllStandardError()` return a `QByteArray`; decode it with the encoding of "
      "the program called. The listing's exit code 3 arrived in `finished` with the `NormalExit` status: the status "
      "tells whether the process ended normally or crashed (`CrashExit`), and the code is the result it reported. "
      "Failures to start (a program that does not exist) arrive through `errorOccurred`. The output may arrive in "
      "several chunks, one `readyReadStandardOutput` for each; that is why the listing's slot ignores empty chunks. "
      "In real programs, accumulate the chunks and process them line by line (`canReadLine()`/`readLine()`)."),

    h2("QCommandLineParser"),
    p("For applications that accept arguments — open a file, run in batch, choose units —, `QCommandLineParser` "
      "generates `--help` and `--version` automatically, validates options and separates positional arguments. "
      "`parse()` only parses; `process()` also handles `--help`/`--version` and exits the program."),
    lst("c16_command_line.py", "QCommandLineParser: options, values, positional arguments and --help"),
    out("c16_command_line"),
    note("NOTE", "In the output, `--version requested? True`: the `-v` option of the simulated command line was "
                 "interpreted as `--version`, registered by `addVersionOption()`. When creating your own options, "
                 "avoid letters already used by the standard options (`-h`, `-v`)."),

    h2("Chapter exercises"),
    nl("Save the tests of Listing 14.4 as JSON with `QSaveFile` and reload them when the application opens.",
       "Read a CSV of measurements with pandas and show it in a `QTableView` with sorting through a proxy.",
       "Run an external Python script with an asynchronous `QProcess` and show its output in a `QPlainTextEdit`.",
       "Watch a folder and automatically list the new `.csv` files that appear in it."),
)

CAP17 = flat(
    ch("2D graphics with QPainter, printing and SVG", ST_INT, [
        "Draw shapes, text and images with QPainter.",
        "Create custom widgets with paintEvent().",
        "Generate printouts, PDFs and SVG files.",
    ]),
    h2("The painting system: QPainter, QPaintDevice and QPaintEngine"),
    p("`QPainter` draws on any `QPaintDevice`: a widget (inside `paintEvent`), a `QImage`, a `QPixmap`, a printer, a "
      "`QPdfWriter` or a `QSvgGenerator`. The same drawing code serves all of them — each device's `QPaintEngine` "
      "translates the calls. This allows, for example, reusing the painting of a chart on screen and in the PDF "
      "report."),
    lst("c17_primitives.py", "QPainter on a QImage: pens, brushes, gradients, paths, transformations and text"),
    out("c17_primitives"),
    img("Primitives drawn by Listing 17.1", "f17_1_primitives.png", width_cm=9.0),

    h2("Pens, brushes and gradients"),
    h3("QPen and QBrush"),
    p("The **pen** (`QPen`) defines outlines and lines: color, width, style (`SolidLine`, `DashLine`…), cap "
      "(`PenCapStyle`) and join. The **brush** (`QBrush`) defines the fill: solid color, pattern, gradient or "
      "texture. `Qt.PenStyle.NoPen` and `Qt.BrushStyle.NoBrush` turn each one off."),
    h3("QLinearGradient, QRadialGradient and QConicalGradient"),
    p("Gradients are defined by stop points (`setColorAt(position, color)`) and used as a brush. The linear one "
      "varies along a line; the radial one, from a center; the conical one, around a center (useful in circular "
      "indicators)."),

    h2("Shapes, paths and transformations"),
    h3("Drawing primitives"),
    p("`drawLine`, `drawRect`, `drawRoundedRect`, `drawEllipse`, `drawArc`, `drawPie`, `drawPolygon`, "
      "`drawPolyline`, `drawPoint` and `drawText` cover most needs. Use the floating-point versions (`QPointF`, "
      "`QRectF`) together with `RenderHint.Antialiasing` for precise and smooth strokes."),
    h3("QPainterPath"),
    p("A path combines line segments, Bézier curves, arcs and subpaths into a single shape, which can be filled, "
      "outlined, used for clipping (`setClipPath`) or for collision detection in Chapter 18."),
    h3("QTransform and coordinate systems"),
    p("`translate`, `rotate` and `scale` change the painter's coordinate system. Wrap transformations in "
      "`save()`/`restore()` so as not to affect the rest of the drawing — as in the fan of lines of Listing 17.1. The "
      "gauge of Section 17.6 uses the same technique to draw in logical coordinates from −100 to 100, regardless of "
      "the size of the widget."),

    h2("Text: QFont, QFontMetrics and QStaticText"),
    p("`QFontMetrics` measures text before drawing it — width (`horizontalAdvance`), line height, bounding "
      "rectangle — and abbreviates long texts with `elidedText()`. `QStaticText` keeps the layout of a text that "
      "does not change, speeding up frequent repaints."),
    lst("c17_images.py", "QImage (pixels), QPixmap (display), QFontMetrics (text) and QStylePainter"),
    out("c17_images"),

    h2("Images: QImage, QPixmap, QPicture and QBitmap"),
    p("`QImage` is hardware-independent and gives direct access to the pixels — use it to process, generate and "
      "save images, including outside the interface thread. `QPixmap` is optimized for display on screen and must "
      "be created and used in the interface thread. `QBitmap` is a monochrome pixmap (masks); `QPicture` records "
      "painting commands to replay them later. Convert with `QPixmap.fromImage()` and `pixmap.toImage()`."),

    h2("Custom widgets with paintEvent()"),
    p("A custom widget inherits from `QWidget`, keeps its state in properties, draws everything in `paintEvent()` "
      "and calls `update()` when the state changes. `update()` only **schedules** the repaint — several calls in a "
      "row result in a single painting, in the next cycle of the event loop. Never call `paintEvent()` directly."),
    h3("Example: analog pressure gauge"),
    lst("c17_gauge.py", "Custom widget: analog pressure gauge drawn with QPainter"),
    out("c17_gauge"),
    img("Custom pressure-gauge widget drawn with QPainter", "f17_2_gauge.png", width_cm=12.0),
    p("The gauge exposes `value` as a `pyqtProperty` with a notification signal — that is why it can be animated in "
      "Chapter 19 and connected to any numeric signal. `sizeHint()` and `minimumSizeHint()` tell the layout the "
      "desired sizes. On the scale, the `:g` format prevents values such as 1.5 or 4.5 from being rounded to "
      "integers — a bug present in the first version of the listing and caught while reviewing Figure 17.2."),
    h3("QStylePainter and style options"),
    p("For widgets that imitate standard controls (a button with extra drawing, for example), `QStylePainter` with a "
      "filled-in `QStyleOption` (`initFrom(self)`) draws the standard parts through the current style — keeping the "
      "look consistent with the rest of the application and with the style sheets."),

    h2("Printing with QtPrintSupport"),
    h3("QPrinter, QPrintDialog and QPageSetupDialog"),
    p("`QPrinter` is a paint device: the same `QPainter` draws on it. `QPrintDialog` lets the user choose the "
      "printer and pages; `QPageSetupDialog`, the paper and margins. Configured with `setOutputFormat(PdfFormat)`, "
      "`QPrinter` writes a PDF instead of printing."),
    h3("QPrintPreviewDialog and QPrintPreviewWidget"),
    p("The preview calls, through the `paintRequested(QPrinter)` signal, the same drawing function used for "
      "printing — write the report's drawing only once, receiving the device as a parameter."),
    snip('''from PyQt6.QtPrintSupport import QPrintPreviewDialog

preview = QPrintPreviewDialog(self)
# slot signature: def draw_report(self, printer: QPrinter) -> None
preview.paintRequested.connect(self.draw_report)
preview.exec()'''),
    lst("c17_print_svg.py", "Printing to PDF (QPrinter), QPdfWriter, QSvgGenerator and QSvgRenderer"),
    out("c17_print_svg"),

    h2("Generating PDF with QPdfWriter"),
    p("`QPdfWriter` generates PDF without depending on the printing subsystem, with control of resolution, page "
      "layout, title and metadata. Coordinates are in device units: at 300 dpi, a whole A4 sheet measures about "
      "2,480 × 3,508 units, and `width()`/`height()` already subtract the layout margins — always compute the "
      "positions from these values (2,125 × 3,154 in the output of Listing 17.4, with 15 mm margins). State the unit "
      "of the margins explicitly (`QPageLayout.Unit.Millimeter`): the default is the typographic point."),

    h2("SVG: QSvgRenderer, QSvgGenerator and QSvgWidget"),
    p("`QSvgGenerator` is a device that records the `QPainter` commands as vector SVG — ideal for report figures. "
      "`QSvgRenderer` draws an SVG on any device, at any scale, and `QSvgWidget` (QtSvgWidgets module) shows it "
      "directly in a layout."),

    h2("Chapter exercises"),
    nl("Add to the gauge a mark for the maximum value recorded, resettable with a double click.",
       "Create a simple bar-chart widget with axes and labels using only `QPainter`.",
       "Generate a two-page PDF report with a header, a table of tests and the image of the gauge.",
       "Export the drawing of Listing 17.1 to SVG and reopen it with `QSvgWidget`."),
)

CAP18 = flat(
    ch("Graphics View Framework", ST_INT, [
        "Model 2D scenes with thousands of interactive items.",
        "Create custom items with collision detection.",
        "Implement zoom, pan and graphic effects.",
    ]),
    h2("Scene, view and items"),
    p("The Graphics View Framework separates the **scene** (`QGraphicsScene`), which contains and manages the items, "
      "from the **views** (`QGraphicsView`), which show it with their own zoom, rotation and scrolling. It is the "
      "right tool for interactive diagrams, process synoptics, layout editors and maps with many objects, thanks to "
      "a spatial index that quickly locates the visible items."),
    lst("c18_scene.py", "Graphics View: scene with standard and custom items, two views, collision and zoom"),
    out("c18_scene"),
    img("A QGraphicsScene shown by two QGraphicsView with different transformations", "f18_1_scene.png"),

    h2("Standard items"),
    p("The scene offers convenience methods for ready-made items: `addRect`, `addEllipse`, `addLine`, `addPath`, "
      "`addPolygon`, `addPixmap`, `addText` and `addSimpleText`. Each item has a position (`setPos`), a stacking "
      "order (`setZValue`), its own transformation and interaction flags."),

    h2("Custom items: boundingRect(), shape() and paint()"),
    p("A custom item inherits from `QGraphicsItem` — or from `QGraphicsObject`, when it needs signals and "
      "properties (for example, for animation). Three methods are essential: `boundingRect()` delimits the area the "
      "item may paint (including the outline width); `shape()` defines the exact shape used for clicks and "
      "collisions; and `paint()` draws the item in its local coordinates."),

    h2("Coordinate systems and transformations"),
    p("There are three systems: the **item's** (local), the **scene's** and the **view's** (widget pixels). "
      "Conversions are made with `mapToScene`/`mapFromScene` (items and views) and `mapToItem`. Transforming the "
      "view (`scale`, `rotate`) does not change the scene; transforming an item affects only it and its children."),

    h2("Interaction"),
    h3("Selection, movement and item flags"),
    p("Flags such as `ItemIsMovable` and `ItemIsSelectable` enable dragging and selection with the mouse, with no "
      "extra code. With `ItemSendsGeometryChanges`, the item receives `itemChange()` before each change of position "
      "and can adjust it — in the listing, the valves snap to a 10-unit grid (`setPos(213, 127)` resulted in "
      "`(210, 130)`)."),
    h3("Collision detection"),
    p("`collidingItems()` returns the items that overlap an item, using `shape()` by default; "
      "`scene.items(region)` and `scene.itemAt(point, transformation)` locate items by position. Since the valve's "
      "shape is a polygon, the collision considers the real drawing, not just the bounding rectangle."),

    h2("Zoom, pan and navigation"),
    p("Zoom is a scaling of the view (`scale()`), usually applied with the mouse wheel, as in `ZoomView`; anchor it "
      "at the cursor with `setTransformationAnchor(ViewportAnchor.AnchorUnderMouse)`. Dragging the visible area "
      "(*pan*) is enabled with `setDragMode(DragMode.ScrollHandDrag)`; `fitInView()` frames a whole region."),

    h2("Widgets in the scene: QGraphicsProxyWidget and QGraphicsWidget"),
    p("`scene.addWidget(widget)` inserts an ordinary widget into the scene through a `QGraphicsProxyWidget` — the "
      "text field of Figure 18.1 remains editable and follows the view's transformations. `QGraphicsWidget` is the "
      "base for items whose geometry is managed by the scene's own layouts (`QGraphicsLinearLayout`, "
      "`QGraphicsGridLayout`)."),

    h2("Effects: QGraphicsBlurEffect, QGraphicsDropShadowEffect, QGraphicsOpacityEffect and QGraphicsColorizeEffect"),
    p("Graphic effects apply to items and also to ordinary widgets (`setGraphicsEffect`): blur, drop shadow, "
      "opacity and colorization. Each item or widget accepts a single effect. They are processed in software and "
      "have a performance cost: avoid them on numerous or continuously animated items."),

    h2("Chapter exercises"),
    nl("Add connections (lines) between valves that follow the movement of the items.",
       "Show in a status bar the scene coordinates of the cursor, using `mapToScene`.",
       "Implement a minimap: a second view with `fitInView` of the whole scene and a rectangle of the visible area.",
       "Highlight in red the valves that collide with another one while being dragged."),
)

CAP19 = flat(
    ch("Animations and state machines", ST_INT, [
        "Animate widget properties with easing curves.",
        "Compose sequential and parallel animations.",
        "Model behaviors with QtStateMachine.",
    ]),
    h2("Animation framework"),
    p("Animations make state changes understandable — a panel that slides, an alarm that blinks, a needle that "
      "moves to the new value. Qt's framework animates **properties** over time, integrated with the event loop, "
      "with no threads or manual loops."),
    lst("c19_animations.py", "QPropertyAnimation, QVariantAnimation, groups and QTimeLine"),
    out("c19_animations"),
    h3("QPropertyAnimation and QVariantAnimation"),
    p("`QPropertyAnimation(object, b\"property\")` interpolates a Qt property — built-in (`pos`, `geometry`, `size`, "
      "`windowOpacity`) or declared with `pyqtProperty`, like the `value` of the gauge of Chapter 17. You set the "
      "duration, the start value (optional: when absent, the current value is used) and the end value. "
      "`QVariantAnimation` interpolates values without a target and delivers each step through the `valueChanged` "
      "signal, to be applied freely."),
    h3("Easing curves: QEasingCurve"),
    p("The easing curve turns the progress of time into progress of the value. `Out` curves decelerate at the end "
      "(natural for arrival movements); `InOut` curves accelerate and decelerate; `Bounce`, `Elastic` and `Back` "
      "overshoot or oscillate around the final value. Figure 19.1 was generated with the values computed by "
      "`QEasingCurve.valueForProgress()` itself."),
    img("Most used easing curves (QEasingCurve)", "f19_1_easing.png", width_cm=14.0),
    h3("Groups: QSequentialAnimationGroup, QParallelAnimationGroup and QPauseAnimation"),
    p("Groups compose animations: parallel (run together), sequential (one after the other) and pauses. Groups can "
      "contain groups, and the total duration is computed automatically — 600 ms in the output (300 for the parallel "
      "group, 100 for the pause and 200 for the return). The `finished` signal chains actions at the end."),

    h2("QTimeLine"),
    p("`QTimeLine` provides only the timeline — values from 0 to 1 (`valueChanged`) or frame numbers "
      "(`frameChanged`) — for animations in which the code itself decides what to do at each step, such as "
      "switching the images of a sequence."),

    h2("State machines with QtStateMachine"),
    p("Interfaces with modes (idle, testing, paused, completed) tend to accumulate `if`s spread over the slots. A "
      "**state machine** makes explicit the states, the allowed transitions and what changes in each state. In "
      "Qt 6, the framework lives in the **QtStateMachine** module (in Qt 5 it was part of QtCore)."),
    lst("c19_state_machine.py", "QStateMachine: states, signal transitions, assigned properties and history"),
    out("c19_state_machine"),
    h3("QStateMachine, QState and QFinalState"),
    p("States can be compound: `test` contains `pressurizing` and `stabilizing`, with its own initial state. On "
      "entering a top-level `QFinalState`, the machine ends and emits `finished`. The machine is asynchronous: it "
      "starts with `start()` and processes the transitions in the event loop."),
    h3("Transitions: QSignalTransition, QEventTransition, QKeyEventTransition and QMouseEventTransition"),
    p("`state.addTransition(signal, target)` creates a `QSignalTransition`. There are also transitions triggered by "
      "events (`QEventTransition`), keys (`QKeyEventTransition`) and the mouse (`QMouseEventTransition`). A "
      "transition defined on a compound state applies to all of its substates — like `pause` and `complete` in the "
      "listing."),
    h3("History states: QHistoryState"),
    p("A `QHistoryState` remembers which substate was active when the compound state was left. In the output, the "
      "test was paused during `stabilizing` and, when resumed through the history, went back to `stabilizing` — and "
      "not to the initial state `pressurizing`."),
    h3("Animations associated with transitions"),
    p("`assignProperty(object, \"property\", value)` defines values applied when entering each state. With "
      "`transition.addAnimation(QPropertyAnimation(...))` or `machine.addDefaultAnimation(...)`, those changes become "
      "animated — combining the two frameworks of this chapter."),

    h2("Chapter exercises"),
    nl("Animate the `value` of the gauge of Chapter 17 with `QPropertyAnimation` and an `OutCubic` curve.",
       "Make an alarm label blink indefinitely with `QSequentialAnimationGroup` and `setLoopCount(-1)`.",
       "Model with `QStateMachine` the states of a serial connection (disconnected, connecting, connected, error).",
       "Associate color animations with the transitions of the machine of Listing 19.2 using `assignProperty`."),
)
