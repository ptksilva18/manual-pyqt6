# runner: ticks=60
"""Depuração: QLoggingCategory, regras de filtro, manipulador de mensagens e
QT_DEBUG_PLUGINS."""

import os
import subprocess
import sys

from PyQt6.QtCore import (
    QLoggingCategory,
    QMessageLogContext,
    QtMsgType,
    qInstallMessageHandler,
)
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QWidget

# O construtor C++ guarda só o PONTEIRO para o nome: mantenha os bytes vivos no módulo.
# (No teste, categorias criadas com str temporária ignoraram as regras de filtro.)
NOME_IO, NOME_CALC = b"ensaios.io", b"ensaios.calculo"
IO = QLoggingCategory(NOME_IO)
CALC = QLoggingCategory(NOME_CALC)
capturadas: list[str] = []


def manipulador(tipo: QtMsgType, contexto: QMessageLogContext, mensagem: str) -> None:
    """Recebe TODAS as mensagens do Qt (C++ e Python), com tipo e categoria."""
    capturadas.append(f"[{tipo.name}] {contexto.category}: {mensagem}")


def main() -> int:
    app = QApplication(sys.argv)
    anterior = qInstallMessageHandler(manipulador)
    print("Antes das regras: ensaios.io debug =", IO.isDebugEnabled())
    QLoggingCategory.setFilterRules("ensaios.*.debug=false\nensaios.calculo.debug=true")
    print(
        "Depois: ensaios.io debug =",
        IO.isDebugEnabled(),
        "| ensaios.calculo debug =",
        CALC.isDebugEnabled(),
        "| ensaios.io warning =",
        IO.isWarningEnabled(),
    )
    w = QWidget()
    w.setLayout(QVBoxLayout())
    w.setLayout(QHBoxLayout())  # erro de uso: o Qt emite um aviso pela categoria padrão
    qInstallMessageHandler(anterior)
    for linha in capturadas:
        print("capturada:", linha[:110])

    ambiente = dict(os.environ, QT_DEBUG_PLUGINS="1", QT_QPA_PLATFORM="offscreen")
    r = subprocess.run(
        [
            sys.executable,
            "-c",
            "from PyQt6.QtWidgets import QApplication; QApplication([])",
        ],
        env=ambiente,
        capture_output=True,
        text=True,
    )
    carregadas = [
        os.path.basename(ln.split('"')[1])
        for ln in r.stderr.splitlines()
        if ln.endswith(" loaded library")
    ]
    print(
        f"QT_DEBUG_PLUGINS=1: {len(r.stderr.splitlines())} linhas de diagnóstico; "
        f"plugins carregados: {carregadas}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
