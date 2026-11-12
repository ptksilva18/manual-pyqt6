"""Área de transferência: texto, dados MIME e notificação de mudança."""
import sys

from PyQt6.QtCore import QMimeData
from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    cb = QApplication.clipboard()
    cb.dataChanged.connect(lambda: print("dataChanged: novo conteúdo"))

    cb.setText("PT-101;345.0;bar")
    print("texto:", cb.text())

    mime = QMimeData()                              # vários formatos ao mesmo tempo
    mime.setText("345 bar")
    mime.setHtml("<b>345</b> bar")
    cb.setMimeData(mime)
    atual = cb.mimeData()
    print("formatos:", [f for f in atual.formats() if f.startswith("text/")])
    print("html:", atual.html())
