"""Reimplementing event handlers (mouse, keyboard, window)."""
import sys

from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QCloseEvent, QKeyEvent, QMouseEvent, QResizeEvent
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication, QWidget


class Sketchpad(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)   # to receive keyboard input
        self.can_close = False

    def mousePressEvent(self, e: QMouseEvent) -> None:
        p = e.position().toPoint()
        print(f"press   {e.button().name} at ({p.x()}, {p.y()})")

    def mouseMoveEvent(self, e: QMouseEvent) -> None:  # no mouseTracking: button held
        p = e.position().toPoint()
        print(f"move    to ({p.x()}, {p.y()}) buttons={e.buttons().name}")

    def mouseReleaseEvent(self, e: QMouseEvent) -> None:
        print(f"release {e.button().name}")

    def keyPressEvent(self, e: QKeyEvent) -> None:
        if e.key() == Qt.Key.Key_Escape:
            print("Esc key -> clear selection")
        elif (e.modifiers() & Qt.KeyboardModifier.ControlModifier
              and e.key() == Qt.Key.Key_Z):
            print("Ctrl+Z -> undo")
        else:
            super().keyPressEvent(e)                       # passes on the rest

    def resizeEvent(self, e: QResizeEvent) -> None:
        print(f"resize  {e.oldSize().width()}x{e.oldSize().height()} -> "
              f"{e.size().width()}x{e.size().height()}")

    def closeEvent(self, e: QCloseEvent) -> None:
        if self.can_close:
            print("close   accepted")
            e.accept()
        else:
            print("close   ignored (there are unsaved changes)")
            e.ignore()                                     # the window stays open


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Sketchpad()
    w.resize(300, 200)
    w.show()
    QTest.qWaitForWindowExposed(w)
    QTest.mousePress(w, Qt.MouseButton.LeftButton, pos=QPoint(10, 10))
    QTest.mouseMove(w, QPoint(50, 40))
    QTest.mouseRelease(w, Qt.MouseButton.LeftButton, pos=QPoint(50, 40))
    QTest.keyClick(w, Qt.Key.Key_Escape)
    QTest.keyClick(w, Qt.Key.Key_Z, Qt.KeyboardModifier.ControlModifier)
    w.resize(400, 250)
    print("closed?", w.close())
    w.can_close = True
    print("closed?", w.close())
