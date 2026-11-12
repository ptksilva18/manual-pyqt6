# Gerador do MAN-PYQT6-001 (Rev. 0)

O manual é gerado a partir deste repositório: `build.py` monta o OOXML (Word) diretamente, lendo o
texto dos módulos `part*.py`/`anexo_b.py`, o código de `data/listings/` e as saídas reais de
`data/outputs/`. Nenhuma saída é digitada à mão: todas vêm do `runner.py`.

A variável `MANUAL_LANG` escolhe a edição: `pt` (padrão) ou `en`. Com `MANUAL_LANG=en`, o texto vem de
`en/*.py` (mesmos nomes de módulo, com precedência no `sys.path`) e os dados de `en/data/`; os textos
fixos do documento (legendas, sumário, capa) ficam em `i18n.py`. Em inglês, veja [GENERATOR.md](GENERATOR.md).

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
- `qhelpgenerator` (Qt 6.4, Ubuntu): `data/listings/resources/ajuda/manual.qch` e
  `en/data/listings/resources/help/manual.qch`;
- edição em inglês: `en/data/listings/c13_engcalc_pt_BR.qm` e `en/data/figs/raw_designer_xvfb.png`.

## Fluxo

```bash
python runner.py                 # executa todas as listagens (opções na 1a linha "# runner: ...")
python shots2.py                 # capturas das Partes I e II (inclui shots.py)
python shots3.py                 # capturas das Partes III e IV (xcb/offscreen, 2x)
python shots4.py                 # Figuras 31.2 e 31.3 (janela e relatório do projeto integrador)
python diagrams.py && python diagrams2.py
python listings_index.py --check build/p2.docx.meta.json   # data/listings/INDICE.md
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

## Edição em inglês

O mesmo fluxo, com `MANUAL_LANG=en` e os scripts de figuras de `en/`:

```bash
export MANUAL_LANG=en
python runner.py
python en/shots2.py && python en/shots3.py && python en/shots4.py
python en/diagrams.py && python en/diagrams2.py
./run_pass.sh e1 && python pages.py build/e1_audit.pdf build/e1_audit.docx.meta.json build/pag_en.json
./run_pass.sh e2 build/pag_en.json   # repita até 0 divergências
python listings_index.py --check build/e2.docx.meta.json   # en/data/listings/INDEX.md
```

No inglês, o `runner.py` usa a variável `SERIAL_PORT` (em vez de `PORTA_SERIAL`) e o certificado
`server.crt`/`server.key` (em vez de `servidor.*`).
