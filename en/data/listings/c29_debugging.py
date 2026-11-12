# runner: ticks=60
"""Debugging: QLoggingCategory, filter rules, message handler and
QT_DEBUG_PLUGINS."""

import os
import subprocess
import sys

from PyQt6.QtCore import (
    QLoggingCategory,
    QMessageLogContext,
    QtMsgType,
    qInstallMessageHandler,
)
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QWidget

# The C++ constructor keeps only the POINTER to the name: keep the bytes alive in the
# module.
# (In the test, categories created with a temporary str ignored the filter rules.)
IO_NAME, CALC_NAME = b"tests.io", b"tests.calculation"
IO = QLoggingCategory(IO_NAME)
CALC = QLoggingCategory(CALC_NAME)
captured: list[str] = []


def handler(msg_type: QtMsgType, context: QMessageLogContext, message: str) -> None:
    """Receives ALL Qt messages (C++ and Python), with type and category."""
    captured.append(f"[{msg_type.name}] {context.category}: {message}")


def main() -> int:
    app = QApplication(sys.argv)
    previous = qInstallMessageHandler(handler)
    print("Before the rules: tests.io debug =", IO.isDebugEnabled())
    QLoggingCategory.setFilterRules("tests.*.debug=false\ntests.calculation.debug=true")
    print(
        "After: tests.io debug =",
        IO.isDebugEnabled(),
        "| tests.calculation debug =",
        CALC.isDebugEnabled(),
        "| tests.io warning =",
        IO.isWarningEnabled(),
    )
    w = QWidget()
    w.setLayout(QVBoxLayout())
    w.setLayout(QHBoxLayout())  # usage error: Qt warns through the default category
    qInstallMessageHandler(previous)
    for line in captured:
        print("captured:", line[:110])

    environment = dict(os.environ, QT_DEBUG_PLUGINS="1", QT_QPA_PLATFORM="offscreen")
    r = subprocess.run(
        [
            sys.executable,
            "-c",
            "from PyQt6.QtWidgets import QApplication; QApplication([])",
        ],
        env=environment,
        capture_output=True,
        text=True,
    )
    loaded = [
        os.path.basename(ln.split('"')[1])
        for ln in r.stderr.splitlines()
        if ln.endswith(" loaded library")
    ]
    print(
        f"QT_DEBUG_PLUGINS=1: {len(r.stderr.splitlines())} diagnostic lines; "
        f"plugins loaded: {loaded}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
