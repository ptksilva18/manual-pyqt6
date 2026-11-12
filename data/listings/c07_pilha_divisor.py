"""QStackedWidget, QSplitter e QScrollArea."""
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QLabel, QListWidget, QScrollArea, QSplitter, QStackedWidget,
    QVBoxLayout, QWidget,
)


def pagina_longa(n: int) -> QScrollArea:
    conteudo = QWidget()
    lay = QVBoxLayout(conteudo)
    for i in range(n):
        lay.addWidget(QLabel(f"Item de verificação {i + 1}"))
    area = QScrollArea()
    area.setWidget(conteudo)
    area.setWidgetResizable(True)                     # o conteúdo acompanha a largura
    return area


if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = QListWidget()
    menu.addItems(["Geral", "Checklist", "Sobre"])
    paginas = QStackedWidget()
    centro = Qt.AlignmentFlag.AlignCenter
    paginas.addWidget(QLabel("Configurações gerais", alignment=centro))
    paginas.addWidget(pagina_longa(40))
    paginas.addWidget(QLabel("Versão 0.1.0", alignment=centro))
    menu.currentRowChanged.connect(paginas.setCurrentIndex)   # navegação

    divisor = QSplitter(Qt.Orientation.Horizontal)
    divisor.addWidget(menu)
    divisor.addWidget(paginas)
    divisor.setStretchFactor(1, 3)                    # painel direito cresce 3x mais
    divisor.setWindowTitle("QSplitter + QStackedWidget + QScrollArea")
    divisor.resize(600, 300)
    divisor.show()

    menu.setCurrentRow(1)
    print("página atual:", paginas.currentIndex())
    app.processEvents()
    print("tamanhos do splitter (px):", divisor.sizes())
    estado = divisor.saveState()                      # pode ser salvo em QSettings
    print("estado serializado (bytes):", len(estado))
    sys.exit(app.exec())
