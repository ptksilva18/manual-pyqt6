# -*- coding: utf-8 -*-
"""Verified tabular data (PyQt6 6.12.0) used in the text — English edition."""

# ---------------------------------------------------------------------------
# Table 1.4 - module map (data verified in the PyQt6 6.12.0 wheels)
# ---------------------------------------------------------------------------
MODULE_ROWS = [
    # module, pip package, purpose, status/remark, chapter
    ["QtCore", "PyQt6", "Non-GUI core: QObject, signals/slots, event loop, threads, files, models", "Essential", "5, 13, 16, 20"],
    ["QtGui", "PyQt6", "Window-system integration, 2D painting, fonts, images, actions, input events", "Essential", "8, 12, 17"],
    ["QtWidgets", "PyQt6", "Classic desktop widgets, layouts, dialogs, Graphics View", "Essential", "6–10, 14, 18"],
    ["QtSql", "PyQt6", "Database access and SQL models", "Active", "15"],
    ["QtPrintSupport", "PyQt6", "Printing, print preview and page dialogs", "Active", "17"],
    ["QtSvg / QtSvgWidgets", "PyQt6", "SVG rendering and generation; SVG display widget", "Active", "17"],
    ["QtNetwork", "PyQt6", "HTTP, TCP/UDP, SSL/TLS, DNS", "Active", "21"],
    ["QtWebSockets", "PyQt6", "WebSocket client and server (RFC 6455)", "Active", "21"],
    ["QtSerialPort", "PyQt6", "Physical and virtual serial ports (instrumentation)", "Active", "21"],
    ["QtBluetooth / QtNfc", "PyQt6", "Bluetooth and NFC connectivity", "Active (platform-dependent)", "21"],
    ["QtDBus", "PyQt6", "Inter-process communication over D-Bus", "Active (Linux/Unix)", "21"],
    ["QtRemoteObjects", "PyQt6", "Sharing QObjects between processes/machines", "Active", "21"],
    ["QtMultimedia / QtMultimediaWidgets", "PyQt6", "Audio, video, camera, capture; video widget", "Active", "23"],
    ["QtSpatialAudio", "PyQt6", "3D spatial sound", "Active", "23"],
    ["QtTextToSpeech", "PyQt6", "Speech synthesis", "Active", "23"],
    ["QtPositioning", "PyQt6", "Positioning (GNSS, Wi-Fi, NMEA)", "Active", "23"],
    ["QtSensors", "PyQt6", "Access to device sensors", "Active", "23"],
    ["QtOpenGL / QtOpenGLWidgets", "PyQt6", "OpenGL integration; QOpenGLWidget", "Active", "25"],
    ["QtQml / QtQuick", "PyQt6", "QML engine and Qt Quick", "Active", "26"],
    ["QtQuickWidgets", "PyQt6", "QQuickWidget: QML embedded in Widgets applications", "Active", "26"],
    ["QtQuick3D", "PyQt6", "Python integration with Qt Quick 3D", "Active (recommended 3D stack)", "25"],
    ["QtStateMachine", "PyQt6", "Hierarchical state machines", "Active", "19"],
    ["QtHelp", "PyQt6", "Searchable documentation built into the application", "Active", "24"],
    ["QtWebChannel", "PyQt6", "Bridge between QObjects and JavaScript", "Active", "24"],
    ["QtDesigner", "PyQt6", "Widget plugins for Qt Designer", "Active", "11"],
    ["QtTest", "PyQt6", "GUI testing: QTest, QSignalSpy, QAbstractItemModelTester", "Active", "28"],
    ["QtXml", "PyQt6", "DOM interface for XML", "Active", "16"],
    ["QAxContainer", "PyQt6 (Windows only)", "ActiveX controls and COM objects", "Active (Windows)", "24"],
    ["uic / lupdate", "PyQt6", "Subpackages: loading .ui files (pyuic6) and extracting translations (pylupdate6)", "Tools", "11, 13"],
    ["sip", "PyQt6 (PyQt6-sip)", "Support module of the bindings (sip.isdeleted, sip.delete…)", "Infrastructure", "29"],
    ["QtCharts", "PyQt6-Charts", "2D charts on top of Graphics View", "Deprecated since Qt 6.10 (use QtGraphs)", "22"],
    ["QtGraphs / QtGraphsWidgets", "PyQt6-Graphs", "2D (via QML) and 3D graphs; 3D items for Widgets", "Active (replaces Charts/DataVisualization)", "22"],
    ["QtDataVisualization", "PyQt6-DataVisualization", "3D bar, scatter and surface graphs", "Deprecated since Qt 6.10 (use QtGraphs)", "22"],
    ["Qt3DCore, Qt3DRender, Qt3DExtras, Qt3DInput, Qt3DLogic, Qt3DAnimation", "PyQt6-3D", "Qt 3D framework", "Deprecated since Qt 6.8 (prefer Qt Quick 3D)", "25"],
    ["QtNetworkAuth", "PyQt6-NetworkAuth", "OAuth 1.0 and OAuth 2.0", "Active", "21"],
    ["QtWebEngineCore / QtWebEngineWidgets / QtWebEngineQuick", "PyQt6-WebEngine", "Chromium-based web browser engine", "Active", "24"],
]

PYQT5_TO_6 = [
    ["Enums", "Qt.AlignCenter", "Qt.AlignmentFlag.AlignCenter (the fully qualified name is mandatory)"],
    ["Event loop", "app.exec_() / dialog.exec_()", "app.exec() / dialog.exec() (exec_ was removed)"],
    ["Actions and shortcuts", "QtWidgets.QAction, QShortcut, QActionGroup", "Moved to QtGui"],
    ["Undo/Redo", "QtWidgets.QUndoStack, QUndoCommand, QUndoGroup", "Moved to QtGui (QUndoView stays in QtWidgets)"],
    ["File model", "QtWidgets.QFileSystemModel", "Moved to QtGui"],
    ["Screens", "QDesktopWidget", "Removed; use QScreen (QGuiApplication.primaryScreen(), screens())"],
    ["Regular expressions", "QRegExp", "Removed; use QRegularExpression"],
    ["Font metrics", "QFontMetrics.width()", "Removed; use horizontalAdvance()"],
    ["Mouse events", "event.pos() (QPoint)", "event.position() (QPointF); pos() still exists but is obsolete in Qt 6"],
    ["OpenGL", "QtWidgets.QOpenGLWidget", "Moved to QtOpenGLWidgets"],
    ["SVG", "QtSvg.QSvgWidget", "Moved to QtSvgWidgets"],
    ["Multimedia", "QMediaPlayer with implicit output", "Redesigned API: QMediaPlayer + QAudioOutput + QVideoWidget/QVideoSink"],
    ["High-DPI", "AA_EnableHighDpiScaling required", "High-DPI scaling always on"],
    ["Resources", "pyrcc5", "No pyrcc6: use files/importlib.resources or QDir.addSearchPath()"],
]

CONVENTIONS = [
    ["Body text", "Calibri 11 pt, justified", "Conceptual explanations"],
    ["`Inline code`", "Consolas, grey background", "Names of classes, methods, variables: `QWidget.show()`"],
    ["Code listing", "Consolas 8 pt block with a blue side bar", "Complete programs, numbered as Listing N.M"],
    ["**Bold**", "Highlight", "Key terms at first occurrence"],
    ["*Italic*", "Emphasis", "Foreign terms and titles of works"],
    ["NOTE / TIP / WARNING box", "Box with a colored bar", "Complementary information, good practices and pitfalls"],
    ["Output", "\"Output\" title followed by a Consolas block", "Real output captured when running the preceding listing"],
    ["✔ green line after the listing", "Green italic", "Code run and verified, or file loaded by a verified listing"],
    ["⚠ orange line after the listing", "Orange italic", "Code that requires a platform unavailable in the test environment (e.g. Windows)"],
]
