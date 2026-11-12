# -*- coding: utf-8 -*-
"""Parte I — Capítulos 8 a 10 (Step 2)."""
from blocks import ST_BAS, bl, ch, flat, h2, h3, img, lst, nl, note, out, p, snip, tab

CAP08 = flat(
    ch("Janela principal: QMainWindow", ST_BAS, [
        "Construir a estrutura completa de uma janela principal.",
        "Criar ações reutilizáveis em menus, barras de ferramentas e atalhos.",
        "Persistir geometria e estado da janela entre sessões.",
    ]),
    p("Este capítulo é construído em torno de uma única listagem — um diário de ensaios com todas as áreas da "
      "janela principal. Cada seção comenta um trecho dela."),
    lst("c08_janela_principal.py", "Janela principal completa: ações, menus, barra de ferramentas, docks e QSettings"),
    out("c08_janela_principal"),

    h2("Anatomia da QMainWindow"),
    p("A `QMainWindow` possui um layout próprio, com regiões reservadas. Por isso, **não se instala um layout "
      "nela**: o conteúdo vai para o widget central (`setCentralWidget`), e os demais elementos são adicionados "
      "pelos métodos específicos."),
    img("Áreas da QMainWindow", "f8_1_mainwindow.png"),
    p("A Figura 8.1 é a captura da Listagem 8.1. As barras de menus e de status são criadas sob demanda na primeira "
      "chamada a `menuBar()` e `statusBar()`."),

    h2("Ações: QAction e QActionGroup"),
    p("Uma **ação** representa um comando do usuário independentemente de onde ele aparece. A mesma `QAction` "
      "pode estar no menu, na barra de ferramentas e em um menu de contexto: texto, ícone, atalho, estado "
      "habilitado e estado marcado ficam sincronizados em todos os lugares. O sinal principal é `triggered(bool)`."),
    h3("Texto, ícone, tooltip e status tip"),
    p("O `&` no texto define a tecla de acesso no menu (Alt+N para `&Novo`). Na Listagem 8.1, os ícones vêm de "
      "`QStyle.standardIcon()`, disponível em qualquer plataforma; em aplicações reais, use ícones próprios em SVG "
      "ou, no Qt 6.7 ou superior, os ícones de tema por `QIcon.fromTheme(QIcon.ThemeIcon.DocumentOpen)`. O "
      "`statusTip` aparece na barra de status quando o mouse passa sobre a ação."),
    h3("Atalhos com QKeySequence e QShortcut"),
    p("Prefira `QKeySequence.StandardKey` (`New`, `Open`, `Save`, `Copy`, `Undo`…): o Qt traduz para o atalho "
      "convencional de cada plataforma (Ctrl+S no Windows/Linux, ⌘S no macOS). Para atalhos sem ação visível, "
      "use `QShortcut(QKeySequence(\"Ctrl+Shift+D\"), self, self.depurar)`."),
    h3("Ações checáveis e grupos exclusivos"),
    p("Com `checkable=True`, a ação mantém um estado ligado/desligado e emite `toggled(bool)` — como *Quebra de "
      "linha*. Um `QActionGroup` (exclusivo por padrão) faz um conjunto de ações checáveis se comportar como botões "
      "de rádio, e seu sinal `triggered(QAction)` informa qual foi escolhida — como o submenu *Unidades*."),

    h2("Menus: QMenuBar e QMenu"),
    h3("Submenus e separadores"),
    p("`menuBar().addMenu(\"&Arquivo\")` cria um menu; `addAction`/`addActions` insere ações; `addSeparator()` "
      "agrupa visualmente; `menu.addMenu(...)` cria submenus. O menu *Painéis* recebe a `toggleViewAction()` de "
      "cada dock: uma ação pronta, checável, que mostra e oculta o painel."),
    h3("Menus de contexto"),
    p("Há duas formas de oferecer menu de contexto (clique direito): definir `ContextMenuPolicy.ActionsContextMenu` "
      "e adicionar ações ao widget, ou — mais flexível — `CustomContextMenu` e tratar o sinal "
      "`customContextMenuRequested(QPoint)`, montando um `QMenu` conforme o item clicado. A posição recebida está "
      "nas coordenadas do widget e precisa ser convertida para coordenadas globais (`mapToGlobal`) antes de "
      "`menu.exec()`."),

    h2("Barras de ferramentas: QToolBar"),
    p("`QToolBar` exibe ações como botões. Pode ser movida pelo usuário entre as áreas permitidas "
      "(`setAllowedAreas`), desanexada (`setFloatable`) e fixada (`setMovable(False)`). `setToolButtonStyle()` "
      "escolhe entre só ícone, só texto ou ambos. Toda barra deve ter `objectName` para que `saveState()` "
      "consiga gravar sua posição."),

    h2("Barra de status: QStatusBar"),
    p("Mensagens temporárias são exibidas com `showMessage(texto, ms)`. Widgets permanentes "
      "(`addPermanentWidget`) ficam à direita e não são cobertos por mensagens — como o contador de linhas da "
      "listagem. `addWidget` insere widgets normais à esquerda."),

    h2("Painéis acopláveis: QDockWidget"),
    p("Docks são painéis que o usuário pode mover entre as bordas da janela, empilhar em abas, desanexar como "
      "janelas flutuantes ou fechar. `setAllowedAreas()` restringe as bordas permitidas; `setFeatures()` controla "
      "se pode ser movido, fechado ou flutuar; `setDockOptions()` da janela habilita aninhamento e abas "
      "(`AllowNestedDocks`, `AllowTabbedDocks`). Como as barras, cada dock precisa de `objectName`."),

    h2("Widget central, abas e MDI"),
    h3("QTabWidget como área central"),
    p("Um `QTabWidget` como widget central é o arranjo típico de aplicações com vários documentos. Na listagem, "
      "`documentMode=True` dá aparência mais limpa e `tabsClosable=True` mostra o botão de fechar, cujo sinal "
      "`tabCloseRequested(int)` é conectado a `removeTab`."),
    h3("QMdiArea e QMdiSubWindow"),
    p("A alternativa clássica é a interface de múltiplos documentos (MDI): `QMdiArea` como widget central e cada "
      "documento em uma `QMdiSubWindow`, com janelas internas que podem ser lado a lado (`tileSubWindows`) ou em "
      "cascata (`cascadeSubWindows`). Útil quando o usuário precisa comparar documentos lado a lado."),
    snip('''from PyQt6.QtWidgets import QMdiArea, QTextEdit

area = QMdiArea()
self.setCentralWidget(area)
sub = area.addSubWindow(QTextEdit())
sub.setWindowTitle("Ensaio 1")
sub.show()
area.tileSubWindows()'''),

    h2("Persistência de estado com QSettings"),
    p("`QSettings` grava pares chave–valor no local padrão de cada plataforma: Registro do Windows, arquivos `.plist` "
      "no macOS e arquivos INI em `~/.config` no Linux. O par organização/aplicação identifica o conjunto de "
      "configurações. A Listagem 8.1 grava em `closeEvent` e restaura no construtor, e a saída comprova o ciclo: "
      "na primeira abertura não há estado; após fechar, a segunda abertura restaura geometria e estado."),
    h3("saveGeometry() e restoreGeometry()"),
    p("Gravam tamanho, posição, estado maximizado e tela da janela. `restoreGeometry()` ajusta a janela caso a tela "
      "original não exista mais (por exemplo, um monitor desconectado)."),
    h3("saveState() e restoreState()"),
    p("Gravam a disposição de barras de ferramentas e docks. O parâmetro opcional `version` permite descartar "
      "estados salvos por versões antigas da interface, quando a estrutura de docks muda."),
    note("ATENÇÃO", "Sem `objectName` em cada `QToolBar` e `QDockWidget`, o Qt emite um aviso e não consegue "
                    "restaurar a posição desses elementos."),

    h2("Tela de abertura: QSplashScreen"),
    p("Aplicações que demoram a iniciar devem mostrar uma tela de abertura. `showMessage()` exibe o andamento, "
      "`app.processEvents()` mantém a tela atualizada durante o trabalho síncrono, e `finish(janela)` fecha a splash "
      "quando a janela principal aparece."),
    lst("c08_splash.py", "QSplashScreen durante a inicialização"),
    out("c08_splash"),

    h2("Exercícios do capítulo"),
    nl("Acrescente à Listagem 8.1 a ação *Abrir* (`StandardKey.Open`) com um `QFileDialog` e um menu *Ajuda → Sobre*.",
       "Crie um segundo dock com um `QTextEdit` de observações e permita empilhá-lo em abas com o primeiro.",
       "Grave em `QSettings` o sistema de unidades escolhido no `QActionGroup` e restaure-o na abertura.",
       "Substitua o `QTabWidget` central por uma `QMdiArea` e adicione ações para organizar as subjanelas."),
)

CAP09 = flat(
    ch("Diálogos", ST_BAS, [
        "Distinguir diálogos modais e não modais.",
        "Usar os diálogos padrão do Qt.",
        "Criar diálogos e assistentes personalizados com validação.",
    ]),
    h2("QDialog: modal e não modal"),
    p("Um **diálogo** é uma janela secundária para uma tarefa curta: confirmar, escolher, preencher dados. "
      "**Modal** é o diálogo que bloqueia a interação com as outras janelas até ser fechado; **não modal** convive "
      "com a janela principal (por exemplo, uma caixa *Localizar*)."),
    h3("exec(), open() e show()"),
    tab("Formas de exibir um QDialog", ["Método", "Modalidade", "Retorno"],
        [["exec()", "Modal à aplicação; inicia um event loop local", "Bloqueia o código até fechar e retorna o código de resultado"],
         ["open()", "Modal à janela pai (window modal)", "Retorna imediatamente; o resultado chega pelo sinal finished(int)"],
         ["show()", "Não modal (por padrão)", "Retorna imediatamente; o diálogo convive com a janela principal"]],
        [1600, 3471, 4000]),
    p("`exec()` é o mais simples de usar, pois o código continua apenas depois da resposta. `open()` é preferível "
      "em aplicações com várias janelas: não cria um event loop aninhado e, no macOS, exibe o diálogo como "
      "*sheet* preso à janela pai."),
    h3("accept(), reject() e o código de resultado"),
    p("`accept()` fecha o diálogo com resultado `QDialog.DialogCode.Accepted` (1) e `reject()` com `Rejected` (0); "
      "a tecla Esc e o botão de fechar chamam `reject()`. Os sinais `accepted`, `rejected` e `finished(int)` "
      "notificam o fechamento."),

    h2("QMessageBox"),
    p("Caixa de mensagem padrão para informar, avisar, confirmar ou relatar erros."),
    lst("c09_messagebox.py", "QMessageBox: métodos estáticos e caixa personalizada"),
    out("c09_messagebox"),
    h3("Métodos estáticos: information, question, warning, critical, about"),
    p("Os métodos estáticos criam, exibem e destroem a caixa em uma linha, retornando o botão escolhido "
      "(`QMessageBox.StandardButton`). Em operações destrutivas, defina como padrão a opção **segura** "
      "(`defaultButton=No`), para que um Enter acidental não apague dados. Fechar a caixa com Esc equivale ao botão "
      "de escape — na listagem, `No`."),
    h3("Botões padrão e personalizados"),
    p("Para controle total, crie a instância: texto principal, texto informativo, ícone, texto detalhado "
      "(expansível) e botões padrão ou personalizados (`addButton(texto, papel)`). A Listagem 9.1 simula o clique "
      "em *Discard* com um `QTimer` apenas para que o exemplo rode sem intervenção."),
    note("NOTA", "Os textos dos botões padrão (OK, Cancel, Save…) e dos diálogos do Qt aparecem em inglês até que "
                 "as traduções do próprio Qt sejam carregadas com `QTranslator` — tema do Capítulo 13. A Figura 9.1 "
                 "mostra os diálogos sem tradução."),

    h2("Diálogos padrão"),
    img("Diálogos padrão do Qt", "f9_1_dialogos.png", width_cm=15.0),
    h3("QFileDialog"),
    p("Seleção de arquivos e pastas. Os métodos estáticos `getOpenFileName`, `getOpenFileNames`, "
      "`getSaveFileName` e `getExistingDirectory` retornam uma tupla `(caminho, filtro_escolhido)` — caminho vazio "
      "se o usuário cancelar. Por padrão, o Qt usa o diálogo **nativo** do sistema; a opção `DontUseNativeDialog` "
      "força o diálogo do próprio Qt (Figura 9.1), que pode ser personalizado."),
    snip('''caminho, _ = QFileDialog.getOpenFileName(
    self, "Abrir ensaio", str(Path.home()), "Ensaios (*.json *.csv);;Todos (*)")
if caminho:                      # string vazia = cancelado
    self.carregar(Path(caminho))'''),
    h3("QColorDialog e QFontDialog"),
    p("`QColorDialog.getColor(inicial, parent)` retorna um `QColor` (verifique `isValid()`, falso se cancelado). "
      "`QFontDialog.getFont(inicial, parent)` retorna a tupla `(QFont, ok)`."),
    h3("QInputDialog"),
    p("Coleta um único valor: `getText`, `getInt`, `getDouble`, `getItem` (lista) e `getMultiLineText`. Todos "
      "retornam `(valor, ok)`; `getDouble` aceita mínimo, máximo, casas decimais e passo."),
    h3("QProgressDialog"),
    p("Mostra o andamento de uma operação longa com botão de cancelamento. `setMinimumDuration(ms)` evita exibir o "
      "diálogo em operações rápidas; `wasCanceled()` informa se o usuário cancelou. Com `autoReset` ativo (padrão), "
      "ao atingir o máximo o diálogo é reiniciado e `value()` volta a −1 — comportamento visível na saída da "
      "Listagem 9.2."),
    lst("c09_padrao.py", "Diálogos padrão: QInputDialog, QProgressDialog e QFileDialog (não nativo)"),
    out("c09_padrao"),
    note("ATENÇÃO", "O laço da Listagem 9.2 chama `processEvents()` para manter o diálogo responsivo, mas o trabalho "
                    "continua na thread da interface. Para tarefas realmente longas, use uma thread de trabalho "
                    "(Capítulo 20) e atualize o progresso por sinais."),
    h3("QErrorMessage"),
    p("Diálogo de erro com a caixa *Mostrar esta mensagem novamente*: mensagens que o usuário optou por ocultar não "
      "voltam a aparecer durante a sessão. Útil para avisos repetitivos e não críticos."),

    h2("Diálogos personalizados"),
    h3("Composição com QDialogButtonBox"),
    p("Um diálogo próprio é uma subclasse de `QDialog` com um layout de campos e uma `QDialogButtonBox`, cujos "
      "sinais `accepted` e `rejected` são ligados a `accept()` e `reject()`. Depois de `exec()`, o chamador lê os "
      "dados por um método do diálogo — de preferência retornando um objeto de dados (`dataclass`), e não os widgets."),
    lst("c09_dialogo.py", "Diálogo personalizado com QDialogButtonBox e validação antes de accept()"),
    out("c09_dialogo"),
    h3("Validação de dados antes de accept()"),
    p("Reimplementar `accept()` é a forma mais robusta de validar: o diálogo só fecha com dados válidos, "
      "independentemente de como o usuário confirmou (botão, Enter). Na listagem, a primeira tentativa sem tag "
      "mantém o diálogo aberto e exibe a mensagem; a segunda, válida, fecha e entrega o objeto `Ensaio`. Uma "
      "alternativa complementar é desabilitar o botão OK enquanto o formulário estiver incompleto."),

    h2("Assistentes: QWizard e QWizardPage"),
    p("`QWizard` conduz o usuário por uma sequência de páginas (`QWizardPage`) com botões Voltar/Avançar/Concluir. "
      "`registerField(\"nome*\", widget)` registra um campo acessível em todas as páginas por `field(\"nome\")`; o "
      "asterisco torna o campo obrigatório, desabilitando *Avançar* enquanto estiver vazio. `initializePage()` é "
      "chamado ao entrar em cada página — o lugar para montar resumos."),
    lst("c09_wizard.py", "QWizard com campos registrados (registerField) e páginas encadeadas"),
    out("c09_wizard"),

    h2("Exercícios do capítulo"),
    nl("Crie um diálogo *Preferências* com `QDialogButtonBox` (OK, Cancelar, Aplicar) que só aplique as mudanças ao clicar OK ou Aplicar.",
       "Modifique a Listagem 9.3 para desabilitar o OK enquanto a tag estiver vazia, sem reimplementar `accept()`.",
       "Use `QFileDialog.getSaveFileName` para salvar o resultado do diálogo de ensaio em JSON.",
       "Acrescente ao assistente da Listagem 9.4 uma página condicional exibida apenas quando as unidades forem *Imperial* (`nextId()`)."),
)

CAP10 = flat(
    ch("Eventos", ST_BAS, [
        "Entender como eventos são gerados, despachados e propagados.",
        "Reimplementar manipuladores de eventos e instalar filtros.",
        "Implementar arrastar-e-soltar e uso da área de transferência.",
    ]),
    h2("O sistema de eventos"),
    p("Sinais informam que *algo aconteceu em um objeto*; **eventos** são a matéria-prima de baixo nível de onde "
      "esses sinais nascem: um clique é um `QMouseEvent` entregue ao botão, que, ao tratá-lo, emite `clicked`. "
      "Tratar eventos diretamente é necessário quando se cria um widget próprio, quando se quer alterar o "
      "comportamento padrão de um widget ou reagir a algo para o qual não existe sinal."),
    h3("QEvent e tipos de evento"),
    p("Todo evento é um objeto de uma subclasse de `QEvent` com um tipo (`QEvent.Type`): `MouseButtonPress`, "
      "`KeyPress`, `Resize`, `Paint`, `Close`, `FocusIn`, `Timer`… São produzidos pelo sistema operacional (via "
      "plugin de plataforma), pelo próprio Qt (timers, repintura) ou pela aplicação (`postEvent`, `sendEvent`)."),
    h3("Propagação, accept() e ignore()"),
    p("Cada evento tem uma marca de aceitação. Eventos de entrada (mouse, teclado, roda) que um widget **ignora** "
      "são reenviados ao widget pai, subindo pela árvore até que alguém os aceite. Ao sobrescrever um manipulador, "
      "chame a implementação da classe base para o que não tratar — ela decide corretamente sobre aceitar ou "
      "propagar."),
    img("Caminho de um evento desde o sistema operacional até o widget", "f10_1_eventos.png"),

    h2("Reimplementação de manipuladores"),
    p("Cada tipo de evento tem um método virtual em `QWidget` que pode ser sobrescrito. A Listagem 10.1 implementa "
      "vários deles e usa o módulo `QtTest` para gerar eventos reais de mouse e teclado — a mesma técnica dos "
      "testes automatizados do Capítulo 28."),
    lst("c10_manipuladores.py", "Reimplementação de manipuladores de eventos (mouse, teclado, janela)"),
    out("c10_manipuladores"),
    h3("Mouse: mousePressEvent, mouseMoveEvent, mouseReleaseEvent, wheelEvent"),
    p("`event.position()` retorna a posição em coordenadas do widget como `QPointF` (use `globalPosition()` para "
      "coordenadas de tela); `button()` indica o botão que causou o evento e `buttons()` todos os botões "
      "pressionados no momento. Por padrão, `mouseMoveEvent` só é recebido com algum botão pressionado; para "
      "receber movimentos livres, ative `setMouseTracking(True)`. `wheelEvent` informa a rotação em "
      "`angleDelta()` (unidades de 1/8 de grau; um passo típico vale 120)."),
    h3("Teclado: keyPressEvent e keyReleaseEvent"),
    p("Somente o widget com **foco** recebe eventos de teclado; widgets próprios precisam de `setFocusPolicy()`. "
      "`event.key()` retorna um `Qt.Key`, `event.modifiers()` as teclas modificadoras e `event.text()` o texto "
      "gerado. Teclas não tratadas devem ser repassadas a `super().keyPressEvent(e)`, para que atalhos e navegação "
      "continuem funcionando."),
    h3("Janela: resizeEvent, moveEvent, showEvent e closeEvent"),
    p("`resizeEvent` informa tamanho antigo e novo (o primeiro, antes de a janela ser exibida, tem tamanho antigo "
      "inválido −1×−1, como na saída). `closeEvent` é o ponto para confirmar o fechamento: `event.ignore()` mantém "
      "a janela aberta e faz `close()` retornar `False`."),
    h3("Foco e hover: focusInEvent, enterEvent e leaveEvent"),
    p("`focusInEvent`/`focusOutEvent` acompanham o foco do teclado (útil para validar ao sair do campo). `enterEvent` "
      "(que no Qt 6 recebe um `QEnterEvent`, com posição) e `leaveEvent` acompanham a entrada e saída do cursor, "
      "base para efeitos de *hover* em widgets próprios."),

    h2("Filtros de eventos: installEventFilter()"),
    p("Um **filtro de eventos** é um objeto que intercepta os eventos destinados a outro, antes que este os receba, "
      "sem necessidade de subclasse. `eventFilter(obj, ev)` retorna `True` para **consumir** o evento ou `False` "
      "para deixá-lo seguir. Um mesmo filtro pode observar vários objetos, e um filtro instalado na própria "
      "`QApplication` vê todos os eventos de todos os objetos (use com parcimônia, pelo custo)."),
    lst("c10_filtro.py", "Filtro de eventos: um objeto observa e intercepta eventos de outro"),
    out("c10_filtro"),
    note("DICA", "Para restringir caracteres em campos de texto, um validador (Capítulo 6) costuma ser a solução mais "
                 "simples. Filtros são indicados para comportamentos transversais: atalhos globais, registro de "
                 "atividade, bloqueio temporário de interação."),

    h2("Eventos personalizados: postEvent() e sendEvent()"),
    p("A aplicação pode criar seus próprios tipos de evento, numerados a partir de `QEvent.Type.User` com "
      "`QEvent.registerEventType()`, que garante um identificador não usado. `postEvent()` **enfileira** o evento "
      "(entregue pelo event loop, de forma assíncrona e segura entre threads); `sendEvent()` o entrega "
      "**imediatamente**, de forma síncrona. A saída da Listagem 10.3 mostra a diferença na ordem de execução."),
    lst("c10_evento_proprio.py", "Eventos personalizados: registerEventType, postEvent (assíncrono) e sendEvent"),
    out("c10_evento_proprio"),
    p("Na maioria dos casos, sinais personalizados resolvem a comunicação entre objetos com menos código; eventos "
      "próprios são úteis quando se quer aproveitar a fila de eventos, filtros e a compressão de eventos do Qt."),

    h2("Arrastar e soltar"),
    h3("QDrag e QMimeData"),
    p("O conteúdo arrastado é empacotado em `QMimeData`, que pode conter vários formatos ao mesmo tempo (texto, "
      "HTML, URLs de arquivos, imagens, formatos próprios). Para **iniciar** um arraste a partir de um widget "
      "próprio, crie um `QDrag` com o `QMimeData` em `mouseMoveEvent` (após o mouse se deslocar mais que "
      "`QApplication.startDragDistance()`) e chame `drag.exec(acoes)`. Widgets de visão (listas, árvores, "
      "tabelas) já trazem suporte a arraste embutido."),
    h3("dragEnterEvent, dragMoveEvent e dropEvent"),
    p("Para **receber**, o widget chama `setAcceptDrops(True)` e trata `dragEnterEvent` (aceitar ou recusar o "
      "conteúdo), opcionalmente `dragMoveEvent` (aceitar só em certas regiões) e `dropEvent` (processar). A "
      "Listagem 10.4 aceita apenas arquivos `.csv` e, para ser executável sem interação, gera os mesmos eventos "
      "que o sistema enviaria em um arraste real."),
    lst("c10_arrastar_soltar.py", "Arrastar e soltar: alvo que aceita apenas arquivos .csv"),
    out("c10_arrastar_soltar"),

    h2("Área de transferência: QClipboard"),
    p("`QApplication.clipboard()` dá acesso à área de transferência do sistema. `setText()`/`text()` cobrem o caso "
      "comum; `setMimeData()` publica vários formatos de uma vez, permitindo que o aplicativo de destino escolha o "
      "mais rico que entende (por exemplo, HTML em um editor de texto e texto puro em um terminal). O sinal "
      "`dataChanged` avisa quando o conteúdo muda."),
    lst("c10_clipboard.py", "Área de transferência: texto, dados MIME e notificação de mudança"),
    out("c10_clipboard"),
    note("NOTA", "No Linux/X11 existe também a *seleção* (texto selecionado, colado com o botão do meio), acessível "
                 "com `clipboard.text(QClipboard.Mode.Selection)`."),

    h2("Exercícios do capítulo"),
    nl("Crie um widget que desenhe um ponto onde o usuário clicar (guarde as posições e chame `update()`; a pintura "
       "será detalhada no Capítulo 17).",
       "Modifique a Listagem 10.1 para mostrar as coordenadas do mouse em um `QLabel` usando `setMouseTracking(True)`.",
       "Implemente um filtro de eventos que registre em log todo `FocusIn` dos campos de um formulário.",
       "Permita soltar arquivos `.json` sobre a janela da Listagem 8.1 para abri-los em uma nova aba.",
       "Crie a ação *Copiar resultados* que publica na área de transferência texto puro (CSV) e HTML (tabela)."),
)
