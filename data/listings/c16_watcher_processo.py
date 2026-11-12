"""QFileSystemWatcher e QProcess (execução síncrona e assíncrona)."""

import sys
import tempfile
from pathlib import Path

from PyQt6.QtCore import QEventLoop, QFileSystemWatcher, QProcess, QTimer
from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    arquivo = Path(tempfile.mkdtemp()) / "parametros.txt"
    arquivo.write_text("pressao=345\n", encoding="utf-8")

    vigia = QFileSystemWatcher([str(arquivo)])
    loop = QEventLoop()
    vigia.fileChanged.connect(
        lambda c: (print("fileChanged:", Path(c).name), loop.quit())
    )
    QTimer.singleShot(
        200, lambda: arquivo.write_text("pressao=350\n", encoding="utf-8")
    )
    QTimer.singleShot(5000, loop.quit)  # salvaguarda
    loop.exec()

    # Síncrono: bloqueia até terminar (aceitável apenas para comandos rápidos)
    p = QProcess()
    p.start(sys.executable, ["-c", "print(2 * 345)"])
    p.waitForFinished(5000)
    print(
        "síncrono ->",
        bytes(p.readAllStandardOutput()).decode().strip(),
        "| código:",
        p.exitCode(),
    )

    # Assíncrono: a interface continua respondendo; resultados chegam por sinais
    assinc = QProcess()
    assinc.setProgram(sys.executable)
    assinc.setArguments(["-c", "import sys; print('saida ok'); sys.exit(3)"])

    def ler_saida():
        # A saída pode chegar em partes: ignore trechos vazios
        texto = bytes(assinc.readAllStandardOutput()).decode().strip()
        if texto:
            print("stdout:", texto)

    assinc.readyReadStandardOutput.connect(ler_saida)
    assinc.finished.connect(
        lambda codigo, status: (
            print("finished: código", codigo, "|", status.name),
            app.quit(),
        )
    )
    assinc.errorOccurred.connect(lambda e: print("erro:", e.name))
    assinc.start()
    app.exec()
