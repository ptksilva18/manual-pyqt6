# Gerador do MAN-PYQT6-001 (Rev. 0)

O manual é gerado a partir deste repositório: `build.py` monta o OOXML (Word) diretamente, lendo o
texto dos módulos `part*.py`/`anexo_b.py`, o código de `data/listings/` e as saídas reais de
`data/outputs/`. Nenhuma saída é digitada à mão: todas vêm do `runner.py`.

## Requisitos

- Python ≥ 3.10 (testado com 3.13) e os pacotes de [`requirements.txt`](requirements.txt).
- LibreOffice (`soffice`) para o PDF de auditoria e Poppler (`pdftotext`, `pdfinfo`).
- Fontes DejaVu (`fonts-dejavu-core`) para diagramas e capturas.

Ferramentas de sistema usadas pelas listagens das Partes III e IV (Ubuntu 24.04):

```
apt: xvfb mesa-vulkan-drivers socat dbus dbus-x11 qt6-documentation-tools openssl libxcb-cursor0
```

- Xvfb :99 + plataforma xcb para OpenGL/RHI (QtGraphs, Qt Quick 3D, QOpenGLWidget, Vulkan);
- `socat` cria o par de portas seriais virtuais (opção `serial` do runner);
- `dbus-run-session` isola o barramento D-Bus (opção `dbus` do runner);
- `openssl` gera o certificado de teste da Listagem 21.4 (automático no `runner.py`).

Resultados de uso único já incluídos em `data/`:

- `pyside6-lrelease` (PySide6-Essentials 6.12.0): `data/listings/c13_calceng_pt_BR.qm`;
- Qt Designer sob Xvfb: `data/figs/raw_designer_xvfb.png`;
- `qhelpgenerator` (Qt 6.4, Ubuntu): `data/listings/resources/ajuda/manual.qch`.

## Fluxo

```bash
python runner.py                 # executa todas as listagens (opções na 1a linha "# runner: ...")
python shots2.py                 # capturas das Partes I e II (inclui shots.py)
python shots3.py                 # capturas das Partes III a V (xcb/offscreen, 2x)
python diagrams.py && python diagrams2.py
./run_pass.sh p1                 # 1a passada: build/p1.docx + PDF de auditoria
python pages.py build/p1_audit.pdf build/p1_audit.docx.meta.json build/pag.json
./run_pass.sh p2 build/pag.json  # 2a passada; repita (pages.py + run_pass.sh) até 0 divergências
```

`run_pass.sh` gera dois arquivos:

- `build/<nome>.docx` — versão para Word, com legendas por campo (no Word: Ctrl+A e F9 para atualizar);
- `build/<nome>_audit.docx/.pdf` — legendas estáticas, renderizado pelo LibreOffice; é deste PDF que
  saem os números de página do sumário e das listas, e é ele o PDF publicado.

Use a variável `SOFFICE` se o executável do LibreOffice não estiver no `PATH`.

Opções de cada listagem (primeira linha `# runner: ...`): `ticks=N`, `timeout=N`, `xcb`, `dbus`,
`serial`, `env=K:V` — detalhes no cabeçalho de [`runner.py`](runner.py).
