# runner: ticks=40
"""Plugins com importlib: descoberta em pasta e por entry points, API estável e
isolamento."""

import importlib.metadata
import importlib.util
import os
import sys
from collections.abc import Callable
from types import ModuleType

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow

AQUI = os.path.dirname(os.path.abspath(__file__))
VERSAO_API = 1
GRUPO_ENTRY_POINTS = "manual_pyqt6.plugins"


class AppAPI:
    """Fachada estável oferecida aos plugins: eles não tocam na janela diretamente."""

    def __init__(self, janela: QMainWindow) -> None:
        self._janela = janela
        self._menu = janela.menuBar().addMenu("Plugins")
        self.mensagens: list[str] = []

    def adicionar_acao(self, texto: str, funcao: Callable[[], None]) -> QAction:
        acao = self._menu.addAction(texto)
        acao.triggered.connect(funcao)
        return acao

    def pressao(self) -> float:
        return 345.0

    def mostrar(self, texto: str) -> None:
        self.mensagens.append(texto)
        self._janela.statusBar().showMessage(texto)


def carregar_arquivo(caminho: str) -> ModuleType:
    nome = "plugin_" + os.path.splitext(os.path.basename(caminho))[0]
    spec = importlib.util.spec_from_file_location(nome, caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(
        modulo
    )  # executa o código do plugin: confie apenas na origem
    return modulo


def descobrir(pasta: str) -> list[ModuleType]:
    modulos = []
    for arquivo in sorted(os.listdir(pasta)):
        if arquivo.endswith(".py") and not arquivo.startswith("_"):
            modulos.append(carregar_arquivo(os.path.join(pasta, arquivo)))
    for ep in importlib.metadata.entry_points(
        group=GRUPO_ENTRY_POINTS
    ):  # pacotes instalados
        modulos.append(ep.load())
    return modulos


def ativar(modulos: list[ModuleType], api: AppAPI) -> None:
    for mod in modulos:
        nome = getattr(mod, "NOME", mod.__name__)
        if getattr(mod, "VERSAO_API", None) != VERSAO_API:
            print(
                f"  ignorado  {nome!r}: VERSAO_API={getattr(mod, 'VERSAO_API', None)} "
                f"(esperada {VERSAO_API})"
            )
            continue
        try:
            mod.registrar(api)
            print(f"  ativado   {nome!r}")
        except Exception as exc:  # um plugin defeituoso não derruba a aplicação
            print(f"  falhou    {nome!r}: {type(exc).__name__}: {exc}")


def main() -> int:
    app = QApplication(sys.argv)
    janela = QMainWindow()
    api = AppAPI(janela)
    modulos = descobrir(os.path.join(AQUI, "plugins_demo"))
    print(
        f"{len(modulos)} plugins encontrados (pasta + entry points "
        f"'{GRUPO_ENTRY_POINTS}')"
    )
    ativar(modulos, api)
    acoes = api._menu.actions()
    print("Menu Plugins:", [a.text() for a in acoes])
    acoes[0].trigger()  # simula o clique do usuário
    print("Mensagem do plugin:", api.mensagens[-1])
    janela.show()
    app.processEvents()
    return 0


if __name__ == "__main__":
    sys.exit(main())
