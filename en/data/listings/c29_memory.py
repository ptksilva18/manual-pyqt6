# runner: ticks=60
"""Python/C++ memory pitfalls: destroyed objects, sip.isdeleted and faulthandler."""

import gc
import subprocess
import sys

from PyQt6 import sip
from PyQt6.QtCore import QEvent
from PyQt6.QtWidgets import QApplication, QLabel, QTableView, QWidget


def main() -> int:
    app = QApplication(sys.argv)

    # 1) The parent destroys the C++ children; the Python object still exists, "empty".
    parent = QWidget()
    label = QLabel("PT-101", parent)
    parent.deleteLater()
    # Processes the deleteLater now (normally, the event loop does this).
    app.sendPostedEvents(None, QEvent.Type.DeferredDelete.value)
    print("1) sip.isdeleted(label) =", sip.isdeleted(label))
    try:
        label.setText("x")
    except RuntimeError as exc:
        print("   RuntimeError:", exc)

    # 2) Temporary: the header belongs to the table, which is collected at the end of the
    #    expression.
    header = QTableView().horizontalHeader()
    gc.collect()
    print("2) header of a temporary table destroyed?", sip.isdeleted(header))

    # 3) Object without a parent and without a Python reference: it vanishes immediately.
    def create_window_wrongly() -> None:
        window = QWidget()
        window.setWindowTitle("vanishes when the function returns")
        window.show()

    create_window_wrongly()
    print(
        "3) visible top-level windows after the function:",
        [w.windowTitle() for w in app.topLevelWidgets() if w.isVisible()],
    )

    # 4) Crash in native code: faulthandler shows the Python stack before dying.
    code = "import faulthandler, ctypes; faulthandler.enable(); ctypes.string_at(0)"
    r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    lines = [ln.strip() for ln in r.stderr.splitlines() if ln.strip()]
    print(
        f"4) child process ended with code {r.returncode}; faulthandler reported:"
    )
    for ln in lines[:1] + [ln for ln in lines if ln.startswith("File")][-1:]:
        print("   " + ln)
    return 0


if __name__ == "__main__":
    sys.exit(main())
