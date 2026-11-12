"""Standard dialogs: QInputDialog, QProgressDialog and QFileDialog (non-native)."""
import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QFileDialog, QInputDialog, QProgressDialog

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Static QInputDialog: returns (value, ok).
    # The timer simulates the user clicking "Cancel".
    QTimer.singleShot(0, lambda: QApplication.activeModalWidget().reject())
    value, ok = QInputDialog.getDouble(None, "Safety factor", "Factor:",
                                       1.5, 1.0, 5.0, 2)
    print("getDouble ->", (value, ok))

    # QProgressDialog for a task in steps, with cancellation
    prog = QProgressDialog("Processing files…", "Cancel", 0, 5)
    prog.setMinimumDuration(0)                 # shows up immediately
    for i in range(5):
        prog.setValue(i)
        app.processEvents()
        if prog.wasCanceled():
            break
    prog.setValue(5)
    print("value after finishing:", prog.value(), "(autoReset resets it to -1)",
          "| canceled?", prog.wasCanceled())

    # QFileDialog configured as an object (option: Qt's dialog instead of the native one)
    dlg = QFileDialog(None, "Open test", "", "Tests (*.json *.csv);;All (*)")
    dlg.setFileMode(QFileDialog.FileMode.ExistingFile)
    dlg.setOption(QFileDialog.Option.DontUseNativeDialog, True)
    print("filters:", dlg.nameFilters())
    QTimer.singleShot(0, dlg.reject)
    print("file chosen?", bool(dlg.exec()))
