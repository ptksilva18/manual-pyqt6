"""QSaveFile + QTextStream (texto) e QDataStream (binário versionado)."""

import sys
import tempfile
from pathlib import Path

from PyQt6.QtCore import QDataStream, QFile, QIODevice, QSaveFile, QTextStream
from PyQt6.QtWidgets import QApplication

OM = QIODevice.OpenModeFlag

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pasta = Path(tempfile.mkdtemp())

    # Texto com gravação atômica: o arquivo final só é substituído no commit()
    destino = pasta / "relatorio.txt"
    f = QSaveFile(str(destino))
    if not f.open(OM.WriteOnly | OM.Text):
        sys.exit(f.errorString())
    s = QTextStream(f)  # UTF-8 por padrão no Qt 6
    s << "Ensaio hidrostático\n" << "Pressão: " << 345.0 << " bar\n"
    s.flush()
    print(
        "commit:",
        f.commit(),
        "| conteúdo:",
        destino.read_text(encoding="utf-8").split("\n"),
    )

    # Binário com QDataStream: formato portável entre plataformas, com versão
    binario = pasta / "medicoes.bin"
    w = QFile(str(binario))
    w.open(OM.WriteOnly)
    out = QDataStream(w)
    out.setVersion(QDataStream.Version.Qt_6_0)  # fixe a versão do formato
    out.writeUInt32(0xCA1C0001)  # "número mágico" do arquivo
    out.writeQString("PT-101")
    out.writeUInt32(3)
    for v in (101.3, 205.7, 344.9):
        out.writeDouble(v)
    w.close()

    r = QFile(str(binario))
    r.open(OM.ReadOnly)
    inp = QDataStream(r)
    inp.setVersion(QDataStream.Version.Qt_6_0)
    magico = inp.readUInt32()
    tag = inp.readQString()
    n = inp.readUInt32()
    valores = [inp.readDouble() for _ in range(n)]
    print(f"mágico ok? {magico == 0xCA1C0001} | {tag} | {valores}")
    print(f"status da leitura: {inp.status().name}")
    print("tamanho do arquivo:", binario.stat().st_size, "bytes")
