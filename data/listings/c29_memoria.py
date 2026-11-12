# runner: ticks=60
"""Armadilhas de memória Python/C++: objetos destruídos, sip.isdeleted e faulthandler."""

import gc
import subprocess
import sys

from PyQt6 import sip
from PyQt6.QtCore import QEvent
from PyQt6.QtWidgets import QApplication, QLabel, QTableView, QWidget


def main() -> int:
    app = QApplication(sys.argv)

    # 1) O pai destrói os filhos C++; o objeto Python continua existindo, "vazio".
    pai = QWidget()
    rotulo = QLabel("PT-101", pai)
    pai.deleteLater()
    # Processa o deleteLater agora (normalmente, quem faz isso é o event loop).
    app.sendPostedEvents(None, QEvent.Type.DeferredDelete.value)
    print("1) sip.isdeleted(rotulo) =", sip.isdeleted(rotulo))
    try:
        rotulo.setText("x")
    except RuntimeError as exc:
        print("   RuntimeError:", exc)

    # 2) Temporário: o cabeçalho pertence à tabela, que é coletada ao fim da expressão.
    cabecalho = QTableView().horizontalHeader()
    gc.collect()
    print("2) cabeçalho de tabela temporária destruído?", sip.isdeleted(cabecalho))

    # 3) Objeto sem pai e sem referência Python: some imediatamente.
    def criar_janela_errado() -> None:
        janela = QWidget()
        janela.setWindowTitle("some ao sair da função")
        janela.show()

    criar_janela_errado()
    print(
        "3) janelas de topo visíveis após a função:",
        [w.windowTitle() for w in app.topLevelWidgets() if w.isVisible()],
    )

    # 4) Falha em código nativo: faulthandler mostra a pilha Python antes de morrer.
    codigo = "import faulthandler, ctypes; faulthandler.enable(); ctypes.string_at(0)"
    r = subprocess.run([sys.executable, "-c", codigo], capture_output=True, text=True)
    linhas = [ln.strip() for ln in r.stderr.splitlines() if ln.strip()]
    print(
        f"4) processo filho terminou com código {r.returncode}; faulthandler relatou:"
    )
    for ln in linhas[:1] + [ln for ln in linhas if ln.startswith("File")][-1:]:
        print("   " + ln)
    return 0


if __name__ == "__main__":
    sys.exit(main())
