"""Testes de interface com pytest-qt: fluxo completo e tratamento de erro."""

from pathlib import Path

import pytest
from PyQt6.QtWidgets import QMessageBox

from ensaios.dominio import Criterio
from ensaios.janela import JanelaPrincipal
from ensaios.repositorio import Repositorio
from ensaios.servicos import ServicoAnalise

CSV = Path(__file__).resolve().parent.parent / "dados" / "TH-01.csv"


@pytest.fixture
def janela(qtbot, tmp_path):
    repo = Repositorio(tmp_path / "teste.sqlite")
    j = JanelaPrincipal(repo, ServicoAnalise())
    qtbot.addWidget(j)
    yield j
    j.servico.aguardar()
    repo.fechar()


def test_acoes_desabilitadas_sem_ensaio(janela):
    assert not janela.acao_importar.isEnabled()
    assert not janela.acao_analisar.isEnabled()
    assert not janela.acao_relatorio.isEnabled()


def test_fluxo_completo(janela, qtbot, tmp_path):
    janela.novo_ensaio("TH-01", "linha de serviço", Criterio(coef_temp_bar_c=0.25))
    assert janela.importar_csv(str(CSV))
    assert janela.modelo_leituras.rowCount() == 13
    with qtbot.waitSignal(janela.servico.concluido, timeout=5000) as bloqueio:
        janela.acao_analisar.trigger()
    resultado = bloqueio.args[1]
    assert resultado.aprovado
    assert resultado.queda_bar == pytest.approx(0.224, abs=0.001)
    assert "APROVADO" in janela.painel.text()
    assert janela.acao_relatorio.isEnabled()
    pdf = janela.relatorio(str(tmp_path / "r.pdf"))
    assert pdf.read_bytes()[:5] == b"%PDF-"


def test_codigo_repetido_mostra_aviso(janela, monkeypatch):
    avisos = []
    monkeypatch.setattr(QMessageBox, "warning", lambda *a: avisos.append(a[2]))
    janela.novo_ensaio("TH-02")
    assert janela.novo_ensaio("TH-02") is None
    assert "UNIQUE" in avisos[0]
    assert janela.modelo_ensaios.rowCount() == 1


def test_csv_invalido_nao_altera_leituras(janela, monkeypatch, tmp_path):
    erros = []
    monkeypatch.setattr(QMessageBox, "critical", lambda *a: erros.append(a[2]))
    janela.novo_ensaio("TH-03")
    ruim = tmp_path / "ruim.csv"
    ruim.write_text("t;p;T\n0;x;1\n", encoding="utf-8")
    assert not janela.importar_csv(str(ruim))
    assert "linha 2" in erros[0]
    assert janela.modelo_leituras.rowCount() == 0
