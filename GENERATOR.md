# Generator of MAN-PYQT6-001 (Rev. 0)

The manual is generated from this repository: `build.py` writes the OOXML (Word) directly, reading the
text of the content modules, the code of the listings and the actual outputs recorded by `runner.py`.
No output is typed by hand.

The `MANUAL_LANG` variable selects the edition: `pt` (default) or `en`.

| | Portuguese (`MANUAL_LANG=pt`) | English (`MANUAL_LANG=en`) |
|---|---|---|
| Text | `front.py`, `part*.py`, `anexo_b.py`, `part2_anexos.py` | `en/*.py` (same module names, first on `sys.path`) |
| Listings / outputs / figures | `data/listings/`, `data/outputs/`, `data/figs/` | `en/data/listings/`, `en/data/outputs/`, `en/data/figs/` |
| Fixed document strings (captions, contents, cover) | `i18n.py` | `i18n.py` |

The Portuguese version of this file is [GERADOR.md](GERADOR.md).

## Requirements

- Python ≥ 3.10 (tested with 3.13) and the packages of [`requirements.txt`](requirements.txt).
- LibreOffice (`soffice`) for the audit PDF and Poppler (`pdftotext`, `pdfinfo`, `pdftoppm`).
- DejaVu fonts (`fonts-dejavu-core`) for diagrams and screenshots.

System tools used by the listings of Parts III and IV (Ubuntu 24.04):

```
apt: xvfb mesa-vulkan-drivers socat dbus dbus-x11 qt6-documentation-tools openssl libxcb-cursor0
```

- Xvfb :99 + the xcb platform for OpenGL/RHI (QtGraphs, Qt Quick 3D, QOpenGLWidget, Vulkan);
- `socat` creates the pair of virtual serial ports (`serial` option of the runner; the English listing
  reads the `SERIAL_PORT` variable);
- `dbus-run-session` isolates the D-Bus bus (`dbus` option of the runner);
- `openssl` generates the test certificate of Listing 21.4 (automatic in `runner.py`; `server.crt`/
  `server.key` in English).

One-off results already included:

- `pyside6-lrelease` (PySide6-Essentials 6.12.0): `en/data/listings/c13_engcalc_pt_BR.qm`;
- Qt Designer under Xvfb: `en/data/figs/raw_designer_xvfb.png`;
- `qhelpgenerator` (Qt 6.4, Ubuntu): `en/data/listings/resources/help/manual.qch`.

## Workflow (English edition)

```bash
export MANUAL_LANG=en
python runner.py                 # runs every listing (options on the first line, "# runner: ...")
python en/shots2.py              # screenshots of Parts I and II (includes en/shots.py)
python en/shots3.py              # screenshots of Parts III and IV (xcb/offscreen, 2x)
python en/shots4.py              # Figures 31.2 and 31.3 (window and report of the capstone project)
python en/diagrams.py && python en/diagrams2.py
./run_pass.sh e1                 # 1st pass: build/e1.docx + audit PDF
python pages.py build/e1_audit.pdf build/e1_audit.docx.meta.json build/pag_en.json
./run_pass.sh e2 build/pag_en.json   # 2nd pass; repeat (pages.py + run_pass.sh) until 0 divergences
python listings_index.py --check build/e2.docx.meta.json   # writes en/data/listings/INDEX.md
```

`run_pass.sh` produces two files:

- `build/<name>.docx` — Word version, with field-based captions (in Word: Ctrl+A and F9 to update);
- `build/<name>_audit.docx/.pdf` — static captions, rendered by LibreOffice; the page numbers of the
  table of contents and of the lists come from this PDF, and it is the published PDF.

Use the `SOFFICE` variable if the LibreOffice executable is not on the `PATH`.

Options of each listing (first line `# runner: ...`): `ticks=N`, `timeout=N`, `xcb`, `dbus`, `serial`,
`env=K:V` — details in the header of [`runner.py`](runner.py).
