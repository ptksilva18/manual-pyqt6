"""Classic pitfall: a lambda in a loop connected to clicked(bool)."""
import sys
from functools import partial

from PyQt6.QtWidgets import QApplication, QPushButton

log: list[str] = []


def on_click(index: int) -> None:
    log.append(f"button {index}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    buttons = [QPushButton(f"B{i}") for i in range(3)]

    for i, b in enumerate(buttons):
        # WRONG: clicked sends 'checked' (bool), which overwrites the default value i
        b.clicked.connect(lambda i=i: log.append(f"wrong: {i!r}"))
        # RIGHT (1): reserve the first parameter for 'checked'
        b.clicked.connect(lambda checked=False, i=i: on_click(i))
        # RIGHT (2): functools.partial fixes the argument in advance
        b.clicked.connect(partial(log.append, f"partial: {i}"))

    for b in buttons:
        b.click()                      # simulates the click (emits clicked)
    print("\n".join(log))
