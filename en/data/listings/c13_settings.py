"""QSettings in INI format: types, groups, arrays and default values."""

import shutil
import sys
import tempfile
from pathlib import Path

from PyQt6.QtCore import QSettings
from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    file = Path(tempfile.mkdtemp()) / "engcalc.ini"
    s = QSettings(str(file), QSettings.Format.IniFormat)

    s.beginGroup("units")
    s.setValue("pressure", "bar")
    s.setValue("decimals", 2)
    s.setValue("show_psi", True)
    s.endGroup()
    s.beginWriteArray("recent")
    for i, name in enumerate(["bop_test.json", "riser_vi.json"]):
        s.setArrayIndex(i)
        s.setValue("file", name)
    s.endArray()
    s.sync()  # writes to disk now
    print(file.read_text(encoding="utf-8"))

    # Within the same run QSettings uses a cache; a copy simulates the next session
    copy = shutil.copy(file, file.with_name("next_session.ini"))
    read = QSettings(str(copy), QSettings.Format.IniFormat)
    print("no type=   ->", repr(read.value("units/decimals")))
    print("type=int   ->", repr(read.value("units/decimals", type=int)))
    print("type=bool  ->", repr(read.value("units/show_psi", type=bool)))
    print("default    ->", repr(read.value("units/temperature", "°C")))
    n = read.beginReadArray("recent")
    print(
        "recent:",
        [(read.setArrayIndex(i), read.value("file"))[1] for i in range(n)],
    )
    read.endArray()
