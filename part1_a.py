# -*- coding: utf-8 -*-
"""Parte I — Capítulos 1 a 3 (Step 2)."""
from blocks import (ST_BAS, bl, ch, code, fig, flat, h2, h3, h4, img, lst, nl, note, out, p, part,
                    snip, tab)
import outline_data as D

CAP01 = flat(
    ch("Introdução ao PyQt6 e ao ecossistema Qt", ST_BAS, [
        "Entender o que são o Qt e o PyQt6 e como os bindings funcionam.",
        "Conhecer o mapa completo de módulos do PyQt6 6.12 e o estado de cada um.",
        "Identificar as diferenças práticas entre PyQt5, PyQt6 e PySide6.",
    ]),
    h2("Objetivo e público-alvo do manual"),
    p("Este manual ensina a construir **aplicações desktop profissionais** em Python usando o PyQt6. O ponto de "
      "partida é zero: não se exige experiência prévia com interfaces gráficas, apenas noções de programação. "
      "O ponto de chegada é uma aplicação completa — com janela principal, persistência de dados, gráficos, "
      "processamento em segundo plano, testes automatizados e instalador — construída com as mesmas práticas "
      "usadas em ferramentas de engenharia de uso diário."),
    p("O público-alvo inclui engenheiros, cientistas e analistas que já escrevem scripts em Python e precisam "
      "transformá-los em ferramentas com interface gráfica utilizáveis por outras pessoas, além de "
      "desenvolvedores que vêm de outros toolkits (Tkinter, wxPython, PyQt5) e desejam dominar o PyQt6 "
      "com profundidade."),
    p("Três princípios guiam o texto:"),
    bl("**Precisão verificável**: todas as listagens marcadas com ✔ foram executadas com PyQt6 6.12.0 e Qt 6.12.0; "
       "as saídas mostradas nos blocos *Saída* são as saídas reais dessas execuções, e as figuras com janelas são "
       "capturas das próprias listagens.",
       "**Progressão sem saltos**: cada conceito é introduzido antes de ser usado e retomado em contextos mais ricos "
       "nos capítulos seguintes.",
       "**Prática profissional desde o início**: estrutura de projeto, type hints, tratamento de erros e "
       "separação entre interface e lógica aparecem já na Parte I, e não como apêndice."),

    h2("Organização do manual"),
    p("O manual está dividido em cinco Partes, cada uma correspondente a um nível de profundidade, seguidas de "
      "anexos de referência. Cada capítulo abre com um quadro de objetivos e termina com exercícios."),
    h3("Partes, níveis e trilhas de aprendizado"),
    tab("Partes do manual e trilhas de leitura", ["Parte", "Nível", "Pré-requisito", "Para quem"],
        [["I — Fundamentos (Cap. 1–10)", "Básico", "Python básico", "Todos os leitores, em sequência"],
         ["II — Interface profissional (Cap. 11–19)", "Intermediário", "Parte I", "Quem vai construir aplicações reais"],
         ["III — Desenvolvimento avançado (Cap. 20–26)", "Avançado", "Partes I e II", "Escolha os capítulos conforme o projeto"],
         ["IV — Qualidade e distribuição (Cap. 27–30)", "Avançado", "Partes I e II", "Quem vai manter e distribuir software"],
         ["V — Projeto integrador (Cap. 31)", "Consolidação", "Partes I a IV", "Revisão prática de todo o conteúdo"]],
        [3171, 1500, 1700, 2700]),
    p("A **trilha mínima** para produzir uma ferramenta útil é: Capítulos 1 a 10, 11 (Qt Designer), 14 "
      "(Model/View), 20 (concorrência) e 30 (empacotamento). A **trilha completa** percorre todos os capítulos em ordem."),
    h3("Projeto integrador transversal"),
    p("Ao longo do manual, os exemplos convergem para uma mesma aplicação técnica — uma calculadora de "
      "engenharia com registro de ensaios. Na Parte I ela ganha forma: janela mínima (Capítulo 4), formulários "
      "com validação (Capítulos 6 e 7), janela principal com menus, painéis e persistência de estado "
      "(Capítulo 8), diálogos de entrada de dados (Capítulo 9) e tratamento de eventos (Capítulo 10). As Partes "
      "seguintes acrescentam banco de dados, gráficos, threads, testes e instalador, culminando no Capítulo 31."),
    h3("Convenções tipográficas e de código"),
    p("As convenções abaixo são usadas em todo o documento."),
    tab("Convenções tipográficas adotadas no manual", ["Elemento", "Formatação", "Uso"], D.CONVENTIONS, [2600, 2900, 3571]),
    note("NOTA", "Quadros de NOTA trazem informações complementares que não interrompem o raciocínio principal."),
    note("DICA", "Quadros de DICA trazem boas práticas e atalhos de produtividade."),
    note("ATENÇÃO", "Quadros de ATENÇÃO alertam para erros comuns, armadilhas de memória e problemas de portabilidade."),
    p("Nas listagens, as cores seguem o padrão de editores modernos: palavras-chave em azul, textos (*strings*) em "
      "vermelho-escuro, comentários em verde e números em verde-azulado. Trechos curtos sem legenda são "
      "fragmentos ilustrativos; programas completos recebem legenda numerada (Listagem N.M)."),

    h2("O que são o Qt e o PyQt6"),
    p("O **Qt** é um framework multiplataforma escrito em C++ para construir aplicações com interface gráfica e "
      "também serviços sem interface. Ele oferece widgets, gráficos 2D e 3D, rede, banco de dados, multimídia, "
      "internacionalização, threads e muito mais, com o mesmo código-fonte em Windows, macOS e Linux. O "
      "**PyQt6** é o conjunto de *bindings* que expõe essa API ao Python: cada classe C++ do Qt aparece como uma "
      "classe Python com os mesmos nomes de métodos."),
    h3("Breve histórico: Qt, PyQt4, PyQt5, PyQt6 e PySide6"),
    p("O Qt teve sua primeira versão pública em 1995, criada pela norueguesa Trolltech; desde então passou pela "
      "Nokia e hoje é desenvolvido pela The Qt Company, com contribuições da comunidade do Qt Project. A "
      "Riverbank Computing publica o PyQt desde 1998, acompanhando as gerações principais do Qt: PyQt4 (Qt 4), "
      "PyQt5 (Qt 5) e PyQt6 (Qt 6). O Qt 6.0 foi lançado em dezembro de 2020, e o PyQt6 o acompanhou."),
    p("Em paralelo, existe o **PySide**, iniciado pela Nokia em 2009 e hoje mantido pela própria The Qt Company "
      "sob o nome oficial *Qt for Python* (pacote **PySide6** para o Qt 6). PyQt6 e PySide6 cobrem "
      "essencialmente a mesma API do Qt; as diferenças estão no licenciamento e em alguns detalhes de nomes, "
      "discutidos na Seção 1.3.4."),
    h3("Arquitetura dos bindings: SIP, PyQt6-sip e PyQt6-Qt6"),
    p("Os módulos do PyQt6 são extensões compiladas (arquivos `.pyd` no Windows e `.so` no Linux/macOS) geradas "
      "pela ferramenta **SIP**, também da Riverbank. Ao executar `pip install PyQt6`, três pacotes são instalados: "
      "**PyQt6** (os módulos de extensão e as ferramentas `pyuic6` e `pylupdate6`), **PyQt6-sip** (o módulo de "
      "suporte `PyQt6.sip`, que gerencia a correspondência entre objetos Python e C++) e **PyQt6-Qt6** (as "
      "bibliotecas Qt compiladas, incluindo os plugins de plataforma). Não é preciso instalar o Qt separadamente."),
    img("Arquitetura em camadas de uma aplicação PyQt6", "f1_1_arquitetura.png"),
    p("A Figura 1.1 mostra o fluxo em tempo de execução: o código Python chama métodos dos bindings, que chamam "
      "as bibliotecas C++; no sentido inverso, eventos do sistema operacional chegam ao Qt pelo **plugin de "
      "plataforma** e retornam ao Python como chamadas a métodos sobrescritos e a *slots* conectados a sinais."),
    note("NOTA", "Cada objeto Qt criado em Python tem duas partes: o *wrapper* Python e o objeto C++. O Capítulo 5 "
                 "mostra por que essa dualidade importa para o gerenciamento de memória."),
    h3("Licenciamento: GPL v3, licença comercial e implicações de distribuição"),
    p("O PyQt6 é distribuído sob **duas licenças**: GPL v3 e uma licença comercial vendida pela Riverbank Computing. "
      "Pela GPL v3, quem **distribui** uma aplicação que usa o PyQt6 deve distribuí-la também sob licença "
      "compatível com a GPL, disponibilizando o código-fonte aos destinatários. Uso interno sem distribuição a "
      "terceiros não aciona essa obrigação de distribuição. Para software proprietário distribuído, é necessária a "
      "licença comercial do PyQt6."),
    p("O PySide6, por sua vez, está disponível sob LGPL v3 (além de GPL e licença comercial), o que permite "
      "aplicações proprietárias desde que respeitadas as condições da LGPL. O tema é retomado no Capítulo 30, "
      "no contexto do empacotamento."),
    note("IMPORTANTE", "Este manual não constitui aconselhamento jurídico. Antes de distribuir software, consulte o "
                       "texto das licenças e, se necessário, o departamento jurídico da sua organização."),
    h3("PyQt6 versus PySide6"),
    h4("Diferenças de API: pyqtSignal/Signal, pyqtSlot/Slot, pyqtProperty/Property"),
    p("A maior parte do código é idêntica entre os dois bindings, bastando trocar o pacote importado. As diferenças "
      "mais frequentes estão resumidas abaixo."),
    tab("Diferenças frequentes entre PyQt6 e PySide6", ["Recurso", "PyQt6", "PySide6"],
        [["Declaração de sinal", "`pyqtSignal(...)`", "`Signal(...)`"],
         ["Decorador de slot", "`@pyqtSlot(...)`", "`@Slot(...)`"],
         ["Propriedade Qt", "`pyqtProperty(...)`", "`Property(...)`"],
         ["Carga de .ui em tempo de execução", "`uic.loadUi()`", "`QUiLoader` (módulo QtUiTools)"],
         ["Gerador de código a partir de .ui", "`pyuic6`", "`pyside6-uic`"],
         ["Compilador de recursos (.qrc)", "Não incluído", "`pyside6-rcc`"],
         ["Licenças", "GPL v3 ou comercial", "LGPL v3, GPL ou comercial"],
         ["Mantenedor", "Riverbank Computing", "The Qt Company"]],
        [2900, 2900, 3271]),
    h4("Critérios de escolha para projetos profissionais"),
    p("Do ponto de vista técnico, ambos são maduros e acompanham as versões do Qt. A escolha costuma ser decidida "
      "por três fatores: (1) **licença** — distribuição de software proprietário favorece PySide6 (LGPL) ou a "
      "licença comercial do PyQt6; (2) **base de código existente** — projetos e equipes que já usam PyQt5 migram "
      "com menos atrito para PyQt6; (3) **ecossistema** — bibliotecas de terceiros às vezes suportam apenas um dos "
      "bindings. Este manual usa PyQt6, mas os conceitos se aplicam integralmente ao PySide6."),

    h2("Mapa de módulos do PyQt6 6.12"),
    p("A tabela a seguir relaciona todos os módulos de extensão distribuídos nas wheels oficiais do PyQt6 6.12.0 e dos pacotes add-on, "
      "com o pacote `pip` que os fornece e a situação de cada módulo no Qt 6.12. Os capítulos indicados na última coluna tratam de cada módulo."),
    tab("Módulos do PyQt6 6.12 e pacotes add-on", ["Módulo", "Pacote pip", "Finalidade", "Situação", "Cap."],
        D.MODULE_ROWS, [2050, 1500, 3021, 1800, 700], font=16),
    note("NOTA", "QtPdf e QtPdfWidgets constam da documentação de módulos da Riverbank, porém não estão presentes nas wheels "
                 "PyQt6 6.12.0 nem PyQt6-WebEngine 6.140.0 publicadas no PyPI (verificado para Linux, Windows e macOS). "
                 "O tema é tratado no Capítulo 24 com essa ressalva."),
    img("Mapa de módulos do PyQt6 agrupados por domínio", "f1_2_mapa_modulos.png"),
    p("Na prática, a quase totalidade das aplicações desktop usa apenas três módulos — **QtCore**, **QtGui** e "
      "**QtWidgets** —, que são o foco da Parte I. Os demais são incorporados conforme a necessidade do projeto."),

    h2("Principais mudanças de PyQt5 para PyQt6"),
    p("Quem vem do PyQt5 encontrará a mesma arquitetura, mas com mudanças que quebram a compatibilidade de "
      "código-fonte. A tabela resume as mais frequentes."),
    tab("Principais diferenças entre PyQt5 e PyQt6", ["Tema", "PyQt5", "PyQt6"], D.PYQT5_TO_6, [1900, 2900, 4271], font=17),
    h3("Enums com escopo obrigatório"),
    p("No PyQt6, os enums do Qt são enums Python (`enum.Enum` e `enum.Flag`) e precisam ser escritos com o nome "
      "completo: o nome do enum faz parte do caminho. O atalho do PyQt5 deixou de existir."),
    snip('''from PyQt6.QtCore import Qt

rotulo.setAlignment(Qt.AlignmentFlag.AlignCenter)          # PyQt6
# rotulo.setAlignment(Qt.AlignCenter)              # PyQt5: AttributeError no PyQt6
botao = Qt.MouseButton.LeftButton
flags = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter   # combinação de Flag'''),
    note("DICA", "Para descobrir o nome do enum, consulte a assinatura do método nos stubs (`.pyi`) instalados com o "
                 "PyQt6 — o editor mostra o tipo esperado, por exemplo `Qt.AlignmentFlag`."),
    h3("exec() no lugar de exec_()"),
    p("Como `exec` deixou de ser palavra reservada no Python 3, o PyQt6 removeu os aliases `exec_()`. Use "
      "`app.exec()`, `dialogo.exec()` e `menu.exec(...)`."),
    h3("Classes realocadas entre módulos"),
    p("No Qt 6, algumas classes que não dependem de widgets foram movidas de QtWidgets para QtGui: `QAction`, "
      "`QActionGroup`, `QShortcut`, `QUndoCommand`, `QUndoStack`, `QUndoGroup` e `QFileSystemModel`. Do mesmo modo, "
      "`QOpenGLWidget` passou para QtOpenGLWidgets e `QSvgWidget` para QtSvgWidgets. O sintoma típico em código "
      "migrado é um `ImportError` na linha de importação."),
    h3("APIs removidas e seus substitutos"),
    bl("`QDesktopWidget` → `QScreen`, obtido com `QGuiApplication.primaryScreen()` ou `screens()`.",
       "`QRegExp` → `QRegularExpression` (e `QRegExpValidator` → `QRegularExpressionValidator`).",
       "`QFontMetrics.width()` → `QFontMetrics.horizontalAdvance()`.",
       "`event.pos()` em eventos de mouse continua existindo, mas é obsoleto: prefira `event.position()`, que "
       "retorna `QPointF`.",
       "Atributos de High-DPI (`AA_EnableHighDpiScaling`) não são mais necessários: o escalonamento é sempre ativo.",
       "`pyrcc5` não tem equivalente no PyQt6; recursos são tratados no Capítulo 13."),

    h2("Exercícios do capítulo"),
    nl("Liste os três pacotes instalados por `pip install PyQt6` e explique a função de cada um.",
       "Em quais condições a GPL v3 exige que o código-fonte de uma aplicação PyQt6 seja disponibilizado?",
       "Reescreva para PyQt6: `label.setAlignment(Qt.AlignRight | Qt.AlignTop)` e `app.exec_()`.",
       "Usando a Tabela 1.5, identifique o módulo que fornece `QAction` no PyQt6 e explique o motivo da mudança.",
       "Consulte a Tabela 1.4 e indique quais módulos você usaria para uma aplicação que lê uma porta serial, "
       "grava os dados em SQLite e plota gráficos 2D."),
)

CAP02 = flat(
    ch("Preparação do ambiente de desenvolvimento", ST_BAS, [
        "Instalar Python, PyQt6 e add-ons em ambiente virtual isolado.",
        "Configurar IDE, type checking e o Qt Designer.",
        "Organizar um projeto com estrutura profissional e pyproject.toml.",
    ]),
    h2("Requisitos de sistema"),
    h3("Versões de Python suportadas (PyQt6 6.12 requer Python ≥ 3.10)"),
    p("O PyQt6 6.12.0 declara `Requires-Python >= 3.10`. As wheels são do tipo **abi3** (ABI estável do CPython): "
      "uma única wheel atende a todas as versões de Python a partir da 3.10, sem recompilação. Use preferencialmente "
      "uma versão recente e suportada do Python 3 (os exemplos deste manual foram executados com Python 3.13)."),
    h3("Plataformas: Windows, Linux e macOS"),
    tab("Wheels do PyQt6 6.12.0 publicadas no PyPI", ["Sistema", "Arquitetura", "Requisito mínimo da wheel"],
        [["Windows", "x86-64 (win_amd64)", "Windows de 64 bits suportado pelo Qt 6.12"],
         ["Windows", "ARM64 (win_arm64)", "Windows on ARM"],
         ["Linux", "x86-64", "glibc ≥ 2.34 (tag manylinux_2_34)"],
         ["Linux", "ARM64 (aarch64)", "glibc ≥ 2.39 (tag manylinux_2_39)"],
         ["macOS", "universal2 (Intel e Apple Silicon)", "macOS 14 ou superior (tag macosx_14_0)"]],
        [1700, 3200, 4171]),
    p("Em plataformas sem wheel compatível, o `pip` tenta compilar a partir do código-fonte, o que exige o Qt "
      "instalado e um compilador — cenário que deve ser evitado em projetos comuns."),
    note("ATENÇÃO", "Em distribuições Linux mínimas, a aplicação pode falhar ao abrir com a mensagem *Could not load "
                    "the Qt platform plugin \"xcb\"*. A partir do Qt 6.5, o plugin xcb exige a biblioteca "
                    "**xcb-cursor** (pacote `libxcb-cursor0` no Debian/Ubuntu). Execute com a variável de ambiente "
                    "`QT_DEBUG_PLUGINS=1` para ver qual dependência está faltando."),

    h2("Ambientes virtuais e gerenciamento de pacotes"),
    p("Um **ambiente virtual** (venv) é uma cópia isolada do interpretador com seu próprio diretório de pacotes. "
      "Cada projeto deve ter o seu: assim, versões diferentes do PyQt6 convivem na mesma máquina e o "
      "projeto declara exatamente do que depende."),
    h3("Criação e ativação de venv"),
    h4("Windows (PowerShell e cmd)"),
    snip('''# PowerShell, na pasta do projeto
py -3.13 -m venv .venv
.venv\\Scripts\\Activate.ps1          # o prompt passa a exibir (.venv)

# cmd.exe
.venv\\Scripts\\activate.bat

deactivate                            # sai do ambiente virtual''', lang="text"),
    note("DICA", "Se o PowerShell recusar a ativação por política de execução, libere scripts locais para o seu "
                 "usuário com `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`."),
    h4("Linux e macOS"),
    snip('''python3 -m venv .venv                 # Debian/Ubuntu: requer o pacote python3-venv
source .venv/bin/activate
python -c "import sys; print(sys.prefix)"   # deve apontar para .../.venv''', lang="text"),
    h3("Instalação do PyQt6 e dos pacotes add-on"),
    snip('''python -m pip install --upgrade pip
python -m pip install PyQt6                       # núcleo + demais módulos padrão
python -m pip install PyQt6-Charts PyQt6-Graphs   # add-ons: instale apenas o necessário
python -m pip install PyQt6-WebEngine''', lang="text"),
    tab("Pacotes PyQt6 distribuídos pela Riverbank Computing no PyPI",
        ["Pacote pip", "Módulos fornecidos", "Versão verificada"],
        [["PyQt6", "Núcleo: 32 módulos (+ QAxContainer no Windows), uic, lupdate, sip", "6.12.0"],
         ["PyQt6-Charts", "QtCharts", "6.12.0"],
         ["PyQt6-Graphs", "QtGraphs, QtGraphsWidgets", "6.12.0"],
         ["PyQt6-DataVisualization", "QtDataVisualization", "6.12.0"],
         ["PyQt6-3D", "Qt3DAnimation, Qt3DCore, Qt3DExtras, Qt3DInput, Qt3DLogic, Qt3DRender", "6.12.0"],
         ["PyQt6-NetworkAuth", "QtNetworkAuth", "6.12.0"],
         ["PyQt6-WebEngine", "QtWebEngineCore, QtWebEngineQuick, QtWebEngineWidgets", "6.140.0"]],
        [2400, 4971, 1700]),
    note("NOTA", "Use sempre `python -m pip` em vez de `pip`: garante que o pacote será instalado no interpretador "
                 "ativo (o do venv), e não em outro Python que esteja antes no PATH."),
    h3("Fixação de versões e reprodutibilidade (requirements.txt, pip freeze, lock files)"),
    p("O PyQt6 6.12.0 depende de `PyQt6-Qt6 >= 6.12.0, < 6.13.0` e de `PyQt6-sip >= 13.13, < 14`: o pacote de "
      "bindings e o pacote com as bibliotecas Qt devem ter a mesma versão *minor*. Para que todos os "
      "desenvolvedores e o servidor de integração contínua usem exatamente o mesmo ambiente, registre as versões:"),
    snip('''python -m pip freeze > requirements.txt     # registra versões exatas do venv atual
python -m pip install -r requirements.txt    # reproduz o ambiente em outra máquina

# trecho típico de requirements.txt
PyQt6==6.12.0
PyQt6-Qt6==6.12.0
PyQt6-sip==13.13.0''', lang="text"),
    p("Ferramentas de lock (por exemplo, `pip-tools`, `uv` ou `poetry`) automatizam esse processo e também "
      "registram *hashes* dos arquivos, o que reforça a segurança da cadeia de suprimentos."),

    h2("Ferramentas de desenvolvimento"),
    h3("Configuração do VS Code e do PyCharm"),
    p("No **VS Code**, instale a extensão Python (Microsoft) e selecione o interpretador do venv com o comando "
      "*Python: Select Interpreter*; a depuração passa a usar esse ambiente. No **PyCharm**, configure o "
      "interpretador em *Settings → Project → Python Interpreter* apontando para `.venv`. Em ambos, verifique que o "
      "autocompletar mostra os métodos de `QWidget` — sinal de que os stubs do PyQt6 foram encontrados."),
    h3("Type hints e arquivos .pyi do PyQt6 (mypy e pyright)"),
    p("O PyQt6 instala arquivos de stubs (`QtCore.pyi`, `QtWidgets.pyi` etc.) e o marcador `py.typed`. Isso permite "
      "verificação estática de tipos com `mypy` ou `pyright` e autocompletar preciso, inclusive dos nomes de enums. "
      "Anotar as próprias classes (`def __init__(self, parent: QWidget | None = None) -> None`) aproveita esse "
      "recurso e documenta a intenção do código."),
    h3("Obtenção e execução do Qt Designer"),
    p("O **Qt Designer** — editor visual de formulários usado no Capítulo 11 — não faz parte das wheels do PyQt6. "
      "As alternativas mais comuns são: (1) o instalador oficial do Qt, que inclui o Qt Designer e o Qt Creator; "
      "(2) os pacotes da distribuição Linux; (3) o executável `pyside6-designer`, que acompanha o pacote PySide6 — "
      "instale-o em um venv separado para não misturar os bindings. Os arquivos `.ui` produzidos são XML puro e "
      "independem do binding que os carregará."),

    h2("Verificação da instalação"),
    p("O script a seguir confirma as versões do PyQt6 e do Qt e verifica quais pacotes add-on estão presentes."),
    lst("c02_verifica.py", "Script de verificação da instalação do PyQt6 e dos add-ons"),
    out("c02_verifica"),
    p("`PYQT_VERSION_STR` é a versão dos bindings; `QT_VERSION_STR` é a versão do Qt em tempo de execução, e "
      "`QLibraryInfo.version()` é a versão do Qt contra a qual os bindings foram compilados. Divergência entre "
      "elas indica mistura de pacotes de versões diferentes."),

    h2("Estrutura profissional de projeto"),
    h3("Layout de diretórios (src layout)"),
    img("Estrutura de diretórios recomendada para um projeto PyQt6", "f2_1_estrutura.png"),
    p("O **src layout** coloca o pacote dentro de `src/`, o que obriga os testes a importarem o pacote instalado "
      "(e não arquivos soltos da pasta), revelando cedo problemas de empacotamento. A separação em `ui/`, "
      "`models/` e `services/` antecipa a arquitetura do Capítulo 27: cálculos em `services/` não importam Qt e "
      "podem ser testados e reutilizados independentemente da interface."),
    h3("O arquivo pyproject.toml"),
    lst("c02_pyproject.toml", "Modelo de pyproject.toml para aplicação PyQt6", lang="toml"),
    p("A seção `[project.gui-scripts]` cria, na instalação, um executável `calc-engenharia` que chama a função "
      "`main()` do módulo `calc_engenharia.__main__`; no Windows, scripts *gui* são iniciados sem abrir a janela "
      "do console. Com o projeto instalado em modo editável (`python -m pip install -e .[dev]`), as alterações no "
      "código têm efeito imediato. O modelo da Listagem 2.2 foi validado gerando uma wheel com `pip wheel`."),
    snip('''# src/calc_engenharia/__main__.py
import sys


def main() -> int:
    from calc_engenharia.app import executar      # importação tardia
    return executar(sys.argv)


if __name__ == "__main__":                         # permite: python -m calc_engenharia
    sys.exit(main())'''),

    h2("Exercícios do capítulo"),
    nl("Crie um venv, instale o PyQt6 e execute a Listagem 2.1. Anote as versões exibidas.",
       "Gere o `requirements.txt` do seu ambiente e explique por que `PyQt6` e `PyQt6-Qt6` devem ter a mesma versão minor.",
       "Monte a estrutura da Figura 2.1 com o `pyproject.toml` da Listagem 2.2 e instale-o com `pip install -e .`.",
       "Configure o `mypy` no projeto e verifique um arquivo que chame `QLabel.setAlignment` com um argumento inválido."),
)

CAP03 = flat(
    ch("Python essencial para programação de interfaces", ST_BAS, [
        "Revisar os recursos de Python mais usados em código PyQt6.",
        "Dominar classes, herança, callables e decoradores no contexto de GUI.",
        "Aplicar type hints, dataclasses e enum em código de interface.",
    ]),
    p("Este capítulo não é um curso de Python: ele revisa, com exemplos em PyQt6, os recursos da linguagem que "
      "aparecem em praticamente toda aplicação gráfica. Quem já domina orientação a objetos pode ler apenas as "
      "seções 3.1.3, 3.2 e 3.5, que tratam de particularidades do PyQt."),
    h2("Programação orientada a objetos"),
    h3("Classes, instâncias e o método __init__"),
    p("Em PyQt6, praticamente toda janela é uma **classe** que herda de um widget do Qt. O método `__init__` monta "
      "a interface (cria widgets, layouts e conexões) e guarda em atributos (`self.campo`, `self.botao`) os "
      "widgets que precisarão ser acessados depois. Widgets usados apenas na montagem podem ficar em variáveis "
      "locais, pois o Qt os mantém vivos pela relação pai–filho (Capítulo 5)."),
    h3("Herança e super() em subclasses de widgets"),
    p("Ao herdar de uma classe Qt, chame `super().__init__(...)` **antes** de usar qualquer recurso da classe base: "
      "é essa chamada que cria o objeto C++. Por convenção, o último parâmetro do construtor é `parent`, repassado à base."),
    lst("c03_heranca.py", "Herança e super(): uma subclasse de QWidget com parâmetros próprios"),
    out("c03_heranca"),
    p("A ordem de resolução de métodos (MRO) mostra a cadeia: `PainelResultado → PainelTitulado → QWidget → QObject`. "
      "Os métodos do Qt podem ser sobrescritos como quaisquer métodos Python — é assim que se tratam eventos no "
      "Capítulo 10."),
    h3("Herança múltipla, mixins e restrições com QObject"),
    p("Uma classe Python pode herdar de **apenas uma classe Qt**, mas pode combinar quantos *mixins* Python puros "
      "forem necessários. O PyQt6 suporta herança múltipla cooperativa: cada `__init__` deve aceitar e repassar "
      "`*args, **kwargs` para que a cadeia de `super()` alcance a classe Qt."),
    lst("c03_mixin.py", "Mixin Python puro combinado com uma única classe Qt"),
    out("c03_mixin"),
    note("ATENÇÃO", "Herdar de duas classes Qt ao mesmo tempo (por exemplo, `class X(QLabel, QPushButton)`) não é "
                    "suportado. Para combinar comportamentos de widgets, use composição: um widget que contém outros."),
    h3("@property do Python versus pyqtProperty"),
    p("O `@property` do Python cria atributos calculados visíveis apenas ao código Python. Já `pyqtProperty` "
      "registra a propriedade no **sistema de metaobjetos** do Qt, tornando-a acessível por `property()`/"
      "`setProperty()`, por animações (Capítulo 19), pelo QML (Capítulo 26) e por folhas de estilo."),
    lst("c03_property.py", "@property (Python) versus pyqtProperty (visível ao sistema de metaobjetos)"),
    out("c03_property"),
    p("Observe que `setProperty('nivel', 80.0)` passou pelo *setter* e foi limitado à capacidade (50,0), e que o "
      "sinal `nivelChanged` foi emitido nas duas alterações. Já `property('capacidade')` retorna `None`: o "
      "`@property` comum não existe para o Qt."),

    h2("Funções como objetos"),
    h3("Callables, lambdas e closures"),
    p("Conectar um sinal significa entregar ao Qt um **callable**: função, método, `lambda`, objeto com `__call__` ou "
      "`functools.partial`. Lambdas são práticas para adaptar argumentos, mas têm uma armadilha bem conhecida "
      "quando criadas em laços e conectadas a sinais que enviam argumentos, como `clicked(bool)`."),
    lst("c03_lambda.py", "Armadilha clássica: lambda em laço conectado a clicked(bool)"),
    out("c03_lambda"),
    p("Na forma errada, o PyQt passa o argumento `checked` (False) do sinal para o primeiro parâmetro da lambda, "
      "sobrescrevendo o valor *default* `i` — todos os botões registram `False`. A correção é reservar o primeiro "
      "parâmetro para o argumento do sinal (`lambda checked=False, i=i: ...`) ou usar `partial`."),
    h3("functools.partial para passar argumentos a slots"),
    p("`partial(funcao, arg1)` cria um novo callable com argumentos fixados no momento da criação. É mais legível "
      "que uma lambda quando o objetivo é apenas pré-preencher argumentos, e o valor fixado não depende de "
      "variáveis que mudam depois (o problema de *late binding* das closures)."),

    h2("Decoradores"),
    p("Decoradores envolvem uma função para acrescentar comportamento. Em PyQt6, o decorador mais usado é "
      "`@pyqtSlot`, que declara a assinatura C++ do slot. Decoradores próprios — para medir tempo, registrar log "
      "ou tratar erros — podem ser combinados com ele."),
    lst("c03_decorador.py", "Decoradores: um decorador próprio empilhado com @pyqtSlot"),
    out("c03_decorador"),
    note("DICA", "Use sempre `functools.wraps` nos decoradores próprios (preserva nome e metadados da função) e "
                 "mantenha `@pyqtSlot` como o decorador mais externo, para que a declaração do slot seja aplicada "
                 "à função final."),

    h2("Type hints, dataclasses e enum"),
    p("`dataclass` é ideal para os **dados** que a interface exibe e edita (um ensaio, um tubo, um poço); `Enum` "
      "representa conjuntos fechados de opções (materiais, unidades, estados). O `QComboBox` pode guardar, junto "
      "de cada texto, um objeto Python arbitrário no parâmetro `userData` — inclusive um membro de enum."),
    lst("c03_dataclass_enum.py", "dataclass + Enum alimentando um QComboBox (dado associado com userData)"),
    out("c03_dataclass_enum"),
    p("`frozen=True` torna a instância imutável — útil para valores que trafegam entre a interface e a camada de "
      "cálculo sem risco de alteração acidental."),

    h2("Exceções e gerenciadores de contexto"),
    p("Este é um ponto em que o PyQt6 difere do Python comum: uma exceção **não tratada** dentro de um slot ou de "
      "um método chamado pelo Qt faz o PyQt chamar `qFatal()`, o que **encerra o processo** abruptamente. Em "
      "ferramentas de uso diário, isso significa perder o trabalho do usuário. A solução é instalar um "
      "`sys.excepthook` próprio, que o PyQt6 chama no lugar do encerramento."),
    lst("c03_excecoes.py", "Exceções em slots: excepthook global mantém a aplicação viva"),
    out("c03_excecoes"),
    p("Sem a linha `sys.excepthook = tratador_global`, o mesmo programa termina com o *traceback* e o sinal "
      "*Aborted* (código de saída 134 no Linux) — comportamento verificado na mesma versão do PyQt6. Em aplicações "
      "reais, o tratador grava o erro em log e exibe uma mensagem amigável (Capítulo 27)."),
    p("**Gerenciadores de contexto** (`with`) garantem a liberação de recursos mesmo em caso de exceção. Além de "
      "arquivos, várias classes do PyQt6 suportam `with`: `QSignalBlocker` (bloqueia sinais temporariamente, "
      "Capítulo 5) e `QMutexLocker` (trava de thread, Capítulo 20)."),
    snip('''from PyQt6.QtCore import QSignalBlocker

with QSignalBlocker(spin):        # alterações abaixo não emitem valueChanged
    spin.setValue(0.0)
# ao sair do bloco, os sinais voltam a ser emitidos normalmente'''),

    h2("Módulos, pacotes e importações"),
    p("Importe explicitamente as classes que usa — isso deixa claro de qual módulo cada classe vem e evita "
      "conflitos de nomes. Nunca use `from PyQt6.QtWidgets import *`."),
    snip('''# Estilo 1: classes explícitas (o mais comum neste manual)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow

# Estilo 2: módulos (útil quando muitas classes são usadas)
from PyQt6 import QtCore, QtWidgets
janela = QtWidgets.QMainWindow()

# Dentro do próprio pacote (src/calc_engenharia/ui/janela.py)
from ..services.tubos import pressao_barlow     # importação relativa'''),

    h2("Exercícios do capítulo"),
    nl("Crie a classe `PainelAlarme(PainelResultado)` que pinta o valor em vermelho quando ultrapassar um limite.",
       "Modifique a Listagem 3.4 para usar `partial` em vez de lambda e confirme a saída.",
       "Escreva um decorador `@registrar` que imprima os argumentos recebidos por um slot e teste-o com `@pyqtSlot(int)`.",
       "Execute a Listagem 3.7 com a linha do `excepthook` comentada e observe o código de saída do processo.",
       "Crie um `Enum` de unidades de pressão e preencha um `QComboBox` com `userData` contendo o fator de conversão."),
)
