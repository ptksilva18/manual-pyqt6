"""QFileSystemModel: asynchronous loading of directories (directoryLoaded signal)."""

import sys
import tempfile
from pathlib import Path

from PyQt6.QtCore import QDir, QEventLoop, Qt, QTimer
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtWidgets import QApplication, QTreeView

if __name__ == "__main__":
    app = QApplication(sys.argv)
    folder = Path(tempfile.mkdtemp())
    for name in ("test_01.csv", "test_02.csv", "notes.txt"):
        (folder / name).write_text("data\n", encoding="utf-8")
    (folder / "photos").mkdir()

    model = QFileSystemModel()
    model.setFilter(QDir.Filter.AllEntries | QDir.Filter.NoDotAndDotDot)
    model.setNameFilters(["*.csv"])
    # hides (instead of disabling) the rest
    model.setNameFilterDisables(False)
    wait = QEventLoop()
    model.directoryLoaded.connect(lambda path: wait.quit())
    root = model.setRootPath(str(folder))  # starts reading in the background
    QTimer.singleShot(3000, wait.quit)  # safeguard
    wait.exec()  # waits for the directoryLoaded signal

    view = QTreeView()
    view.setModel(model)
    view.setRootIndex(root)
    names = sorted(model.index(i, 0, root).data() for i in range(model.rowCount(root)))
    print("visible entries:", names)
    horizontal = Qt.Orientation.Horizontal
    print(
        "columns:",
        [model.headerData(c, horizontal) for c in range(model.columnCount())],
    )
