# Professional Python GUI Development Manual (PyQt6)

**MAN-PYQT6-001 · Rev. 0** — building desktop applications with PyQt6, from zero to advanced.
Available in **English** and in **Brazilian Portuguese** · [Leia em português](README.pt-BR.md)

[![Code: GPL-3.0-only](https://img.shields.io/badge/code-GPL--3.0--only-blue)](LICENSES/GPL-3.0-only.txt)
[![Text: CC BY-SA 4.0](https://img.shields.io/badge/text-CC%20BY--SA%204.0-lightgrey)](LICENSES/CC-BY-SA-4.0.txt)
[![REUSE](https://img.shields.io/badge/REUSE-compliant-green)](REUSE.toml)

A teaching manual that goes from the first `QApplication` to a complete technical application, tested
and packaged. 163 of the 169 code listings were **run and verified** (139 directly, 24 through the
listing that loads them); the other 6 are 4 support files and 2 Windows-only examples. The output
printed in the manual is the program's actual output. The English edition is a full localization,
not just a text translation: identifiers, comments, messages and outputs were translated, every
runnable listing was run again in its English form, and the screenshots and diagrams were
regenerated from the English code.

| | English edition | Portuguese edition (pt-BR) |
|---|---|---|
| Pages | 407 | 408 |
| Code listings | 169 | 169 |
| — run directly / verified by another listing / support / Windows only | 139 / 24 / 4 / 2 | 139 / 24 / 4 / 2 |
| Figures / tables | 36 / 99 | 36 / 99 |
| Reference versions | Python ≥ 3.10 (tested with 3.13) · PyQt6 6.12.0 · Qt 6.12 LTS | same |

Both editions have the same structure: identical numbering of chapters, sections, figures, tables and
listings, so a reference such as "Listing 20.2" points to the same example in either language.

## Download the manual

The PDF and DOCX of both editions are on the **[Releases](https://github.com/ptksilva18/manual-pyqt6/releases/latest)**
page.

## Contents

- **Part I — Fundamentals (Ch. 1–10):** the Qt ecosystem, environment, essential Python for GUIs, first
  application, `QObject`/signals and slots, widgets, layouts, `QMainWindow`, dialogs and events.
- **Part II — Professional interface (Ch. 11–19):** Qt Designer, styles and themes, resources and
  internationalization, Model/View, QtSql, files and processes, QPainter/printing/SVG, Graphics View,
  animations and state machines.
- **Part III — Advanced development (Ch. 20–26):** concurrency and asyncio, networking and devices
  (serial, TLS), scientific visualization, multimedia, web and integrated help, OpenGL/Vulkan/3D, QML.
- **Part IV — Quality, architecture and distribution (Ch. 27–30):** layered architecture (MVP/MVVM,
  dependency injection, plugins), testing with pytest-qt, performance and accessibility, packaging with
  PyInstaller and cx_Freeze.
- **Part V — Capstone project (Ch. 31):** a leak test monitor with SQLite, background analysis, chart,
  PDF report, tests and a standalone executable.
- **Annexes:** catalog of PyQt6 6.12 classes by module, the `Qt` namespace and enums, Qt Style Sheets,
  command-line tools. References and glossary are included as well.

## Repository layout

```
en/data/listings/      English edition: code of every listing (cNN_* = Chapter NN) — see INDEX.md
en/data/listings/c31_app/   capstone project, English (package "leaktest")
en/data/outputs/       actual outputs of the English listings (printed in the manual)
data/listings/         Portuguese edition: code of every listing — see INDICE.md
data/listings/c31_app/ capstone project, Portuguese (package "ensaios")
data/outputs/          actual outputs of the Portuguese listings
data/figs/, en/data/figs/, img/   figures and cover
runner.py              runs the listings headless and records the outputs
build.py, part*.py     document generator (Portuguese text); en/*.py holds the English text
```

[`en/data/listings/INDEX.md`](en/data/listings/INDEX.md) maps each listing number to its file
(Portuguese: [`data/listings/INDICE.md`](data/listings/INDICE.md)).

## Running the examples

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt

python en/data/listings/c04_first.py      # opens the first window of Chapter 4
```

Capstone project (Chapter 31):

```bash
cd en/data/listings/c31_app
python -m leaktest                 # opens the application
python -m pytest -q                # 13 tests
cd ../../../..
python en/data/listings/c31_delivery.py   # tests + self-test + PyInstaller + self-test of the executable
```

To run **all** the listings without a display (Linux), use `MANUAL_LANG=en python runner.py`, or
`MANUAL_LANG=en python runner.py <filter>` (for example, `MANUAL_LANG=en python runner.py c21`); without
`MANUAL_LANG`, the runner uses the Portuguese edition. Some listings of Parts III and IV need system
tools (Xvfb, socat, dbus); the full list is in [GENERATOR.md](GENERATOR.md). The **test** certificate
used by Listing 21.4 is generated automatically by `runner.py` (the private key is not versioned).

## License

| What | License |
|---|---|
| Code: listings, capstone project, document generator | [GPL-3.0-only](LICENSES/GPL-3.0-only.txt), the same as PyQt6 |
| Text, figures, tables and example outputs (manual in PDF/DOCX and `.md` files) | [CC BY-SA 4.0](LICENSES/CC-BY-SA-4.0.txt) |
| `DejaVuSansMono.ttf` font (used by one listing) | [Bitstream Vera](LICENSES/Bitstream-Vera.txt) (DejaVu changes in the public domain) |

The listings printed in the manual are GPL-3.0-only as well. The file-by-file detail is in
[`REUSE.toml`](REUSE.toml), following the [REUSE](https://reuse.software/) standard.

**If you distribute an application made with PyQt6:** PyQt6 is offered by Riverbank Computing under the
GPL v3 or a commercial license (not under the LGPL). An application distributed to third parties with
PyQt6 under the GPL must be distributed under a license compatible with the GPL v3, with the source code
available. For closed source, the commercial license is required — see the
[Riverbank FAQ](https://www.riverbankcomputing.com/commercial/license-faq). Personal use, study and
internal tools that are not distributed do not trigger these obligations. *This is not legal advice.*

Trademarks and third-party material: see [NOTICE.md](NOTICE.md).

## How to cite

OLIVEIRA, P. S. *Professional Python GUI Development Manual* (MAN-PYQT6-001), Rev. 0. 2026.
Available at: https://github.com/ptksilva18/manual-pyqt6. License CC BY-SA 4.0.

The metadata is in [`CITATION.cff`](CITATION.cff); GitHub shows the "Cite this repository" button.

## Contributing

Found an error, an unclear passage or an example that does not run on your platform? Open an *issue*
stating the operating system, the Python and PyQt6 versions, the edition (English or Portuguese) and the
listing involved.
