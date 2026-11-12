# runner: ticks=6000 timeout=900
"""Packages c30_app with PyInstaller (onedir), runs the result and checks its contents."""

import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


def size_mb(folder: str) -> float:
    total = 0
    for root, _dirs, files in os.walk(folder):
        total += sum(os.path.getsize(os.path.join(root, f)) for f in files)
    return total / 1024**2


def main() -> int:
    work = tempfile.mkdtemp()
    project = shutil.copytree(
        os.path.join(HERE, "c30_app"), os.path.join(work, "c30_app")
    )
    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--log-level",
        "WARN",
        "--distpath",
        os.path.join(work, "dist"),
        "--workpath",
        os.path.join(work, "build"),
        "monitor_app.spec",
    ]
    print("$ pyinstaller --noconfirm monitor_app.spec")
    r = subprocess.run(command, cwd=project, capture_output=True, text=True)
    print("PyInstaller exit code:", r.returncode)
    if r.returncode != 0:
        print(r.stderr[-2000:])
        return 1
    dist = os.path.join(work, "dist", "monitor_app")
    exe = os.path.join(
        dist, "monitor_app.exe" if sys.platform == "win32" else "monitor_app"
    )
    internal = os.path.join(dist, "_internal")
    print(f"folder generated: dist/monitor_app ({size_mb(dist):.0f} MB)")
    print(
        "contents of _internal/PyQt6/Qt6:",
        sorted(os.listdir(os.path.join(internal, "PyQt6", "Qt6"))),
    )
    print("resources included:", sorted(os.listdir(os.path.join(internal, "resources"))))
    environment = dict(os.environ, QT_QPA_PLATFORM="offscreen")
    r = subprocess.run(
        [exe, "--selftest"], env=environment, capture_output=True, text=True, timeout=60
    )
    print(f"frozen executable (code {r.returncode}):")
    for line in r.stdout.splitlines():
        print("  " + line)
    shutil.rmtree(work)
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
