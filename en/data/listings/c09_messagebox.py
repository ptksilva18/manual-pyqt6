"""QMessageBox: static methods and a customized box."""
import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QMessageBox

SB = QMessageBox.StandardButton


def confirm_delete(parent=None) -> bool:
    answer = QMessageBox.question(
        parent, "Delete record",
        "Delete the selected test?\nThis operation cannot be undone.",
        SB.Yes | SB.No, defaultButton=SB.No)          # 'No' as the default: safer
    return answer == SB.Yes


def ask_save(parent=None) -> str:
    box = QMessageBox(parent)
    box.setIcon(QMessageBox.Icon.Warning)
    box.setWindowTitle("Unsaved changes")
    box.setText("The document has been modified.")
    box.setInformativeText("Do you want to save your changes?")
    box.setStandardButtons(SB.Save | SB.Discard | SB.Cancel)
    box.setDefaultButton(SB.Save)
    box.setDetailedText("File: test_345bar.json\nLast saved: 10:42")
    QTimer.singleShot(0, box.button(SB.Discard).click)     # simulates the user
    result = SB(box.exec())
    return result.name


if __name__ == "__main__":
    app = QApplication(sys.argv)
    QTimer.singleShot(0, lambda: QApplication.activeModalWidget().close())  # mimics Esc
    print("deletion confirmed?", confirm_delete())
    print("choice when saving:", ask_save())
