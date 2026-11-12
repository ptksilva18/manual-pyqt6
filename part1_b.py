# -*- coding: utf-8 -*-
"""Parte I — Capítulos 4 a 7 (Step 2)."""
from blocks import ST_BAS, bl, ch, flat, h2, h3, h4, img, lst, nl, note, out, p, snip, tab

CAP04 = flat(
    ch("Primeira aplicação com PyQt6", ST_BAS, [
        "Escrever, executar e entender a menor aplicação PyQt6 possível.",
        "Compreender o objeto de aplicação e o event loop.",
        "Evoluir para uma janela baseada em subclasse de QMainWindow.",
    ]),
    h2("Anatomia mínima de uma aplicação"),
    p("Toda aplicação PyQt6 com interface gráfica segue os mesmos quatro passos, numerados nos comentários da "
      "Listagem 4.1: criar o objeto de aplicação, criar ao menos uma janela, exibi-la e entrar no *event loop*."),
    lst("c04_primeira.py", "Primeira aplicação PyQt6"),
    img("Janela produzida pela primeira aplicação", "f4_1_primeira.png", width_cm=8.0),
    nl("`QApplication(sys.argv)` cria o objeto de aplicação, que inicializa o Qt, carrega o plugin de plataforma "
       "e processa argumentos de linha de comando. Deve existir **exatamente um** por processo e ser criado antes "
       "de qualquer widget.",
       "Um widget criado **sem pai** torna-se uma janela de nível superior; aqui, um `QLabel` serve de janela.",
       "`show()` agenda a exibição. Nada aparece na tela ainda: a pintura acontece quando o event loop roda.",
       "`app.exec()` entra no event loop e só retorna quando a aplicação termina; seu valor de retorno é o código "
       "de saída, repassado a `sys.exit()`."),
    note("ATENÇÃO", "Criar um widget antes do `QApplication` produz o erro fatal *QWidget: Must construct a "
                    "QApplication before a QWidget*, que encerra o processo."),
    h3("QApplication, QGuiApplication e QCoreApplication"),
    tab("Classes de aplicação do Qt", ["Classe", "Módulo", "Quando usar"],
        [["QCoreApplication", "QtCore", "Programas sem interface gráfica que usam o event loop (servidores, serviços, ferramentas de linha de comando com timers e rede)"],
         ["QGuiApplication", "QtGui", "Aplicações gráficas sem widgets, como aplicações Qt Quick/QML (Capítulo 26)"],
         ["QApplication", "QtWidgets", "Aplicações com widgets — o caso de todo este manual até o Capítulo 25"]],
        [2300, 1500, 5271]),
    p("As três formam uma hierarquia (`QApplication` herda de `QGuiApplication`, que herda de `QCoreApplication`). "
      "A instância única pode ser obtida em qualquer ponto do programa com `QApplication.instance()`."),
    h3("sys.argv e argumentos de linha de comando"),
    p("O construtor recebe a lista de argumentos para que o Qt reconheça opções próprias, como `-style` ou "
      "`-platform`. O PyQt6 **remove da lista** as opções que o Qt consumiu, deixando as demais para o programa."),
    lst("c04_argumentos.py", "Argumentos de linha de comando: o Qt consome as opções que reconhece"),
    out("c04_argumentos"),
    p("Para analisar os argumentos restantes de forma robusta, use `argparse` do Python ou `QCommandLineParser` "
      "do Qt (Capítulo 16)."),
    h3("O event loop"),
    p("Uma aplicação gráfica passa a maior parte do tempo **esperando**: por um clique, uma tecla, um timer, dados "
      "da rede. O event loop é o laço, iniciado por `exec()`, que aguarda o próximo evento, o entrega ao objeto de "
      "destino, executa os manipuladores e slots correspondentes e repinta o que mudou. A Figura 4.2 resume o "
      "ciclo de vida completo."),
    img("Ciclo de vida de uma aplicação PyQt6 e o event loop", "f4_2_ciclo.png"),
    note("IMPORTANTE", "Enquanto um slot está executando, o event loop está parado: a janela não repinta e não "
                       "responde ao usuário. Todo código de slot deve ser rápido. Cálculos longos vão para outra "
                       "thread (Capítulo 20) ou são divididos em etapas com `QTimer` (Capítulo 5)."),

    h2("QWidget como janela de nível superior"),
    p("Qualquer widget sem pai é exibido como janela, com moldura e barra de título fornecidas pelo sistema "
      "operacional. Para janelas simples — utilitários, diálogos próprios, protótipos —, uma subclasse de `QWidget` "
      "com um layout é suficiente. O tipo e a decoração da janela são controlados por *window flags*:"),
    snip('''from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget

painel = QWidget()
painel.setWindowTitle("Monitor")
painel.setWindowFlags(Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint)
painel.setMinimumSize(320, 200)
painel.show()'''),
    p("Note que `setWindowFlags()` deve ser chamado antes de `show()`; chamá-lo numa janela já visível a oculta, "
      "e é preciso chamar `show()` de novo."),

    h2("Subclasse de QMainWindow"),
    p("`QMainWindow` é a classe própria para a janela principal de aplicações: ela já reserva áreas para barra de "
      "menus, barras de ferramentas, painéis acopláveis, barra de status e um **widget central** (Capítulo 8). "
      "O padrão profissional é criar uma subclasse e montar a interface no `__init__`, mantendo o bloco "
      "`if __name__ == \"__main__\"` apenas com a inicialização."),
    lst("c04_mainwindow.py", "Janela principal como subclasse de QMainWindow"),
    p("A função `main()` retornando o código de saída facilita testes e o uso como *entry point* no "
      "`pyproject.toml` (Listagem 2.2)."),

    h2("Encerramento da aplicação"),
    h3("sys.exit(app.exec()) e códigos de saída"),
    p("`app.exec()` retorna o valor passado a `app.exit(codigo)`; `app.quit()` equivale a `exit(0)`. Repassar esse "
      "valor a `sys.exit()` permite que scripts e agendadores identifiquem falhas (convenção: 0 = sucesso). "
      "Para encerrar com erro após exibir uma mensagem, use `QApplication.exit(1)`."),
    h3("quitOnLastWindowClosed e aboutToQuit"),
    p("Por padrão, a aplicação termina quando a última janela visível é fechada (`quitOnLastWindowClosed()` igual "
      "a `True`). Aplicações que vivem na bandeja do sistema (Capítulo 23) desativam esse comportamento com "
      "`app.setQuitOnLastWindowClosed(False)`. O sinal `aboutToQuit` é emitido imediatamente antes de `exec()` "
      "retornar — o lugar certo para gravar configurações e liberar recursos."),
    lst("c04_ciclo_vida.py", "Metadados, aboutToQuit e quitOnLastWindowClosed"),
    out("c04_ciclo_vida"),

    h2("Metadados da aplicação: nome, organização, versão e ícone"),
    p("Os metadados definidos na Listagem 4.4 não são decorativos: `organizationName` e `applicationName` "
      "determinam onde o `QSettings` grava as preferências (Capítulo 8) e onde `QStandardPaths` localiza pastas de "
      "dados (Capítulo 13); `applicationDisplayName` é acrescentado ao título das janelas em algumas plataformas; "
      "`applicationVersion` alimenta diálogos *Sobre* e o `QCommandLineParser`. O ícone padrão de todas as "
      "janelas é definido uma vez na aplicação:"),
    snip('''from PyQt6.QtGui import QIcon

app.setWindowIcon(QIcon("resources/icone.svg"))   # SVG escala bem em telas High-DPI
app.setDesktopFileName("calc-engenharia")          # Linux/Wayland: arquivo .desktop'''),

    h2("Exercícios do capítulo"),
    nl("Modifique a Listagem 4.1 para exibir um `QPushButton` como janela e conecte `clicked` a `app.quit`.",
       "Execute a Listagem 4.2 com a opção `-style windows` na linha de comando e compare a aparência.",
       "Altere a Listagem 4.4 para que a aplicação continue rodando após fechar a janela; encerre-a com um `QTimer`.",
       "Crie a função `main()` de um projeto com a estrutura da Figura 2.1, chamada pelo `__main__.py`."),
)

CAP05 = flat(
    ch("QObject, sinais e slots", ST_BAS, [
        "Compreender QObject, a árvore de objetos e o gerenciamento de memória.",
        "Conectar, criar e desconectar sinais e slots com segurança.",
        "Usar propriedades, metaobjetos e temporizadores.",
    ]),
    h2("QObject: a classe base do Qt"),
    p("`QObject` é a raiz de quase todas as classes do Qt que têm identidade (widgets, timers, modelos, sockets). Ele "
      "fornece quatro serviços fundamentais: a **árvore de objetos** pai–filho, **sinais e slots**, "
      "**propriedades** e **eventos**. Classes de valor, como `QPoint` ou `QColor`, não herdam de `QObject`."),
    h3("Hierarquia pai–filho e propriedade de memória"),
    p("Todo `QObject` pode ter um pai, passado no construtor ou por `setParent()`. O pai **é dono** dos filhos: ao "
      "ser destruído, destrói todos eles recursivamente. Para widgets, a relação tem um segundo efeito: um widget "
      "filho é desenhado dentro da área do pai, e um widget sem pai é uma janela."),
    img("Árvore de objetos pai–filho de uma janela", "f5_1_arvore.png"),
    h3("objectName, findChild() e findChildren()"),
    p("O `objectName` identifica um objeto dentro da árvore. Ele é usado por `findChild()` e `findChildren()`, por "
      "folhas de estilo (seletor `#nome`), pelo Qt Designer e pelo `saveState()` da janela principal."),
    lst("c05_arvore.py", "Árvore de objetos: pai-filho, objectName, findChild/findChildren e destroyed"),
    out("c05_arvore"),
    p("Três detalhes da saída merecem atenção: o layout aparece como filho da janela (ele foi criado com "
      "`QVBoxLayout(janela)`); os widgets adicionados ao layout foram **reparentados** para a janela; e cada "
      "`QLineEdit` possui um filho interno sem nome, criado pelo próprio Qt — por isso buscas devem filtrar por "
      "tipo e nome, e não pela posição na lista."),
    h3("deleteLater() e o ciclo de vida C++ versus Python"),
    p("Para destruir um objeto Qt, use `deleteLater()`: a destruição ocorre no próximo ciclo do event loop, quando "
      "é seguro (por exemplo, depois que o slot que está tratando um sinal desse objeto terminar). O sinal "
      "`destroyed` avisa quando o objeto C++ deixou de existir."),
    p("Como cada objeto tem uma parte Python e uma parte C++, é possível que a variável Python continue existindo "
      "depois que o pai destruiu o objeto C++. Qualquer acesso então gera `RuntimeError`; o módulo `PyQt6.sip` "
      "permite detectar essa situação."),
    lst("c05_vida_cpp.py", "Ciclo de vida C++ x Python: referência para objeto C++ já destruído"),
    out("c05_vida_cpp"),
    note("ATENÇÃO", "O problema inverso também ocorre: um widget **sem pai** guardado apenas em variável local é "
                    "destruído pelo coletor de lixo do Python ao fim da função — a janela \"pisca\" e some. Guarde "
                    "janelas em atributos (`self.janela_dados = ...`) ou dê a elas um pai."),

    h2("Sinais e slots"),
    p("Sinais e slots são o mecanismo de comunicação entre objetos do Qt. Um **sinal** é emitido quando algo "
      "acontece (um botão foi clicado, um valor mudou); um **slot** é qualquer callable conectado a ele. O emissor "
      "não sabe quem está conectado, o que reduz o acoplamento entre partes da aplicação."),
    img("Mecanismo de sinais e slots", "f5_2_sinais.png"),
    h3("Conectando sinais embutidos"),
    p("Os widgets do Qt já declaram dezenas de sinais. A conexão usa a sintaxe `objeto.sinal.connect(callable)`; "
      "os argumentos do sinal são passados ao callable, que pode aceitar menos argumentos que o sinal envia."),
    snip('''botao.clicked.connect(self.calcular)                 # clicked(bool) -> calcular()
campo.textChanged.connect(self.validar)               # textChanged(str) -> validar(texto)
spin.valueChanged.connect(barra.setValue)             # slot de outro widget
combo.currentIndexChanged.connect(lambda i: print(i))'''),
    h3("Sinais personalizados com pyqtSignal"),
    h4("Declaração como atributo de classe"),
    p("Sinais próprios são declarados com `pyqtSignal(tipos...)` **no corpo da classe**, nunca dentro do "
      "`__init__`, e somente em subclasses de `QObject`. Cada instância recebe automaticamente seu sinal ligado "
      "(*bound signal*), com os métodos `connect()`, `disconnect()` e `emit()`."),
    h4("Sinais com argumentos e sobrecargas"),
    p("Os tipos declarados definem a assinatura: `pyqtSignal(str, float)` emite dois argumentos. Um sinal "
      "sobrecarregado aceita listas de tipos (`pyqtSignal([int], [str])`), e a variante desejada é escolhida por "
      "indexação: `sinal[int]`."),
    lst("c05_sinais.py", "Sinais personalizados: declaração, argumentos, sobrecarga e conexões"),
    out("c05_sinais"),
    p("A leitura repetida (250,0) não gerou emissão porque o método só emite quando o valor muda — prática "
      "recomendada para evitar laços de atualização. Após o `disconnect`, apenas o *log* continuou recebendo."),
    h3("Slots com @pyqtSlot"),
    p("Qualquer callable funciona como slot, mas decorar métodos com `@pyqtSlot(tipos)` traz vantagens: o método "
      "é registrado no metaobjeto (acessível por `QMetaObject.invokeMethod` e pelo QML), a conexão é ligeiramente "
      "mais eficiente e, em conexões entre threads, o slot é executado na thread do objeto receptor (Capítulo 20)."),
    h3("Passando argumentos adicionais (lambda e functools.partial)"),
    p("Quando o slot precisa de informações que o sinal não envia — por exemplo, qual botão foi clicado —, use "
      "`lambda` ou `functools.partial`, observando a armadilha do argumento `checked` apresentada na Listagem 3.4."),
    h3("Tipos de conexão"),
    p("O segundo argumento de `connect()` define como o slot é chamado."),
    tab("Valores de Qt.ConnectionType", ["Valor", "Comportamento"],
        [["AutoConnection", "Padrão. Direta se emissor e receptor estão na mesma thread; enfileirada caso contrário."],
         ["DirectConnection", "O slot é executado imediatamente, na thread do emissor."],
         ["QueuedConnection", "O slot é executado no event loop da thread do receptor."],
         ["BlockingQueuedConnection", "Como QueuedConnection, mas o emissor bloqueia até o slot retornar (nunca na mesma thread)."],
         ["UniqueConnection", "Flag combinável: impede conexões duplicadas."],
         ["SingleShotConnection", "Flag combinável: a conexão é desfeita após a primeira emissão."]],
        [2600, 6471]),
    lst("c05_conexoes.py", "Tipos de conexão, UniqueConnection, SingleShotConnection e bloqueio de sinais"),
    out("c05_conexoes"),
    h3("Desconexão, blockSignals() e QSignalBlocker"),
    p("`sinal.disconnect(slot)` remove uma conexão específica; `sinal.disconnect()` remove todas. Para suprimir "
      "sinais temporariamente — por exemplo, ao preencher um formulário a partir de dados salvos, sem disparar "
      "validações —, prefira `QSignalBlocker` em um bloco `with` a chamar `blockSignals(True)` e "
      "`blockSignals(False)` manualmente: o bloqueio é desfeito mesmo se ocorrer uma exceção."),

    h2("Propriedades: pyqtProperty e propriedades dinâmicas"),
    p("Propriedades declaradas com `pyqtProperty` (como decorador ou função) entram no metaobjeto, com tipo, "
      "*getter*, *setter* e sinal de notificação. **Propriedades dinâmicas**, criadas com `setProperty()` em um "
      "objeto qualquer, não precisam de declaração — são úteis para marcar widgets (por exemplo, `perigoso=True`) "
      "e estilizá-los com seletores de folha de estilo (Capítulo 12)."),
    lst("c05_meta.py", "Propriedades dinâmicas e introspecção com QMetaObject"),
    out("c05_meta"),

    h2("Sistema de metaobjetos e introspecção"),
    p("O **QMetaObject** descreve, em tempo de execução, o nome da classe, suas propriedades, sinais, slots e enums. "
      "É ele que permite ao Qt conectar sinais por nome, ao Qt Designer listar propriedades editáveis e ao QML "
      "acessar objetos Python. Na Listagem 5.5, os laços começam em `propertyOffset()` e `methodOffset()` para "
      "listar apenas o que a própria classe declarou, excluindo o herdado de `QObject`."),

    h2("Temporizadores: QTimer, QBasicTimer e QElapsedTimer"),
    p("`QTimer` emite `timeout` periodicamente ou uma única vez (`QTimer.singleShot`). Ele depende do event loop: "
      "o intervalo é um mínimo, não uma garantia de tempo real. `QBasicTimer` é uma alternativa leve, sem sinais, "
      "tratada em `timerEvent()`. `QElapsedTimer` mede intervalos com relógio monotônico."),
    lst("c05_timers.py", "QTimer (periódico e singleShot), QElapsedTimer e QBasicTimer"),
    out("c05_timers"),
    p("O número exato de leituras periódicas pode variar em ±1 conforme a carga da máquina — consequência direta de "
      "o temporizador depender do event loop. O tipo de temporizador (`Qt.TimerType.PreciseTimer`, `CoarseTimer` ou "
      "`VeryCoarseTimer`) ajusta a precisão desejada e o consumo de energia."),
    note("DICA", "`QTimer.singleShot(0, funcao)` agenda `funcao` para logo depois que o event loop processar os "
                 "eventos pendentes — útil para concluir a inicialização após a janela aparecer."),

    h2("Tipos de valor do QtCore: QPoint, QSize, QRect, QDate, QDateTime, QUrl"),
    p("O QtCore fornece tipos de valor usados em toda a API: geometria inteira (`QPoint`, `QSize`, `QRect`) e de "
      "ponto flutuante (`QPointF`, `QSizeF`, `QRectF`), datas e horas (`QDate`, `QTime`, `QDateTime`, `QTimeZone`) "
      "e endereços (`QUrl`)."),
    lst("c05_tipos.py", "Tipos de valor do QtCore: geometria, datas e URLs"),
    out("c05_tipos"),
    note("ATENÇÃO", "Por razões históricas, para `QRect` inteiro vale `right() = left() + width() - 1` (199 para uma "
                    "largura de 200), e o centro é arredondado para baixo. Em cálculos geométricos precisos, use "
                    "`QRectF`, onde `right() = left() + width()`."),

    h2("Exercícios do capítulo"),
    nl("Acrescente à Listagem 5.3 um sinal `faixaNormal` emitido quando o valor volta abaixo do limite.",
       "Crie um objeto com `pyqtProperty` `temperatura` e conecte o sinal de notificação a um `QLCDNumber`.",
       "Usando `findChildren`, escreva uma função que limpe todos os `QLineEdit` de um formulário.",
       "Demonstre com `QTimer.singleShot` que um slot `QueuedConnection` só executa após o retorno do código atual.",
       "Calcule com `QDate` quantos dias úteis (segunda a sexta) há entre duas datas informadas."),
)

CAP06 = flat(
    ch("Widgets fundamentais", ST_BAS, [
        "Conhecer as propriedades comuns a todos os widgets.",
        "Utilizar os widgets de exibição, botões e entrada de dados.",
        "Associar cada widget aos seus sinais mais relevantes.",
    ]),
    h2("QWidget: propriedades e métodos comuns"),
    p("Todos os elementos visuais herdam de `QWidget`. Por isso, as propriedades desta seção valem para qualquer "
      "widget do capítulo. No PyQt6, propriedades Qt podem ser passadas diretamente como argumentos nomeados no "
      "construtor — `QSpinBox(minimum=0, maximum=100, suffix=\" %\")` —, recurso usado em várias listagens."),
    h3("Geometria, tamanho mínimo/máximo e visibilidade"),
    p("`resize()`, `move()` e `setGeometry()` posicionam janelas; dentro de layouts, quem decide a geometria é o "
      "layout (Capítulo 7), respeitando `setMinimumSize()`, `setMaximumSize()` e `setFixedSize()`. `show()`, "
      "`hide()` e `setVisible()` controlam a visibilidade; `isVisible()` informa o estado efetivo."),
    h3("Habilitação, foco, tooltip, status tip e cursor"),
    snip('''botao.setEnabled(False)                          # também desabilita os filhos
campo.setFocus()                                 # recebe o foco do teclado
campo.setToolTip("Pressão manométrica, em bar")  # balão ao repousar o mouse
acao.setStatusTip("Salva o registro atual")      # texto na barra de status (Cap. 8)
area.setCursor(Qt.CursorShape.CrossCursor)'''),
    h3("Flags e estados de janela (Qt.WindowType, Qt.WindowState)"),
    p("Para janelas, `Qt.WindowType` define o tipo e a decoração (`Dialog`, `Tool`, `FramelessWindowHint`, "
      "`WindowStaysOnTopHint`) e `Qt.WindowState` o estado (`WindowMaximized`, `WindowMinimized`, "
      "`WindowFullScreen`), também acessível por `showMaximized()` e `showFullScreen()`."),
    img("Galeria dos widgets fundamentais", "f6_1_galeria.png", width_cm=14.0),
    p("A Figura 6.1 é a captura da Listagem 6.1, que reúne os widgets descritos nas próximas seções."),
    lst("c06_galeria.py", "Galeria dos widgets fundamentais"),

    h2("Widgets de exibição"),
    h3("QLabel: texto, rich text, imagens e links"),
    p("`QLabel` exibe texto simples, *rich text* (subconjunto de HTML) ou uma imagem (`setPixmap`). Com "
      "`setOpenExternalLinks(True)`, links `<a href>` abrem no navegador; com `setBuddy(campo)`, o atalho `&` do "
      "rótulo leva o foco ao campo associado (Capítulo 7). `setWordWrap(True)` quebra linhas longas."),
    h3("QLCDNumber"),
    p("Exibe números com aparência de display de sete segmentos. `display()` aceita `int`, `float` ou `str`; "
      "`setDigitCount()` define a quantidade de dígitos e `setMode()` a base (decimal, hexadecimal, octal, binária)."),
    h3("QProgressBar"),
    p("Mostra o progresso de uma operação entre `minimum()` e `maximum()`. Com mínimo e máximo iguais a 0, entra em "
      "modo indeterminado (animação contínua), útil quando o total é desconhecido. `setFormat(\"%v de %m\")` "
      "personaliza o texto."),

    h2("Botões"),
    h3("QAbstractButton e QPushButton"),
    p("`QAbstractButton` define o comportamento comum: texto, ícone, atalho, estado checável e os sinais "
      "`clicked(bool)`, `pressed`, `released` e `toggled(bool)`. `QPushButton` é o botão de comando padrão; "
      "`setDefault(True)` o torna acionável pela tecla Enter em diálogos."),
    h3("QToolButton e QCommandLinkButton"),
    p("`QToolButton` é o botão compacto de barras de ferramentas; pode exibir um menu (`setMenu`) com o modo de "
      "abertura definido por `ToolButtonPopupMode` (`DelayedPopup`, `MenuButtonPopup`, `InstantPopup`). "
      "`QCommandLinkButton` é um botão grande com texto descritivo, usado em assistentes."),
    h3("QCheckBox e QRadioButton"),
    p("`QCheckBox` representa uma opção liga/desliga, com terceiro estado opcional (`setTristate`); o sinal "
      "`checkStateChanged(Qt.CheckState)` informa o estado completo. `QRadioButton` representa uma escolha "
      "exclusiva: botões com o mesmo pai são mutuamente exclusivos automaticamente."),
    h3("QButtonGroup e exclusividade"),
    p("`QButtonGroup` agrupa botões logicamente (sem efeito visual), associa um identificador inteiro a cada um e "
      "emite `idClicked(int)`. É a forma recomendada de tratar um conjunto de opções com um único slot."),
    lst("c06_botoes.py", "Botões checáveis, QButtonGroup exclusivo e QDialogButtonBox"),
    out("c06_botoes"),
    h3("QDialogButtonBox"),
    p("Organiza botões padronizados (OK, Cancelar, Aplicar, Salvar…) na **ordem e posição corretas para cada "
      "plataforma** — no Windows, OK fica à esquerda de Cancelar; no macOS, à direita. Emite `accepted` e "
      "`rejected` conforme o papel do botão. Seu uso em diálogos é detalhado no Capítulo 9."),

    h2("Entrada de texto"),
    h3("QLineEdit"),
    p("Campo de uma linha, o widget de entrada mais usado. Seus sinais distinguem a origem da alteração: "
      "`textEdited` só é emitido por edição do usuário; `textChanged` também por código (`setText`); "
      "`editingFinished` ao pressionar Enter ou perder o foco com conteúdo aceitável; `returnPressed` ao pressionar Enter."),
    lst("c06_lineedit.py", "QLineEdit: validadores, máscara, modo de eco e autocompletar"),
    out("c06_lineedit"),
    h4("Modos de eco e placeholder"),
    p("`EchoMode` define o que é exibido: `Normal`, `NoEcho`, `Password` e `PasswordEchoOnEdit`. O texto real "
      "continua disponível em `text()`; `displayText()` retorna o que aparece na tela. `placeholderText` mostra uma "
      "dica enquanto o campo está vazio."),
    h4("Máscaras de entrada (inputMask)"),
    p("A máscara restringe caractere a caractere: `9` exige dígito, `A` exige letra, `>` converte para maiúsculas, "
      "e o trecho após `;` define o caractere de preenchimento. `hasAcceptableInput()` informa se a máscara está "
      "completa."),
    h4("Validadores: QIntValidator, QDoubleValidator, QRegularExpressionValidator"),
    p("Um validador classifica o texto em três estados: `Acceptable` (válido), `Intermediate` (pode se tornar "
      "válido com mais digitação — por exemplo, `700` acima do máximo) e `Invalid` (bloqueado na digitação). "
      "Enquanto o estado não for `Acceptable`, `editingFinished` não é emitido."),
    note("ATENÇÃO", "`QDoubleValidator` respeita o **idioma (locale)**: em pt-BR, o separador decimal é a vírgula e "
                    "`345.5` é classificado como `Intermediate`, enquanto `345,5` é `Acceptable` (verificado com "
                    "`QLocale` pt-BR). Por isso a Listagem 6.3 fixa `QLocale.c()`. Decida conscientemente qual "
                    "convenção a sua aplicação adota e converta com `QLocale.toDouble()`."),
    h4("Autocompletar com QCompleter"),
    p("`QCompleter` sugere valores a partir de uma lista ou de um modelo (Capítulo 14). Configure sensibilidade a "
      "maiúsculas (`setCaseSensitivity`), modo de filtragem (`setFilterMode`, por exemplo `Qt.MatchFlag.MatchContains`) "
      "e modo de apresentação (`setCompletionMode`)."),
    h3("QTextEdit e QTextBrowser"),
    p("`QTextEdit` edita texto multilinha com formatação (*rich text*), baseado em `QTextDocument`. Use "
      "`toPlainText()`/`setPlainText()` para texto puro e `toHtml()`/`setHtml()` ou `toMarkdown()`/`setMarkdown()` "
      "para conteúdo formatado. `QTextBrowser` é a variante somente leitura com navegação por links — adequada para "
      "telas de ajuda."),
    h3("QPlainTextEdit"),
    p("Editor de texto puro otimizado para grandes volumes: logs, arquivos de dados, código. É significativamente "
      "mais eficiente que `QTextEdit` para milhares de linhas; `setMaximumBlockCount(n)` limita o número de linhas "
      "mantidas, ideal para janelas de log contínuo."),

    h2("Entrada numérica e de faixa"),
    h3("QSpinBox e QDoubleSpinBox"),
    p("Campos numéricos com setas, limites (`minimum`, `maximum`), passo (`singleStep`), prefixo e sufixo (unidade). "
      "`QDoubleSpinBox` acrescenta `decimals`. Com `setStepType(QAbstractSpinBox.StepType.AdaptiveDecimalStepType)`, "
      "o passo se adapta à ordem de grandeza do valor. `setKeyboardTracking(False)` faz `valueChanged` ser emitido "
      "apenas ao confirmar a edição, e não a cada tecla."),
    h3("QSlider, QDial e QScrollBar"),
    p("Os três derivam de `QAbstractSlider` e trabalham com **inteiros**. Para grandezas reais, mapeie a escala, como "
      "na Listagem 6.4, que sincroniza um slider de 0 a 1000 com um spin box de 0,0 a 100,0 %. `sliderMoved` é "
      "emitido apenas durante o arraste; `valueChanged`, a cada mudança de valor."),
    lst("c06_numericos.py", "Sincronizando QSlider e QDoubleSpinBox; QComboBox com dados associados"),
    out("c06_numericos"),
    p("A sincronização bidirecional não entra em laço infinito porque os widgets do Qt só emitem `valueChanged` "
      "quando o valor efetivamente muda."),

    h2("Seleção em listas: QComboBox e QFontComboBox"),
    p("`QComboBox` apresenta uma lista suspensa. Cada item tem texto, ícone opcional e **dados associados** "
      "(`addItem(texto, dado)`, `itemData(i)`, `currentData()`), o que permite separar o que o usuário vê do valor "
      "usado pelo programa — como os fatores de conversão da Listagem 6.4. Com `setEditable(True)`, aceita "
      "digitação livre. `QFontComboBox` é uma especialização que lista as fontes instaladas."),

    h2("Data e hora: QDateEdit, QTimeEdit, QDateTimeEdit e QCalendarWidget"),
    p("Editores de data e hora trabalham com `QDate`, `QTime` e `QDateTime`. Configure `displayFormat` (por exemplo, "
      "`\"dd/MM/yyyy\"`), limites (`setMinimumDate`, `setMaximumDate`) e `calendarPopup=True` para abrir um "
      "calendário. `QCalendarWidget` é o calendário completo, embutível em qualquer layout."),

    h2("Agrupadores e molduras: QGroupBox, QFrame, QToolBox e QTabWidget"),
    p("`QGroupBox` agrupa widgets com moldura e título — e pode ser checável, habilitando ou desabilitando todo o "
      "conteúdo. `QFrame` desenha linhas e molduras (`setFrameShape`). `QToolBox` organiza páginas em seções "
      "expansíveis e `QTabWidget` em abas; ambos permitem formulários extensos sem rolagem."),

    h2("Captura de atalhos: QKeySequenceEdit"),
    p("`QKeySequenceEdit` captura uma combinação de teclas digitada pelo usuário e a disponibiliza como "
      "`QKeySequence` — o widget usado em telas de configuração de atalhos personalizados."),
    tab("Widgets fundamentais e seus sinais principais", ["Widget", "Sinais principais", "Uso típico"],
        [["QPushButton", "clicked, pressed, released, toggled", "Disparar uma ação: calcular, salvar, abrir"],
         ["QLineEdit", "textChanged, textEdited, editingFinished, returnPressed", "Texto curto: tags, nomes, valores validados"],
         ["QSpinBox", "valueChanged, textChanged", "Inteiros limitados: quantidades, contagens"],
         ["QComboBox", "currentIndexChanged, currentTextChanged, activated", "Escolha em lista fechada: material, unidade"],
         ["QSlider", "valueChanged, sliderMoved, sliderReleased", "Ajuste contínuo visual: abertura, zoom"],
         ["QCheckBox", "checkStateChanged, toggled", "Opção liga/desliga: incluir margem de segurança"]],
        [2200, 4371, 2500]),

    h2("Exercícios do capítulo"),
    nl("Crie um campo de tag no formato `AA-9999` com `QRegularExpressionValidator` e conversão para maiúsculas.",
       "Implemente um conversor de unidades de pressão com `QDoubleSpinBox` e `QComboBox` usando `currentData()`.",
       "Use `QButtonGroup` para selecionar a norma de projeto entre três opções e exiba a escolha em um `QLabel`.",
       "Construa uma janela de log com `QPlainTextEdit` limitada a 500 linhas, alimentada por um `QTimer`.",
       "Explique, com um exemplo, a diferença entre os sinais `textChanged` e `textEdited`."),
)

CAP07 = flat(
    ch("Layouts e gerenciamento de geometria", ST_BAS, [
        "Substituir posicionamento absoluto por gerenciadores de layout.",
        "Combinar layouts aninhados para interfaces responsivas.",
        "Controlar o redimensionamento com QSizePolicy, stretch e QSplitter.",
    ]),
    h2("Por que usar layouts"),
    p("Posicionar widgets com coordenadas fixas (`move`, `setGeometry`) quebra com facilidade: fontes maiores, "
      "tradução para outro idioma, escala High-DPI ou simples redimensionamento da janela deixam textos cortados "
      "e espaços desperdiçados. Os **gerenciadores de layout** calculam a geometria automaticamente a partir do "
      "tamanho preferido de cada widget (`sizeHint`), de suas políticas de tamanho e do espaço disponível, e "
      "recalculam tudo sempre que algo muda."),
    note("DICA", "Instalar um layout em um widget é simples: passe o widget no construtor do layout "
                 "(`QVBoxLayout(self)`) ou chame `self.setLayout(layout)`. Os widgets adicionados ao layout são "
                 "reparentados automaticamente para o widget que o possui."),

    h2("Layouts de caixa: QHBoxLayout e QVBoxLayout"),
    p("`QHBoxLayout` alinha itens horizontalmente e `QVBoxLayout` verticalmente. Itens podem ser widgets "
      "(`addWidget`), outros layouts (`addLayout`), espaços fixos (`addSpacing`) ou elásticos (`addStretch`)."),
    lst("c07_caixas.py", "QHBoxLayout e QVBoxLayout: margens, espaçamento, stretch e alinhamento"),
    out("c07_caixas"),
    h3("Margens, espaçamento e alinhamento"),
    p("`setContentsMargins(esq, topo, dir, base)` define o espaço entre a borda do widget e os itens; "
      "`setSpacing()` o espaço entre itens. O parâmetro `alignment` de `addWidget` alinha um item dentro da sua "
      "célula sem esticá-lo — como o rótulo `Rev. 0B`, mantido à direita."),
    h3("Fatores de stretch e QSpacerItem"),
    p("O fator de *stretch* distribui o espaço extra proporcionalmente. Na Listagem 7.1, o `QTextEdit` tem "
      "stretch 1 e os demais itens 0: todo o espaço vertical adicional vai para ele, como mostra a saída — ao "
      "aumentar a janela em 200 px, o editor cresceu exatamente 200 px. Um `addStretch()` antes dos botões "
      "cria um `QSpacerItem` elástico que os empurra para a direita."),
    img("Comportamento de QHBoxLayout e QVBoxLayout", "f7_1_caixas.png"),

    h2("QGridLayout"),
    p("Organiza itens em linhas e colunas. `addWidget(w, linha, coluna)` posiciona em uma célula e "
      "`addWidget(w, linha, coluna, rowSpan, colSpan)` mescla células."),
    lst("c07_grade.py", "QGridLayout: teclado numérico com células mescladas (row/column span)"),
    out("c07_grade"),
    h3("Linhas, colunas e células mescladas (span)"),
    p("O visor ocupa a linha 0 inteira (1 linha × 4 colunas) e o botão `0` ocupa duas colunas da última linha. "
      "`getItemPosition()` devolve a posição e os *spans* de qualquer item, útil em interfaces geradas por código."),
    h3("Stretch de linhas e colunas"),
    p("`setColumnStretch(c, fator)` e `setRowStretch(l, fator)` controlam a distribuição de espaço extra entre "
      "colunas e linhas; `setColumnMinimumWidth()` garante uma largura mínima."),

    h2("QFormLayout"),
    p("Layout de duas colunas especializado em formulários: rótulos à esquerda, campos à direita. `addRow(texto, campo)` "
      "cria o rótulo e o associa ao campo como **buddy** — o `&` no texto define um atalho Alt+letra que leva o "
      "foco ao campo. Além disso, o `QFormLayout` adota automaticamente o alinhamento de rótulos esperado em cada "
      "plataforma."),
    lst("c07_formulario.py", "QFormLayout: rótulos e campos alinhados, com políticas de quebra e crescimento"),
    out("c07_formulario"),
    h3("Políticas de quebra de linha e crescimento de campos"),
    p("`RowWrapPolicy` decide quando o rótulo fica acima do campo (`DontWrapRows`, `WrapLongRows`, `WrapAllRows`) — "
      "útil em telas estreitas. `FieldGrowthPolicy` decide quais campos se esticam (`FieldsStayAtSizeHint`, "
      "`ExpandingFieldsGrow`, `AllNonFixedFieldsGrow`)."),

    h2("QStackedLayout e QStackedWidget"),
    p("Empilham várias páginas e exibem uma por vez (`setCurrentIndex`). Não oferecem navegação própria: combine "
      "com uma lista, um `QComboBox` ou botões. `QStackedWidget` é o widget pronto que usa um `QStackedLayout` "
      "internamente; é a base de telas de configuração e assistentes personalizados."),

    h2("Layouts aninhados"),
    p("Interfaces reais combinam layouts: cada `QGroupBox` tem seu próprio layout, e um layout externo os organiza. "
      "A Listagem 7.4 monta uma tela de verificação de tubo com quatro níveis: coluna principal (`QVBoxLayout`), "
      "formulário de entrada (`QFormLayout`), grade de resultados (`QGridLayout`) e linha de botões (`QHBoxLayout`)."),
    lst("c07_composicao.py", "Composição com layouts aninhados"),
    out("c07_composicao"),
    img("Exemplo de composição com layouts aninhados", "f7_2_composicao.png", width_cm=10.5),
    p("Os resultados exibidos são calculados pela própria listagem — D/t, diâmetro interno e a pressão de Barlow "
      "P = 2·SMYS·t/OD com os valores de entrada (OD = 273,1 mm, t = 12,7 mm, SMYS = 448 MPa) —, e a saída confirma "
      "que os rótulos estão coerentes com o cálculo. No Capítulo 8, esses valores passam a ser recalculados a cada "
      "alteração de campo."),

    h2("Políticas de tamanho"),
    h3("sizeHint() e minimumSizeHint()"),
    p("Cada widget informa ao layout seu tamanho preferido (`sizeHint()`) e o menor tamanho razoável "
      "(`minimumSizeHint()`). Em widgets próprios, sobrescreva esses métodos para que o layout os dimensione "
      "corretamente."),
    h3("QSizePolicy"),
    p("A política de tamanho diz ao layout como interpretar o `sizeHint` em cada direção, e o *stretch factor* da "
      "política desempata entre widgets que querem crescer."),
    tab("Valores de QSizePolicy.Policy", ["Política", "Comportamento"],
        [["Fixed", "sizeHint() é o único tamanho aceitável."],
         ["Minimum", "sizeHint() é o mínimo; pode crescer, sem vantagem em crescer."],
         ["Maximum", "sizeHint() é o máximo; pode encolher."],
         ["Preferred", "sizeHint() é o preferido; pode crescer ou encolher."],
         ["MinimumExpanding", "sizeHint() é o mínimo; aproveita espaço extra."],
         ["Expanding", "sizeHint() é sensato; deseja o máximo de espaço possível."],
         ["Ignored", "sizeHint() é ignorado; recebe o máximo de espaço possível."]],
        [2600, 6471]),
    snip('''from PyQt6.QtWidgets import QSizePolicy

grafico.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
botao.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)'''),

    h2("QSplitter"),
    p("`QSplitter` divide o espaço entre widgets com alças que o usuário arrasta. `setStretchFactor()` define como o "
      "espaço extra é repartido ao redimensionar, `setSizes()` fixa tamanhos iniciais e `saveState()`/`restoreState()` "
      "permitem lembrar a divisão escolhida pelo usuário entre sessões (Capítulo 8)."),
    lst("c07_pilha_divisor.py", "QStackedWidget, QSplitter e QScrollArea"),
    out("c07_pilha_divisor"),

    h2("QScrollArea"),
    p("Envolve um widget maior que o espaço disponível, adicionando barras de rolagem. Use `setWidget()` com um "
      "widget que já tenha seu layout e, quase sempre, `setWidgetResizable(True)`, para que o conteúdo acompanhe a "
      "largura da área. Sem essa chamada, o conteúdo mantém o tamanho do seu `sizeHint` no momento da inserção."),

    h2("Exercícios do capítulo"),
    nl("Reproduza a Figura 7.1 e altere o stretch para que o editor e o rótulo superior dividam o espaço extra 3:1.",
       "Complete o teclado da Listagem 7.2 com a avaliação da expressão ao clicar em `=` (use `ast` para avaliar com segurança).",
       "Adapte a Listagem 7.4 para recalcular os resultados a cada `valueChanged` dos campos.",
       "Crie uma tela de configurações com `QListWidget` + `QStackedWidget` em um `QSplitter` cuja divisão seja salva com `QSettings`."),
)
