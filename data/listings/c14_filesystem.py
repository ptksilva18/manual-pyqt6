"""QFileSystemModel: carregamento assíncrono de diretórios (sinal directoryLoaded)."""

import sys
import tempfile
from pathlib import Path

from PyQt6.QtCore import QDir, QEventLoop, Qt, QTimer
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtWidgets import QApplication, QTreeView

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pasta = Path(tempfile.mkdtemp())
    for nome in ("ensaio_01.csv", "ensaio_02.csv", "notas.txt"):
        (pasta / nome).write_text("dados\n", encoding="utf-8")
    (pasta / "fotos").mkdir()

    modelo = QFileSystemModel()
    modelo.setFilter(QDir.Filter.AllEntries | QDir.Filter.NoDotAndDotDot)
    modelo.setNameFilters(["*.csv"])
    # oculta (em vez de desabilitar) o resto
    modelo.setNameFilterDisables(False)
    espera = QEventLoop()
    modelo.directoryLoaded.connect(lambda caminho: espera.quit())
    raiz = modelo.setRootPath(str(pasta))  # inicia a leitura em segundo plano
    QTimer.singleShot(3000, espera.quit)  # salvaguarda
    espera.exec()  # aguarda o sinal directoryLoaded

    vista = QTreeView()
    vista.setModel(modelo)
    vista.setRootIndex(raiz)
    nomes = sorted(
        modelo.index(i, 0, raiz).data() for i in range(modelo.rowCount(raiz))
    )
    print("entradas visíveis:", nomes)
    horizontal = Qt.Orientation.Horizontal
    print(
        "colunas:",
        [modelo.headerData(c, horizontal) for c in range(modelo.columnCount())],
    )
