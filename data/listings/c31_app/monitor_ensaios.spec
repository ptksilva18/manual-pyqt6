# -*- mode: python ; coding: utf-8 -*-
# pyinstaller --noconfirm monitor_ensaios.spec   (gera dist/MonitorEnsaios, modo onedir)
a = Analysis(
    ["executar.py"],
    datas=[("dados/TH-01.csv", "dados")],      # exemplo distribuído com a aplicação
    # pkg_resources/setuptools: puxados indiretamente; o hook de runtime deles falhou no
    # executável ("platformdirs package is required"). pandas e scipy: não usados.
    excludes=["tkinter", "pkg_resources", "setuptools", "pandas", "scipy", "IPython",
              "PyQt6.QtWebEngineCore", "PyQt6.QtWebEngineWidgets", "PyQt6.QtQuick3D",
              "PyQt6.Qt3DCore", "PyQt6.QtMultimedia"],
)
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name="MonitorEnsaios",
          console=False, upx=False)
coll = COLLECT(exe, a.binaries, a.datas, upx=False, name="MonitorEnsaios")
