"""QFileSystemWatcher and QProcess (synchronous and asynchronous execution)."""

import sys
import tempfile
from pathlib import Path

from PyQt6.QtCore import QEventLoop, QFileSystemWatcher, QProcess, QTimer
from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    file = Path(tempfile.mkdtemp()) / "parameters.txt"
    file.write_text("pressure=345\n", encoding="utf-8")

    watcher = QFileSystemWatcher([str(file)])
    loop = QEventLoop()
    watcher.fileChanged.connect(
        lambda c: (print("fileChanged:", Path(c).name), loop.quit())
    )
    QTimer.singleShot(
        200, lambda: file.write_text("pressure=350\n", encoding="utf-8")
    )
    QTimer.singleShot(5000, loop.quit)  # safeguard
    loop.exec()

    # Synchronous: blocks until it finishes (acceptable only for quick commands)
    p = QProcess()
    p.start(sys.executable, ["-c", "print(2 * 345)"])
    p.waitForFinished(5000)
    print(
        "synchronous ->",
        bytes(p.readAllStandardOutput()).decode().strip(),
        "| code:",
        p.exitCode(),
    )

    # Asynchronous: the interface keeps responding; results arrive through signals
    proc = QProcess()
    proc.setProgram(sys.executable)
    proc.setArguments(["-c", "import sys; print('output ok'); sys.exit(3)"])

    def read_output():
        # The output may arrive in pieces: ignore empty chunks
        text = bytes(proc.readAllStandardOutput()).decode().strip()
        if text:
            print("stdout:", text)

    proc.readyReadStandardOutput.connect(read_output)
    proc.finished.connect(
        lambda code, status: (
            print("finished: code", code, "|", status.name),
            app.quit(),
        )
    )
    proc.errorOccurred.connect(lambda e: print("error:", e.name))
    proc.start()
    app.exec()
