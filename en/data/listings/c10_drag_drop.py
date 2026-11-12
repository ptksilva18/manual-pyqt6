"""Drag and drop: a target that accepts only .csv files."""
import sys

from PyQt6.QtCore import QMimeData, QPointF, Qt, QUrl
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
from PyQt6.QtWidgets import QApplication, QLabel


class CsvTarget(QLabel):
    def __init__(self) -> None:
        super().__init__("Drop a .csv file here")
        self.setAcceptDrops(True)                         # enables receiving drops
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    @staticmethod
    def _csv(mime: QMimeData) -> list[str]:
        return [u.toLocalFile() for u in mime.urls()
                if u.isLocalFile() and u.toLocalFile().lower().endswith(".csv")]

    def dragEnterEvent(self, e: QDragEnterEvent) -> None:
        if e.mimeData().hasUrls() and self._csv(e.mimeData()):
            e.acceptProposedAction()                      # cursor shows "can drop"
        else:
            e.ignore()

    def dropEvent(self, e: QDropEvent) -> None:
        files = self._csv(e.mimeData())
        self.setText("\n".join(files))
        e.acceptProposedAction()


def simulate(target: QLabel, path: str) -> None:
    """Generates the events the system would send during a real drag."""
    mime = QMimeData()
    mime.setUrls([QUrl.fromLocalFile(path)])
    action, buttons = Qt.DropAction.CopyAction, Qt.MouseButton.LeftButton
    enter = QDragEnterEvent(target.rect().center(), action, mime, buttons,
                            Qt.KeyboardModifier.NoModifier)
    QApplication.sendEvent(target, enter)
    print(f"{path}: accepted? {enter.isAccepted()}")
    if enter.isAccepted():
        drop = QDropEvent(QPointF(target.rect().center()), action, mime, buttons,
                          Qt.KeyboardModifier.NoModifier)
        QApplication.sendEvent(target, drop)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    target = CsvTarget()
    target.show()
    simulate(target, "/data/report.pdf")
    simulate(target, "/data/bop_test.csv")
    print("label:", target.text())
