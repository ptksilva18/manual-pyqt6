"""Primeira aplicação PyQt6: janela mínima com um rótulo centralizado."""
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel


def main() -> int:
    app = QApplication(sys.argv)            # 1. objeto de aplicação (único)
    label = QLabel("Olá, PyQt6!")           # 2. widget sem pai = janela
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.resize(320, 120)
    label.setWindowTitle("Primeira aplicação")
    label.show()                            # 3. torna a janela visível
    return app.exec()                       # 4. entra no event loop


if __name__ == "__main__":
    sys.exit(main())
