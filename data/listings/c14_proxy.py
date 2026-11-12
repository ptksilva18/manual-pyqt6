"""Modelos proxy: ordenação/filtragem, transposição e concatenação."""

import sys

from PyQt6.QtCore import (
    QConcatenateTablesProxyModel,
    QRegularExpression,
    QSortFilterProxyModel,
    Qt,
    QTransposeProxyModel,
)
from PyQt6.QtWidgets import QApplication, QTableView

from c14_modelo_tabela import Ensaio, ModeloEnsaios


def tags(modelo) -> list[str]:
    return [modelo.index(r, 0).data() for r in range(modelo.rowCount())]


class FiltroPressao(QSortFilterProxyModel):
    """Filtra por texto da tag E por pressão mínima (filtro personalizado)."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.pressao_minima = 0.0

    def filterAcceptsRow(self, linha: int, pai) -> bool:
        origem = self.sourceModel()
        p = origem.index(linha, 1, pai).data(Qt.ItemDataRole.EditRole)
        return p >= self.pressao_minima and super().filterAcceptsRow(linha, pai)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    base = ModeloEnsaios(
        [
            Ensaio("BOP-02", 310.5, False),
            Ensaio("BOP-01", 345.0, True),
            Ensaio("XT-07", 690.0, True),
        ]
    )

    proxy = FiltroPressao()
    proxy.setSourceModel(base)
    proxy.setSortRole(Qt.ItemDataRole.EditRole)  # ordena pelo valor numérico
    proxy.setFilterKeyColumn(0)
    vista = QTableView()
    vista.setModel(proxy)
    vista.setSortingEnabled(True)

    proxy.sort(1, Qt.SortOrder.DescendingOrder)
    print("ordenado por pressão (desc):", tags(proxy))
    proxy.setFilterRegularExpression(QRegularExpression("^BOP"))
    print("filtro ^BOP:", tags(proxy))
    proxy.pressao_minima = 320.0
    # reaplica o filtro personalizado
    proxy.invalidateRowsFilter()
    print("^BOP e >= 320 bar:", tags(proxy))
    origem = proxy.mapToSource(proxy.index(0, 0))
    print("linha 0 do proxy = linha", origem.row(), "do modelo-fonte")

    transposto = QTransposeProxyModel()
    transposto.setSourceModel(base)
    print(
        "transposto:",
        transposto.rowCount(),
        "x",
        transposto.columnCount(),
        "| linha 0:",
        [transposto.index(0, c).data() for c in range(transposto.columnCount())],
    )

    extra = ModeloEnsaios([Ensaio("MPD-01", 100.0, True)])
    junto = QConcatenateTablesProxyModel()
    junto.addSourceModel(base)
    junto.addSourceModel(extra)
    print("concatenado:", tags(junto))
