# -*- coding: utf-8 -*-
"""
Estrutura (outline) do manual MAN-PYQT6-001.

Cada bloco e um dict com a chave 'k' (tipo). Tipos:
  part   - divisor de Parte (pagina propria)
  h      - titulo numerado (nivel 1..4); nivel 1 = capitulo
  hu     - titulo nivel 1 nao numerado (Prefacio, Referencias, Glossario)
  ha     - titulo de Anexo (nivel 1..3), numeracao A, A.1, A.1.1
  p      - paragrafo de corpo (suporta **negrito**, *italico*, `codigo`)
  obj    - quadro "Objetivos do capitulo"
  bl     - lista com marcadores
  fig    - figura (placeholder) + legenda
  tab    - tabela + legenda
  code   - listagem de codigo + legenda
  note   - quadro de destaque (NOTA / DICA / ATENCAO / IMPORTANTE)
  catalog- tabelas automaticas do Anexo A (catalogo de classes)

Os passos (steps) do plano de trabalho:
  1 = estrutura (esta revisao) | 2 = Basico | 3 = Intermediario
  4 = Avancado | 5 = consolidacao / emissao final
"""

from blocks import *  # noqa: F401,F403
from blocks import _D, STEP_NAME, ST_BAS, ST_INT, ST_AVA, ST_FIN, TBD  # noqa: F401

# O conteudo vem dos modulos do idioma ativo (raiz = pt; en/ = en, ver i18n.py e build.py)
from front import ANNEXES, CATALOG_GROUPS, FRONT_UNNUMBERED  # noqa: E402,F401
import part1 as P1  # noqa: E402
import part2 as P2  # noqa: E402
import part3 as P3  # noqa: E402
import part4 as P4  # noqa: E402
import part5 as P5  # noqa: E402

BODY = flat(
    P1.PART1,
    P2.PART2,
    P3.PART3,
    P4.PART4,
    P5.PART5,
)
