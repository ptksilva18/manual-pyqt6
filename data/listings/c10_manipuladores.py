"""Reimplementação de manipuladores de eventos (mouse, teclado, janela)."""
import sys

from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QCloseEvent, QKeyEvent, QMouseEvent, QResizeEvent
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication, QWidget


class Prancheta(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)   # para receber teclado
        self.pode_fechar = False

    def mousePressEvent(self, e: QMouseEvent) -> None:
        p = e.position().toPoint()
        print(f"press   {e.button().name} em ({p.x()}, {p.y()})")

    def mouseMoveEvent(self, e: QMouseEvent) -> None:  # sem mouseTracking: só com botão
        p = e.position().toPoint()
        print(f"move    para ({p.x()}, {p.y()}) botões={e.buttons().name}")

    def mouseReleaseEvent(self, e: QMouseEvent) -> None:
        print(f"release {e.button().name}")

    def keyPressEvent(self, e: QKeyEvent) -> None:
        if e.key() == Qt.Key.Key_Escape:
            print("tecla Esc -> limpar seleção")
        elif (e.modifiers() & Qt.KeyboardModifier.ControlModifier
              and e.key() == Qt.Key.Key_Z):
            print("Ctrl+Z -> desfazer")
        else:
            super().keyPressEvent(e)                       # repassa o que não tratou

    def resizeEvent(self, e: QResizeEvent) -> None:
        print(f"resize  {e.oldSize().width()}x{e.oldSize().height()} -> "
              f"{e.size().width()}x{e.size().height()}")

    def closeEvent(self, e: QCloseEvent) -> None:
        if self.pode_fechar:
            print("close   aceito")
            e.accept()
        else:
            print("close   ignorado (há alterações não salvas)")
            e.ignore()                                     # a janela continua aberta


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Prancheta()
    w.resize(300, 200)
    w.show()
    QTest.qWaitForWindowExposed(w)
    QTest.mousePress(w, Qt.MouseButton.LeftButton, pos=QPoint(10, 10))
    QTest.mouseMove(w, QPoint(50, 40))
    QTest.mouseRelease(w, Qt.MouseButton.LeftButton, pos=QPoint(50, 40))
    QTest.keyClick(w, Qt.Key.Key_Escape)
    QTest.keyClick(w, Qt.Key.Key_Z, Qt.KeyboardModifier.ControlModifier)
    w.resize(400, 250)
    print("fechou?", w.close())
    w.pode_fechar = True
    print("fechou?", w.close())
