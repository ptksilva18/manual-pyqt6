# runner: ticks=300 timeout=180
"""Executa a suíte com pytest-cov, como em um servidor de integração contínua (sem
tela)."""

import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))


def main() -> int:
    ambiente = dict(
        os.environ, QT_QPA_PLATFORM="offscreen", PYTHONDONTWRITEBYTECODE="1"
    )
    comando = [
        sys.executable,
        "-m",
        "pytest",
        "c28_test_calculadora.py",
        "-q",
        "--no-header",
        "-p",
        "no:cacheprovider",
        "--cov=c28_calculadora",
        "--cov-branch",
        "--cov-report=term-missing",
    ]
    print("$", " ".join(["python"] + comando[1:]))
    r = subprocess.run(comando, cwd=AQUI, env=ambiente, capture_output=True, text=True)
    linhas = [ln for ln in r.stdout.splitlines() if ln.strip()]
    for ln in linhas:
        if (
            ln.startswith(("Name", "-", "c28_", "TOTAL"))
            or " passed" in ln
            or " failed" in ln
        ):
            print(ln)
    if os.path.exists(os.path.join(AQUI, ".coverage")):
        os.remove(os.path.join(AQUI, ".coverage"))
    print("código de saída do pytest:", r.returncode)
    return r.returncode


if __name__ == "__main__":
    sys.exit(main())
