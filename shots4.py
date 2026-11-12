# -*- coding: utf-8 -*-
"""Figuras 31.2 e 31.3: janela principal após o autoteste e primeira página do relatório PDF,
ambas produzidas pela própria aplicação do projeto integrador.

Figura 31.2: "python -m ensaios --autoteste PASTA --captura BRUTO" (offscreen, 2x), com a mesma
moldura das demais capturas. Figura 31.3: página 1 do PDF gravado pelo autoteste, renderizada
com pdftoppm (110 dpi) sobre margem cinza de 20 px.
"""
import os
import shutil
import subprocess
import sys
import tempfile

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(HERE, "data", "listings", "c31_app")
FIG = os.path.join(HERE, "data", "figs")
sys.path.insert(0, HERE)
from shots3 import framed  # noqa: E402  (mesma moldura das demais capturas)


def main() -> int:
    work = tempfile.mkdtemp()
    raw = os.path.join(work, "window.png")
    env = dict(os.environ, QT_QPA_PLATFORM="offscreen", QT_SCALE_FACTOR="2",
               PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run([sys.executable, "-m", "ensaios", "--autoteste", work, "--captura", raw],
                       cwd=APP, env=env, capture_output=True, text=True, timeout=120)
    print(r.stdout.strip())
    if r.returncode != 0 or not os.path.exists(raw):
        print(r.stderr[-1500:])
        return 1
    framed(raw, "Monitor de Ensaios 1.0.0", "f31_2_janela.png")
    pdf = os.path.join(work, "TH-01.pdf")
    subprocess.run(["pdftoppm", "-f", "1", "-l", "1", "-r", "110", "-png", pdf,
                    os.path.join(work, "page")], check=True)
    page = Image.open(os.path.join(work, "page-1.png")).convert("RGB")
    canvas = Image.new("RGB", (page.width + 40, page.height + 40), (205, 210, 218))
    canvas.paste(page, (20, 20))
    canvas.save(os.path.join(FIG, "f31_3_relatorio.png"), dpi=(300, 300))
    for name in ("f31_2_janela.png", "f31_3_relatorio.png"):
        print(f"{name}: {Image.open(os.path.join(FIG, name)).size}")
    shutil.rmtree(work)
    return 0


if __name__ == "__main__":
    sys.exit(main())
