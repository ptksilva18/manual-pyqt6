# runner: ticks=60
"""Synchronization: QMutex, QReadWriteLock and a bounded buffer with QWaitCondition."""

import sys
from collections import deque

from PyQt6.QtCore import (
    QMutex,
    QReadLocker,
    QReadWriteLock,
    QSemaphore,
    QThread,
    QWaitCondition,
    QWriteLocker,
)
from PyQt6.QtWidgets import QApplication


class Counter:
    def __init__(self) -> None:
        self._mutex = QMutex()
        self.value = 0

    def increment(self) -> None:
        # In PyQt6 6.12, QMutexLocker failed intermittently under contention between
        # threads (segmentation fault, verified); lock()/unlock() in try/finally did not.
        self._mutex.lock()
        try:
            self.value += 1
        finally:  # releases the mutex even if an exception occurs
            self._mutex.unlock()


class Incrementer(QThread):
    def __init__(self, counter: Counter, n: int) -> None:
        super().__init__()
        self.counter, self.n = counter, n

    def run(self) -> None:
        for _ in range(self.n):
            self.counter.increment()


class PropertyTable:
    """Many simultaneous readers, one writer at a time."""

    def __init__(self) -> None:
        self._lock = QReadWriteLock()
        self._data = {"steel_E_GPa": 207.0}
        self.reads = 0

    def read(self, key: str) -> float:
        with QReadLocker(self._lock):
            self.reads += 1  # approximate count: only illustrates concurrent access
            return self._data[key]

    def write(self, key: str, value: float) -> None:
        with QWriteLocker(self._lock):
            self._data[key] = value


class BoundedBuffer:
    """Fixed-capacity queue: the producer waits if full; the consumer, if empty."""

    def __init__(self, capacity: int) -> None:
        self._queue: deque[float | None] = deque()
        self._cap = capacity
        self._mutex = QMutex()
        self._not_full = QWaitCondition()
        self._not_empty = QWaitCondition()
        self.max_occupancy = 0

    def put(self, item: float | None) -> None:
        self._mutex.lock()
        try:
            while len(self._queue) >= self._cap:
                self._not_full.wait(self._mutex)  # releases the mutex while waiting
            self._queue.append(item)
            self.max_occupancy = max(self.max_occupancy, len(self._queue))
            self._not_empty.wakeOne()
        finally:
            self._mutex.unlock()

    def take(self) -> float | None:
        self._mutex.lock()
        try:
            while not self._queue:
                self._not_empty.wait(self._mutex)
            item = self._queue.popleft()
            self._not_full.wakeOne()
            return item
        finally:
            self._mutex.unlock()


class FunctionThread(QThread):
    """Runs any function in run() (PyQt6 does not expose QThread.create())."""

    def __init__(self, function) -> None:
        super().__init__()
        self.function = function

    def run(self) -> None:
        self.function()


class Producer(QThread):
    def __init__(self, buf: BoundedBuffer, n: int) -> None:
        super().__init__()
        self.buf, self.n = buf, n

    def run(self) -> None:
        for i in range(self.n):
            self.buf.put(float(i))
        self.buf.put(None)  # end sentinel


class Consumer(QThread):
    def __init__(self, buf: BoundedBuffer) -> None:
        super().__init__()
        self.buf, self.total, self.count = buf, 0.0, 0

    def run(self) -> None:
        while (item := self.buf.take()) is not None:
            self.total += item
            self.count += 1


def main() -> int:
    app = QApplication(sys.argv)

    counter = Counter()
    threads = [Incrementer(counter, 50_000) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.wait()
    print(f"QMutex: counter = {counter.value} (expected {4 * 50_000})")

    table = PropertyTable()
    readers = [
        FunctionThread(lambda: [table.read("steel_E_GPa") for _ in range(2_000)])
        for _ in range(3)
    ]
    writer = FunctionThread(lambda: table.write("steel_E_GPa", 210.0))
    for t in (*readers, writer):
        t.start()
    for t in (*readers, writer):
        t.wait()
    print(f"QReadWriteLock: final value = {table.read('steel_E_GPa')} GPa")

    buf = BoundedBuffer(capacity=8)
    prod, cons = Producer(buf, 10_000), Consumer(buf)
    cons.start()
    prod.start()
    prod.wait()
    cons.wait()
    print(
        f"QWaitCondition: consumed {cons.count} items, sum = {cons.total:.0f} "
        f"(expected {sum(range(10_000))}); maximum occupancy = {buf.max_occupancy} <= 8"
    )

    slots = QSemaphore(2)  # at most 2 simultaneous accesses to a resource
    print(
        f"QSemaphore: available = {slots.available()}; tryAcquire(2) = "
        f"{slots.tryAcquire(2)}; tryAcquire(1) = {slots.tryAcquire(1)}"
    )
    slots.release(2)
    print(f"QSemaphore: after release(2), available = {slots.available()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
