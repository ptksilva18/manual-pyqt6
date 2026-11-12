# Manual Profissional de Python com Interface Gráfica (PyQt6)

**MAN-PYQT6-001 · Rev. 0** — desenvolvimento de aplicações desktop com PyQt6, do zero ao avançado.

[![Código: GPL-3.0-only](https://img.shields.io/badge/c%C3%B3digo-GPL--3.0--only-blue)](LICENSES/GPL-3.0-only.txt)
[![Texto: CC BY-SA 4.0](https://img.shields.io/badge/texto-CC%20BY--SA%204.0-lightgrey)](LICENSES/CC-BY-SA-4.0.txt)
[![REUSE](https://img.shields.io/badge/REUSE-conforme-green)](REUSE.toml)

Um manual didático em português que vai do primeiro `QApplication` até uma aplicação técnica completa,
testada e empacotada. Cada listagem de código foi **executada e verificada**: a saída impressa no
manual é a saída real do programa.

| | |
|---|---|
| Páginas | 408 |
| Listagens de código | 169 (139 executadas diretamente, 24 verificadas por outra listagem, 4 de apoio, 2 só para Windows) |
| Figuras / tabelas | 36 / 99 |
| Versões de referência | Python ≥ 3.10 (testado com 3.13) · PyQt6 6.12.0 · Qt 6.12 LTS |

## Baixar o manual

O PDF e o DOCX ficam na página de **[Releases](https://github.com/ptksilva18/manual-pyqt6/releases/latest)**.

## Conteúdo

- **Parte I — Fundamentos (Cap. 1–10):** ecossistema Qt, ambiente, Python essencial para interfaces,
  primeira aplicação, `QObject`/sinais e slots, widgets, layouts, `QMainWindow`, diálogos e eventos.
- **Parte II — Interface profissional (Cap. 11–19):** Qt Designer, estilos e temas, recursos e
  internacionalização, Model/View, QtSql, arquivos e processos, QPainter/impressão/SVG,
  Graphics View, animações e máquinas de estado.
- **Parte III — Desenvolvimento avançado (Cap. 20–26):** concorrência e asyncio, redes e dispositivos
  (serial, TLS), visualização científica, multimídia, web e ajuda integrada, OpenGL/Vulkan/3D, QML.
- **Parte IV — Qualidade, arquitetura e distribuição (Cap. 27–30):** arquitetura em camadas (MVP/MVVM,
  injeção de dependências, plugins), testes com pytest-qt, desempenho e acessibilidade,
  empacotamento com PyInstaller e cx_Freeze.
- **Parte V — Projeto integrador (Cap. 31):** monitor de ensaios de estanqueidade com SQLite,
  análise em segundo plano, gráfico, relatório PDF, testes e executável.
- **Anexos:** catálogo de classes do PyQt6 6.12 por módulo, namespace `Qt` e enums, Qt Style Sheets,
  ferramentas de linha de comando. Também há referências e glossário.

## Estrutura do repositório

```
data/listings/      código de todas as listagens (cNN_* = Capítulo NN) — ver INDICE.md
data/listings/c30_app/   aplicação de exemplo do Capítulo 30 (empacotamento)
data/listings/c31_app/   projeto integrador do Capítulo 31
data/outputs/       saídas reais capturadas pelo runner.py (impressas no manual)
data/figs/, img/    figuras e capa
runner.py           executa as listagens em modo headless e grava as saídas
build.py, part*.py  gerador do documento Word (ver GERADOR.md)
```

O arquivo [`data/listings/INDICE.md`](data/listings/INDICE.md) relaciona cada número de listagem
ao arquivo correspondente.

## Rodar os exemplos

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt

python data/listings/c04_primeira.py      # abre a primeira janela do Capítulo 4
```

Projeto integrador (Capítulo 31):

```bash
cd data/listings/c31_app
python -m ensaios                  # abre a aplicação
python -m pytest -q                # 13 testes
cd ../../..
python data/listings/c31_entrega.py   # testes + autoteste + PyInstaller + autoteste do executável
```

Para executar **todas** as listagens sem tela (Linux), use `python runner.py` ou
`python runner.py <filtro>` (por exemplo, `python runner.py c21`). Algumas listagens das Partes III e IV
precisam de ferramentas do sistema (Xvfb, socat, dbus); a lista completa está em
[GERADOR.md](GERADOR.md). O certificado de **teste** usado pela Listagem 21.4 é gerado
automaticamente pelo `runner.py` (a chave privada não é versionada).

## Licença

| O quê | Licença |
|---|---|
| Código: listagens, projeto integrador, gerador do documento | [GPL-3.0-only](LICENSES/GPL-3.0-only.txt), a mesma do PyQt6 |
| Texto, figuras, tabelas e saídas de exemplo (manual em PDF/DOCX e arquivos `.md`) | [CC BY-SA 4.0](LICENSES/CC-BY-SA-4.0.txt) |
| Fonte `DejaVuSansMono.ttf` (usada por uma listagem) | [Bitstream Vera](LICENSES/Bitstream-Vera.txt) (alterações DejaVu em domínio público) |

As listagens impressas no manual também são GPL-3.0-only. O detalhamento arquivo a arquivo está em
[`REUSE.toml`](REUSE.toml), no padrão [REUSE](https://reuse.software/).

**Se você for distribuir uma aplicação feita com PyQt6:** o PyQt6 é oferecido pela Riverbank Computing
sob GPL v3 ou licença comercial (não sob LGPL). Uma aplicação distribuída a terceiros com o PyQt6 sob
GPL precisa ser distribuída sob licença compatível com a GPL v3, com o código-fonte disponível. Para
código fechado, é necessária a licença comercial — veja o
[FAQ da Riverbank](https://www.riverbankcomputing.com/commercial/license-faq). Uso pessoal, estudo
e ferramentas internas não distribuídas não disparam essas obrigações. *Isto não é aconselhamento
jurídico.*

Marcas e materiais de terceiros: ver [AVISOS.md](AVISOS.md).

## Como citar

OLIVEIRA, P. S. *Manual Profissional de Python com Interface Gráfica* (MAN-PYQT6-001), Rev. 0. 2026.
Disponível em: https://github.com/ptksilva18/manual-pyqt6. Licença CC BY-SA 4.0.

Os metadados estão em [`CITATION.cff`](CITATION.cff); o GitHub mostra o botão “Cite this repository”.

## Contribuições

Encontrou um erro, um trecho pouco claro ou um exemplo que não roda na sua plataforma? Abra uma
*issue* informando o sistema, a versão do Python e do PyQt6 e a listagem envolvida.
