# -*- mode: python ; coding: utf-8 -*-
# Especificação do PyInstaller (gerada com pyi-makespec e ajustada). Uso:
#   pyinstaller --noconfirm app_ensaios.spec
a = Analysis(
    ["app_ensaios.py"],
    pathex=[],
    binaries=[],
    datas=[("recursos", "recursos")],          # (origem, destino dentro do pacote)
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=["tkinter", "PyQt6.QtWebEngineCore", "PyQt6.QtWebEngineWidgets",
              "PyQt6.Qt3DCore", "PyQt6.QtQuick3D"],   # reduz o tamanho
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,                     # onedir: bibliotecas fora do executável
    name="app_ensaios",
    debug=False,
    strip=False,
    upx=False,
    console=True,                              # False para aplicação gráfica sem terminal
)
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=False, name="app_ensaios")
