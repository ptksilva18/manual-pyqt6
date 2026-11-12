"""Janela principal: lista de ensaios, leituras, gráfico, resultado e ações."""

from pathlib import Path

import pyqtgraph as pg
from PyQt6.QtCore import QSettings, Qt
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtWidgets import (
    QDockWidget,
    QFileDialog,
    QInputDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QSplitter,
    QTableView,
    QTabWidget,
)

from . import __version__
from .dominio import Criterio, ErroDados, Resultado
from .importacao import ler_csv
from .modelos import ModeloEnsaios, ModeloLeituras
from .relatorio import gerar_pdf
from .repositorio import Repositorio
from .servicos import ServicoAnalise


class JanelaPrincipal(QMainWindow):
    def __init__(self, repo: Repositorio, servico: ServicoAnalise) -> None:
        super().__init__()
        self.repo, self.servico = repo, servico
        self.resultado: Resultado | None = None
        self.setWindowTitle(f"Monitor de Ensaios {__version__}")
        self.modelo_ensaios, self.modelo_leituras = ModeloEnsaios(), ModeloLeituras()
        self.tabela_ensaios = QTableView()
        self.tabela_ensaios.setModel(self.modelo_ensaios)
        self.tabela_ensaios.setSelectionBehavior(
            QTableView.SelectionBehavior.SelectRows
        )
        self.tabela_ensaios.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.tabela_ensaios.horizontalHeader().setStretchLastSection(True)
        self.tabela_leituras = QTableView()
        self.tabela_leituras.setModel(self.modelo_leituras)
        self.grafico = pg.PlotWidget(background="w")
        self.grafico.setLabel("bottom", "Tempo (min)")
        self.grafico.setLabel("left", "Pressão (bar)")
        self.grafico.showGrid(x=True, y=True, alpha=0.3)
        self.curva = self.grafico.plot(
            pen=pg.mkPen("#2E75B6", width=2),
            symbol="o",
            symbolSize=5,
            symbolBrush="#2E75B6",
        )
        abas = QTabWidget()
        abas.addTab(self.grafico, "Gráfico")
        abas.addTab(self.tabela_leituras, "Leituras")
        divisor = QSplitter()
        divisor.addWidget(self.tabela_ensaios)
        divisor.addWidget(abas)
        divisor.setStretchFactor(1, 3)
        self.setCentralWidget(divisor)
        self.painel = QLabel("Selecione um ensaio.")
        self.painel.setObjectName("painelResultado")
        self.painel.setWordWrap(True)
        self.painel.setMargin(8)
        doca = QDockWidget("Resultado", self)
        doca.setObjectName("docaResultado")
        doca.setWidget(self.painel)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, doca)
        self._criar_acoes()
        self.servico.concluido.connect(self._ao_concluir)
        self.servico.falhou.connect(self._ao_falhar)
        self.tabela_ensaios.selectionModel().currentRowChanged.connect(
            self._ao_selecionar
        )
        self.statusBar().showMessage("Pronto")
        self.recarregar()

    def _criar_acoes(self) -> None:
        barra = self.addToolBar("Ensaio")
        barra.setObjectName("barraEnsaio")
        menu = self.menuBar().addMenu("&Ensaio")
        defs = [
            (
                "acao_novo",
                "&Novo ensaio...",
                QKeySequence.StandardKey.New,
                self.novo_ensaio,
            ),
            (
                "acao_importar",
                "&Importar CSV...",
                QKeySequence("Ctrl+I"),
                self.importar_csv,
            ),
            ("acao_analisar", "&Analisar", QKeySequence("F5"), self.analisar),
            (
                "acao_relatorio",
                "&Relatório PDF...",
                QKeySequence("Ctrl+P"),
                self.relatorio,
            ),
        ]
        for nome, texto, atalho, slot in defs:
            acao = QAction(texto, self)
            acao.setShortcut(atalho)
            acao.triggered.connect(slot)
            setattr(self, nome, acao)
            menu.addAction(acao)
            barra.addAction(acao)
        self._atualizar_acoes()

    def _atualizar_acoes(self) -> None:
        tem_ensaio = self.ensaio_atual() is not None
        tem_leituras = self.modelo_leituras.rowCount() > 0
        self.acao_importar.setEnabled(tem_ensaio)
        self.acao_analisar.setEnabled(tem_ensaio and tem_leituras)
        self.acao_relatorio.setEnabled(self.resultado is not None)

    # ------------------------------------------------------------- estado
    def ensaio_atual(self) -> int | None:
        idx = self.tabela_ensaios.selectionModel().currentIndex()
        return self.modelo_ensaios.ensaio_id(idx.row()) if idx.isValid() else None

    def recarregar(self, selecionar: int | None = None) -> None:
        self.modelo_ensaios.recarregar(self.repo.listar())
        for linha in range(self.modelo_ensaios.rowCount()):
            if self.modelo_ensaios.ensaio_id(linha) == selecionar:
                self.tabela_ensaios.selectRow(linha)

    def _ao_selecionar(self, atual, _anterior) -> None:
        self.resultado = None
        eid = self.ensaio_atual()
        leituras = self.repo.leituras(eid) if eid is not None else []
        self.modelo_leituras.definir(leituras)
        self.curva.setData([lt.t_min for lt in leituras], [lt.p_bar for lt in leituras])
        self.painel.setText(
            "Leituras carregadas." if leituras else "Ensaio sem leituras."
        )
        self._atualizar_acoes()

    # ------------------------------------------------------------- ações
    def novo_ensaio(
        self,
        codigo: str | None = None,
        descricao: str = "",
        criterio: Criterio | None = None,
    ) -> int | None:
        if codigo is None:
            codigo, ok = QInputDialog.getText(self, "Novo ensaio", "Código do ensaio:")
            if not ok or not codigo.strip():
                return None
        try:
            eid = self.repo.criar_ensaio(
                codigo.strip(), descricao, criterio or Criterio()
            )
        except Exception as exc:  # sqlite3.IntegrityError: código repetido
            QMessageBox.warning(self, "Novo ensaio", f"Não foi possível criar: {exc}")
            return None
        self.recarregar(selecionar=eid)
        return eid

    def importar_csv(self, caminho: str | None = None) -> bool:
        eid = self.ensaio_atual()
        if eid is None:
            return False
        if caminho is None:
            caminho, _ = QFileDialog.getOpenFileName(
                self, "Importar leituras", "", "CSV (*.csv)"
            )
            if not caminho:
                return False
        try:
            leituras = ler_csv(caminho)
        except (OSError, ErroDados) as exc:
            QMessageBox.critical(self, "Importar CSV", str(exc))
            return False
        self.repo.substituir_leituras(eid, leituras)
        self._ao_selecionar(None, None)
        self.statusBar().showMessage(
            f"{len(leituras)} leituras importadas de " f"{Path(caminho).name}", 5000
        )
        return True

    def analisar(self) -> None:
        eid = self.ensaio_atual()
        if eid is None:
            return
        self.acao_analisar.setEnabled(False)
        self.statusBar().showMessage("Analisando...")
        self.servico.analisar(
            eid, self.modelo_leituras.leituras(), self.repo.criterio(eid)
        )

    def _ao_concluir(self, eid: int, r: Resultado) -> None:
        if eid != self.ensaio_atual():  # o usuário trocou de ensaio durante a análise
            return
        self.resultado = r
        cor = "#548235" if r.aprovado else "#C00000"
        texto = (
            f"<b style='color:{cor}'>{'APROVADO' if r.aprovado else 'REPROVADO'}</b> — "
            f"queda {r.queda_bar:.3f} bar ({r.queda_pct:.3f} %), "
            f"taxa {r.taxa_bar_h:.3f} bar/h, patamar {r.duracao_min:.0f} min"
        )
        if r.motivos:
            texto += "<br>" + "; ".join(r.motivos)
        self.painel.setText(texto)
        self.statusBar().showMessage("Análise concluída", 5000)
        self._atualizar_acoes()

    def _ao_falhar(self, eid: int, mensagem: str) -> None:
        self.painel.setText(f"<b style='color:#C55A11'>Dados inválidos:</b> {mensagem}")
        self.statusBar().showMessage("Análise não realizada", 5000)
        self._atualizar_acoes()

    def relatorio(self, destino: str | None = None) -> Path | None:
        eid = self.ensaio_atual()
        if eid is None or self.resultado is None:
            return None
        idx = self.tabela_ensaios.selectionModel().currentIndex()
        codigo = self.modelo_ensaios.index(idx.row(), 0).data()
        descricao = self.modelo_ensaios.index(idx.row(), 1).data()
        if destino is None:
            destino, _ = QFileDialog.getSaveFileName(
                self, "Salvar relatório", f"{codigo}.pdf", "PDF (*.pdf)"
            )
            if not destino:
                return None
        return gerar_pdf(
            destino,
            codigo,
            descricao,
            self.modelo_leituras.leituras(),
            self.repo.criterio(eid),
            self.resultado,
        )

    # ------------------------------------------------------------- estado da janela
    def restaurar(self, cfg: QSettings) -> None:
        geometria, estado = cfg.value("janela/geometria"), cfg.value("janela/estado")
        if geometria is not None:
            self.restoreGeometry(geometria)
        if estado is not None:
            self.restoreState(estado)

    def closeEvent(self, evento) -> None:
        cfg = QSettings()
        cfg.setValue("janela/geometria", self.saveGeometry())
        cfg.setValue("janela/estado", self.saveState())
        self.servico.aguardar()
        super().closeEvent(evento)
