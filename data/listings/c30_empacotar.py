# runner: ticks=6000 timeout=900
"""Empacota c30_app com PyInstaller (onedir), executa o resultado e confere o conteúdo."""

import os
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))


def tamanho_mb(pasta: str) -> float:
    total = 0
    for raiz, _dirs, arquivos in os.walk(pasta):
        total += sum(os.path.getsize(os.path.join(raiz, a)) for a in arquivos)
    return total / 1024**2


def main() -> int:
    obra = tempfile.mkdtemp()
    projeto = shutil.copytree(
        os.path.join(AQUI, "c30_app"), os.path.join(obra, "c30_app")
    )
    comando = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--log-level",
        "WARN",
        "--distpath",
        os.path.join(obra, "dist"),
        "--workpath",
        os.path.join(obra, "build"),
        "app_ensaios.spec",
    ]
    print("$ pyinstaller --noconfirm app_ensaios.spec")
    r = subprocess.run(comando, cwd=projeto, capture_output=True, text=True)
    print("código de saída do PyInstaller:", r.returncode)
    if r.returncode != 0:
        print(r.stderr[-2000:])
        return 1
    dist = os.path.join(obra, "dist", "app_ensaios")
    exe = os.path.join(
        dist, "app_ensaios.exe" if sys.platform == "win32" else "app_ensaios"
    )
    interno = os.path.join(dist, "_internal")
    print(f"pasta gerada: dist/app_ensaios ({tamanho_mb(dist):.0f} MB)")
    print(
        "conteúdo de _internal/PyQt6/Qt6:",
        sorted(os.listdir(os.path.join(interno, "PyQt6", "Qt6"))),
    )
    print("recursos incluídos:", sorted(os.listdir(os.path.join(interno, "recursos"))))
    ambiente = dict(os.environ, QT_QPA_PLATFORM="offscreen")
    r = subprocess.run(
        [exe, "--autoteste"], env=ambiente, capture_output=True, text=True, timeout=60
    )
    print(f"executável congelado (código {r.returncode}):")
    for linha in r.stdout.splitlines():
        print("  " + linha)
    shutil.rmtree(obra)
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
