# Index of the listings of MAN-PYQT6-001 (English edition)

Correspondence between the number of each listing in the manual and the file in this folder.

- **✔ run** — run by [`runner.py`](../../../runner.py) (`MANUAL_LANG=en`); the actual output is in `../outputs/<name>.txt`.
- **✔ (indirect)** — file loaded or executed by another listing, as stated in the note.
- **⚠** — not run in the test environment (Linux): requires Windows.
- **support** — support file (configuration template, `.ui` interface or `.ts` translation) shown in the manual; when another listing uses it, the chapter says so.

| Listing | Title | File | Verification |
|---|---|---|---|
| 2.1 | Script that verifies the installation of PyQt6 and the add-ons | [`c02_check.py`](c02_check.py) | ✔ run |
| 2.2 | pyproject.toml template for a PyQt6 application | [`c02_pyproject.toml`](c02_pyproject.toml) | support |
| 3.1 | Inheritance and super(): a QWidget subclass with its own parameters | [`c03_inheritance.py`](c03_inheritance.py) | ✔ run |
| 3.2 | Pure-Python mixin combined with a single Qt class | [`c03_mixin.py`](c03_mixin.py) | ✔ run |
| 3.3 | @property (Python) versus pyqtProperty (visible to the meta-object system) | [`c03_property.py`](c03_property.py) | ✔ run |
| 3.4 | Classic pitfall: a lambda in a loop connected to clicked(bool) | [`c03_lambda.py`](c03_lambda.py) | ✔ run |
| 3.5 | Decorators: a custom decorator stacked with @pyqtSlot | [`c03_decorator.py`](c03_decorator.py) | ✔ run |
| 3.6 | dataclass + Enum feeding a QComboBox (associated data via userData) | [`c03_dataclass_enum.py`](c03_dataclass_enum.py) | ✔ run |
| 3.7 | Exceptions in slots: a global excepthook keeps the application alive | [`c03_exceptions.py`](c03_exceptions.py) | ✔ run |
| 4.1 | First PyQt6 application | [`c04_first.py`](c04_first.py) | ✔ run |
| 4.2 | Command-line arguments: Qt consumes the options it recognizes | [`c04_arguments.py`](c04_arguments.py) | ✔ run |
| 4.3 | Main window as a QMainWindow subclass | [`c04_mainwindow.py`](c04_mainwindow.py) | ✔ run |
| 4.4 | Metadata, aboutToQuit and quitOnLastWindowClosed | [`c04_lifecycle.py`](c04_lifecycle.py) | ✔ run |
| 5.1 | Object tree: parent-child, objectName, findChild/findChildren and destroyed | [`c05_tree.py`](c05_tree.py) | ✔ run |
| 5.2 | C++ x Python life cycle: a reference to a C++ object already destroyed | [`c05_cpp_lifetime.py`](c05_cpp_lifetime.py) | ✔ run |
| 5.3 | Custom signals: declaration, arguments, overloads and connections | [`c05_signals.py`](c05_signals.py) | ✔ run |
| 5.4 | Connection types, UniqueConnection, SingleShotConnection and signal blocking | [`c05_connections.py`](c05_connections.py) | ✔ run |
| 5.5 | Dynamic properties and introspection with QMetaObject | [`c05_meta.py`](c05_meta.py) | ✔ run |
| 5.6 | QTimer (periodic and singleShot), QElapsedTimer and QBasicTimer | [`c05_timers.py`](c05_timers.py) | ✔ run |
| 5.7 | QtCore value types: geometry, dates and URLs | [`c05_types.py`](c05_types.py) | ✔ run |
| 6.1 | Gallery of the fundamental widgets | [`c06_gallery.py`](c06_gallery.py) | ✔ run |
| 6.2 | Checkable buttons, exclusive QButtonGroup and QDialogButtonBox | [`c06_buttons.py`](c06_buttons.py) | ✔ run |
| 6.3 | QLineEdit: validators, input mask, echo mode and autocompletion | [`c06_lineedit.py`](c06_lineedit.py) | ✔ run |
| 6.4 | Synchronizing QSlider and QDoubleSpinBox; QComboBox with associated data | [`c06_numeric.py`](c06_numeric.py) | ✔ run |
| 7.1 | QHBoxLayout and QVBoxLayout: margins, spacing, stretch and alignment | [`c07_boxes.py`](c07_boxes.py) | ✔ run |
| 7.2 | QGridLayout: numeric keypad with merged cells (row/column span) | [`c07_grid.py`](c07_grid.py) | ✔ run |
| 7.3 | QFormLayout: aligned labels and fields, with wrapping and growth policies | [`c07_form.py`](c07_form.py) | ✔ run |
| 7.4 | Composition with nested layouts | [`c07_composition.py`](c07_composition.py) | ✔ run |
| 7.5 | QStackedWidget, QSplitter and QScrollArea | [`c07_stack_splitter.py`](c07_stack_splitter.py) | ✔ run |
| 8.1 | Complete main window: actions, menus, toolbar, docks and QSettings | [`c08_main_window.py`](c08_main_window.py) | ✔ run |
| 8.2 | QSplashScreen during start-up | [`c08_splash.py`](c08_splash.py) | ✔ run |
| 9.1 | QMessageBox: static methods and a customized box | [`c09_messagebox.py`](c09_messagebox.py) | ✔ run |
| 9.2 | Standard dialogs: QInputDialog, QProgressDialog and QFileDialog (non-native) | [`c09_standard.py`](c09_standard.py) | ✔ run |
| 9.3 | Custom dialog with QDialogButtonBox and validation before accept() | [`c09_dialog.py`](c09_dialog.py) | ✔ run |
| 9.4 | QWizard with registered fields (registerField) and chained pages | [`c09_wizard.py`](c09_wizard.py) | ✔ run |
| 10.1 | Reimplementing event handlers (mouse, keyboard, window) | [`c10_handlers.py`](c10_handlers.py) | ✔ run |
| 10.2 | Event filter: one object watches and intercepts the events of another | [`c10_filter.py`](c10_filter.py) | ✔ run |
| 10.3 | Custom events: registerEventType, postEvent (asynchronous) and sendEvent | [`c10_custom_event.py`](c10_custom_event.py) | ✔ run |
| 10.4 | Drag and drop: a target that accepts only .csv files | [`c10_drag_drop.py`](c10_drag_drop.py) | ✔ run |
| 10.5 | Clipboard: text, MIME data and change notification | [`c10_clipboard.py`](c10_clipboard.py) | ✔ run |
| 11.1 | .ui file produced by Qt Designer (XML) | [`c11_well_data.ui`](c11_well_data.ui) | support |
| 11.2 | Loading a .ui file dynamically with uic.loadUi() | [`c11_loadui.py`](c11_loadui.py) | ✔ run |
| 11.3 | Code generated by pyuic6 6.12.0 from Listing 11.1 | [`ui_well_data.py`](ui_well_data.py) | ✔ run |
| 11.4 | Code generated by pyuic6: integration by composition and by multiple inheritance | [`c11_composition_ui.py`](c11_composition_ui.py) | ✔ run |
| 11.5 | Custom widget used through promotion in Qt Designer | [`c11_widgets.py`](c11_widgets.py) | ✔ run |
| 11.6 | <customwidgets> excerpt of a .ui with a promoted widget | [`c11_promoted.ui`](c11_promoted.ui) | support |
| 11.7 | Widget promotion: the .ui refers to PressureField, defined in c11_widgets.py | [`c11_promotion.py`](c11_promotion.py) | ✔ run |
| 11.8 | Widget plugin for Qt Designer written in Python (QtDesigner module) | [`c11_plugin.py`](c11_plugin.py) | ✔ run |
| 12.1 | QStyleFactory, switching styles and QProxyStyle for a targeted adjustment | [`c12_styles.py`](c12_styles.py) | ✔ run |
| 12.2 | QPalette: programmatic dark theme and the system color scheme | [`c12_palette.py`](c12_palette.py) | ✔ run |
| 12.3 | Qt Style Sheets: light and dark themes, selectors, subcontrols and pseudo-states | [`c12_themes.py`](c12_themes.py) | ✔ run |
| 12.4 | Embedded fonts (QFontDatabase) and icons (QIcon from SVG) | [`c12_fonts_icons.py`](c12_fonts_icons.py) | ✔ run |
| 12.5 | High-DPI: rounding policy and pixmaps with devicePixelRatio | [`c12_highdpi.py`](c12_highdpi.py) | ✔ run |
| 13.1 | Resources without pyrcc: paths relative to the package and QDir search prefixes | [`c13_resources.py`](c13_resources.py) | ✔ run |
| 13.2 | QSettings in INI format: types, groups, arrays and default values | [`c13_settings.py`](c13_settings.py) | ✔ run |
| 13.3 | QStandardPaths, QDir and QFileInfo: where to store each kind of file | [`c13_paths.py`](c13_paths.py) | ✔ run |
| 13.4 | Internationalization: tr(), the application's QTranslator and Qt's own translations | [`c13_translation.py`](c13_translation.py) | ✔ run |
| 13.5 | .ts file generated by pylupdate6 and translated | [`c13_engcalc_pt_BR.ts`](c13_engcalc_pt_BR.ts) | support |
| 13.6 | QLocale: formatting and parsing numbers, dates and currency per language | [`c13_locale.py`](c13_locale.py) | ✔ run |
| 13.7 | Qt messages redirected to the logging module (qInstallMessageHandler) | [`c13_log.py`](c13_log.py) | ✔ run |
| 14.1 | Convenience widgets: QListWidget, QTreeWidget and QTableWidget | [`c14_convenience.py`](c14_convenience.py) | ✔ run |
| 14.2 | Ready-made models: QStringListModel and QStandardItemModel | [`c14_ready_models.py`](c14_ready_models.py) | ✔ run |
| 14.3 | QFileSystemModel: asynchronous loading of directories (directoryLoaded signal) | [`c14_filesystem.py`](c14_filesystem.py) | ✔ run |
| 14.4 | Custom table model: reading, editing, roles and insertion/removal | [`c14_table_model.py`](c14_table_model.py) | ✔ run |
| 14.5 | Hierarchical model with QAbstractItemModel: index(), parent() and internalPointer | [`c14_tree_model.py`](c14_tree_model.py) | ✔ run |
| 14.6 | Custom delegate: numeric editor with limits and formatted text | [`c14_delegate.py`](c14_delegate.py) | ✔ run |
| 14.7 | Proxy models: sorting/filtering, transposition and concatenation | [`c14_proxy.py`](c14_proxy.py) | ✔ run |
| 14.8 | QItemSelectionModel and QDataWidgetMapper: a form bound to the selected row | [`c14_selection_mapper.py`](c14_selection_mapper.py) | ✔ run |
| 15.1 | QtSql with SQLite: connection, DDL, prepared queries, transactions and errors | [`c15_sqlite.py`](c15_sqlite.py) | ✔ run |
| 15.2 | SQL models: QSqlQueryModel, QSqlTableModel (editing) and QSqlRelationalTableModel | [`c15_sql_models.py`](c15_sql_models.py) | ✔ run |
| 16.1 | QSaveFile + QTextStream (text) and QDataStream (versioned binary) | [`c16_files.py`](c16_files.py) | ✔ run |
| 16.2 | JSON (json module and QJsonDocument) and XML (QXmlStreamWriter/Reader and QtXml DOM) | [`c16_json_xml.py`](c16_json_xml.py) | ✔ run |
| 16.3 | CSV with the csv module and with pandas, shown in a QTableView by a generic model | [`c16_csv_pandas.py`](c16_csv_pandas.py) | ✔ run |
| 16.4 | QFileSystemWatcher and QProcess (synchronous and asynchronous execution) | [`c16_watcher_process.py`](c16_watcher_process.py) | ✔ run |
| 16.5 | QCommandLineParser: options, values, positional arguments and --help | [`c16_command_line.py`](c16_command_line.py) | ✔ run |
| 17.1 | QPainter on a QImage: pens, brushes, gradients, paths, transformations and text | [`c17_primitives.py`](c17_primitives.py) | ✔ run |
| 17.2 | QImage (pixels), QPixmap (display), QFontMetrics (text) and QStylePainter | [`c17_images.py`](c17_images.py) | ✔ run |
| 17.3 | Custom widget: analog pressure gauge drawn with QPainter | [`c17_gauge.py`](c17_gauge.py) | ✔ run |
| 17.4 | Printing to PDF (QPrinter), QPdfWriter, QSvgGenerator and QSvgRenderer | [`c17_print_svg.py`](c17_print_svg.py) | ✔ run |
| 18.1 | Graphics View: scene with standard and custom items, two views, collision and zoom | [`c18_scene.py`](c18_scene.py) | ✔ run |
| 19.1 | QPropertyAnimation, QVariantAnimation, groups and QTimeLine | [`c19_animations.py`](c19_animations.py) | ✔ run |
| 19.2 | QStateMachine: states, signal transitions, assigned properties and history | [`c19_state_machine.py`](c19_state_machine.py) | ✔ run |
| 20.1 | Event loop responsiveness: computation in the GUI thread versus in a worker | [`c20_blocking.py`](c20_blocking.py) | ✔ run |
| 20.2 | Worker pattern with moveToThread(): progress, result, error and cancellation | [`c20_worker.py`](c20_worker.py) | ✔ run |
| 20.3 | QThread subclass: run() in the new thread, slots in the thread of origin | [`c20_qthread_sub.py`](c20_qthread_sub.py) | ✔ run |
| 20.4 | QThreadPool with QRunnable, helper signals and callables | [`c20_pool.py`](c20_pool.py) | ✔ run |
| 20.5 | Synchronization: QMutex, QReadWriteLock, QWaitCondition and QSemaphore | [`c20_sync.py`](c20_sync.py) | ✔ run |
| 20.6 | Connection types between threads and QMetaObject.invokeMethod | [`c20_thread_signals.py`](c20_thread_signals.py) | ✔ run |
| 20.7 | concurrent.futures with processes and threads integrated with Qt | [`c20_futures.py`](c20_futures.py) | ✔ run |
| 20.8 | asyncio on top of the Qt event loop with qasync | [`c20_asyncio.py`](c20_asyncio.py) | ✔ run |
| 21.1 | HTTP with QNetworkAccessManager: GET/POST JSON, errors, timeout and progress | [`c21_http.py`](c21_http.py) | ✔ run |
| 21.2 | TCP with QTcpServer and QTcpSocket: line protocol and framing | [`c21_tcp.py`](c21_tcp.py) | ✔ run |
| 21.3 | UDP with QUdpSocket and binary datagrams | [`c21_udp.py`](c21_udp.py) | ✔ run |
| 21.4 | TLS with QSslServer and QSslSocket: certificate and name verification | [`c21_tls.py`](c21_tls.py) | ✔ run |
| 21.5 | WebSockets: server and client exchanging JSON and binary data | [`c21_websocket.py`](c21_websocket.py) | ✔ run |
| 21.6 | OAuth 2.0 Authorization Code + PKCE with QOAuth2AuthorizationCodeFlow | [`c21_oauth.py`](c21_oauth.py) | ✔ run |
| 21.7 | QtRemoteObjects: source and dynamic replica in separate processes | [`c21_remoteobjects.py`](c21_remoteobjects.py) | ✔ run |
| 21.8 | D-Bus: exported service and client in another process | [`c21_dbus.py`](c21_dbus.py) | ✔ run |
| 21.9 | QSerialPort: acquisition of ASCII lines from an instrument | [`c21_serial.py`](c21_serial.py) | ✔ run |
| 21.10 | Bluetooth LE and NFC: discovery with handling of missing hardware | [`c21_bluetooth.py`](c21_bluetooth.py) | ✔ run |
| 22.1 | GraphsView in QML: theme, axes, line series and scatter series | [`c22_graphs2d.qml`](c22_graphs2d.qml) | ✔ (indirect): File loaded and rendered by Listing 22.2 (run and verified) |
| 22.2 | QtGraphs 2D fed by Python in a QQuickWidget | [`c22_graphs2d.py`](c22_graphs2d.py) | ✔ run |
| 22.3 | 3D surface with Q3DSurfaceWidgetItem, color gradient and camera | [`c22_graphs3d.py`](c22_graphs3d.py) | ✔ run |
| 22.4 | QtCharts: line, spline, scatter, logarithmic axis, bars and pie | [`c22_qtcharts.py`](c22_qtcharts.py) | ✔ run |
| 22.5 | Embedded Matplotlib with navigation toolbar and redrawing per parameter | [`c22_matplotlib.py`](c22_matplotlib.py) | ✔ run |
| 22.6 | pyqtgraph: oscilloscope with a circular buffer and QTimer | [`c22_pyqtgraph.py`](c22_pyqtgraph.py) | ✔ run |
| 22.7 | Cost per frame (data + painting) of pyqtgraph, QtCharts and Matplotlib | [`c22_performance.py`](c22_performance.py) | ✔ run |
| 23.1 | Audio playback and decoding with QMediaPlayer and QAudioDecoder | [`c23_audio.py`](c23_audio.py) | ✔ run |
| 23.2 | Capture and recording: QMediaCaptureSession, QMediaRecorder and QAudioBufferInput | [`c23_recording.py`](c23_recording.py) | ✔ run |
| 23.3 | QtSpatialAudio: engine, listener, room and positioned source | [`c23_spatial.py`](c23_spatial.py) | ✔ run |
| 23.4 | QTextToSpeech: engines, voices, languages and speech queue | [`c23_speech.py`](c23_speech.py) | ✔ run |
| 23.5 | QtPositioning: NMEA log in simulation mode, distance, azimuth and zone | [`c23_position.py`](c23_position.py) | ✔ run |
| 23.6 | QtSensors: backend discovery, filters and handling of absence | [`c23_sensors.py`](c23_sensors.py) | ✔ run |
| 23.7 | System tray, QDesktopServices and permissions | [`c23_desktop.py`](c23_desktop.py) | ✔ run |
| 24.1 | QWebEngineView: HTML, JavaScript, console, navigation control and PDF | [`c24_webengine.py`](c24_webengine.py) | ✔ run |
| 24.2 | Own profile, engapp:// scheme, interceptor and download | [`c24_schemes.py`](c24_schemes.py) | ✔ run |
| 24.3 | Page that uses the bridge: property, slot with return value and signal | [`c24_webchannel.html`](c24_webchannel.html) | ✔ (indirect): Page loaded and executed by Listing 24.4 (run and verified) |
| 24.4 | QWebChannel: Python object published to JavaScript | [`c24_webchannel.py`](c24_webchannel.py) | ✔ run |
| 24.5 | Displaying a PDF with the built-in viewer of QWebEngineView | [`c24_pdf.py`](c24_pdf.py) | ✔ run |
| 24.6 | Help project (.qhp): table of contents, keywords and files | [`resources/help/manual.qhp`](resources/help/manual.qhp) | ✔ (indirect): Compiled with qhelpgenerator; the resulting .qch is used by Listing 24.7 |
| 24.7 | QtHelp: registering the .qch, index, contents, display and search | [`c24_help.py`](c24_help.py) | ✔ run |
| 24.8 | QAxContainer: exporting results to Microsoft Excel via COM | [`c24_activex.py.win`](c24_activex.py.win) | ⚠ Not run in the test environment (Linux): requires Windows with Microsoft Excel |
| 25.1 | QOpenGLWidget with OpenGL 4.1 Core: shaders, VBO, VAO and uniform | [`c25_opengl.py`](c25_opengl.py) | ✔ run |
| 25.2 | QRhiWidget: render pass with an animated clear | [`c25_rhi.py`](c25_rhi.py) | ✔ run |
| 25.3 | QVulkanInstance: version, layers, extensions and creation | [`c25_vulkan.py`](c25_vulkan.py) | ✔ run |
| 25.4 | Qt Quick 3D scene: camera, light, models and a property controlled by Python | [`c25_quick3d.qml`](c25_quick3d.qml) | ✔ (indirect): File loaded and rendered by Listing 25.5 (run and verified) |
| 25.5 | Qt Quick 3D in a QQuickWidget, controlled by Python | [`c25_quick3d.py`](c25_quick3d.py) | ✔ run |
| 25.6 | Qt 3D: entity, mesh, material, transform and camera | [`c25_qt3d.py`](c25_qt3d.py) | ✔ run |
| 26.1 | QML interface that uses a singleton and a type defined in Python | [`c26_main.qml`](c26_main.qml) | ✔ (indirect): File loaded by Listing 26.2 (run and verified) |
| 26.2 | QQmlApplicationEngine with singleton, registered type, properties and signals | [`c26_engine.py`](c26_engine.py) | ✔ run |
| 26.3 | ListView with a delegate that uses required properties | [`c26_model.qml`](c26_model.qml) | ✔ (indirect): File loaded by Listing 26.4 (run and verified) |
| 26.4 | QAbstractListModel with roleNames() displayed in QML | [`c26_model.py`](c26_model.py) | ✔ run |
| 26.5 | Circular indicator in QML with property, signal and animation | [`c26_indicator.qml`](c26_indicator.qml) | ✔ (indirect): File loaded by Listing 26.6 (run and verified) |
| 26.6 | QQuickWidget in a Widgets window with a QSlider and a QML signal | [`c26_qquickwidget.py`](c26_qquickwidget.py) | ✔ run |
| 27.1 | MVP: pure domain, presenter and two views (widget and fake) | [`c27_mvp.py`](c27_mvp.py) | ✔ run |
| 27.2 | MVVM: ViewModel with notifiable properties and two-way binding | [`c27_mvvm.py`](c27_mvvm.py) | ✔ run |
| 27.3 | Application TOML configuration file | [`c27_config.toml`](c27_config.toml) | ✔ (indirect): Read by Listing 27.4 (run and verified) |
| 27.4 | Dependency injection: typed configuration, composition root and repositories | [`c27_di.py`](c27_di.py) | ✔ run |
| 27.5 | QUndoStack: commands, merging, macros, clean state and QUndoView | [`c27_undo.py`](c27_undo.py) | ✔ run |
| 27.6 | Example plugin (plugins_demo folder) | [`plugins_demo/unit_converter.py`](plugins_demo/unit_converter.py) | ✔ (indirect): Loaded and executed by Listing 27.7 (run and verified) |
| 27.7 | Discovery, version validation and isolation of plugins | [`c27_plugins.py`](c27_plugins.py) | ✔ run |
| 27.8 | sys.excepthook and threading.excepthook with an error report | [`c27_exceptions.py`](c27_exceptions.py) | ✔ run |
| 28.1 | Widget under test: hydrostatic pressure calculator | [`c28_calculator.py`](c28_calculator.py) | ✔ run |
| 28.2 | QtTest with unittest: keyboard, mouse, QSignalSpy and QAbstractItemModelTester | [`c28_qtest.py`](c28_qtest.py) | ✔ run |
| 28.3 | Tests with pytest-qt: qtbot, waitSignal, assertNotEmitted and parametrization | [`c28_test_calculator.py`](c28_test_calculator.py) | ✔ run |
| 28.4 | GitHub Actions: matrix of systems and Python versions with headless tests | [`c28_ci.yml`](c28_ci.yml) | ✔ (indirect): YAML syntax validated with a parser; commands equivalent to those run in this chapter |
| 28.5 | Running the suite with pytest-cov, as in continuous integration | [`c28_coverage.py`](c28_coverage.py) | ✔ run |
| 28.6 | Visual regression: comparison with a reference image | [`c28_visual_regression.py`](c28_visual_regression.py) | ✔ run |
| 29.1 | cProfile and QElapsedTimer: slow model versus cached model | [`c29_performance.py`](c29_performance.py) | ✔ run |
| 29.2 | QLoggingCategory, filter rules, message handler and QT_DEBUG_PLUGINS | [`c29_debugging.py`](c29_debugging.py) | ✔ run |
| 29.3 | Destroyed C++ objects, temporaries, unreferenced objects and faulthandler | [`c29_memory.py`](c29_memory.py) | ✔ run |
| 29.4 | Accessible names, buddies, tab order, contrast and preferences | [`c29_accessibility.py`](c29_accessibility.py) | ✔ run |
| 30.1 | Application to be packaged: resources, theme, translation and self-test | [`c30_app/monitor_app.py`](c30_app/monitor_app.py) | ✔ (indirect): Packaged and executed by Listing 30.3 (run and verified) |
| 30.2 | PyInstaller .spec file (onedir, data and exclusions) | [`c30_app/monitor_app.spec`](c30_app/monitor_app.spec) | ✔ (indirect): Used by Listing 30.3 (run and verified) |
| 30.3 | Packaging with PyInstaller and running the frozen result | [`c30_package.py`](c30_package.py) | ✔ run |
| 30.4 | Inno Setup script for the folder generated by PyInstaller | [`c30_installer.iss`](c30_installer.iss) | ⚠ Not run in the test environment (Linux): requires Inno Setup 6.3+ on Windows |
| 31.1 | app.py — composition root, data folders and self-test | [`c31_app/leaktest/app.py`](c31_app/leaktest/app.py) | ✔ (indirect): Executed by Listing 31.13 (tests, self-test of the source code and of the frozen executable) |
| 31.2 | window.py — main window, actions and integration of the components | [`c31_app/leaktest/window.py`](c31_app/leaktest/window.py) | ✔ (indirect): Executed by Listing 31.13 (tests, self-test of the source code and of the frozen executable) |
| 31.3 | data/TH-01.csv — example readings | [`c31_app/data/TH-01.csv`](c31_app/data/TH-01.csv) | ✔ (indirect): Read by the self-test and by the tests of Listing 31.11 |
| 31.4 | domain.py — analysis rules in pure Python | [`c31_app/leaktest/domain.py`](c31_app/leaktest/domain.py) | ✔ (indirect): Executed by Listing 31.13 (tests, self-test of the source code and of the frozen executable) |
| 31.5 | csv_import.py — reading CSV with separator detection | [`c31_app/leaktest/csv_import.py`](c31_app/leaktest/csv_import.py) | ✔ (indirect): Executed by Listing 31.13 (tests, self-test of the source code and of the frozen executable) |
| 31.6 | repository.py — persistence in SQLite | [`c31_app/leaktest/repository.py`](c31_app/leaktest/repository.py) | ✔ (indirect): Executed by Listing 31.13 (tests, self-test of the source code and of the frozen executable) |
| 31.7 | models.py — table models for tests and readings | [`c31_app/leaktest/models.py`](c31_app/leaktest/models.py) | ✔ (indirect): Executed by Listing 31.13 (tests, self-test of the source code and of the frozen executable) |
| 31.8 | services.py — analysis in a QThreadPool with the result by signal | [`c31_app/leaktest/services.py`](c31_app/leaktest/services.py) | ✔ (indirect): Executed by Listing 31.13 (tests, self-test of the source code and of the frozen executable) |
| 31.9 | report.py — HTML + Matplotlib → QTextDocument → PDF | [`c31_app/leaktest/report.py`](c31_app/leaktest/report.py) | ✔ (indirect): Executed by Listing 31.13 (tests, self-test of the source code and of the frozen executable) |
| 31.10 | tests/test_domain.py — tests of the domain and of the import | [`c31_app/tests/test_domain.py`](c31_app/tests/test_domain.py) | ✔ (indirect): Executed by Listing 31.13 (tests, self-test of the source code and of the frozen executable) |
| 31.11 | tests/test_window.py — interface tests with pytest-qt | [`c31_app/tests/test_window.py`](c31_app/tests/test_window.py) | ✔ (indirect): Executed by Listing 31.13 (tests, self-test of the source code and of the frozen executable) |
| 31.12 | leak_test_monitor.spec — packaging with PyInstaller | [`c31_app/leak_test_monitor.spec`](c31_app/leak_test_monitor.spec) | ✔ (indirect): Executed by Listing 31.13 (tests, self-test of the source code and of the frozen executable) |
| 31.13 | Delivery script: tests, self-test, packaging and retest of the executable | [`c31_delivery.py`](c31_delivery.py) | ✔ run |
