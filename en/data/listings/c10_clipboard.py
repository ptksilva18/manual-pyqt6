"""Clipboard: text, MIME data and change notification."""
import sys

from PyQt6.QtCore import QMimeData
from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    cb = QApplication.clipboard()
    cb.dataChanged.connect(lambda: print("dataChanged: new content"))

    cb.setText("PT-101;345.0;bar")
    print("text:", cb.text())

    mime = QMimeData()                              # several formats at once
    mime.setText("345 bar")
    mime.setHtml("<b>345</b> bar")
    cb.setMimeData(mime)
    current = cb.mimeData()
    print("formats:", [f for f in current.formats() if f.startswith("text/")])
    print("html:", current.html())
