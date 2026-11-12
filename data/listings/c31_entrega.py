# runner: ticks=9000 timeout=900
"""Entrega do projeto integrador: testes com cobertura, autoteste, empacotamento e
reteste."""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PROJETO = Path(__file__).resolve().parent / "c31_app"


def rodar(titulo: str, comando: list[str], cwd: Path, filtro=None) -> int:
    ambiente = dict(
        os.environ, QT_QPA_PLATFORM="offscreen", PYTHONDONTWRITEBYTECODE="1"
    )
    r = subprocess.run(
        comando, cwd=cwd, env=ambiente, capture_output=True, text=True, timeout=600
    )
    print(f"== {titulo} (código {r.returncode})")
    for linha in r.stdout.splitlines():
        if filtro is None or filtro(linha):
            print("  " + linha)
    if r.returncode != 0:
        print(r.stderr[-1500:])
    return r.returncode


def main() -> int:
    obra = Path(tempfile.mkdtemp())
    copia = Path(shutil.copytree(PROJETO, obra / "c31_app"))
    falhas = rodar(
        "1. testes (pytest + cobertura)",
        [
            sys.executable,
            "-m",
            "pytest",
            "tests",
            "-q",
            "--no-header",
            "-p",
            "no:cacheprovider",
            "--cov=ensaios",
            "--cov-report=term",
        ],
        copia,
        lambda ln: ln.startswith(("ensaios", "TOTAL")) or "passed" in ln,
    )
    saida = obra / "fonte"
    saida.mkdir()
    falhas += rodar(
        "2. autoteste a partir do código-fonte",
        [sys.executable, "-m", "ensaios", "--autoteste", str(saida)],
        copia,
    )
    falhas += rodar(
        "3. empacotamento (PyInstaller, onedir)",
        [
            sys.executable,
            "-m",
            "PyInstaller",
            "--noconfirm",
            "--log-level",
            "WARN",
            "monitor_ensaios.spec",
        ],
        copia,
    )
    dist = copia / "dist" / "MonitorEnsaios"
    exe = dist / ("MonitorEnsaios.exe" if sys.platform == "win32" else "MonitorEnsaios")
    tamanho = sum(f.stat().st_size for f in dist.rglob("*") if f.is_file()) / 1024**2
    print(f"   pacote: dist/MonitorEnsaios ({tamanho:.0f} MB)")
    saida_c = obra / "congelado"
    saida_c.mkdir()
    falhas += rodar(
        "4. autoteste do executável congelado",
        [str(exe), "--autoteste", str(saida_c)],
        copia,
    )
    shutil.rmtree(obra)
    print("ENTREGA", "APROVADA" if falhas == 0 else "COM FALHAS")
    return falhas


if __name__ == "__main__":
    sys.exit(main())
