# -*- mode: python ; coding: utf-8 -*-
# PyInstaller specification (generated with pyi-makespec and adjusted). Usage:
#   pyinstaller --noconfirm monitor_app.spec
a = Analysis(
    ["monitor_app.py"],
    pathex=[],
    binaries=[],
    datas=[("resources", "resources")],        # (source, destination inside the package)
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=["tkinter", "PyQt6.QtWebEngineCore", "PyQt6.QtWebEngineWidgets",
              "PyQt6.Qt3DCore", "PyQt6.QtQuick3D"],   # reduces the size
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,                     # onedir: libraries outside the executable
    name="monitor_app",
    debug=False,
    strip=False,
    upx=False,
    console=True,                              # False for a GUI app without a terminal
)
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=False, name="monitor_app")
