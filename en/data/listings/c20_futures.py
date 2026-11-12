# runner: ticks=150 timeout=90
"""concurrent.futures (threads and processes) integrated with Qt through signals."""

import math
import multiprocessing as mp
import os
import sys
from concurrent.futures import Future, ProcessPoolExecutor, ThreadPoolExecutor

from PyQt6.QtCore import QObject, QThread, QTimer, pyqtSignal
from PyQt6.QtWidgets import QApplication


def primes_up_to(n: int) -> int:
    """Sieve of Eratosthenes (CPU-bound): counts the primes <= n."""
    sieve = bytearray([1]) * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for i in range(2, math.isqrt(n) + 1):
        if sieve[i]:
            sieve[i * i :: i] = bytearray(len(range(i * i, n + 1, i)))
    return sum(sieve)


def read_file_slowly(path: str) -> int:
    """I/O task: the GIL is released during the read."""
    with open(path, "rb") as f:
        return len(f.read())


class Bridge(QObject):
    """Receives callbacks from futures (other threads) and re-emits them as Qt signals."""

    ready = pyqtSignal(str, object)

    def track(self, label: str, future: Future) -> None:
        def callback(f: Future) -> None:  # runs in the thread that completed the future
            try:
                self.ready.emit(label, f.result())
            except Exception as exc:
                self.ready.emit(label, exc)

        future.add_done_callback(callback)


def main() -> int:
    app = QApplication(sys.argv)
    QThread.currentThread().setObjectName("GUI")
    bridge = Bridge()
    pending = {"proc-1e6", "proc-2e6", "proc-error", "thread-io"}

    def on_ready(label: str, value: object) -> None:  # executes in the GUI thread
        thread = QThread.currentThread().objectName()
        print(f"{label:<10} -> {value!r:<45} (handled in thread {thread})")
        pending.discard(label)
        if not pending:
            app.quit()

    bridge.ready.connect(on_ready)
    ctx = mp.get_context(
        "spawn"
    )  # the same on Windows, macOS and Linux; requires the __main__ guard
    with ProcessPoolExecutor(
        max_workers=2, mp_context=ctx
    ) as procs, ThreadPoolExecutor(max_workers=2) as threads:
        bridge.track("proc-1e6", procs.submit(primes_up_to, 1_000_000))
        bridge.track("proc-2e6", procs.submit(primes_up_to, 2_000_000))
        bridge.track("proc-error", procs.submit(primes_up_to, -5))
        bridge.track("thread-io", threads.submit(read_file_slowly, os.__file__))
        QTimer.singleShot(60_000, app.quit)  # safeguard
        code = app.exec()
    return code


if __name__ == "__main__":
    sys.exit(main())
