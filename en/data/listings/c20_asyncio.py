# runner: ticks=150
"""asyncio on top of the Qt event loop with the third-party library qasync."""

import asyncio
import sys
import time

import qasync
from PyQt6.QtWidgets import QApplication, QLabel


async def query_sensor(name: str, delay: float) -> tuple[str, float]:
    await asyncio.sleep(delay)  # simulates network I/O without blocking the interface
    return name, 100.0 + delay * 10


def blocking_computation(n: int) -> int:
    return sum(i * i for i in range(n))


async def main_task(label: QLabel) -> None:
    t0 = time.perf_counter()
    readings = await asyncio.gather(
        query_sensor("PT-101", 0.30),
        query_sensor("PT-102", 0.20),
        query_sensor("TT-201", 0.10),
    )
    dt = time.perf_counter() - t0
    print(f"3 concurrent queries in {dt:.2f} s (sequentially it would take 0.60 s)")
    for name, value in readings:
        print(f"  {name}: {value:.1f}")
    label.setText(" | ".join(f"{n}={v:.1f}" for n, v in readings))

    result = await asyncio.to_thread(blocking_computation, 2_000_000)  # off the loop
    print(f"to_thread: sum of squares = {result}")

    try:
        await asyncio.wait_for(query_sensor("PT-999", 5.0), timeout=0.2)
    except TimeoutError:
        print("wait_for: the query to PT-999 exceeded 0.2 s and was canceled")
    print(f"Window label: {label.text()!r}")


def main() -> int:
    app = QApplication(sys.argv)
    label = QLabel("waiting...")
    label.show()
    loop = qasync.QEventLoop(app)  # a single loop: Qt events + asyncio coroutines
    asyncio.set_event_loop(loop)
    with loop:
        loop.run_until_complete(main_task(label))
    return 0


if __name__ == "__main__":
    sys.exit(main())
