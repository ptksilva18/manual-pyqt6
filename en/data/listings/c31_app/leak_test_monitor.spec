# -*- mode: python ; coding: utf-8 -*-
# pyinstaller --noconfirm leak_test_monitor.spec  (output: dist/LeakTestMonitor, onedir)
a = Analysis(
    ["run.py"],
    datas=[("data/TH-01.csv", "data")],        # example distributed with the application
    # pkg_resources/setuptools: pulled in indirectly; their runtime hook failed in the
    # executable ("platformdirs package is required"). pandas and scipy: not used.
    excludes=["tkinter", "pkg_resources", "setuptools", "pandas", "scipy", "IPython",
              "PyQt6.QtWebEngineCore", "PyQt6.QtWebEngineWidgets", "PyQt6.QtQuick3D",
              "PyQt6.Qt3DCore", "PyQt6.QtMultimedia"],
)
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name="LeakTestMonitor",
          console=False, upx=False)
coll = COLLECT(exe, a.binaries, a.datas, upx=False, name="LeakTestMonitor")
