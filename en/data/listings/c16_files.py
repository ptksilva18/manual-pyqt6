"""QSaveFile + QTextStream (text) and QDataStream (versioned binary)."""

import sys
import tempfile
from pathlib import Path

from PyQt6.QtCore import QDataStream, QFile, QIODevice, QSaveFile, QTextStream
from PyQt6.QtWidgets import QApplication

OM = QIODevice.OpenModeFlag

if __name__ == "__main__":
    app = QApplication(sys.argv)
    folder = Path(tempfile.mkdtemp())

    # Text with atomic saving: the final file is replaced only on commit()
    target = folder / "report.txt"
    f = QSaveFile(str(target))
    if not f.open(OM.WriteOnly | OM.Text):
        sys.exit(f.errorString())
    s = QTextStream(f)  # UTF-8 by default in Qt 6
    s << "Hydrostatic test\n" << "Pressure: " << 345.0 << " bar\n"
    s.flush()
    print(
        "commit:",
        f.commit(),
        "| content:",
        target.read_text(encoding="utf-8").split("\n"),
    )

    # Binary with QDataStream: a format portable across platforms, with a version
    binary = folder / "measurements.bin"
    w = QFile(str(binary))
    w.open(OM.WriteOnly)
    out = QDataStream(w)
    out.setVersion(QDataStream.Version.Qt_6_0)  # pin the format version
    out.writeUInt32(0xCA1C0001)  # the file's "magic number"
    out.writeQString("PT-101")
    out.writeUInt32(3)
    for v in (101.3, 205.7, 344.9):
        out.writeDouble(v)
    w.close()

    r = QFile(str(binary))
    r.open(OM.ReadOnly)
    inp = QDataStream(r)
    inp.setVersion(QDataStream.Version.Qt_6_0)
    magic = inp.readUInt32()
    tag = inp.readQString()
    n = inp.readUInt32()
    values = [inp.readDouble() for _ in range(n)]
    print(f"magic ok? {magic == 0xCA1C0001} | {tag} | {values}")
    print(f"read status: {inp.status().name}")
    print("file size:", binary.stat().st_size, "bytes")
