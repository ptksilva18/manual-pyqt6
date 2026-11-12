# -*- coding: utf-8 -*-
"""Part III — Chapters 23 to 26 (English edition)."""
from blocks import ST_AVA, bl, ch, flat, h2, h3, img, lst, nl, note, out, p, snip, tab

CAP23 = flat(
    ch("Multimedia and system integration", ST_AVA, [
        "Play and capture audio and video.",
        "Use speech synthesis, positioning and sensors.",
        "Integrate the application with the system tray and the desktop.",
    ]),
    p("The features in this chapter depend on hardware (sound card, camera, GNSS, sensors) and on operating "
      "system services. The listings were run on a Linux server **without** those devices; that is why, besides "
      "the main path, they show how to detect missing resources and degrade gracefully — a requirement of any "
      "professional application."),
    h2("QtMultimedia"),
    p("The Qt 6 multimedia API was redesigned relative to Qt 5: the player (`QMediaPlayer`) no longer has an "
      "implicit output, and capture is organized around a session (`QMediaCaptureSession`) that connects "
      "inputs (camera, microphone, screen) to outputs (preview, photo, recorder). In the PyQt6-Qt6 6.12 wheels "
      "for Linux, the only multimedia plugin is the one based on **FFmpeg** (verified), which decodes and "
      "encodes the usual formats without depending on system codecs."),
    h3("Playback: QMediaPlayer, QAudioOutput and QVideoWidget"),
    p("`QMediaPlayer` controls the media (`setSource`, `play`, `pause`, `stop`, `setPosition`) and reports "
      "progress through `mediaStatusChanged`, `playbackStateChanged`, `durationChanged` and `positionChanged`. "
      "Sound only comes out if a `QAudioOutput` is associated; video requires `setVideoOutput()` with a "
      "`QVideoWidget` (Widgets), a `QGraphicsVideoItem` (Graphics View) or a `QVideoSink` (frames for your own "
      "processing). `QAudioDecoder` decodes the file into memory, without playing it — useful for signal "
      "analysis."),
    lst("c23_audio.py", "Audio playback and decoding with QMediaPlayer and QAudioDecoder"),
    out("c23_audio"),
    p("Even without an audio output, the player went through all the states up to `EndOfMedia`, and the decoder "
      "delivered the 22 050 samples (0.5 s at 44.1 kHz) with the expected peak — the one-unit difference comes "
      "from truncation when generating the sine."),
    note("WARNING", "In the test environment (Linux container with PipeWire libraries, but no audio server "
                    "running), `QMediaDevices.audioOutputs()` terminated the process with a segmentation fault. "
                    "Setting `QT_AUDIO_BACKEND=pulseaudio` (a variable recognized by the Qt Multimedia 6.12 "
                    "library) worked around the problem. On user machines with working audio this is not "
                    "needed; the record serves for diagnosis on test servers."),
    h3("Capture: QCamera, QMediaCaptureSession, QImageCapture and QMediaRecorder"),
    p("The capture session is the central point: `setCamera()`, `setAudioInput()`, `setImageCapture()`, "
      "`setRecorder()` and `setVideoOutput()`. `QMediaRecorder` records in the container and with the codecs "
      "chosen in `QMediaFormat`; `QMediaFormat().supportedFileFormats(Encode)` reports what the backend can "
      "record. Without a microphone or a camera, Listing 23.2 uses `QAudioBufferInput` (Qt 6.8+), which lets "
      "the program itself supply the samples — for example, synthesized signals or signals coming from an "
      "instrument."),
    lst("c23_recording.py", "Capture and recording: QMediaCaptureSession, QMediaRecorder and QAudioBufferInput"),
    out("c23_recording"),
    note("WARNING", "In PyQt6 6.12, connecting `QMediaRecorder.recorderStateChanged` or "
                    "`QMediaRecorder.errorOccurred` fails with `TypeError` (\"No such signal\"): the signal "
                    "signature is not found. Listing 23.2 works around the problem by polling `recorderState()` "
                    "and `error()` with a `QTimer`. The `QMediaPlayer` signals work normally."),
    h3("Sound effects: QSoundEffect"),
    p("For short, low-latency sounds (clicks, alarms), `QSoundEffect` loads an uncompressed WAV file into "
      "memory and plays it repeatedly with `play()`, with control of volume and repetitions "
      "(`setLoopCount`). Without an output device, its `status()` goes to `Error` — handle that state instead "
      "of assuming the sound was played."),
    h3("Devices: QMediaDevices"),
    p("`QMediaDevices` lists cameras (`videoInputs`), microphones (`audioInputs`) and outputs "
      "(`audioOutputs`), reports the system defaults and emits signals when devices are connected or removed "
      "(`audioOutputsChanged`, `videoInputsChanged`). React to these signals to switch devices without "
      "restarting the application."),

    h2("Spatial audio: QtSpatialAudio"),
    p("QtSpatialAudio positions sound sources in 3D around a listener, with distance attenuation, occlusion and "
      "room reverberation — useful in simulators and training. The position unit is defined by "
      "`distanceScale` (the default is centimeters; `DistanceScaleMeter` makes positions count as meters)."),
    lst("c23_spatial.py", "QtSpatialAudio: engine, listener, room and positioned source"),
    out("c23_spatial"),
    note("WARNING", "Destroy sources, rooms and listener before the `QAudioEngine`. In the test, leaving the "
                    "destruction order to Python's garbage collector terminated the process with a segmentation "
                    "fault on exit; the explicit `del` statements of Listing 23.3 solved it. Note also that "
                    "`setLoops()` takes an `int` in PyQt6 (`QSpatialSound.Loops.Infinite.value`)."),

    h2("Speech synthesis: QTextToSpeech"),
    p("`QTextToSpeech` converts text to speech using the system engine (`availableEngines()`; on Linux, for "
      "example, speech-dispatcher). Voices and languages depend on the engine and on what is installed on the "
      "system; choose the voice by language with `availableVoices()`/`availableLocales()` and handle its "
      "absence. `say()` interrupts the current speech; `enqueue()` (Qt 6.6+) appends to the queue. "
      "Listing 23.4 uses the `mock` engine, shipped with Qt for testing, which simulates speech "
      "deterministically."),
    lst("c23_speech.py", "QTextToSpeech: engines, voices, languages and speech queue"),
    out("c23_speech"),

    h2("Positioning: QtPositioning"),
    p("QtPositioning obtains the position from system sources (`QGeoPositionInfoSource.createDefaultSource()`) "
      "or from GNSS receivers that speak **NMEA 0183**, through a serial port, socket or file "
      "(`QNmeaPositionInfoSource`). `QGeoCoordinate` solves basic geodesy on the WGS 84 ellipsoid: "
      "`distanceTo()`, `azimuthTo()` and `atDistanceAndAzimuth()`. Shapes such as `QGeoCircle`, "
      "`QGeoRectangle` and `QGeoPolygon` test membership (`contains`) — for example, exclusion zones around an "
      "offshore unit."),
    lst("c23_position.py", "QtPositioning: NMEA log in simulation mode, distance, azimuth and zone"),
    out("c23_position"),
    p("The `route.nmea` log (GGA and RMC sentences with valid *checksums*) describes a vessel at 8.1 knots on "
      "course 48°; the 29.1 m covered in 7 s (4.16 m/s ≈ 8.1 knots) and the azimuth of 47.9° agree with the "
      "data. In `SimulationMode`, the source follows the timestamps of the sentences; in the field, use "
      "`RealTimeMode` with the receiver's device."),

    h2("Sensors: QtSensors"),
    p("QtSensors gives access to accelerometer, gyroscope, magnetometer, ambient light, proximity and others, "
      "depending on the platform backends (Android, iOS and, on Linux, `iio-sensor-proxy`). On desktop "
      "computers, it is common to have no backend: `QSensor.sensorTypes()` comes back empty and "
      "`connectToBackend()` returns `False`, as in Listing 23.6. Filters (`QSensorFilter` and subclasses) "
      "decide which readings reach the application."),
    lst("c23_sensors.py", "QtSensors: backend discovery, filters and handling of absence"),
    out("c23_sensors"),

    h2("Desktop integration"),
    lst("c23_desktop.py", "System tray, QDesktopServices and permissions"),
    out("c23_desktop"),
    h3("QSystemTrayIcon and notifications"),
    p("Monitoring applications often live in the system tray, with a context menu and notifications "
      "(`showMessage`). Check `isSystemTrayAvailable()` — in some Linux environments (and on servers without a "
      "desktop, such as the test one) there is no tray — and call `setQuitOnLastWindowClosed(False)` so that "
      "closing the last window does not end the program."),
    h3("QDesktopServices: opening URLs and files"),
    p("`QDesktopServices.openUrl()` opens URLs and files in the system's default application (browser, PDF "
      "reader, e-mail client with `mailto:`). `setUrlHandler(scheme, object, \"slot\")` redirects URLs of a "
      "custom scheme into the application, such as `engapp://` in the listing. For **other programs** to open "
      "that scheme, it must be registered with the operating system (Windows registry, `.desktop` file on "
      "Linux, `Info.plist` on macOS)."),
    h3("Application permissions (QPermission)"),
    p("Since Qt 6.5, `QCoreApplication.checkPermission()` and `requestPermission()` handle camera, microphone, "
      "location, Bluetooth, contacts and calendar permissions portably. On platforms with a permission system "
      "(macOS, iOS, Android), the request opens the system dialog and requires the corresponding declarations "
      "in `Info.plist` or in the manifest; on desktop Linux and Windows, as the output shows, the result is "
      "usually `Granted` immediately. Write the code as if the request could be denied."),

    h2("Chapter exercises"),
    nl("Build a player with `QVideoWidget`, a position bar and volume control.",
       "Record in FLAC a signal synthesized with `QAudioBufferInput` and check the file with `QAudioDecoder`.",
       "Use `QNmeaPositionInfoSource` with a `QSerialPort` (Chapter 21) to read a real GNSS receiver.",
       "Implement a polygonal exclusion zone (`QGeoPolygon`) and sound an alarm when entering it.",
       "Turn the test monitor into a tray application with end-of-stage notifications."),
)

CAP24 = flat(
    ch("Web, documents and integrated help", ST_AVA, [
        "Embed a Chromium browser in the application.",
        "Create a two-way bridge between Python and JavaScript.",
        "Offer searchable help and integration with COM/ActiveX.",
    ]),
    p("**Qt WebEngine** embeds Chromium and is distributed in the **PyQt6-WebEngine** package (version 6.140.0 "
      "in this manual's reference). The engine runs in helper processes (`QtWebEngineProcess`), like an "
      "ordinary browser. Import `PyQt6.QtWebEngineWidgets` before creating the `QApplication`."),
    note("NOTE", "The listings in this chapter were run as the root user in a container; in that case Chromium "
                 "requires the `--no-sandbox` option, passed through the `QTWEBENGINE_CHROMIUM_FLAGS` "
                 "environment variable. In production, run the application as an ordinary user and keep the "
                 "*sandbox* enabled."),
    h2("QtWebEngineWidgets: QWebEngineView"),
    p("`QWebEngineView` is the display widget; the content and the behavior live in the associated "
      "`QWebEnginePage`. Besides `load(QUrl)`, `setHtml(html, baseUrl)` displays HTML generated by Python — "
      "reports, tables, charts in JavaScript libraries — with `baseUrl` resolving relative paths. "
      "`runJavaScript(code, callback)` executes JavaScript in the page and returns the result "
      "asynchronously."),
    lst("c24_webengine.py", "QWebEngineView: HTML, JavaScript, console, navigation control and PDF"),
    out("c24_webengine"),
    bl("`javaScriptConsoleMessage()` forwards the page's `console.log` to Python — essential for debugging.",
       "`acceptNavigationRequest()` lets you block navigation away from the application's content. A refused "
       "navigation also emits `loadFinished(False)` (verified): without the guard in `on_loaded()`, the example "
       "would repeat the click indefinitely.",
       "`printToPdf(path)` generates a PDF of the rendered content, with the result in "
       "`pdfPrintingFinished`."),
    h2("QtWebEngineCore"),
    h3("QWebEnginePage and QWebEngineProfile"),
    p("The **profile** holds cache, cookies, local storage, settings and handlers. A `QWebEngineProfile()` "
      "without a name is *off-the-record* (nothing goes to disk); with a name, the data persists in "
      "`persistentStoragePath()`. Several pages can share a profile, and each page must be destroyed before its "
      "profile — hence the `del page` at the end of Listing 24.2."),
    h3("Request interception and URL schemes"),
    p("`QWebEngineUrlRequestInterceptor.interceptRequest()` examines every request of the page and can block it "
      "or add headers; it runs outside the GUI thread and must be fast. A custom scheme (`engapp://`) is "
      "registered with `QWebEngineUrlScheme.registerScheme()` **before** the `QApplication` and served by a "
      "`QWebEngineUrlSchemeHandler`, which answers with data generated by Python — embedded documentation, "
      "reports assembled from a database, files from a package."),
    lst("c24_schemes.py", "Own profile, engapp:// scheme, interceptor and download"),
    out("c24_schemes"),
    h3("Downloads and printing to PDF"),
    p("Downloads arrive at the profile's `downloadRequested` signal as a `QWebEngineDownloadRequest`; set the "
      "folder and the name and call `accept()` — without it, the download is canceled. Progress is followed "
      "through `receivedBytesChanged` and completion through `isFinishedChanged`. For a PDF of the page itself, "
      "`printToPdf()` (Listing 24.1); for printing on a printer, `QWebEngineView.print(QPrinter)`."),

    h2("QtWebChannel: Python ↔ JavaScript bridge"),
    p("**QWebChannel** publishes Python objects to the page's JavaScript: properties are read as attributes, "
      "slots become functions (with the return value delivered by a *callback*) and signals can be connected "
      "to JavaScript functions. On the page side, the `qwebchannel.js` library — built into Qt, in the "
      "`:/qtwebchannel/qwebchannel.js` resource — creates the channel from `qt.webChannelTransport`. In "
      "Listing 24.4, the script is injected with `QWebEngineScript` before the page's code."),
    lst("c24_webchannel.html", "Page that uses the bridge: property, slot with return value and signal",
        lang="html", nota="✔ Page loaded and executed by Listing 24.4 (run and verified)."),
    lst("c24_webchannel.py", "QWebChannel: Python object published to JavaScript"),
    out("c24_webchannel"),
    img("QWebChannel bridge between Python and JavaScript", "f24_1_webchannel.png", 15.0),
    note("WARNING", "Everything published on the channel can be called by any script in the page. Publish only "
                    "facade objects with safe operations and validate the arguments in Python, as if they came "
                    "from an external user."),

    h2("PDF viewing: alternatives and availability (QtPdf not included in the 6.12 wheels)"),
    p("The `QtPdf` and `QtPdfWidgets` modules are not part of the PyQt6 6.12.0 or PyQt6-WebEngine 6.140.0 "
      "wheels (verified by inspecting the installed modules). The alternatives, in order of simplicity:"),
    bl("**Chromium viewer**: `QWebEngineView` displays PDFs with navigation, zoom and search when "
       "`PluginsEnabled` and `PdfViewerEnabled` are on (Listing 24.5).",
       "**System default application**: `QDesktopServices.openUrl(QUrl.fromLocalFile(path))`.",
       "**Own rendering**: libraries such as `pypdfium2` convert pages into images for a `QLabel` or a "
       "`QGraphicsView`. Check each library's license before distributing it (Chapter 30)."),
    lst("c24_pdf.py", "Displaying a PDF with the built-in viewer of QWebEngineView"),
    out("c24_pdf"),

    h2("Integrated help: QtHelp and QHelpEngine"),
    p("QtHelp offers searchable documentation inside the application, in the same format as Qt Assistant. The "
      "workflow has three steps: write HTML pages and a `.qhp` project (table of contents, keywords and "
      "files); compile it with `qhelpgenerator` into a `.qch` file; and register it at run time in a "
      "collection (`.qhc`) with `QHelpEngine`. The ready-made widgets — `contentWidget()`, `indexWidget()` and "
      "those for search — make up the help window."),
    lst("resources/help/manual.qhp", "Help project (.qhp): table of contents, keywords and files",
        lang="xml", nota="✔ Compiled with qhelpgenerator; the resulting .qch is used by Listing 24.7."),
    lst("c24_help.py", "QtHelp: registering the .qch, index, contents, display and search"),
    out("c24_help"),
    bl("`qhelpgenerator` does not ship with the PyQt6 wheels. In the test, the one from Ubuntu's "
       "`qt6-documentation-tools` package (Qt 6.4) was used, and the `.qch` was read normally by QtHelp 6.12.",
       "In Qt 6, `QHelpEngineCore` is **read-only by default**: without `setReadOnly(False)`, "
       "`registerDocumentation()` returns `False` with the error \"Cannot register namespace\" (verified).",
       "The pages use `qthelp://namespace/folder/file` URLs; `QTextBrowser` needs a reimplemented "
       "`loadResource()` to read them with `fileData()`.",
       "Full-text search requires indexing (`reindexDocumentation()`); in Qt 6, `search()` takes the query as "
       "text."),

    h2("COM/ActiveX automation on Windows: QAxContainer"),
    p("The `QAxContainer` module, present only in the PyQt6 wheels for Windows, controls COM objects and "
      "ActiveX controls: Microsoft Office, legacy supervisory systems, instruments with a COM driver. "
      "`QAxObject(\"ProgID\")` creates the object; `querySubObject()` navigates the hierarchy; `dynamicCall()` "
      "calls methods with a Qt-style signature; COM properties are read and written with `property()` and "
      "`setProperty()`; the `exception` signal reports COM errors."),
    lst("c24_activex.py.win", "QAxContainer: exporting results to Microsoft Excel via COM",
        nota="⚠ Not run in the test environment (Linux): requires Windows with Microsoft Excel. The names of "
             "classes, methods and signals were checked against the QAxContainer.pyi stubs file of the "
             "PyQt6 6.12.0 wheel for Windows."),
    p("Writing is done cell by cell, one COM call per value — simple and supported by any Excel version, but "
      "slow for large volumes. For thousands of rows, generate the file directly with a spreadsheet library "
      "(for example, `openpyxl`) or export CSV, and use COM automation only for what requires Excel running "
      "(macros, pivot charts, printing)."),

    h2("Chapter exercises"),
    nl("Generate an HTML report from a `QSqlQueryModel` (Chapter 15), display it in a `QWebEngineView` and "
       "export it to PDF.",
       "Add to the bridge of Listing 24.4 a slot that receives a JSON object and validates its fields.",
       "Use a JavaScript chart (for example, a charting library served through the `engapp://` scheme) fed "
       "by a Python signal every second.",
       "Build a help window with table of contents, index and search using the `QHelpEngine` widgets.",
       "On Windows, read an input spreadsheet with `QAxObject` and import the data into a Qt model."),
)

CAP25 = flat(
    ch("OpenGL, Vulkan and 3D", ST_AVA, [
        "Render with OpenGL inside widgets.",
        "Know Qt's 3D options and their current status.",
        "Choose between Qt Quick 3D, Qt 3D (deprecated) and low-level rendering.",
    ]),
    p("All the examples in this chapter require graphics acceleration. They were run under a virtual X11 server "
      "(Xvfb) with Mesa (OpenGL 4.5 and Vulkan in software: llvmpipe and lavapipe). On the `offscreen` "
      "platform there is no OpenGL context, and `QOpenGLWidget` reports \"not supported on this platform\"."),
    h2("QOpenGLWidget and the QtOpenGL module"),
    p("`QOpenGLWidget` renders into a *framebuffer object* and is composited with the other widgets, coexisting "
      "with layouts, overlays and QSS. The helper classes of the `QtOpenGL` module — `QOpenGLShaderProgram`, "
      "`QOpenGLBuffer`, `QOpenGLVertexArrayObject`, `QOpenGLTexture`, `QOpenGLFramebufferObject` — "
      "encapsulate the OpenGL objects. The context version and profile are requested with "
      "`QSurfaceFormat.setDefaultFormat()` **before** creating the `QApplication`."),
    h3("initializeGL(), resizeGL() and paintGL()"),
    bl("`initializeGL()`: once, with the context current — compile shaders and create buffers and textures.",
       "`resizeGL(w, h)`: on every resize — adjust projection and aspect ratio.",
       "`paintGL()`: on every frame — draw. To animate, call `update()`; never call `paintGL()` directly.",
       "Outside these methods, call `makeCurrent()`/`doneCurrent()` before using OpenGL functions."),
    lst("c25_opengl.py", "QOpenGLWidget with OpenGL 4.1 Core: shaders, VBO, VAO and uniform"),
    out("c25_opengl"),
    img("Triangle rendered with OpenGL 4.1 Core in a QOpenGLWidget", "f25_1_opengl.png", 9.0),
    h3("Shaders, buffers and textures"),
    p("In the *Core* profile, all drawing goes through GLSL shaders. The VAO remembers the VBO and the attribute "
      "layout (`setAttributeBuffer(location, type, offset, tupleSize, stride)`); uniforms such as the `mvp` "
      "matrix (`QMatrix4x4`) are set with `setUniformValue()`. Textures come from a `QImage` with "
      "`QOpenGLTexture(image.mirrored())` — OpenGL expects the origin in the lower-left corner."),
    note("WARNING", "PyQt6 ships only the OpenGL 2.0, 2.1 and 4.1 Core function tables. Requesting the table of "
                    "the context actually created (4.5 in the test) raises `TypeError: "
                    "QOpenGLFunctions_4_5_Core is not supported by PyQt6` (verified); request 4.1 Core "
                    "explicitly, as in the listing. PyQt6 does not export the `GL_*` constants either: use the "
                    "values from the specification or the PyOpenGL package."),

    h2("QRhiWidget and the rendering hardware abstraction (QRhi)"),
    p("**QRhi** (*Rendering Hardware Interface*) is the layer Qt 6 uses to draw Qt Quick, Qt Quick 3D and "
      "QtGraphs on top of each platform's native API: Direct3D 11/12, Metal, Vulkan or OpenGL. `QRhiWidget` "
      "(Qt 6.7+) exposes this layer to Widgets: `initialize()` creates resources and `render()` records "
      "commands in a `QRhiCommandBuffer`. Shaders are written in Vulkan GLSL and precompiled to the `.qsb` "
      "format by the `qsb` tool, which does not ship with the PyQt6 wheels (it is, for example, in PySide6, "
      "as `pyside6-qsb`, and in the Qt SDK)."),
    lst("c25_rhi.py", "QRhiWidget: render pass with an animated clear"),
    out("c25_rhi"),
    p("A complete pipeline adds, in `initialize()`, `rhi.newBuffer()` for the vertices, "
      "`rhi.newShaderResourceBindings()` for uniforms and textures and `rhi.newGraphicsPipeline()` with the "
      "`QShader.fromSerialized(qsb_data)` stages; in `render()`, `setGraphicsPipeline()`, "
      "`setShaderResources()`, `setVertexInput()` and `draw()` between `beginPass()` and `endPass()`. The gain "
      "over plain OpenGL is portability: the same code uses Direct3D on Windows and Metal on macOS."),

    h2("Vulkan: QVulkanInstance"),
    p("For direct Vulkan, the starting point is `QVulkanInstance`: API version, layers (such as the "
      "`VK_LAYER_KHRONOS_validation` validation layer, when installed) and extensions. The instance is "
      "associated with a window through `QWindow.setVulkanInstance()`. For most Python applications, Vulkan is "
      "used indirectly — via QRhi — rather than called directly."),
    lst("c25_vulkan.py", "QVulkanInstance: version, layers, extensions and creation"),
    out("c25_vulkan"),
    p("Set the API version before `create()`: in the test, without `setApiVersion()`, the loader rejected "
      "`apiVersion = 0` and the instance was not created."),

    h2("Qt Quick 3D with Python"),
    p("**Qt Quick 3D** is the 3D stack recommended by Qt: scenes declared in QML (`View3D`, cameras, lights, "
      "`Model` with meshes and PBR materials), rendered by QRhi, with glTF model import through the `balsam` "
      "tool. Python controls the scene through properties and can generate its own geometry by subclassing "
      "`QQuick3DGeometry` (`QtQuick3D` module)."),
    lst("c25_quick3d.qml", "Qt Quick 3D scene: camera, light, models and a property controlled by Python",
        lang="qml", nota="✔ File loaded and rendered by Listing 25.5 (run and verified)."),
    lst("c25_quick3d.py", "Qt Quick 3D in a QQuickWidget, controlled by Python"),
    out("c25_quick3d"),
    img("Qt Quick 3D scene rendered in a QQuickWidget", "f25_2_quick3d.png", 10.0),

    h2("Qt 3D (deprecated since Qt 6.8)"),
    h3("Qt3DCore, Qt3DRender, Qt3DExtras, Qt3DInput, Qt3DLogic and Qt3DAnimation"),
    p("Qt 3D organizes the scene into **entities** made up of **components** (mesh, material, transform), with "
      "a configurable *frame graph* and input, logic and animation aspects. It is still in the PyQt6-3D 6.12 "
      "package, but it has been deprecated since Qt 6.8 and should not be chosen for new projects."),
    lst("c25_qt3d.py", "Qt 3D: entity, mesh, material, transform and camera"),
    out("c25_qt3d"),
    h3("Migration strategy"),
    bl("Rewrite the scene in Qt Quick 3D: `QEntity` + components become a `Model` with `source`/`geometry` "
       "and `materials`; `QTransform` becomes `position`, `eulerRotation` and `scale`.",
       "Procedural meshes (`QCuboidMesh`, `QSphereMesh`...) correspond to the `#Cube`, `#Sphere`, "
       "`#Cylinder`, `#Cone` and `#Rectangle` primitives; meshes from files are converted with `balsam`.",
       "`QPhongMaterial` is close to `DefaultMaterial`; prefer `PrincipledMaterial` (PBR).",
       "Camera controllers: `OrbitCameraController` and `WasdController` (QtQuick3D.Helpers module).",
       "For scientific data visualization, evaluate QtGraphs first (Chapter 22)."),

    h2("Chapter exercises"),
    nl("Add a texture loaded from a `QImage` to the triangle of Listing 25.1.",
       "Compile a pair of shaders with `pyside6-qsb` and draw a triangle with `QRhiWidget`.",
       "Generate a surface with `QQuick3DGeometry` from a NumPy mesh and display it in Qt Quick 3D.",
       "Migrate the scene of Listing 25.6 to Qt Quick 3D, keeping the orbit camera."),
)

CAP26 = flat(
    ch("QML and Qt Quick with Python", ST_AVA, [
        "Decide between Qt Widgets and Qt Quick for each project.",
        "Expose Python objects, properties and models to QML.",
        "Combine QML and Widgets in the same application.",
    ]),
    h2("Qt Widgets versus Qt Quick"),
    tab("Qt Widgets versus Qt Quick", ["Criterion", "Qt Widgets", "Qt Quick (QML)"],
        [["Paradigm", "Imperative, in Python", "Declarative (QML) + logic in Python"],
         ["Appearance", "Native desktop; QSS", "Free, animated, fluid; Quick Controls styles"],
         ["Rendering", "Raster (CPU), with optional OpenGL", "Accelerated scene graph (QRhi)"],
         ["Dense forms and tables", "Excellent (mature Model/View)", "Possible, with more work"],
         ["Touch, animation, embedded screens", "Limited", "Excellent"],
         ["Modern charts and 3D", "Via QQuickWidget", "Native (QtGraphs, Quick 3D)"],
         ["Tools", "Qt Designer", "Qt Design Studio, qmllint, qmlls"]],
        [2600, 3100, 3371]),
    p("It is not an exclusive choice: technical applications often have their body in Widgets (forms, tables, "
      "trees) and visual components in QML embedded with `QQuickWidget` (Section 26.5)."),

    h2("QQmlApplicationEngine and QQuickView"),
    p("`QQmlApplicationEngine` loads a QML file whose root is a window (`Window`/`ApplicationWindow`). "
      "`QQuickView` is a window that displays any QML item, with `rootContext()` for context properties. In "
      "both, check for errors: an empty `engine.rootObjects()` or `view.status() == Error` indicates failure, "
      "and the `warnings` signal carries the messages with file and line."),

    h2("Exposing Python to QML"),
    lst("c26_main.qml", "QML interface that uses a singleton and a type defined in Python", lang="qml",
        nota="✔ File loaded by Listing 26.2 (run and verified)."),
    lst("c26_engine.py", "QQmlApplicationEngine with singleton, registered type, properties and signals"),
    out("c26_engine"),
    h3("Context properties and singleton objects"),
    p("There are two ways of handing a ready-made Python object to QML. "
      "`rootContext().setContextProperty(\"name\", obj)` (Listing 26.4) is simple, but the name is resolved "
      "dynamically and the tools (qmllint, qmlls) do not know it. `qmlRegisterSingletonInstance(uri, major, "
      "minor, \"Name\", obj)` registers the object in a module (`import Engineering 1.0`), with a known name — "
      "the recommended way. In both cases, keep a Python reference to the object while QML uses it."),
    h3("pyqtProperty with a notify signal"),
    p("QML only updates *bindings* when the property has a notification signal: declare "
      "`pyqtProperty(type, notify=signal)` and emit the signal on every change. In the listing, switching the "
      "unit emits `unitChanged`, and the pressure label — which reads `Calculator.unit` — is re-evaluated "
      "automatically (2944.70 psi for 2000 m). Slots with `@pyqtSlot(..., result=type)` can be called from QML "
      "and return values."),
    h3("Type registration: qmlRegisterType() and related functions"),
    p("`qmlRegisterType(Class, uri, major, minor, \"Name\")` allows the Python class to be **instantiated** "
      "inside QML (`Tank { diameter: 3.0 }`). The related functions are `qmlRegisterSingletonType`, "
      "`qmlRegisterUncreatableType` (visible but non-instantiable type, for enums and attached types) and "
      "`qmlRegisterAnonymousType`."),
    note("WARNING", "To get in Python an object created by QML from a Python type, declare "
                    "`property QtObject name: id` in the root. In the test, a `property alias` to the same object "
                    "reached Python as an unusable `sip.voidptr`, and `findChild()` did not find it — non-visual "
                    "objects declared in an `ApplicationWindow` are not its QObject children."),

    h2("Python models in QML"),
    p("Any `QAbstractItemModel` from Chapter 14 can feed `ListView`, `TableView`, `Repeater` and the like. QML "
      "does not use columns or `DisplayRole`: it accesses **roles by name**, defined in `roleNames()`. In the "
      "delegate, declare each role as a `required property` — the recommended way in Qt 6, which makes the "
      "dependencies explicit and verifiable."),
    lst("c26_model.qml", "ListView with a delegate that uses required properties", lang="qml",
        nota="✔ File loaded by Listing 26.4 (run and verified)."),
    lst("c26_model.py", "QAbstractListModel with roleNames() displayed in QML"),
    out("c26_model"),
    p("The model notifications (`beginInsertRows`/`endInsertRows`, `dataChanged` with the list of roles) "
      "update the list without recreating the existing delegates: the third well appeared and the first one "
      "became inactive."),

    h2("QQuickWidget: QML inside Widgets applications"),
    p("`QQuickWidget` is a widget that displays a QML scene: it goes into layouts, receives focus and can be "
      "captured with `grab()`. Communication in both directions uses properties (`rootObject().setProperty`) "
      "and signals declared in QML, connected directly in Python (`root.alarm.connect(...)`)."),
    lst("c26_indicator.qml", "Circular indicator in QML with property, signal and animation", lang="qml",
        nota="✔ File loaded by Listing 26.6 (run and verified)."),
    lst("c26_qquickwidget.py", "QQuickWidget in a Widgets window with a QSlider and a QML signal"),
    out("c26_qquickwidget"),
    img("QML component (indicator) controlled by a QSlider in a Widgets window", "f26_1_qquickwidget.png", 9.5),
    note("TIP", "`QQuickWidget` draws into a texture and composites it with the widgets, which has a cost. For "
                "a large, independent QML scene, `QWidget.createWindowContainer(QQuickView)` is more efficient, "
                "with the restriction that nothing can be overlaid on the embedded window."),

    h2("Qt Quick Controls and styles"),
    p("Qt Quick Controls (`Button`, `SpinBox`, `ApplicationWindow`...) have interchangeable styles. PyQt6 does "
      "not include the `QtQuickControls2` module (there is no `QQuickStyle`); the style is chosen by the "
      "`QT_QUICK_CONTROLS_STYLE` environment variable, by the `qtquickcontrols2.conf` file packaged with the "
      "QML or by the `-style` command-line argument. Listing 26.2 ran with `Fusion`."),
    tab("Qt Quick Controls styles present in the PyQt6-Qt6 6.12 wheels (Linux)",
        ["Style", "Characteristics"],
        [["Basic", "Light and neutral; base for custom styles"],
         ["Fusion", "Desktop look, the same as the Widgets Fusion style"],
         ["Material", "Google Material Design, with light/dark themes and accent color"],
         ["Universal", "Microsoft design guidelines (Universal)"],
         ["FluentWinUI3", "Windows 11 look (WinUI 3)"],
         ["Imagine", "Based on images (9-patch) supplied by the project"],
         ["Native", "Selects the platform's native style (Windows, macOS, iOS)"]],
        [2200, 6871]),

    h2("Chapter exercises"),
    nl("Add to Listing 26.2 a `TextField` with numeric validation bound to `Tank.level`.",
       "Display the `WellModel` model in a QML `TableView` with two columns.",
       "Implement the indicator of Listing 26.5 as a `QQuickPaintedItem` in Python and compare.",
       "Run Listing 26.2 with the Material and Universal styles and compare the screenshots."),
)
