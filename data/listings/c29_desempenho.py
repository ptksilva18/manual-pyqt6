# runner: ticks=600 timeout=180
"""Medição e otimização: cProfile, QElapsedTimer, modelo com cache e inserção em lote."""

import cProfile
import io
import math
import pstats
import sys

from PyQt6.QtCore import QAbstractTableModel, QElapsedTimer, QLocale, QModelIndex, Qt
from PyQt6.QtWidgets import QApplication, QHeaderView, QTableView

N_LINHAS, N_COLUNAS = 20_000, 6


def valor(linha: int, coluna: int) -> float:
    return math.sin(linha * 0.001 + coluna) * 1000.0


class ModeloLento(QAbstractTableModel):
    """Calcula e formata a cada chamada de data() — chamada milhares de vezes por
    pintura."""

    def __init__(self) -> None:
        super().__init__()
        self.local = QLocale(QLocale.Language.Portuguese, QLocale.Country.Brazil)

    def rowCount(self, parent=QModelIndex()) -> int:
        return 0 if parent.isValid() else N_LINHAS

    def columnCount(self, parent=QModelIndex()) -> int:
        return 0 if parent.isValid() else N_COLUNAS

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            return self.local.toString(valor(index.row(), index.column()), "f", 3)
        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        return None


class ModeloRapido(ModeloLento):
    """Pré-formata uma vez e responde só aos papéis usados; alinhamento constante."""

    ALINHAMENTO = Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter

    def __init__(self) -> None:
        super().__init__()
        self.cache = [
            [self.local.toString(valor(r, c), "f", 3) for c in range(N_COLUNAS)]
            for r in range(N_LINHAS)
        ]

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            return self.cache[index.row()][index.column()]
        if role == Qt.ItemDataRole.TextAlignmentRole:
            return self.ALINHAMENTO
        return None


def medir_pintura(modelo, ajustar_colunas: bool) -> float:
    vista = QTableView()
    vista.setModel(modelo)
    vista.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
    vista.resize(900, 600)
    vista.show()
    QApplication.processEvents()
    relogio = QElapsedTimer()
    relogio.start()
    if ajustar_colunas:
        # Mede o texto de até resizeContentsPrecision() linhas por coluna (padrão: 1000).
        vista.resizeColumnsToContents()
    for _ in range(20):
        vista.viewport().repaint()
    ms = relogio.nsecsElapsed() / 1e6
    vista.close()
    return ms


def main() -> int:
    app = QApplication(sys.argv)  # noqa: F841
    perfil = cProfile.Profile()
    perfil.enable()
    t_lento = medir_pintura(ModeloLento(), ajustar_colunas=True)
    perfil.disable()
    relogio = QElapsedTimer()
    relogio.start()
    rapido = ModeloRapido()
    t_cache = relogio.nsecsElapsed() / 1e6
    t_rapido = medir_pintura(rapido, ajustar_colunas=False)
    print(f"Modelo lento + resizeColumnsToContents: {t_lento:8.1f} ms")
    print(
        f"Modelo com cache, larguras fixas       : {t_rapido:8.1f} ms "
        f"(~{t_lento / t_rapido:.0f}x mais rápido)"
    )
    tabela = (
        QTableView()
    )  # manter a referência: o cabeçalho pertence à tabela (Seção 29.4)
    print(
        f"Custo único de pré-formatar {N_LINHAS * N_COLUNAS} células: {t_cache:.1f} ms; "
        f"precisão de resizeColumnsToContents: "
        f"{tabela.horizontalHeader().resizeContentsPrecision()} linhas"
    )
    saida = io.StringIO()
    pstats.Stats(perfil, stream=saida).sort_stats("cumulative").print_stats(
        "data|valor", 3
    )
    print("cProfile — funções Python mais custosas (filtro 'data|valor'):")
    for linha in saida.getvalue().splitlines():
        if "ncalls" in linha or ("c29_desempenho.py" in linha and "(" in linha):
            print("  " + linha.replace(__file__, "c29_desempenho.py").strip())
    return 0


if __name__ == "__main__":
    sys.exit(main())
