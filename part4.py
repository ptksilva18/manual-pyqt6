# -*- coding: utf-8 -*-
"""Parte IV — Capítulos 27 a 30 (Step 4)."""
from blocks import ST_AVA, bl, ch, flat, h2, h3, img, lst, nl, note, out, p, part, snip, tab

CAP27 = flat(
    ch("Arquitetura de aplicações PyQt6", ST_AVA, [
        "Separar interface, lógica de aplicação e domínio.",
        "Aplicar padrões MVC, MVP e MVVM com PyQt6.",
        "Implementar desfazer/refazer e extensibilidade por plugins.",
    ]),
    h2("Camadas e separação de responsabilidades"),
    p("Aplicações técnicas vivem muitos anos e sobrevivem a várias interfaces. O que garante essa longevidade "
      "é a separação em camadas, com dependências apontando sempre para dentro: a interface depende da lógica, "
      "nunca o contrário. O **domínio** — cálculos, regras de aceitação, unidades — é Python puro, sem `import` "
      "do PyQt6, e pode ser testado, reutilizado em scripts e validado contra planilhas e normas de forma "
      "independente."),
    img("Arquitetura em camadas recomendada", "f27_1_camadas.png", 15.0),
    bl("**Views**: widgets, arquivos `.ui` e QML. Exibem e capturam; não calculam nem acessam arquivos.",
       "**Presenters/ViewModels**: estado e comportamento da tela; traduzem entre a view e os serviços.",
       "**Serviços de aplicação**: casos de uso (\"registrar ensaio\", \"gerar relatório\"), threads, undo.",
       "**Domínio**: entidades e funções puras; a parte mais estável e mais testada do sistema.",
       "**Infraestrutura**: banco de dados, arquivos, rede, instrumentos — atrás de interfaces substituíveis."),

    h2("Padrões de apresentação: MVC, MVP e MVVM"),
    p("Os três padrões separam a interface da lógica; diferem em quem conhece quem. No **MVC** clássico, o "
      "controlador recebe a entrada e atualiza o modelo, e a view observa o modelo — no Qt, a arquitetura "
      "Model/View (Capítulo 14) funde view e controlador. No **MVP**, a view é passiva e expõe uma interface "
      "mínima; o *presenter* lê os valores, chama o domínio e manda a view exibir o resultado. Como o "
      "presenter conversa com um `Protocol`, ele pode ser testado com uma view falsa, sem `QApplication`."),
    lst("c27_mvp.py", "MVP: domínio puro, presenter e duas views (widget e falsa)"),
    out("c27_mvp"),
    p("No **MVVM**, o *ViewModel* expõe propriedades observáveis (`pyqtProperty` com `notify`) e a view se "
      "liga a elas. É o modelo natural do QML (Capítulo 26) e funciona bem com Widgets quando a ligação é "
      "encapsulada em uma função. A Listagem 27.2 mostra um detalhe que separa protótipos de produtos: ao "
      "atualizar o widget a partir do ViewModel, os sinais do widget são bloqueados (`QSignalBlocker`); sem "
      "isso, o valor arredondado pelo widget (3 casas) voltaria ao ViewModel, e a conversão bar ↔ psi "
      "acumularia erro a cada ida e volta."),
    lst("c27_mvvm.py", "MVVM: ViewModel com propriedades notificáveis e ligação bidirecional"),
    out("c27_mvvm"),

    h2("Injeção de dependências e configuração"),
    p("Um serviço que cria suas próprias dependências (`self.repo = RepositorioSQLite(...)`) fica preso a "
      "elas. Com **injeção de dependências**, ele as recebe prontas no construtor, e um único ponto — a "
      "**raiz de composição** — decide as implementações concretas a partir da configuração. Em Python não é "
      "preciso um *framework*: construtores, `Protocol` e uma função `compor()` bastam. A configuração vem de "
      "um arquivo TOML (lido com `tomllib`, da biblioteca padrão) e pode ser sobreposta por variáveis de "
      "ambiente, útil em servidores e testes."),
    lst("c27_config.toml", "Arquivo de configuração TOML da aplicação", lang="text",
        nota="✔ Lido pela Listagem 27.4 (executada e verificada)."),
    lst("c27_di.py", "Injeção de dependências: configuração tipada, raiz de composição e repositórios"),
    out("c27_di"),
    p("O limite de 0,3 % veio da variável de ambiente `ENSAIOS_LIMITES__QUEDA_ADMISSIVEL_PCT`, definida no "
      "teste, e não do arquivo (0,5 %). O mesmo `ServicoEnsaios` funcionou com os dois repositórios sem "
      "nenhuma alteração. Preferências do **usuário** (geometria de janelas, últimos arquivos) continuam no "
      "`QSettings` (Capítulo 13); a configuração da **aplicação** (backends, limites, endereços) fica no "
      "arquivo versionado."),

    h2("Command pattern: QUndoStack, QUndoCommand e QUndoView"),
    p("Desfazer/refazer confiável exige que toda alteração do documento passe por um **comando** que saiba "
      "executar-se (`redo()`) e reverter-se (`undo()`). `QUndoStack.push()` executa o comando e o empilha; "
      "`id()` e `mergeWith()` fundem edições sucessivas (girar um `QDial` não deve gerar cem passos); "
      "`beginMacro()`/`endMacro()` agrupam comandos; `setClean()`/`isClean()` marcam o ponto salvo, para "
      "perguntar \"salvar alterações?\" apenas quando necessário."),
    lst("c27_undo.py", "QUndoStack: comandos, fusão, macros, estado limpo e QUndoView"),
    out("c27_undo"),
    p("As três edições de PT-101 viraram um único comando; desfazer a macro restaurou as duas pressões de uma "
      "vez e devolveu a pilha ao estado limpo. `createUndoAction()`/`createRedoAction()` criam `QAction`s cujo "
      "texto e habilitação acompanham a pilha — prontas para o menu Editar. `QUndoGroup` coordena pilhas de "
      "vários documentos abertos."),
    note("ATENÇÃO", "No PyQt6, `QUndoStack`, `QUndoCommand` e `QUndoGroup` estão em `QtGui`; apenas "
                    "`QUndoView` permanece em `QtWidgets` (Tabela 1.5)."),

    h2("Plugins e extensibilidade com importlib"),
    p("Plugins permitem que equipes acrescentem funções — exportadores, cálculos específicos de um cliente, "
      "drivers de instrumentos — sem alterar o núcleo. Os ingredientes são: **descoberta** (arquivos em uma "
      "pasta, via `importlib.util`, ou pacotes instalados que declaram *entry points*, via "
      "`importlib.metadata`), um **contrato** versionado (`VERSAO_API`, função `registrar`) e uma **fachada** "
      "estável (`AppAPI`) que expõe só o que o plugin pode usar."),
    lst("plugins_demo/conversor_unidades.py", "Plugin de exemplo (pasta plugins_demo)",
        nota="✔ Carregado e executado pela Listagem 27.7 (executada e verificada)."),
    lst("c27_plugins.py", "Descoberta, validação de versão e isolamento de plugins"),
    out("c27_plugins"),
    p("Um pacote instalável registra seus plugins no `pyproject.toml`, na seção "
      "`[project.entry-points.\"manual_pyqt6.plugins\"]`, com linhas do tipo `conversor = meu_pacote.plugin`. "
      "Lembre que carregar um plugin **executa código**: aceite apenas plugins de origem confiável."),

    h2("Tratamento global de exceções (sys.excepthook) e relatórios de erro"),
    p("Como visto no Capítulo 3, uma exceção não tratada em um slot encerra o processo quando "
      "`sys.excepthook` é o padrão. Um gancho próprio transforma o erro em registro (*log*) e em mensagem ao "
      "usuário, com detalhes copiáveis para o suporte, e a aplicação continua. Exceções em threads Python "
      "passam por `threading.excepthook` (Python 3.8+)."),
    lst("c27_excecoes.py", "sys.excepthook e threading.excepthook com relatório de erro"),
    out("c27_excecoes"),
    note("ATENÇÃO", "Se a caixa de erro for a única janela aberta, fechá-la dispara `quitOnLastWindowClosed` e "
                    "encerra a aplicação — foi o que ocorreu na primeira versão desta listagem, antes de a janela "
                    "principal ser criada. Em aplicações reais a janela principal existe, mas o detalhe importa "
                    "em ferramentas de linha de comando e em testes."),

    h2("Exercícios do capítulo"),
    nl("Escreva testes `pytest` para o `Apresentador` da Listagem 27.1 usando apenas a `VisaoFalsa`.",
       "Acrescente ao ViewModel da Listagem 27.2 a unidade kPa, sem alterar a view além de um novo campo.",
       "Implemente um repositório em arquivo JSON e selecione-o pela configuração TOML.",
       "Torne undoable a inserção e a remoção de linhas em um `QAbstractTableModel` (Capítulo 14).",
       "Empacote um plugin como pacote instalável e descubra-o por *entry point*."),
)

CAP28 = flat(
    ch("Testes automatizados", ST_AVA, [
        "Testar widgets, sinais e modelos de forma automatizada.",
        "Usar QtTest e pytest-qt.",
        "Executar testes de GUI em integração contínua sem tela.",
    ]),
    h2("Estratégia de testes para aplicações de GUI"),
    p("Testes de interface são mais lentos e mais frágeis que testes de funções puras. A arquitetura do "
      "Capítulo 27 permite distribuí-los como uma pirâmide: muitos testes do **domínio** (milissegundos, sem "
      "Qt), um número moderado de testes de **presenters, ViewModels e modelos** (com Qt, sem janelas "
      "visíveis) e poucos testes de **interface** que simulam o usuário nos fluxos críticos."),
    tab("Ferramentas de teste e o que cada uma verifica", ["Ferramenta", "Uso principal", "Execução"],
        [["pytest (ou unittest)", "Domínio, serviços, regras de aceitação", "Sem Qt"],
         ["QAbstractItemModelTester", "Contrato de modelos Model/View", "QtTest, sem janelas"],
         ["QSignalSpy", "Sinais emitidos e seus argumentos", "QtTest"],
         ["QTest", "Teclado, mouse, esperas e janelas expostas", "QtTest, com widgets"],
         ["pytest-qt (qtbot)", "Tudo acima com fixtures pytest e esperas por sinal", "pytest"],
         ["Comparação de imagens", "Regressão visual de widgets desenhados", "Referência versionada"]],
        [2700, 3900, 2471]),
    lst("c28_calculadora.py", "Widget sob teste: calculadora de pressão hidrostática"),
    out("c28_calculadora"),

    h2("QtTest: QTest, QSignalSpy e QAbstractItemModelTester"),
    p("O módulo `QtTest` traz as mesmas ferramentas usadas nos testes do próprio Qt. Com `unittest` da "
      "biblioteca padrão, elas dispensam qualquer dependência externa:"),
    bl("`QTest.keyClicks()`, `keyClick()`, `mouseClick()` e afins geram eventos reais, que passam por "
       "validadores, atalhos e filtros de eventos — diferente de chamar `setText()`.",
       "`QSignalSpy(sinal)` registra cada emissão como uma lista de argumentos; `wait(ms)` aguarda a próxima "
       "emissão rodando o event loop.",
       "`QAbstractItemModelTester` verifica continuamente se o modelo respeita o contrato do Qt "
       "(índices, contagens, sinais de inserção e remoção) enquanto o teste o manipula."),
    lst("c28_qtest.py", "QtTest com unittest: teclado, mouse, QSignalSpy e QAbstractItemModelTester"),
    out("c28_qtest"),

    h2("pytest-qt e a fixture qtbot"),
    p("O plugin **pytest-qt** (licença MIT) integra o Qt ao pytest: cria a `QApplication` uma única vez, "
      "oferece a fixture `qtbot` e captura exceções ocorridas em slots durante o teste, que de outra forma "
      "passariam despercebidas. `qtbot.addWidget()` registra widgets para destruição automática; "
      "`waitSignal()` e `assertNotEmitted()` verificam sinais com prazo; `waitUntil()` repete uma condição até "
      "ela ser verdadeira — a forma correta de esperar, em vez de `time.sleep()`."),
    lst("c28_test_calculadora.py", "Testes com pytest-qt: qtbot, waitSignal, assertNotEmitted e parametrização"),
    out("c28_test_calculadora"),
    p("Um teste parametrizado falhou na primeira execução: o valor esperado para 500 m havia sido calculado "
      "à mão como 51,51 bar, quando o correto é 51,52 bar (50,504 + 1,013). É exatamente o tipo de erro que "
      "testes automatizados existem para revelar — inclusive nos próprios testes."),

    h2("Simulação de mouse e teclado"),
    bl("Para botões, prefira `mouseClick(botao, Qt.MouseButton.LeftButton)`; `botao.click()` não exercita "
       "o caminho de eventos e, portanto, testa menos.",
       "`keyClicks()` respeita validadores: no teste `test_validador_bloqueia_texto`, as letras foram "
       "recusadas pelo `QDoubleValidator` — comportamento que um `setText()` não revelaria.",
       "Atalhos e teclas especiais: `keyClick(widget, Qt.Key.Key_S, Qt.KeyboardModifier.ControlModifier)`.",
       "Arrastar-e-soltar e gestos exigem `mousePress`/`mouseMove`/`mouseRelease` com coordenadas; mantenha "
       "esses testes em pequeno número.",
       "Diálogos modais bloqueiam o teste: injete o diálogo (Capítulo 27) ou feche-o com um `QTimer` criado "
       "antes de `exec()`."),

    h2("Integração contínua headless (QT_QPA_PLATFORM=offscreen)"),
    p("Servidores de integração contínua não têm tela. A plataforma `offscreen` do Qt cria janelas apenas "
      "em memória e é suficiente para a grande maioria dos testes de widgets; para OpenGL, Qt Quick 3D ou "
      "QtGraphs 3D, use um servidor X virtual (Xvfb), como neste manual. No Linux, as wheels do PyQt6 dependem "
      "de bibliotecas do sistema (EGL, OpenGL, xkbcommon, fontconfig, D-Bus — conferidas com `ldd` na "
      "biblioteca `libQt6Gui`), que precisam estar instaladas na imagem do servidor."),
    lst("c28_ci.yml", "GitHub Actions: matriz de sistemas e versões do Python com testes headless",
        lang="text", nota="✔ Sintaxe YAML validada com parser; comandos equivalentes aos executados neste "
                          "capítulo."),

    h2("Cobertura e testes de regressão visual"),
    p("O **pytest-cov** mede quais linhas e ramos (`--cov-branch`) foram executados. A cobertura não prova "
      "correção, mas aponta código nunca exercitado. No relatório abaixo, as linhas ausentes (coluna Missing) são o "
      "bloco de demonstração `if __name__ == \"__main__\"` — exclua-o da medição com `# pragma: no cover` ou com a "
      "configuração `exclude_also` do coverage."),
    lst("c28_cobertura.py", "Execução da suíte com pytest-cov, como em integração contínua"),
    out("c28_cobertura"),
    p("Testes de **regressão visual** comparam a renderização de um widget com uma imagem de referência "
      "aprovada. Para que sejam reprodutíveis, fixe estilo (`Fusion`), fonte, tamanho e fator de escala, e "
      "use tolerância por canal para absorver diferenças de antisserrilhamento. Diferenças de fontes entre "
      "sistemas operacionais são inevitáveis: mantenha referências por plataforma ou rode esses testes em uma "
      "única imagem de servidor."),
    lst("c28_regressao_visual.py", "Regressão visual: comparação com imagem de referência"),
    out("c28_regressao_visual"),

    h2("Exercícios do capítulo"),
    nl("Escreva com pytest-qt os testes do formulário MVP da Listagem 27.1.",
       "Aplique `QAbstractItemModelTester` ao modelo hierárquico do Capítulo 14.",
       "Configure o coverage para excluir blocos `__main__` e atingir 100 % no módulo da calculadora.",
       "Crie um teste de regressão visual para o manômetro do Capítulo 17 com referência versionada.",
       "Adapte o fluxo de CI para executar os testes de QtGraphs 3D sob Xvfb no Linux."),
)

CAP29 = flat(
    ch("Desempenho, depuração e acessibilidade", ST_AVA, [
        "Medir e eliminar gargalos de pintura, modelos e I/O.",
        "Depurar problemas típicos de PyQt6, incluindo objetos C++ destruídos.",
        "Tornar a aplicação acessível a todos os usuários.",
    ]),
    h2("Medição de desempenho (cProfile, QElapsedTimer)"),
    p("Otimize apenas o que foi medido. `QElapsedTimer` (resolução de nanossegundos) mede trechos "
      "específicos; o `cProfile`, da biblioteca padrão, mostra quantas vezes cada função Python foi chamada e "
      "quanto tempo consumiu. Em interfaces, o suspeito habitual é `data()` de modelos, chamado milhares de "
      "vezes a cada pintura."),
    lst("c29_desempenho.py", "cProfile e QElapsedTimer: modelo lento versus modelo com cache"),
    out("c29_desempenho"),

    h2("Otimização de modelos, visões e pintura"),
    bl("**Modelos**: responda só aos papéis usados, devolva constantes pré-construídas e evite formatação e "
       "cálculo em `data()`; o cache da listagem custou da ordem de 100 ms uma única vez para economizar em todas as pinturas. "
       "Para tabelas enormes, carregue sob demanda com `canFetchMore()`/`fetchMore()`.",
       "**Notificações**: prefira `beginResetModel()`/`endResetModel()` ou inserções em bloco a milhares de "
       "`beginInsertRows()` de uma linha; emita `dataChanged` só para o intervalo alterado e com a lista de "
       "papéis.",
       "**Visões**: altura de linha fixa (`QHeaderView.ResizeMode.Fixed`) e larguras definidas evitam medir "
       "conteúdo; `resizeColumnsToContents()` mede até `resizeContentsPrecision()` linhas (1000 por padrão); "
       "em `QListView`, `setUniformItemSizes(True)`.",
       "**Pintura**: em `paintEvent()`, desenhe apenas a região de `event.rect()`, reutilize `QPen`, `QFont` e "
       "`QPainterPath`, e guarde desenhos estáticos em `QPixmap` (ou use `QPixmapCache`).",
       "**Graphics View**: `setItemIndexMethod()`, `ItemCoordinateCache` em itens complexos e "
       "`setViewportUpdateMode()` adequado ao padrão de atualização.",
       "**E/S e cálculo**: sempre fora da thread da GUI (Capítulo 20)."),

    h2("Depuração"),
    h3("Mensagens do Qt: qDebug, qWarning e QLoggingCategory"),
    p("O próprio Qt informa erros de uso por mensagens de aviso — conexões impossíveis, layouts duplicados, "
      "plugins ausentes. `qInstallMessageHandler()` intercepta todas, com tipo e **categoria**, e permite "
      "encaminhá-las ao `logging` do Python (Capítulo 13). `QLoggingCategory` organiza as mensagens da "
      "aplicação em categorias hierárquicas que podem ser ligadas e desligadas por regras, sem alterar o "
      "código."),
    lst("c29_depuracao.py", "QLoggingCategory, regras de filtro, manipulador de mensagens e QT_DEBUG_PLUGINS"),
    out("c29_depuracao"),
    note("ATENÇÃO", "O construtor C++ de `QLoggingCategory` guarda apenas o ponteiro para o nome. No teste, "
                    "uma categoria criada com `str` temporária ignorou as regras de filtro; criada a partir de "
                    "um objeto `bytes` mantido em variável de módulo (como na Listagem 29.2), obedeceu."),
    h3("Variáveis de ambiente de diagnóstico (QT_DEBUG_PLUGINS, QT_LOGGING_RULES)"),
    tab("Variáveis de ambiente úteis para diagnóstico", ["Variável", "Efeito"],
        [["QT_DEBUG_PLUGINS=1", "Detalha a busca e a carga de plugins (plataforma, imagens, SQL...)"],
         ["QT_LOGGING_RULES", "Regras de categorias, p.ex. \"qt.qpa.*=true;app.io.debug=false\""],
         ["QT_MESSAGE_PATTERN", "Formato das mensagens, p.ex. \"%{time} %{category} %{message}\""],
         ["QT_FATAL_WARNINGS=1", "Transforma avisos em falha imediata — útil em testes"],
         ["QT_QPA_PLATFORM", "Plataforma: windows, cocoa, xcb, wayland, offscreen..."],
         ["QT_SCALE_FACTOR", "Fator de escala global (testes de High-DPI, Capítulo 12)"],
         ["QSG_INFO=1", "Informações do grafo de cena do Qt Quick (backend, API gráfica)"],
         ["PYTHONFAULTHANDLER=1", "Ativa o faulthandler do Python sem alterar o código"]],
        [2700, 6371]),
    h3("faulthandler e falhas em código nativo"),
    p("Uma falha de segmentação em código C++ encerra o processo sem *traceback* Python. O módulo "
      "`faulthandler` (ou `python -X faulthandler`) imprime a pilha Python de todas as threads no momento da "
      "falha, indicando a linha que chamou o código nativo — primeiro passo para isolar o problema. Ao longo "
      "deste manual, falhas desse tipo foram documentadas em `QRangeModel` (Capítulo 14), no backend de "
      "áudio e na ordem de destruição do `QAudioEngine` (Capítulo 23)."),

    h2("Gerenciamento de memória: armadilhas entre Python e C++ (sip.isdeleted)"),
    p("Cada objeto Qt tem duas partes: o objeto C++ e o *wrapper* Python. A posse define quem destrói quem: "
      "objetos com pai são destruídos pelo pai (Capítulo 5); objetos sem pai são destruídos quando o wrapper "
      "Python é coletado. As armadilhas da Listagem 29.3 são as mais frequentes:"),
    lst("c29_memoria.py", "Objetos C++ destruídos, temporários, objetos sem referência e faulthandler"),
    out("c29_memoria"),
    bl("**Objeto destruído pelo pai**: o wrapper continua existindo e qualquer uso gera `RuntimeError: wrapped "
       "C/C++ object ... has been deleted`. `sip.isdeleted(obj)` permite testar antes de usar.",
       "**Temporário**: em `QTableView().horizontalHeader()`, a tabela é coletada ao fim da expressão e leva "
       "o cabeçalho junto — o erro apareceu de verdade durante a elaboração da Listagem 29.1.",
       "**Janela sem referência**: criada dentro de uma função e não guardada, desaparece ao retornar. Guarde "
       "a referência (atributo) ou dê um pai.",
       "**Conexões com lambdas** mantêm vivos os objetos capturados; desconecte ou use `functools.partial` "
       "com cuidado em objetos de vida curta.",
       "`deleteLater()` adia a destruição para o event loop — a forma segura de destruir um objeto dentro de "
       "um slot dele mesmo."),

    h2("Acessibilidade"),
    p("Acessibilidade é requisito legal em muitos contextos e beneficia todos os usuários: operação "
      "completa pelo teclado, compatibilidade com leitores de tela e legibilidade sob qualquer condição de "
      "iluminação. O Qt expõe a árvore de widgets às tecnologias assistivas do sistema (UI Automation no "
      "Windows, NSAccessibility no macOS, AT-SPI no Linux)."),
    lst("c29_acessibilidade.py", "Nomes acessíveis, buddies, ordem de tabulação, contraste e preferências"),
    out("c29_acessibilidade"),
    h3("Nomes e descrições acessíveis"),
    p("Leitores de tela anunciam o nome e a função de cada controle. Botões e rótulos com texto já têm nome; "
      "campos e controles gráficos precisam de `setAccessibleName()` e, quando útil, de "
      "`setAccessibleDescription()`. `QLabel.setBuddy()` associa o rótulo ao campo e cria o atalho com `&` "
      "(Alt+T para \"&Tag\")."),
    h3("Navegação por teclado e ordem de tabulação"),
    p("Toda função deve ser alcançável pelo teclado. Defina a ordem de tabulação com `QWidget.setTabOrder()` "
      "(ou no Designer, Capítulo 11), use `focusPolicy` adequada e ofereça atalhos (`QKeySequence`) para as "
      "ações frequentes. A listagem percorre a cadeia de foco com as mesmas regras da tecla Tab."),
    h3("Contraste, tamanho de fonte e QAccessibilityHints"),
    p("As diretrizes WCAG 2.x exigem contraste mínimo de 4,5:1 para texto normal (nível AA). A função "
      "`contraste()` da listagem implementa a fórmula da luminância relativa: o cinza `#999999` sobre branco "
      "(2,85:1) reprova; `#595959` (7,00:1) aprova. Use tamanhos de fonte em pontos — escaláveis com o DPI — e "
      "não fixe alturas de widgets que contêm texto. `QStyleHints.accessibility()` (Qt 6.10+) devolve um "
      "`QAccessibilityHints` com as preferências de contraste e de movimento do sistema, e sinais para reagir "
      "quando mudam."),

    h2("Exercícios do capítulo"),
    nl("Perfile a abertura de um CSV de 100 000 linhas em `QTableView` e otimize até ficar abaixo de 1 s.",
       "Encaminhe todas as mensagens do Qt para o `logging` com categoria e arquivo de origem.",
       "Escreva um utilitário que liste os widgets de uma janela sem `accessibleName` nem texto visível.",
       "Implemente um tema de alto contraste ativado quando `contrastPreference()` indicar `HighContrast`."),
)

CAP30 = flat(
    ch("Empacotamento e distribuição", ST_AVA, [
        "Gerar executáveis independentes para Windows, Linux e macOS.",
        "Incluir plugins Qt, recursos e traduções corretamente.",
        "Produzir instaladores e respeitar as obrigações de licença.",
    ]),
    h2("Visão geral das ferramentas de empacotamento"),
    p("O usuário final não deve precisar instalar Python nem PyQt6. As ferramentas de empacotamento reúnem "
      "o interpretador, o código, as bibliotecas Qt, os plugins (plataforma, estilos, formatos de imagem, "
      "SQL) e os dados da aplicação. Nenhuma faz compilação cruzada: gere o pacote do Windows no Windows, o "
      "do macOS no macOS e o do Linux na distribuição mais antiga que pretende suportar."),
    tab("Ferramentas de empacotamento para aplicações PyQt6", ["Ferramenta", "Abordagem", "Plataformas", "Observações"],
        [["PyInstaller", "Congela interpretador + dependências", "Windows, Linux, macOS",
          "A mais usada; hooks próprios para PyQt6; modos onedir e onefile (6.22.3 testada neste capítulo)"],
         ["Nuitka", "Compila Python para C e congela", "Windows, Linux, macOS",
          "Requer compilador C; o plugin pyqt6 avisa que o suporte ao PyQt6 não é perfeito (threads do Qt) e "
          "recomenda PySide6"],
         ["cx_Freeze", "Congela interpretador + dependências", "Windows, Linux, macOS",
          "Hooks para PyQt6; gera MSI, DMG e AppImage pelos comandos bdist_* (8.7.4 testada)"],
         ["pyqtdeploy (Riverbank)", "Implantação estática, incl. móvel", "Desktop e móvel",
          "Até a versão 3.3.0, suporta apenas Qt 5/PyQt5: não é opção para PyQt6"]],
        [2000, 2500, 1800, 2771], font=16),

    h2("PyInstaller"),
    h3("Arquivo .spec, modo onedir e onefile"),
    p("O PyInstaller analisa os `import`s a partir do script principal e reúne o necessário. O comando "
      "`pyinstaller app.py` gera um arquivo `.spec` — um script Python que descreve o pacote e que deve ser "
      "versionado e editado para os ajustes finos. No modo **onedir** (padrão), o resultado é uma pasta com o "
      "executável e as dependências em `_internal`; no modo **onefile** (`--onefile`), um único executável "
      "que se descompacta em uma pasta temporária a cada execução — mais prático de distribuir, porém com "
      "partida mais lenta. Para instaladores, prefira onedir."),
    lst("c30_app/app_ensaios.py", "Aplicação a empacotar: recursos, tema, tradução e autoteste",
        nota="✔ Empacotada e executada pela Listagem 30.3 (executada e verificada)."),
    lst("c30_app/app_ensaios.spec", "Arquivo .spec do PyInstaller (onedir, dados e exclusões)",
        nota="✔ Usado pela Listagem 30.3 (executada e verificada)."),
    lst("c30_empacotar.py", "Empacotamento com PyInstaller e execução do resultado congelado"),
    out("c30_empacotar"),
    h3("Inclusão de dados, plugins e traduções"),
    bl("**Dados**: declare em `datas` no `.spec` (ou `--add-data origem:destino`) e localize-os em tempo de "
       "execução a partir de `sys._MEIPASS`, como a função `recurso()` da Listagem 30.1 — que também "
       "funciona com o código-fonte não empacotado.",
       "**Plugins e traduções do Qt**: os hooks do PyInstaller para PyQt6 incluem plugins e traduções; a "
       "saída confirma as pastas `plugins` e `translations` e a tradução `qtbase_pt_BR` funcionando no "
       "executável congelado (\"Cancelar\").",
       "**Tamanho**: o pacote de teste ocupou cerca de 235 MB porque inclui todas as bibliotecas Qt que o hook "
       "considera possíveis. Use `excludes` para módulos não usados (WebEngine sozinho ocupa centenas de "
       "megabytes) e confira o resultado executando o autoteste.",
       "**Janela de console**: no Windows e no macOS, use `console=False` no `.spec` (ou `--windowed`) para "
       "aplicações gráficas."),
    note("DICA", "Inclua no executável uma opção de autoteste, como `--autoteste` na Listagem 30.1, e rode-a "
                 "no servidor de integração contínua logo após o empacotamento: plugins ausentes e dados "
                 "esquecidos aparecem antes de chegar ao usuário."),

    h2("Nuitka"),
    p("O Nuitka traduz o código Python para C e o compila, com o modo `--standalone` (pasta) ou `--onefile`. "
      "Exige um compilador C (MSVC, MinGW, GCC ou Clang) e builds mais longos; em troca, oferece partida "
      "rápida e código mais difícil de inspecionar. Para PyQt6, o plugin `pyqt6` informa que o suporte não é "
      "perfeito — por exemplo, threads do Qt — e recomenda PySide6; teste a aplicação compilada com cuidado "
      "antes de adotá-lo."),
    snip(["python -m nuitka --standalone --enable-plugin=pyqt6 \\",
          "    --include-data-dir=recursos=recursos \\",
          "    --windows-console-mode=disable app_ensaios.py"], lang="text"),

    h2("cx_Freeze"),
    p("O cx_Freeze congela a aplicação de forma semelhante ao PyInstaller e se integra ao `setuptools`. Seus "
      "comandos `bdist_msi` (Windows), `bdist_dmg`/`bdist_mac` (macOS) e `bdist_appimage` (Linux) geram "
      "diretamente os formatos de distribuição."),
    snip(["cxfreeze --script app_ensaios.py --target-name app_ensaios \\",
          "    build_exe --include-files=recursos"], lang="text"),
    p("O comando acima foi executado com o cx_Freeze 8.7.4 sobre a aplicação da Listagem 30.1: o "
      "executável gerado passou no autoteste (tema, plugins e tradução). Note que `--include-files` é opção "
      "do subcomando `build_exe`, e que o cx_Freeze coloca os dados ao lado do executável — daí o segundo "
      "ramo da função `recurso()`."),

    h2("Instaladores: Inno Setup, MSI, DMG e AppImage"),
    bl("**Windows**: o Inno Setup (gratuito) gera instaladores `.exe` a partir de um script; para MSI — "
       "exigido por muitas áreas de TI para distribuição centralizada — use o WiX Toolset ou o `bdist_msi` do "
       "cx_Freeze.",
       "**macOS**: distribua o pacote `.app` dentro de uma imagem `.dmg` (`hdiutil create` ou a ferramenta "
       "`create-dmg`), assinado e notarizado.",
       "**Linux**: AppImage (um arquivo executável, sem instalação) com `appimagetool`/`linuxdeploy`, ou "
       "pacotes Flatpak; pacotes `.deb`/`.rpm` para distribuições específicas."),
    lst("c30_instalador.iss", "Script do Inno Setup para a pasta gerada pelo PyInstaller", lang="text",
        allow_long=True, nota="⚠ Não executado no ambiente de teste (Linux): requer Inno Setup 6.3+ no "
                              "Windows. As diretivas seguem a documentação oficial do Inno Setup."),

    h2("Assinatura de código e notarização"),
    p("Executáveis sem assinatura disparam alertas do Windows SmartScreen e são bloqueados pelo Gatekeeper do "
      "macOS. A assinatura exige um certificado de assinatura de código emitido por autoridade certificadora "
      "(Windows) ou uma conta Apple Developer (macOS):"),
    snip(["# Windows (Windows SDK): assinatura com carimbo de tempo",
          "signtool sign /fd SHA256 /tr http://timestamp.digicert.com /td SHA256 /a app_ensaios.exe",
          "",
          "# macOS: assinatura com hardened runtime, notarização e grampeamento",
          "codesign --force --options runtime --timestamp \\",
          "    --sign \"Developer ID Application: Empresa (TEAMID)\" MonitorEnsaios.app",
          "xcrun notarytool submit MonitorEnsaios.dmg --keychain-profile perfil --wait",
          "xcrun stapler staple MonitorEnsaios.dmg"], lang="text"),
    p("Assine primeiro as bibliotecas internas e por último o executável e o pacote; o carimbo de tempo "
      "mantém a assinatura válida após o vencimento do certificado."),

    h2("Licenciamento na distribuição (GPL v3 versus comercial)"),
    p("O PyQt6 é distribuído pela Riverbank Computing sob **GPL v3** ou sob **licença comercial** da "
      "Riverbank. Os pontos práticos, sem substituir a orientação do departamento jurídico:"),
    bl("Ao **distribuir** uma aplicação que usa o PyQt6 sob GPL v3, a aplicação inteira deve ser licenciada "
       "sob termos compatíveis com a GPL v3, e o código-fonte deve ser oferecido a quem recebe o programa. "
       "Isso independe de as bibliotecas Qt estarem sob LGPL.",
       "Para distribuir aplicações de código fechado, é necessária a licença comercial do PyQt (que cobre "
       "também PyQt-Charts, PyQt-Graphs, PyQt-NetworkAuth etc.), usada com o Qt sob LGPL ou sob licença "
       "comercial da Qt.",
       "Alguns módulos Qt — entre eles Qt Charts, Qt Data Visualization, Qt Graphs e Qt Network "
       "Authentication — não estão disponíveis sob LGPL, apenas GPL v3 ou comercial.",
       "O pacote distribuído contém componentes de terceiros com licenças próprias: FFmpeg (LGPL, Capítulo "
       "23), OpenSSL, Chromium (WebEngine) e as bibliotecas Python usadas. Inclua os textos de licença e os "
       "avisos exigidos.",
       "Em geral, as obrigações da GPL são acionadas pela distribuição a terceiros; o uso interno de uma "
       "ferramenta sem distribuí-la tem outro tratamento. Confirme o enquadramento do seu caso com o "
       "jurídico."),
    note("ATENÇÃO", "Este manual não constitui orientação jurídica. Verifique os termos vigentes nas páginas "
                    "de licenciamento da Riverbank Computing e da The Qt Company antes de distribuir qualquer "
                    "software."),

    h2("Exercícios do capítulo"),
    nl("Gere a versão onefile da Listagem 30.3 e compare o tempo de partida com a versão onedir.",
       "Reduza o tamanho do pacote excluindo módulos não usados e confirme com o autoteste.",
       "Crie o instalador do Inno Setup no Windows e teste instalação, atalho e desinstalação.",
       "Monte um fluxo de CI que empacote, execute o autoteste e publique os artefatos por plataforma.",
       "Liste as licenças de todos os componentes incluídos no pacote gerado."),
)

PART4 = flat(
    part("IV", "QUALIDADE, ARQUITETURA E DISTRIBUIÇÃO", "Do código que funciona ao produto que se mantém",
         ST_AVA, "Capítulos 27 a 30 · Nível Avançado"),
    CAP27, CAP28, CAP29, CAP30,
)
