# runner: ticks=60
"""Tratamento global de exceções: sys.excepthook, threading.excepthook e relatório de
erro."""

import logging
import platform
import sys
import threading
import traceback

from PyQt6.QtCore import PYQT_VERSION_STR, QT_VERSION_STR, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox

logging.basicConfig(
    stream=sys.stdout, level=logging.INFO, format="%(levelname)s %(message)s"
)
log = logging.getLogger("ensaios")


def relatorio(tipo, valor, tb) -> str:
    pilha = "".join(traceback.format_exception(tipo, valor, tb))
    ambiente = (
        f"Python {platform.python_version()}, PyQt6 {PYQT_VERSION_STR}, "
        f"Qt {QT_VERSION_STR}, {platform.system()}"
    )
    return f"{ambiente}\n{pilha}"


def tratar_excecao(tipo, valor, tb) -> None:
    """Substitui o comportamento padrão do PyQt6 (abortar o processo) — Capítulo 3."""
    if issubclass(tipo, KeyboardInterrupt):
        sys.__excepthook__(tipo, valor, tb)
        return
    texto = relatorio(tipo, valor, tb)
    log.error("exceção não tratada:\n%s", texto.splitlines()[-1])
    caixa = QMessageBox(
        QMessageBox.Icon.Critical,
        "Erro inesperado",
        "Ocorreu um erro. A operação foi cancelada, e a aplicação continua.",
    )
    caixa.setDetailedText(texto)  # o usuário pode copiar e enviar ao suporte
    caixa.exec()


def tratar_excecao_thread(args: threading.ExceptHookArgs) -> None:
    log.error(
        "exceção na thread %s: %s: %s",
        args.thread.name,
        args.exc_type.__name__,
        args.exc_value,
    )


def main() -> int:
    sys.excepthook = tratar_excecao  # antes de criar a QApplication
    threading.excepthook = tratar_excecao_thread
    app = QApplication(sys.argv)
    janela = QMainWindow()  # sem janela aberta, fechar a caixa de erro encerraria o app
    janela.setWindowTitle("Monitor de ensaios")
    janela.show()

    def slot_com_erro() -> None:
        dados = {"PT-101": 345.0}
        log.info("calculando com %s", dados["PT-102"])  # KeyError dentro de um slot

    QTimer.singleShot(100, slot_com_erro)
    threading.Thread(target=lambda: 1 / 0, name="exportador").start()

    def continua() -> None:
        log.info("a aplicação continuou rodando após os erros")
        app.quit()

    QTimer.singleShot(600, continua)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
