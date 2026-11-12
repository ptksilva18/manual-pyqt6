# -*- coding: utf-8 -*-
"""Part III — Chapters 20 to 22 (English edition)."""
from blocks import ST_AVA, bl, ch, flat, h2, h3, img, lst, nl, note, out, p, snip, tab

CAP20 = flat(
    ch("Concurrency and asynchronous programming", ST_AVA, [
        "Keep the interface responsive during long tasks.",
        "Apply QThread, QThreadPool and synchronization primitives.",
        "Combine the Qt event loop with threading, multiprocessing and asyncio.",
    ]),
    h2("Why never to block the event loop"),
    p("The whole interface — painting, keyboard, mouse, timers, queued signals — is processed by the event loop "
      "of the main thread (Chapter 4). While a slot is running, nothing else happens: the window does not "
      "repaint, the buttons do not respond and the operating system may mark it as \"not responding\". "
      "Listing 20.1 measures this effect with a 20 ms `QTimer`: with the computation in the GUI thread, the "
      "loop stays stopped for 600 ms; with the same computation in a worker, the timer keeps firing "
      "regularly."),
    lst("c20_blocking.py", "Event loop responsiveness: computation in the GUI thread versus in a worker"),
    out("c20_blocking"),
    p("The worker is also Python code and competes with the GUI thread for the **GIL** (*Global Interpreter "
      "Lock*). The interpreter switches between threads every 5 ms (`sys.getswitchinterval()`), which explains "
      "the worst interval of a few tens of milliseconds in the second phase: the interface stays fluid, but "
      "there is no parallelism gain for pure-Python computation. For real CPU parallelism, use processes "
      "(Section 20.6) or libraries that release the GIL in native code, such as NumPy and SciPy in vectorized "
      "operations."),
    note("WARNING", "Widgets may only be created, read and changed in the GUI thread. A secondary thread never "
                    "calls `label.setText()` directly: it emits a signal, and the GUI slot makes the update. "
                    "Breaking this rule produces intermittent failures and freezes that are hard to "
                    "reproduce."),

    h2("QThread"),
    p("`QThread` is not the thread: it is the object that **manages** an operating-system thread. When "
      "`start()` is called, the new thread executes `run()`, whose default implementation runs its own event "
      "loop (`exec()`). It is this event loop that allows objects moved to the thread to receive queued "
      "signals."),
    h3("Worker pattern with moveToThread()"),
    p("The recommended pattern puts the work in a `QObject` (the *worker*) and moves it to the thread with "
      "`moveToThread()`. Listing 20.2 implements the full cycle: the `started` signal triggers `work()`, the "
      "worker publishes progress, result, cancellation or error through signals, and `done` ends the thread's "
      "event loop (`quit`). The `deleteLater()` calls connected to `done` and to `finished` release the worker "
      "and the `QThread` at the right moment, without leaks."),
    lst("c20_worker.py", "Worker pattern with moveToThread(): progress, result, error and cancellation"),
    out("c20_worker"),
    img("Worker pattern with QThread and queued signals", "f20_1_worker.png", 15.0),
    p("Look at the output: `start()` and the progress slots run in the `GUI` thread; `work()` runs in "
      "`integrator-1` and `integrator-2`. Cancellation is **cooperative**: `requestInterruption()` only flags "
      "a request, and the worker checks it between blocks with `isInterruptionRequested()`. The bar stopped "
      "slightly above 40 %, because a block was already being processed when the request arrived — correct and "
      "expected behavior. That is why the Cancel button is disabled in its own click, avoiding repeated "
      "requests."),
    note("TIP", "Exceptions inside the worker do not reach the GUI thread. Catch them in the worker itself and "
                "turn them into an `error(str)` signal, as in Listing 20.2; otherwise the error disappears or "
                "terminates the process (Chapter 3)."),
    h3("QThread subclass: when (not) to use it"),
    p("Reimplementing `run()` is appropriate for self-contained loops that do not need to receive signals — "
      "continuous acquisition, for example. The classic pitfall appears in Listing 20.3: the `QThread` object "
      "belongs to the thread that created it, so **slots declared in the subclass execute in the GUI thread**, "
      "not in `run()`."),
    lst("c20_qthread_sub.py", "QThread subclass: run() in the new thread, slots in the thread of origin"),
    out("c20_qthread_sub"),
    h3("Safe shutdown: requestInterruption(), quit() and wait()"),
    p("A thread still running when the program ends causes the message `QThread: Destroyed while thread is "
      "still running` and may abort the process. The safe sequence is: request the stop "
      "(`requestInterruption()` for loops in `run()`, `quit()` for the worker's event loop), wait with "
      "`wait()` — optionally with a deadline, via `QDeadlineTimer` — and only then destroy the objects. The "
      "`closeEvent()` of Listing 20.2 applies this sequence when the user closes the window with a task in "
      "progress. Avoid `terminate()`: it stops the thread at an arbitrary point and may leave mutexes locked "
      "and data corrupted."),

    h2("QThreadPool and QRunnable"),
    p("For many short, independent tasks, creating one `QThread` per task is wasteful. `QThreadPool` keeps "
      "reusable threads and a queue of `QRunnable` objects. The global pool (`QThreadPool.globalInstance()`) "
      "uses, by default, one thread per logical core; your own pools let you limit concurrency with "
      "`setMaxThreadCount()`. Since `QRunnable` does not inherit from `QObject`, the signals live in a helper "
      "object. PyQt6 also accepts a Python *callable* in `start()`."),
    lst("c20_pool.py", "QThreadPool with QRunnable, helper signals and callables"),
    out("c20_pool"),
    p("`waitForDone()` blocks until the pool is empty and should only be used in scripts, tests or at "
      "shutdown. In the interface, use the completion signals. Task 5 shows the error handling: the exception "
      "is caught in `run()` and reported by the `failed` signal."),

    h2("Synchronization"),
    p("When threads share mutable data, access has to be coordinated. The GIL only protects the internal "
      "integrity of the interpreter, not the program logic: an operation such as `self.value += 1` involves a "
      "read, an addition and a write, and another thread can step in between them."),
    lst("c20_sync.py", "Synchronization: QMutex, QReadWriteLock, QWaitCondition and QSemaphore"),
    out("c20_sync"),
    h3("QMutex, QMutexLocker and QRecursiveMutex"),
    p("`QMutex` guarantees mutual exclusion: `lock()` before the critical section and `unlock()` in a "
      "`finally` block, so that the mutex is released even if an exception occurs. In C++, the usual idiom is "
      "`QMutexLocker`; in PyQt6 6.12, however, it failed in the tests for this manual (see the box below). "
      "`QRecursiveMutex` allows the same thread to lock the mutex more than once, which is useful when a "
      "protected method calls another; prefer, however, to reorganize the code so that it is not needed."),
    note("WARNING", "With 4 threads contending for the same mutex, `with QMutexLocker(mutex):` terminated the "
                    "process with a segmentation fault or *abort* in 5 of 15 runs (PyQt6 6.12.0, Python 3.13); "
                    "creating the `QMutexLocker` without `with` also failed (3 of 12). With `lock()`/`unlock()` "
                    "in `try/finally` and with `threading.Lock`, there were 0 failures in 15 runs; `QReadLocker` "
                    "and `QWriteLocker` used with `with` did not fail either (0 of 12). That is why Listing 20.5 "
                    "uses explicit `lock()`/`unlock()`."),
    h3("QReadWriteLock, QReadLocker and QWriteLocker"),
    p("When reads predominate, `QReadWriteLock` allows several simultaneous readers and a single exclusive "
      "writer. `QReadLocker` and `QWriteLocker` lock in the corresponding mode and release when the `with` "
      "block ends, as in Listing 20.5."),
    h3("QSemaphore and QWaitCondition"),
    p("`QWaitCondition` lets a thread sleep until another one signals a condition (`wakeOne()`, `wakeAll()`); "
      "the wait releases the mutex atomically and reacquires it on waking up. The `while` loop around `wait()` "
      "is mandatory, because the condition must be re-evaluated on waking up. The bounded buffer of the "
      "listing never exceeded 8 items and delivered all 10 000 values, with the sum checked. `QSemaphore` "
      "controls a number of resources (`acquire`, `tryAcquire`, `release`); `QSemaphoreReleaser` releases "
      "automatically when it goes out of scope."),
    note("NOTE", "PyQt6 does not expose `QThread.create()` (a C++ function that accepts a callable). The "
                 "`FunctionThread` class of Listing 20.5 plays this role in five lines."),

    h2("Thread-safe communication through signals"),
    p("Emitting a signal is safe in any thread. The **connection type** defines where the slot executes "
      "(Table 5.1): with `AutoConnection` (the default), if the receiver lives in another thread, Qt copies "
      "the arguments into an event and the slot runs in the event loop of the receiver's thread. Listing 20.6 "
      "confirms each case and shows `QMetaObject.invokeMethod()`, which calls a slot of another object by "
      "name, in that object's thread."),
    lst("c20_thread_signals.py", "Connection types between threads and QMetaObject.invokeMethod"),
    out("c20_thread_signals"),
    bl("**DirectConnection** executed the slot in the `worker` thread: if the slot touched widgets, it would "
       "break the rule of Section 20.1.",
       "**BlockingQueuedConnection** made the emitter wait for the slot to finish — useful to obtain "
       "synchronous confirmation, but it causes a *deadlock* if emitter and receiver are in the same thread.",
       "The order of the lines shows that the queued slots executed after the direct call, in the order of "
       "the emissions."),

    h2("Python threading, concurrent.futures and multiprocessing with Qt"),
    p("The standard-library tools coexist with Qt as long as the golden rule is respected: the result goes "
      "back to the GUI through a signal. In Listing 20.7, `add_done_callback()` is executed in the thread that "
      "completed the future; the callback only emits a signal of a `QObject` that lives in the GUI, and the "
      "queued connection does the rest. The task with an invalid argument shows that exceptions from child "
      "processes are propagated through the `Future`."),
    lst("c20_futures.py", "concurrent.futures with processes and threads integrated with Qt"),
    out("c20_futures"),
    bl("**ThreadPoolExecutor**: I/O (files, network, databases) — the GIL is released while waiting.",
       "**ProcessPoolExecutor**: intensive Python computation — each process has its own interpreter and GIL. "
       "Arguments and results are serialized with `pickle`; functions must be importable at module level.",
       "The `spawn` start method is the default on Windows and macOS and the safest one with Qt on any "
       "system, because `fork` duplicates a process that already has threads and Qt state. With `spawn`, the "
       "`if __name__ == \"__main__\":` guard is mandatory.",
       "Child processes must never create widgets or access Qt objects of the parent process."),

    h2("asyncio and the Qt event loop (third-party integration libraries)"),
    p("`asyncio` has its own event loop, incompatible with `app.exec()`: two loops cannot run at the same time "
      "in the same thread. PyQt6 has no native integration (PySide6 offers the `QtAsyncio` module); the usual "
      "solution is the **qasync** library (BSD license), which implements the `asyncio` loop on top of the Qt "
      "loop. Coroutines and signals then share the same thread, without blocking."),
    lst("c20_asyncio.py", "asyncio on top of the Qt event loop with qasync"),
    out("c20_asyncio"),
    p("The three concurrent queries took about 0.3 s, not 0.60 s; `asyncio.to_thread()` delegated the "
      "blocking computation to a thread and `wait_for()` imposed a deadline on the slow query. Use `asyncio` "
      "when the application already depends on asynchronous libraries (HTTP clients, OPC UA, MQTT); for the "
      "rest, Qt's native resources (signals, `QNetworkAccessManager`, `QThread`) are enough and add no "
      "dependency."),

    h2("Progress and cancellation of long tasks"),
    p("The pattern of Listing 20.2 sums up the good practices:"),
    bl("Publish progress as an **integer percentage** and only when it changes; thousands of signals per "
       "second clog the GUI event queue.",
       "Make cancellation cooperative, with checks at safe points (between blocks, between files).",
       "Disable the controls that start the task while it runs, and the cancel control after it is clicked.",
       "For modal progress dialogs, `QProgressDialog` (Chapter 9) with `canceled` connected to "
       "`requestInterruption()` covers most cases.",
       "Guarantee shutdown in the window's `closeEvent()` and in the application's `aboutToQuit` signal."),

    h2("Chapter exercises"),
    nl("Modify Listing 20.1 to measure the worst interval with the computation done by `numpy.linalg.solve` on "
       "a 2000 × 2000 matrix in the worker, and compare it with the Python loop. Explain the difference based "
       "on the GIL.",
       "Add a Pause/Resume button to Listing 20.2 using `QMutex` and `QWaitCondition`.",
       "Use a `QThreadPool` with `setMaxThreadCount(2)` to process 20 CSV files, showing the overall progress "
       "in a `QProgressBar`.",
       "Rewrite Listing 20.7 to cancel the pending futures when the window is closed (`Future.cancel()` and "
       "`shutdown(cancel_futures=True)`).",
       "Explain why Listing 20.3 printed that `subclass_slot()` executed in the GUI thread, and propose the "
       "fix with the worker pattern."),
)

CAP21 = flat(
    ch("Networking, communication and devices", ST_AVA, [
        "Consume HTTP/REST APIs asynchronously.",
        "Implement TCP, UDP and WebSocket clients and servers.",
        "Communicate with serial, Bluetooth and NFC devices.",
    ]),
    p("All the examples in this chapter use local servers (127.0.0.1) created by the program itself, so they "
      "run without internet access and produce reproducible outputs. The Qt API is asynchronous: no call "
      "blocks the event loop, and the results arrive through signals."),
    h2("HTTP with QNetworkAccessManager"),
    h3("QNetworkRequest and QNetworkReply"),
    p("`QNetworkAccessManager` (NAM) sends requests and immediately returns a `QNetworkReply`; the `finished` "
      "signal indicates completion. A single instance per application (or per thread) is enough: it reuses "
      "connections, cookies and cache. Each reply must be released with `deleteLater()` after use."),
    lst("c21_http.py", "HTTP with QNetworkAccessManager: GET/POST JSON, errors, timeout and progress"),
    out("c21_http"),
    h3("JSON, headers, timeouts and error handling"),
    bl("Known headers use `setHeader(QNetworkRequest.KnownHeaders...)`; the others, "
       "`setRawHeader(b\"Name\", b\"value\")`. In the reply, `header()` and `rawHeader()`.",
       "The HTTP status code comes from `attribute(QNetworkRequest.Attribute.HttpStatusCodeAttribute)`. 4xx/5xx "
       "replies also produce an `error()` other than `NoError` (for example, `ContentNotFoundError` for 404), "
       "but the error body sent by the server is still available in `readAll()`.",
       "By default **there is no transfer timeout** (`transferTimeout()` = 0, verified on Qt 6.12). Set a "
       "global value with `QNetworkAccessManager.setTransferTimeout()` or per request; when it expires, the "
       "error is `TimeoutError`, as in the output.",
       "In Qt 6, redirects are followed by default (`NoLessSafeRedirectPolicy`): from HTTPS to HTTP they are "
       "not, in the other cases they are.",
       "For JSON, `json.loads(bytes(reply.readAll()))` is the most direct way; `QJsonDocument` also works "
       "(Chapter 16)."),
    h3("Upload, download and progress"),
    p("`downloadProgress(received, total)` and `uploadProgress(sent, total)` feed progress bars; `total` is −1 "
      "when the server does not report `Content-Length`. For large files, read the data incrementally in "
      "`readyRead` and write it to disk (preferably with `QSaveFile`), instead of accumulating everything in "
      "memory until `finished`. Sending *multipart* forms uses `QHttpMultiPart`; since Qt 6.7, "
      "`QRestAccessManager` and `QNetworkRequestFactory` offer a convenience API for REST services (both "
      "present in PyQt6 6.12; see Annex A)."),
    note("WARNING", "Do not use `requests` or `urllib` in the GUI thread: they are blocking. If you need those "
                    "libraries, run them in a worker (Chapter 20)."),

    h2("Sockets"),
    h3("TCP: QTcpSocket and QTcpServer"),
    p("TCP delivers a reliable, ordered **stream** of bytes, but does not preserve message boundaries: one "
      "`write()` may arrive in several `readyRead` signals, and several `write()` calls may arrive in a single "
      "one. The application protocol has to define the **framing** — line terminator, length prefix or "
      "self-delimiting format. Listing 21.2 deliberately sent two messages in a single `write()` and one "
      "message in two pieces; framing by line reassembled everything correctly."),
    lst("c21_tcp.py", "TCP with QTcpServer and QTcpSocket: line protocol and framing"),
    out("c21_tcp"),
    h3("UDP: QUdpSocket"),
    p("UDP sends independent **datagrams**, connectionless, with no guarantee of delivery or order, but with "
      "preserved boundaries and low latency — suitable for periodic telemetry, discovery on the local network "
      "and *broadcast*. The binary format of the listing is defined with `struct` (fixed size of 16 bytes)."),
    lst("c21_udp.py", "UDP with QUdpSocket and binary datagrams"),
    out("c21_udp"),
    h3("SSL/TLS: QSslSocket and QSslConfiguration"),
    p("`QSslSocket` adds TLS to a TCP socket; `QSslServer` (Qt 6.4+) accepts encrypted connections. The server "
      "certificate and the private key go into the `QSslConfiguration`. On the client, peer verification is "
      "mandatory by default: an unknown self-signed certificate produces `SelfSignedCertificate`, and a name "
      "that differs from the certificate produces `HostNameMismatch`. The example certificate was generated "
      "with:"),
    snip(["openssl req -x509 -newkey rsa:2048 -nodes -days 3650 \\",
          "    -keyout server.key -out server.crt \\",
          "    -subj \"/CN=localhost/O=PyQt6 Manual (example)\" \\",
          "    -addext \"subjectAltName=DNS:localhost,IP:127.0.0.1\""], lang="text"),
    lst("c21_tls.py", "TLS with QSslServer and QSslSocket: certificate and name verification"),
    out("c21_tls"),
    note("WARNING", "Never call `ignoreSslErrors()` without arguments in production: that turns off the "
                    "protection against man-in-the-middle attacks. For your own CA, add the CA certificate with "
                    "`setCaCertificates()` — as in the listing — or ignore only specific, expected errors."),

    h2("WebSockets: QWebSocket and QWebSocketServer"),
    p("WebSocket (RFC 6455) keeps a bidirectional channel over an HTTP connection, with delimited text and "
      "binary messages — without TCP's framing problem. It is the standard for telemetry dashboards that "
      "receive data from the server in real time. The server's `SecureMode` uses TLS (`wss://`)."),
    lst("c21_websocket.py", "WebSockets: server and client exchanging JSON and binary data"),
    out("c21_websocket"),

    h2("OAuth authentication with QtNetworkAuth"),
    p("The **PyQt6-NetworkAuth** package implements OAuth 1.0 and 2.0. For desktop applications, the "
      "recommended flow is **Authorization Code with PKCE**: the application opens the browser on the "
      "provider's login page, receives the authorization code at a local address "
      "(`QOAuthHttpServerReplyHandler`) and exchanges it for tokens. In Listing 21.6, a minimal local provider "
      "checks the PKCE and the \"browser\" is simulated by an HTTP request; in a real application, connect "
      "`authorizeWithBrowser` to `QDesktopServices.openUrl`."),
    lst("c21_oauth.py", "OAuth 2.0 Authorization Code + PKCE with QOAuth2AuthorizationCodeFlow"),
    out("c21_oauth"),
    bl("The PKCE (S256) was sent automatically by the flow, and the provider validated the `code_verifier`.",
       "`setRequestedScopeTokens()` and `grantedScopeTokens()` are the scope API of Qt 6.9+; the `state` "
       "against CSRF is also generated and checked by Qt.",
       "Store the *refresh token* in the system's secure storage (for example, with the `keyring` library), "
       "never in `QSettings` as plain text.",
       "For custom URL schemes or *app links*, Qt 6.8+ offers `QOAuthUriSchemeReplyHandler`."),

    h2("Remote objects: QtRemoteObjects"),
    p("Qt Remote Objects publishes a `QObject` (the source) to other processes or machines, which use it "
      "through **replicas**: synchronized properties, forwarded signals and remotely invoked slots. The `repc` "
      "compiler generates C++ code from `.rep` files; in Python, the **dynamic replica** (`acquireDynamic`) is "
      "used, and its interface is discovered at run time."),
    lst("c21_remoteobjects.py", "QtRemoteObjects: source and dynamic replica in separate processes"),
    out("c21_remoteobjects"),
    p("The replica should only be used after `initialized`. The remote slot call is asynchronous: the effect "
      "comes back as a property change (`pressureChanged -> 0.0`). `local:` addresses use local sockets; "
      "`tcp://host:port` crosses the network (without encryption: on untrusted networks, use a TLS tunnel)."),

    h2("D-Bus: QtDBus"),
    p("D-Bus is the inter-process communication bus of the Linux desktop (system services, notifications, "
      "power and network managers). The module exists on all platforms, but it is only useful where a D-Bus "
      "daemon is running. Listing 21.8 exports the slots of an object and calls them from another process; "
      "the test was run inside `dbus-run-session`."),
    lst("c21_dbus.py", "D-Bus: exported service and client in another process"),
    out("c21_dbus"),

    h2("Serial ports: QSerialPort and QSerialPortInfo"),
    p("Field instruments, PLCs, sensors and RS-232/RS-485/USB converters are still ubiquitous in engineering. "
      "`QSerialPort` is an asynchronous `QIODevice`: `readyRead` signals data, `canReadLine()`/`readLine()` "
      "handle line protocols and `errorOccurred` reports a disconnected cable or missing permission. "
      "`QSerialPortInfo.availablePorts()` lists the physical ports with description and USB identifiers "
      "(VID/PID)."),
    lst("c21_serial.py", "QSerialPort: acquisition of ASCII lines from an instrument"),
    out("c21_serial"),
    p("In the test, the instrument was simulated by a pair of virtual ports created with `socat` "
      "(`SERIAL_PORT` points to one of the ends); that is why the port used does not appear in "
      "`availablePorts()`, which lists only the detected hardware (`ttyS0`). On Windows, use names such as "
      "`COM3`; on Linux, the user must belong to the `dialout` group (or equivalent) to open `/dev/ttyUSB0`."),
    note("WARNING", "In PyQt6 6.12, `setBaudRate()` takes an `int`: passing `QSerialPort.BaudRate.Baud115200` "
                    "raises `TypeError` (verified). Use the number (`115200`) or the enum's `.value`."),
    img("Data acquisition architecture through a serial port", "f21_1_serial.png", 15.5),

    h2("Bluetooth and NFC"),
    p("**QtBluetooth** covers classic Bluetooth (RFCOMM) and **Low Energy** (BLE): discovery "
      "(`QBluetoothDeviceDiscoveryAgent`), connection to peripherals (`QLowEnergyController`), GATT services "
      "and characteristics (`QLowEnergyService`, `QLowEnergyCharacteristic`) and, on some platforms, the "
      "peripheral role. **QtNfc** reads and writes NFC tags (`QNearFieldManager`, `QNdefMessage`). Both depend "
      "on the system and the hardware — on Linux, Bluetooth uses BlueZ via D-Bus. The code must handle the "
      "absence of an adapter, as in Listing 21.10, run in an environment without Bluetooth and without NFC."),
    lst("c21_bluetooth.py", "Bluetooth LE and NFC: discovery with handling of missing hardware"),
    out("c21_bluetooth"),
    p("Once a peripheral is found, the typical BLE flow is: `QLowEnergyController.createCentral(info)` → "
      "`connectToDevice()` → `discoverServices()` → `createServiceObject(uuid)` → `discoverDetails()` → "
      "reading/writing characteristics or subscribing to notifications (`characteristicChanged`)."),
    snip("""controller = QLowEnergyController.createCentral(info)
controller.connected.connect(controller.discoverServices)
controller.discoveryFinished.connect(lambda: open_service(controller))
controller.errorOccurred.connect(lambda e: print("BLE:", e.name))
controller.connectToDevice()"""),

    h2("Chapter exercises"),
    nl("Add to Listing 21.1 a client with automatic retry (three attempts with exponential backoff) for timeout "
       "errors.",
       "Change the protocol of Listing 21.2 to use a length prefix (4 bytes, *big-endian*) instead of a line "
       "terminator.",
       "Implement a dashboard that receives telemetry over WebSocket and updates a chart (Chapter 22).",
       "In Listing 21.9, move the acquisition to a `QThread` and deliver the samples to the GUI in batches "
       "of 50.",
       "Write a BLE client that subscribes to notifications of a temperature characteristic and records the "
       "values in CSV."),
)

CAP22 = flat(
    ch("Data visualization and scientific charts", ST_AVA, [
        "Choose the right charting library for each case.",
        "Build 2D and 3D charts with QtGraphs and QtCharts.",
        "Integrate Matplotlib and pyqtgraph with real-time updates.",
    ]),
    h2("Overview of the visualization options"),
    tab("Comparison of visualization libraries for PyQt6", ["Library", "Type", "Status", "Recommended for"],
        [["QtGraphs (PyQt6-Graphs)", "2D (QML) and 3D", "Active — successor recommended by Qt",
          "New projects with a modern look and GPU-accelerated 3D"],
         ["QtCharts (PyQt6-Charts)", "2D (Graphics View)", "Deprecated since Qt 6.10",
          "Maintenance of existing code; simple business charts"],
         ["QtDataVisualization", "3D", "Deprecated since Qt 6.10", "Legacy only; migrate to QtGraphs"],
         ["Matplotlib (QtAgg backend)", "2D/3D, publication quality", "External library",
          "Reports, technical figures, wide variety of charts"],
         ["pyqtgraph", "2D/3D, high performance", "External library",
          "Real time, large volumes, oscilloscopes and monitoring"]],
        [2300, 1900, 2200, 2671]),
    p("The choice depends on three factors: **volume and update rate** of the data, the required **graphic "
      "quality** (screen or publication) and the acceptable **dependencies**. Listing 22.7, at the end of the "
      "chapter, measures the cost per update of the three most used approaches."),

    h2("QtGraphs"),
    p("QtGraphs (Qt 6.8+) unifies Qt's 2D and 3D charts on top of Qt Quick and the RHI rendering layer "
      "(Chapter 25). 2D charts are declared in QML (`GraphsView`); 3D charts have classes for Widgets in the "
      "`QtGraphsWidgets` module. Both require graphics acceleration: in the test environment, the listings ran "
      "under a virtual X11 server (Xvfb) with software OpenGL (Mesa llvmpipe); on the `offscreen` platform, "
      "without OpenGL, 3D is not displayed."),
    h3("2D charts with GraphsView in QML (QQuickWidget)"),
    p("The chart is described in QML (Listing 22.1) and embedded in a Widgets application with `QQuickWidget` "
      "(Chapter 26). Python locates series and axes by `objectName` with `findChild()` and manipulates them "
      "through the classes of the `QtGraphs` module (`QLineSeries`, `QScatterSeries`, `QValueAxis`)."),
    lst("c22_graphs2d.qml", "GraphsView in QML: theme, axes, line series and scatter series", lang="qml",
        nota="✔ File loaded and rendered by Listing 22.2 (run and verified)."),
    lst("c22_graphs2d.py", "QtGraphs 2D fed by Python in a QQuickWidget"),
    out("c22_graphs2d"),
    img("QtGraphs 2D chart (GraphsView) in a QQuickWidget", "f22_1_graphs2d.png", 13.0),
    p("Use `replace()` to swap all the points at once: it emits a single update signal, whereas `append()` in "
      "a loop causes one update per point."),
    h3("3D charts: Q3DBarsWidgetItem, Q3DScatterWidgetItem and Q3DSurfaceWidgetItem"),
    p("The 3D items for Widgets are not widgets: they are objects that control a QML scene inside a "
      "`QQuickWidget` given with `setWidget()`. Bars (`Q3DBarsWidgetItem`), scatter (`Q3DScatterWidgetItem`) "
      "and surface (`Q3DSurfaceWidgetItem`) share axes, theme, camera and selection."),
    lst("c22_graphs3d.py", "3D surface with Q3DSurfaceWidgetItem, color gradient and camera"),
    out("c22_graphs3d"),
    img("QtGraphs 3D surface (Q3DSurfaceWidgetItem) with a value gradient", "f22_2_graphs3d.png", 13.0),
    note("WARNING", "In PyQt6 6.12, creating the series with `QSurface3DSeries(proxy)` did not bind the proxy to "
                    "the series: the surface was empty and Qt warned \"series needs to be created to access "
                    "data members\" (verified). Use the default proxy, `series.dataProxy()`, as in Listing 22.3, "
                    "or `setDataProxy()`."),
    h3("Series, axes, data proxies and themes (QGraphsTheme)"),
    bl("**2D series**: `QLineSeries`, `QSplineSeries`, `QScatterSeries`, `QAreaSeries`, `QBarSeries`, "
       "`QPieSeries`; **3D**: `QBar3DSeries`, `QScatter3DSeries`, `QSurface3DSeries`.",
       "**Axes**: `QValueAxis`, `QLogValueAxis`, `QDateTimeAxis`, `QBarCategoryAxis` (2D); `QValue3DAxis`, "
       "`QCategory3DAxis` (3D).",
       "**3D proxies** separate the data source from the series: `QBarDataProxy`, `QScatterDataProxy`, "
       "`QSurfaceDataProxy`, `QHeightMapSurfaceDataProxy` (surface from an image) and the `QItemModel*` proxies "
       "that read directly from a Model/View model (Chapter 14).",
       "**Theme**: `QGraphsTheme` defines the light/dark scheme, series palette, grid and fonts, with ready-made "
       "themes (`QGraphsTheme.Theme`)."),

    h2("QtCharts (legacy)"),
    p("QtCharts was Qt's 2D charting solution for many years and is still present in PyQt6 6.12, but it has "
      "been **deprecated since Qt 6.10**: it keeps working, with no new features. Since it is based on Graphics "
      "View (Chapter 18), it works on any platform, even without graphics acceleration."),
    h3("QChart and QChartView"),
    p("`QChart` contains series, axes, legend and title; `QChartView` is the widget that displays it. Turn on "
      "antialiasing with `setRenderHint()`."),
    lst("c22_qtcharts.py", "QtCharts: line, spline, scatter, logarithmic axis, bars and pie"),
    out("c22_qtcharts"),
    img("Dashboard with four QtCharts charts", "f22_3_qtcharts.png", 15.5),
    h3("Series: line, spline, scatter, area, bars and pie"),
    p("The listing covers the most common cases. Two details avoid frequent errors: the series must be in the "
      "chart (`addSeries`) **before** `attachAxis()`; and the percentage of a slice (`QPieSlice.percentage()`) "
      "is only final after all the slices have been added — computed during insertion, the first slice would "
      "show 100 % (an error found and fixed while preparing this example)."),
    h3("Axes: QValueAxis, QLogValueAxis, QDateTimeAxis, QCategoryAxis"),
    p("`QValueAxis` is linear; `QLogValueAxis` requires positive values and a defined base; `QDateTimeAxis` "
      "takes milliseconds since the epoch (`QDateTime.toMSecsSinceEpoch()`); `QBarCategoryAxis` and "
      "`QCategoryAxis` label categories and ranges. The label format uses `printf` syntax "
      "(`setLabelFormat(\"%.0f\")`)."),
    h3("Migrating from QtCharts to QtGraphs"),
    tab("Correspondence between QtCharts / QtDataVisualization and QtGraphs",
        ["Legacy", "QtGraphs (Qt 6.12)", "Remark"],
        [["QChart + QChartView (Widgets)", "GraphsView (QML) in QQuickWidget", "QtGraphs 2D is declared in QML"],
         ["QLineSeries, QSplineSeries, QScatterSeries", "QLineSeries, QSplineSeries, QScatterSeries",
          "Same names, QtGraphs module"],
         ["QBarSeries, QBarSet, QPieSeries, QPieSlice", "QBarSeries, QBarSet, QPieSeries, QPieSlice",
          "Similar API"],
         ["QValueAxis, QLogValueAxis, QDateTimeAxis, QBarCategoryAxis", "Same names", "See Annex A.3.1"],
         ["QChart.setTheme / QChart.ChartTheme", "QGraphsTheme", "Unified 2D/3D theme"],
         ["Q3DBars, Q3DScatter, Q3DSurface (QtDataVisualization)",
          "Q3DBarsWidgetItem, Q3DScatterWidgetItem, Q3DSurfaceWidgetItem", "Require QQuickWidget"],
         ["Q3DTheme", "QGraphsTheme", "—"],
         ["QBarDataProxy, QScatterDataProxy, QSurfaceDataProxy", "Same names", "Proxies preserved"]],
        [3100, 3300, 2671], font=16),
    p("The correspondence was checked against the class catalog of Annex A. Migration is usually direct for "
      "series and axes; the main work is replacing `QChartView` with a `GraphsView` in QML."),

    h2("QtDataVisualization (legacy) and migration to QtGraphs"),
    p("QtDataVisualization (3D bar, scatter and surface charts) has also been deprecated since Qt 6.10. Its "
      "concepts — series, proxies, axes, camera, theme and selection — were preserved in QtGraphs, as the "
      "previous table shows. The main architectural change is that the charts are no longer windows "
      "(`QWindow`) and have become scene items hosted in a `QQuickWidget`."),

    h2("Embedded Matplotlib: FigureCanvasQTAgg and NavigationToolbar2QT"),
    p("Matplotlib ships a Qt backend (`matplotlib.backends.backend_qtagg`) that works with PyQt6. "
      "`FigureCanvasQTAgg` is a `QWidget` that displays a `Figure`; `NavigationToolbar2QT` adds zoom, pan, "
      "subplot configuration and export. Create the figure with `matplotlib.figure.Figure` — not with "
      "`pyplot` — so that Matplotlib neither opens windows of its own nor keeps global references."),
    lst("c22_matplotlib.py", "Embedded Matplotlib with navigation toolbar and redrawing per parameter"),
    out("c22_matplotlib"),
    img("Matplotlib chart embedded in a PyQt6 window", "f22_4_matplotlib.png", 15.0),
    p("The computed overshoot (52.7 % for ζ = 0.20) matches the theoretical value exp(−πζ/√(1−ζ²)). For "
      "interactive updates, change the data of the existing artists (`set_data`) and use `draw_idle()`, which "
      "groups several requests into a single redraw."),

    h2("pyqtgraph for real-time data"),
    p("**pyqtgraph** is built on Graphics View and NumPy and was designed for fast updates of large volumes. "
      "The key features for real time are: `setData()` on the existing item, `setClipToView(True)` (draws "
      "only the visible part) and `setDownsampling(auto=True, method=\"peak\")` (reduces points while "
      "preserving peaks — essential for vibration signals)."),
    lst("c22_pyqtgraph.py", "pyqtgraph: oscilloscope with a circular buffer and QTimer"),
    out("c22_pyqtgraph"),

    h2("Performance in continuous updating"),
    lst("c22_performance.py", "Cost per frame (data + painting) of pyqtgraph, QtCharts and Matplotlib"),
    out("c22_performance"),
    p("The numbers come from the test machine, with software rendering; what matters is the order of "
      "magnitude. With 20 000 points per frame, pyqtgraph sustained hundreds of frames per second; QtCharts was "
      "limited by converting 20 000 `QPointF` objects created in Python; Matplotlib, by the full redraw of the "
      "figure. Recommendations:"),
    bl("Update the screen at no more than 30–60 Hz, even if the acquisition is faster: accumulate samples and "
       "draw them in batches from a `QTimer`.",
       "Keep the data in NumPy arrays and avoid per-point Python loops.",
       "Reduce the points to what the screen can show (*downsampling*) — 20 000 points in 800 pixels of width "
       "add no visual information.",
       "In Matplotlib, for animation, use *blitting* (`canvas.copy_from_bbox`/`restore_region`) or "
       "`matplotlib.animation`; for reports, draw once.",
       "When measuring the performance of widgets based on Graphics View, force painting of the **viewport**: "
       "`repaint()` on the frame does not draw the scene (a pitfall found while preparing Listing 22.7)."),

    h2("Chapter exercises"),
    nl("Convert the QtCharts dashboard of Listing 22.4 to QtGraphs (2D in QML), keeping the four charts.",
       "Add to the chart of Listing 22.2 a `LineSeries` with the pore pressure gradient and a secondary axis "
       "in psi.",
       "Use `QItemModelSurfaceDataProxy` to display the data of a `QStandardItemModel` in 3D.",
       "Implement *blitting* in the Matplotlib example and measure the gain with the technique of "
       "Listing 22.7.",
       "Integrate the serial acquisition of Listing 21.9 into the oscilloscope of Listing 22.6."),
)
