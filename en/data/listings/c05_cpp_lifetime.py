"""C++ x Python lifetime: a Python reference to a C++ object already destroyed."""
import sys

from PyQt6 import sip
from PyQt6.QtWidgets import QApplication, QLabel, QWidget

if __name__ == "__main__":
    app = QApplication(sys.argv)
    parent = QWidget()
    label = QLabel("child", parent)        # the C++ parent owns the label
    sip.delete(parent)                     # destroys the parent (and its children) now
    print("does label still exist in Python?", label is not None)
    print("C++ object destroyed?", sip.isdeleted(label))
    try:
        label.text()
    except RuntimeError as error:
        print("RuntimeError:", error)
