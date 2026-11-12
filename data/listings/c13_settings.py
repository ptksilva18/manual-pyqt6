"""QSettings em formato INI: tipos, grupos, arrays e valores padrão."""

import shutil
import sys
import tempfile
from pathlib import Path

from PyQt6.QtCore import QSettings
from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    arquivo = Path(tempfile.mkdtemp()) / "calceng.ini"
    s = QSettings(str(arquivo), QSettings.Format.IniFormat)

    s.beginGroup("unidades")
    s.setValue("pressao", "bar")
    s.setValue("casas_decimais", 2)
    s.setValue("mostrar_psi", True)
    s.endGroup()
    s.beginWriteArray("recentes")
    for i, nome in enumerate(["ensaio_bop.json", "riser_vi.json"]):
        s.setArrayIndex(i)
        s.setValue("arquivo", nome)
    s.endArray()
    s.sync()  # grava no disco agora
    print(arquivo.read_text(encoding="utf-8"))

    # Na mesma execução o QSettings usa cache; uma cópia simula a próxima sessão
    copia = shutil.copy(arquivo, arquivo.with_name("proxima_sessao.ini"))
    lido = QSettings(str(copia), QSettings.Format.IniFormat)
    print("sem type=  ->", repr(lido.value("unidades/casas_decimais")))
    print("type=int   ->", repr(lido.value("unidades/casas_decimais", type=int)))
    print("type=bool  ->", repr(lido.value("unidades/mostrar_psi", type=bool)))
    print("padrão     ->", repr(lido.value("unidades/temperatura", "°C")))
    n = lido.beginReadArray("recentes")
    print(
        "recentes:",
        [(lido.setArrayIndex(i), lido.value("arquivo"))[1] for i in range(n)],
    )
    lido.endArray()
