"""Ponto de entrada: python -m ensaios [--autoteste PASTA]."""

import sys
import tempfile
from pathlib import Path

from PyQt6.QtCore import QSettings, QStandardPaths, QTimer
from PyQt6.QtWidgets import QApplication

from . import __version__
from .dominio import Criterio
from .janela import JanelaPrincipal
from .repositorio import Repositorio
from .servicos import ServicoAnalise


def pasta_dados() -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / "dados"
    return Path(__file__).resolve().parent.parent / "dados"


def autoteste(janela: JanelaPrincipal, saida: Path, app: QApplication) -> None:
    """Roteiro completo sem interação: criar, importar, analisar (em thread) e gerar
    PDF."""
    criterio = Criterio(
        duracao_min=60.0, queda_max_pct=0.5, taxa_max_bar_h=1.0, coef_temp_bar_c=0.25
    )  # compensação térmica do fluido aprisionado
    eid = janela.novo_ensaio(
        "TH-01", "Teste de estanqueidade da linha de serviço", criterio
    )
    print(
        f"ensaio criado: id={eid}; ensaios na lista: {janela.modelo_ensaios.rowCount()}"
    )
    janela.importar_csv(str(pasta_dados() / "TH-01.csv"))
    print(
        f"leituras: {janela.modelo_leituras.rowCount()}; "
        f"ação Analisar habilitada: {janela.acao_analisar.isEnabled()}"
    )

    def concluido(_eid, r) -> None:
        print(
            f"resultado: aprovado={r.aprovado}, queda={r.queda_bar:.3f} bar "
            f"({r.queda_pct:.3f} %), taxa={r.taxa_bar_h:.3f} bar/h, "
            f"p_final_corrigida={r.p_final_corrigida:.3f} bar"
        )
        pdf = janela.relatorio(str(saida / "TH-01.pdf"))
        print(
            f"relatório: {pdf.name}, {pdf.stat().st_size} bytes, "
            f"cabeçalho {pdf.read_bytes()[:5]!r}"
        )
        print(
            "painel:", janela.painel.text().split(" — ")[0].split(">")[1].split("<")[0]
        )
        if "--captura" in sys.argv:  # imagem da janela para a documentação
            janela.grab().save(sys.argv[sys.argv.index("--captura") + 1])
        QTimer.singleShot(0, janela.close)

    janela.servico.concluido.connect(concluido)
    janela.acao_analisar.trigger()


def main(argv: list[str]) -> int:
    app = QApplication(argv)
    app.setOrganizationName("ManualPyQt6")
    app.setApplicationName("MonitorEnsaios")
    app.setApplicationVersion(__version__)
    if "--autoteste" in argv:
        saida = Path(argv[argv.index("--autoteste") + 1])
        QSettings.setDefaultFormat(QSettings.Format.IniFormat)
        QSettings.setPath(
            QSettings.Format.IniFormat, QSettings.Scope.UserScope, str(saida)
        )
        banco = saida / "ensaios.sqlite"
    else:
        dados = Path(
            QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.AppDataLocation
            )
        )
        dados.mkdir(parents=True, exist_ok=True)
        banco = dados / "ensaios.sqlite"
    repo = Repositorio(banco)
    janela = JanelaPrincipal(repo, ServicoAnalise())
    janela.restaurar(QSettings())
    janela.resize(1000, 640)
    janela.show()
    if "--autoteste" in argv:
        QTimer.singleShot(0, lambda: autoteste(janela, saida, app))
    codigo = app.exec()
    repo.fechar()
    return codigo


if __name__ == "__main__":
    sys.exit(main(sys.argv))
