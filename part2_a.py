# -*- coding: utf-8 -*-
"""Parte II — Capítulos 11 a 14 (Step 3)."""
from blocks import ST_INT, bl, ch, flat, h2, h3, h4, img, lst, nl, note, out, p, snip, tab

CAP11 = flat(
    ch("Qt Designer e arquivos .ui", ST_INT, [
        "Projetar interfaces visualmente no Qt Designer.",
        "Integrar arquivos .ui em tempo de execução ou por geração de código.",
        "Promover widgets personalizados e entender os limites dos plugins para o Designer.",
    ]),
    p("Até aqui, todas as interfaces foram montadas em código. Para formulários extensos, desenhar a tela "
      "visualmente é mais rápido e facilita revisões com quem vai usar a ferramenta. O **Qt Designer** produz "
      "arquivos `.ui` (XML) que o PyQt6 transforma em widgets — sem perder a possibilidade de complementar tudo "
      "em Python."),
    h2("Visão geral do Qt Designer"),
    img("Interface do Qt Designer com o formulário da Listagem 11.1", "f11_1_designer.png"),
    p("A Figura 11.1 mostra o Qt Designer 6.12 (executável distribuído com o PySide6, ver Seção 2.3.3) com o "
      "formulário deste capítulo aberto. As áreas principais são: (1) a **caixa de widgets**, de onde se arrastam "
      "layouts, espaçadores e widgets; (2) o **editor de formulário**; (3) o **inspetor de objetos**, com a "
      "árvore pai–filho e o `objectName` de cada item; (4) o **editor de propriedades**, que lista as "
      "propriedades Qt do objeto selecionado — as mesmas acessíveis por `setProperty()` (Capítulo 5); e (5) os "
      "editores de sinais/slots, ações e recursos."),
    note("NOTA", "A captura foi obtida executando o Designer sob um servidor X virtual (Xvfb). Na primeira tentativa, "
                 "ele falhou exatamente com o erro do plugin xcb descrito no Capítulo 2 — resolvido ao instalar a "
                 "biblioteca `libxcb-cursor0`."),

    h2("Criação de formulários"),
    p("O fluxo de trabalho é: escolher o modelo (*Widget*, *Dialog with Buttons*, *Main Window*), arrastar os "
      "widgets, **aplicar layouts** e dar a cada widget relevante um `objectName` significativo — é por esse nome "
      "que o código Python acessará o widget. A Listagem 11.1 é o arquivo `.ui` resultante, legível e versionável."),
    lst("c11_dados_poco.ui", "Arquivo .ui produzido pelo Qt Designer (XML)", lang="xml"),
    h3("Layouts no Designer"),
    p("No Designer, seleciona-se um grupo de widgets (ou o formulário inteiro) e aplica-se um layout pela barra de "
      "ferramentas. Um formulário sem layout no nível superior é o erro mais comum: os widgets não acompanham o "
      "redimensionamento. O inspetor de objetos sinaliza esse caso com um ícone de alerta sobre o widget raiz."),
    h3("Conexões de sinais e slots no Designer"),
    p("O editor de sinais/slots permite conectar, por exemplo, `rejected()` da caixa de botões a `close()` do "
      "formulário. Para lógica da aplicação, porém, prefira conectar no código Python: as conexões ficam visíveis, "
      "testáveis e versionadas junto da lógica."),
    h3("Ordem de tabulação e buddies"),
    p("O modo *Edit Tab Order* define a ordem do foco com a tecla Tab (no XML, o bloco `<tabstops>`). O modo *Edit "
      "Buddies* associa rótulos a campos (propriedade `buddy`), habilitando atalhos Alt+letra definidos com `&` no "
      "texto do rótulo, como `&Nome do poço`."),

    h2("Carga dinâmica: uic.loadUi()"),
    p("`uic.loadUi(arquivo, base)` lê o XML em tempo de execução e cria os widgets **dentro** do objeto `base`, "
      "transformando cada `objectName` em atributo. É a forma mais rápida de iterar: altera-se o `.ui` e "
      "reexecuta-se o programa, sem etapa de geração."),
    lst("c11_loadui.py", "Carga dinâmica de um arquivo .ui com uic.loadUi()"),
    out("c11_loadui"),
    note("DICA", "Localize o `.ui` relativamente ao módulo (`Path(__file__).with_name(...)`), e não ao diretório "
                 "de trabalho: assim o programa funciona independentemente de onde for executado."),

    h2("Geração de código: pyuic6"),
    p("A alternativa é converter o `.ui` em um módulo Python com `pyuic6 formulario.ui -o ui_formulario.py`. O "
      "código gerado contém uma classe `Ui_<NomeDoFormulário>` com o método `setupUi(widget)`. As opções mais "
      "úteis são `-x` (acrescenta código para executar e exibir o formulário), `-p` (apenas pré-visualiza) e "
      "`-o` (arquivo de saída); a lista completa está no Anexo D."),
    lst("ui_dados_poco.py", "Código gerado pelo pyuic6 6.12.0 a partir da Listagem 11.1", allow_long=True),
    p("O arquivo é reproduzido exatamente como gerado; por isso algumas linhas longas aparecem quebradas na página."),
    note("ATENÇÃO", "Nunca edite o arquivo gerado: ele é sobrescrito a cada execução do `pyuic6`, como avisa o "
                    "próprio cabeçalho. Toda a lógica fica em outro módulo, que importa a classe `Ui_...`."),
    tab("uic.loadUi() versus pyuic6", ["Critério", "uic.loadUi()", "pyuic6"],
        [["Etapa de build", "Nenhuma", "Gerar o .py a cada mudança no .ui"],
         ["Autocompletar e verificação de tipos", "Limitados (atributos criados em tempo de execução)", "Completos (atributos declarados no código)"],
         ["Empacotamento", "O .ui precisa ser incluído como arquivo de dados", "Apenas código Python"],
         ["Indicado para", "Prototipagem e iteração rápida", "Produção e projetos grandes"]],
        [2600, 3235, 3236]),

    h2("Padrões de integração: composição versus herança"),
    p("A classe gerada pode ser usada de duas formas. Na **composição**, o formulário guarda uma instância em "
      "`self.ui` e acessa os widgets como `self.ui.campoNome` — o espaço de nomes da classe fica limpo e fica "
      "claro o que veio do Designer. Na **herança múltipla**, a classe herda de `QWidget` e de `Ui_...`, e os "
      "widgets viram atributos diretos. Este manual recomenda a composição."),
    lst("c11_composicao_ui.py", "Código gerado pelo pyuic6: integração por composição e por herança múltipla"),
    out("c11_composicao_ui"),

    h2("Promoção de widgets personalizados"),
    p("Para usar no Designer um widget próprio (por exemplo, um `QDoubleSpinBox` já configurado para pressões), "
      "insere-se o widget base e usa-se *Promote to…*, informando o nome da classe e o arquivo de cabeçalho. No "
      "PyQt6, o cabeçalho é convertido em nome de módulo: `c11_widgets.h` → módulo `c11_widgets`; "
      "`pacote/campos.h` → `pacote.campos`."),
    lst("c11_widgets.py", "Widget personalizado usado por promoção no Qt Designer"),
    lst("c11_promovido.ui", "Trecho <customwidgets> de um .ui com widget promovido", lang="xml"),
    lst("c11_promocao.py", "Promoção de widget: o .ui referencia CampoPressao, definido em c11_widgets.py"),
    out("c11_promocao"),

    h2("Plugins para o Designer: módulo QtDesigner"),
    p("O módulo QtDesigner permite escrever plugins que fazem um widget Python aparecer na caixa de widgets do "
      "Designer, com pré-visualização real. A classe do plugin herda de `QPyDesignerCustomWidgetPlugin` e descreve o "
      "widget (nome, grupo, ícone, XML inicial)."),
    lst("c11_plugin.py", "Plugin de widget para o Qt Designer escrito em Python (módulo QtDesigner)"),
    out("c11_plugin"),
    note("ATENÇÃO", "Para o Designer carregar plugins escritos em Python, ele precisa do plugin de interface do "
                    "PyQt6 (a biblioteca que hospeda o interpretador Python dentro do Designer). Esse componente "
                    "**não faz parte** das wheels PyQt6 6.12.0 do PyPI (não há a pasta `plugins/designer` no pacote "
                    "PyQt6-Qt6), e o `pyside6-designer` carrega apenas plugins PySide6. Na prática, com as wheels "
                    "do PyPI, use a **promoção** (Seção 11.6), que atende à grande maioria dos casos."),

    h2("Exercícios do capítulo"),
    nl("Crie no Designer um diálogo de ensaio com `QFormLayout` e `QDialogButtonBox` e carregue-o com `loadUi`.",
       "Gere o mesmo diálogo com `pyuic6` e integre-o por composição, conectando os sinais no código.",
       "Promova um `QLineEdit` para uma classe `CampoTag` que converte o texto para maiúsculas.",
       "Explique por que editar o arquivo gerado pelo `pyuic6` é uma má prática e como organizar o projeto para evitá-la."),
)

CAP12 = flat(
    ch("Estilos, temas e aparência", ST_INT, [
        "Escolher e combinar estilos, paletas e folhas de estilo.",
        "Implementar temas claro e escuro sincronizados com o sistema.",
        "Gerenciar fontes, ícones e telas High-DPI.",
    ]),
    p("A aparência de uma aplicação Qt resulta de três camadas, da mais geral para a mais específica: o **estilo** "
      "(`QStyle`), que desenha os elementos; a **paleta** (`QPalette`), que define as cores; e as **folhas de "
      "estilo** (QSS), que sobrescrevem detalhes com sintaxe semelhante ao CSS."),
    h2("QStyle e QStyleFactory"),
    h3("Estilos disponíveis por plataforma (Fusion, Windows, windowsvista, windows11, macOS)"),
    p("`QStyleFactory.keys()` lista os estilos disponíveis no ambiente. **Fusion** e **Windows** existem em todas "
      "as plataformas; os estilos nativos dependem do sistema: `windowsvista` e `windows11` no Windows (este a "
      "partir do Qt 6.7) e `macOS` no macOS. Por padrão, o Qt escolhe o estilo nativo. O **Fusion** é a escolha "
      "habitual quando se deseja aparência idêntica em todos os sistemas e controle total das cores."),
    h3("QProxyStyle para personalizações pontuais"),
    p("`QProxyStyle` herda o comportamento de um estilo base e permite alterar apenas métricas, dicas ou a pintura "
      "de elementos específicos — sem reescrever um estilo inteiro e sem os efeitos colaterais de uma folha de "
      "estilo."),
    lst("c12_estilos.py", "QStyleFactory, troca de estilo e QProxyStyle para um ajuste pontual"),
    out("c12_estilos"),
    p("A saída lista apenas Windows e Fusion porque o exemplo foi executado em Linux sem plugins de estilo "
      "nativo; no Windows apareceriam também os estilos nativos."),

    h2("QPalette"),
    h3("Grupos e papéis de cor"),
    p("Uma paleta associa cores a **papéis** (`ColorRole`: `Window`, `WindowText`, `Base`, `Text`, `Button`, "
      "`ButtonText`, `Highlight`, `PlaceholderText`, `Accent`…) em três **grupos** (`ColorGroup`): `Active`, "
      "`Inactive` (janela sem foco) e `Disabled`. Um tema escuro consistente define os papéis principais e as cores "
      "do grupo `Disabled`, como na listagem a seguir."),
    lst("c12_paleta.py", "QPalette: tema escuro programático e esquema de cores do sistema"),
    out("c12_paleta"),
    h3("Esquema de cores do sistema: QStyleHints.colorScheme() e Qt.ColorScheme"),
    p("`app.styleHints().colorScheme()` informa se o sistema está em modo claro ou escuro (`Qt.ColorScheme.Light`, "
      "`Dark` ou `Unknown`), e o sinal `colorSchemeChanged` avisa quando o usuário troca o tema do sistema — o "
      "momento de reaplicar paleta e folha de estilo. Desde o Qt 6.8, `setColorScheme()` permite à aplicação "
      "solicitar um esquema específico; o efeito depende do suporte da plataforma. No ambiente de teste da "
      "listagem (plataforma *offscreen*), o esquema é `Unknown` e a solicitação não gera mudança."),

    h2("Qt Style Sheets (QSS)"),
    p("Folhas de estilo aplicam regras do tipo `seletor { propriedade: valor; }` à aplicação inteira "
      "(`app.setStyleSheet`) ou a um widget e seus filhos (`widget.setStyleSheet`). São ideais para temas e "
      "identidade visual. O Anexo C reúne seletores, pseudo-estados, subcontroles e propriedades."),
    lst("c12_temas.py", "Qt Style Sheets: temas claro e escuro, seletores, subcontroles e pseudo-estados"),
    out("c12_temas"),
    img("Mesma interface com tema claro e tema escuro", "f12_1_temas.png"),
    h3("Sintaxe e seletores"),
    tab("Seletores de Qt Style Sheets mais usados", ["Seletor", "Exemplo", "Seleciona"],
        [["Tipo", "`QPushButton`", "Instâncias da classe e subclasses"],
         ["Classe exata", "`.QPushButton`", "Apenas a classe, sem subclasses"],
         ["ID", "`QPushButton#primario`", "O widget com objectName = primario"],
         ["Propriedade", "`QPushButton[perigoso=\"true\"]`", "Widgets cuja propriedade (inclusive dinâmica) tem o valor"],
         ["Descendente", "`QGroupBox QLabel`", "QLabel em qualquer nível dentro de um QGroupBox"],
         ["Filho direto", "`QGroupBox > QLabel`", "QLabel filho imediato de um QGroupBox"]],
        [1900, 3171, 4000]),
    h3("Subcontroles e pseudo-estados"),
    p("Widgets compostos expõem **subcontroles** com `::` — o título de um `QGroupBox` (`::title`), a seta de um "
      "`QComboBox` (`::drop-down`), a alça de um `QSlider` (`::handle`). **Pseudo-estados** com `:` aplicam regras "
      "conforme o estado: `:hover`, `:pressed`, `:focus`, `:checked`, `:disabled`; a negação usa `!` "
      "(`:!enabled`)."),
    h3("Modelo de caixa: margin, border, padding"),
    p("Como no CSS, cada widget estilizado tem margem externa (`margin`), borda (`border`), espaçamento interno "
      "(`padding`) e conteúdo. Ao estilizar um widget composto, defina o conjunto completo de propriedades "
      "relacionadas: ao mudar a borda de um `QComboBox`, por exemplo, o estilo deixa de desenhá-lo nativamente e os "
      "subcontroles também precisam de regras."),
    note("ATENÇÃO", "Propriedades dinâmicas usadas em seletores são avaliadas quando o estilo é aplicado. Ao alterar "
                    "a propriedade depois, chame `style().unpolish(w)` e `style().polish(w)`, como na Listagem 12.3, "
                    "para que o widget seja redesenhado com as regras novas. Propriedades com nome errado geram o "
                    "aviso *Unknown property* em tempo de execução."),
    h3("Organização de temas em arquivos .qss"),
    p("Em projetos reais, mantenha cada tema em um arquivo `.qss` em `resources/`, com as cores parametrizadas "
      "(como os dicionários `CLARO` e `ESCURO` da listagem) ou geradas a partir de um único arquivo-modelo. Aplique "
      "o tema no nível da aplicação, uma única vez, e reaplique ao receber `colorSchemeChanged`."),

    h2("Fontes: QFont, QFontDatabase e fontes embarcadas"),
    p("`QFont` descreve família, tamanho (`pointSize`), peso e estilo. Para garantir a mesma tipografia em todas as "
      "máquinas, distribua o arquivo da fonte com a aplicação e registre-o com "
      "`QFontDatabase.addApplicationFont()`, que retorna um identificador (−1 em caso de falha) cujas famílias são "
      "obtidas por `applicationFontFamilies()`. Verifique a licença da fonte antes de distribuí-la."),
    lst("c12_fontes_icones.py", "Fontes embarcadas (QFontDatabase) e ícones (QIcon a partir de SVG)"),
    out("c12_fontes_icones"),

    h2("Ícones: QIcon, QPixmap e ícones de tema"),
    p("`QIcon` representa um ícone em vários tamanhos, modos (`Normal`, `Disabled`, `Active`, `Selected`) e estados "
      "(`On`/`Off`). Prefira **SVG**: um único arquivo gera pixmaps nítidos em qualquer tamanho e fator de escala. "
      "`QIcon.fromTheme()` busca ícones do tema do sistema — no Qt 6.7 ou superior, com o enum padronizado "
      "`QIcon.ThemeIcon` — e aceita um ícone alternativo para plataformas sem tema."),

    h2("High-DPI"),
    h3("devicePixelRatio e imagens @2x"),
    p("Em telas de alta densidade, o Qt trabalha em **pixels lógicos** e converte para pixels físicos pelo "
      "`devicePixelRatio` (por exemplo, 1,5 em uma escala de 150 %). Pixmaps desenhados pelo programa devem ser "
      "criados com o tamanho físico e marcados com `setDevicePixelRatio()`; arquivos PNG podem ter variantes "
      "`@2x` (como `icone@2x.png`), que o Qt escolhe automaticamente ao carregar `icone.png`."),
    h3("Política de arredondamento do fator de escala"),
    p("`QGuiApplication.setHighDpiScaleFactorRoundingPolicy()` — chamada **antes** de criar a aplicação — decide se "
      "fatores fracionários (125 %, 150 %) são usados como estão (`PassThrough`, padrão no Qt 6) ou arredondados "
      "(`Round`, `Ceil`, `Floor`, `RoundPreferFloor`). Arredondar evita linhas finas desiguais em interfaces "
      "desenhadas pixel a pixel, ao custo de tamanhos ligeiramente diferentes do configurado pelo usuário."),
    lst("c12_highdpi.py", "High-DPI: política de arredondamento e pixmaps com devicePixelRatio"),
    out("c12_highdpi"),

    h2("Exercícios do capítulo"),
    nl("Crie um `QProxyStyle` que aumente a altura dos itens de menu e aplique-o à janela do Capítulo 8.",
       "Converta os temas da Listagem 12.3 em arquivos `.qss` carregados do disco e alterne-os por uma `QAction`.",
       "Faça a aplicação reagir a `colorSchemeChanged` trocando automaticamente entre os temas claro e escuro.",
       "Estilize o `QSlider` com subcontroles `::groove` e `::handle`, incluindo o pseudo-estado `:hover`."),
)

CAP13 = flat(
    ch("Recursos, configurações e internacionalização", ST_INT, [
        "Empacotar e localizar recursos sem depender de pyrcc.",
        "Persistir preferências com QSettings e caminhos padrão.",
        "Traduzir a interface com QTranslator e o Qt Linguist.",
    ]),
    h2("Recursos da aplicação no PyQt6"),
    p("Recursos são os arquivos que acompanham o código: ícones, folhas de estilo, fontes, traduções, modelos. No "
      "C++ e no PySide6 é comum compilá-los com o `rcc`; o PyQt6 **não inclui** o `pyrcc6`. A abordagem recomendada "
      "é distribuí-los como arquivos de dados do pacote e localizá-los em tempo de execução."),
    h3("Caminhos relativos ao pacote e importlib.resources"),
    p("Calcule os caminhos a partir do módulo (`Path(__file__).resolve().parent`) ou use `importlib.resources.files("
      "\"calc_engenharia\")`, que funciona também quando o pacote é instalado como wheel. Declare os arquivos de "
      "dados no `pyproject.toml` (por exemplo, `[tool.setuptools.package-data]`) para que sejam incluídos na "
      "distribuição."),
    h3("QDir.addSearchPath() e prefixos de busca"),
    p("`QDir.addSearchPath(\"icones\", pasta)` registra um prefixo: a partir daí, `QIcon(\"icones:valvula.svg\")`, "
      "e `QFile(\"icones:...\")` encontram o arquivo, e o código não precisa conhecer o caminho real."),
    lst("c13_recursos.py", "Recursos sem pyrcc: caminhos relativos ao pacote e prefixos de busca do QDir"),
    out("c13_recursos"),
    note("ATENÇÃO", "Evite referências a recursos compilados (`:/caminho`, arquivos `.qrc`) em formulários `.ui` usados "
                    "com o PyQt6: como não há `pyrcc6`, esses caminhos não serão resolvidos. Use prefixos de busca ou "
                    "defina os ícones no código."),

    h2("QSettings"),
    h3("Formatos nativo e INI"),
    p("No formato nativo (padrão), o `QSettings` usa o Registro no Windows, arquivos `.plist` no macOS e INI no "
      "Linux. O formato **INI** em arquivo explícito é útil para configurações portáteis, versionáveis ou "
      "compartilhadas. Em ambos, as chaves podem ser agrupadas (`beginGroup`) e listas são gravadas com "
      "`beginWriteArray`."),
    lst("c13_settings.py", "QSettings em formato INI: tipos, grupos, arrays e valores padrão"),
    out("c13_settings"),
    p("A saída demonstra um ponto que causa erros frequentes: lido de um arquivo INI em uma nova sessão, "
      "`casas_decimais` volta como **texto** (`'2'`). Sempre informe o tipo esperado com o argumento `type=` de "
      "`value()` (`type=int`, `type=bool`, `type=float`) e um valor padrão para chaves ausentes."),
    h3("Escopo de usuário e de sistema"),
    p("`QSettings.Scope.UserScope` (padrão) grava no perfil do usuário; `SystemScope` lê configurações comuns a "
      "todos os usuários, normalmente definidas pelo instalador ou pela TI. Na leitura em escopo de usuário, o Qt "
      "recorre às chaves de sistema quando a de usuário não existe."),

    h2("Sistema de arquivos: QStandardPaths, QDir, QFile e QFileInfo"),
    p("Nunca grave dados ao lado do executável: em instalações corporativas essa pasta é somente leitura. "
      "`QStandardPaths.writableLocation()` devolve, para cada finalidade, a pasta correta em cada sistema — dados da "
      "aplicação, configuração, cache, documentos, temporários. Os caminhos incluem organização e nome da aplicação "
      "definidos no `QApplication`."),
    lst("c13_caminhos.py", "QStandardPaths, QDir e QFileInfo: onde guardar cada tipo de arquivo"),
    out("c13_caminhos"),
    p("Os caminhos da saída correspondem a Linux (usuário `root` no ambiente de teste). No Windows, "
      "`AppDataLocation` aponta para `%APPDATA%\\Engenharia\\CalcEng`; no macOS, para "
      "`~/Library/Application Support/Engenharia/CalcEng`."),

    h2("Internacionalização (i18n)"),
    p("Internacionalizar significa preparar o código para ser traduzido sem alterações. A convenção recomendada é "
      "escrever os textos-fonte em **inglês** no código e fornecer as traduções (inclusive para o português) em "
      "arquivos separados. A Figura 13.1 mostra o fluxo completo, que foi executado de ponta a ponta para produzir "
      "as listagens desta seção."),
    img("Fluxo de tradução de uma aplicação PyQt6", "f13_1_traducao.png"),
    h3("tr() e QCoreApplication.translate()"),
    p("Em subclasses de `QObject`, marque textos com `self.tr(\"...\")`: o contexto da tradução é o nome da classe. "
      "Fora de classes, use `QCoreApplication.translate(\"Contexto\", \"texto\")`. Para valores variáveis, use "
      "marcadores `%1`, `%2` no texto-fonte e substitua-os depois da tradução — a ordem das palavras muda entre "
      "idiomas, e o tradutor pode reposicionar os marcadores."),
    lst("c13_traducao.py", "Internacionalização: tr(), QTranslator da aplicação e traduções do próprio Qt"),
    h3("Extração com pylupdate6 e compilação com lrelease"),
    p("O `pylupdate6` varre os arquivos `.py` (e `.ui`) e cria ou atualiza o arquivo `.ts` (XML), preservando "
      "traduções existentes: `pylupdate6 c13_traducao.py --ts c13_calceng_pt_BR.ts`. O tradutor preenche o `.ts` no "
      "**Qt Linguist**, e o `lrelease` compila o resultado em `.qm`, o formato binário carregado pela aplicação. O "
      "PyQt6 não inclui `lrelease` nem Linguist; ambos fazem parte das ferramentas do Qt (instalador oficial, "
      "pacotes da distribuição ou o `pyside6-lrelease` do PySide6, usado aqui)."),
    lst("c13_calceng_pt_BR.ts", "Arquivo .ts gerado pelo pylupdate6 e traduzido", lang="xml"),
    note("NOTA", "O `pylupdate6` não grava o idioma de destino no `.ts`; o atributo `language=\"pt_BR\"` da "
                 "Listagem 13.5 foi definido na etapa de tradução, como faria o Qt Linguist."),
    h3("QTranslator e troca de idioma em tempo de execução"),
    p("Um `QTranslator` carrega um `.qm` e é instalado na aplicação com `installTranslator()`. São necessários "
      "**dois tradutores**: o da aplicação e o dos textos internos do Qt (`qtbase_pt_BR.qm`, distribuído na pasta "
      "`translations` do PyQt6-Qt6 e localizado com `QLibraryInfo`), que traduz botões padrão e diálogos — "
      "resolvendo a observação feita no Capítulo 9."),
    out("c13_traducao"),
    p("Após instalar um tradutor, os textos já exibidos **não mudam sozinhos**: é preciso redefini-los. O padrão "
      "profissional é concentrar os textos em um método `retraduzir()` e chamá-lo no construtor e ao receber "
      "`QEvent.Type.LanguageChange` em `changeEvent()`, que o Qt envia a todos os widgets quando um tradutor é "
      "instalado ou removido."),
    h3("QLocale: números, datas e moedas"),
    p("Traduzir textos não basta: números, datas e moedas seguem convenções regionais. `QLocale` formata e "
      "interpreta valores conforme o idioma e o território."),
    lst("c13_locale.py", "QLocale: formatação e leitura de números, datas e moeda por idioma"),
    out("c13_locale"),
    p("Note que `toDouble(\"1234.5\")` falha em pt_BR, pois o ponto é separador de milhar — o mesmo fenômeno visto "
      "com `QDoubleValidator` no Capítulo 6. Para arquivos de dados, use sempre um formato invariável "
      "(`QLocale.c()` ou o `float()` do Python) e reserve o locale do usuário para a interface."),

    h2("Logging: qInstallMessageHandler() e o módulo logging"),
    p("O Qt emite avisos internos (por exemplo, sobre pintura inválida ou propriedades desconhecidas em QSS) pelo "
      "seu sistema de mensagens. `qInstallMessageHandler()` permite redirecionar essas mensagens para o módulo "
      "`logging` do Python, unificando o registro da aplicação. `QLoggingCategory.setFilterRules()` silencia ou "
      "habilita categorias específicas."),
    lst("c13_log.py", "Mensagens do Qt redirecionadas ao módulo logging (qInstallMessageHandler)"),
    out("c13_log"),
    note("ATENÇÃO", "Verificado com o PyQt6 6.12.0: `qWarning()`, `qDebug()` e afins aceitam apenas texto ASCII — "
                    "uma mensagem com acentos lança `UnicodeEncodeError`, independentemente do locale do sistema. "
                    "Para mensagens da aplicação em português, use diretamente o módulo `logging`."),

    h2("Exercícios do capítulo"),
    nl("Organize os recursos do projeto da Figura 2.1 com `QDir.addSearchPath` para ícones, estilos e traduções.",
       "Grave e restaure em `QSettings` (INI) a lista dos cinco arquivos abertos mais recentemente.",
       "Traduza a janela do Capítulo 8 para inglês e português e implemente a troca de idioma em tempo de "
       "execução com `changeEvent`.",
       "Configure o `logging` para gravar em arquivo, em `AppDataLocation`, as mensagens do Qt e da aplicação."),
)

CAP14 = flat(
    ch("Arquitetura Model/View", ST_INT, [
        "Compreender a separação entre modelo, visão e delegado.",
        "Implementar modelos personalizados de lista, tabela e árvore.",
        "Ordenar, filtrar e editar dados com proxies e delegados.",
    ]),
    h2("Conceitos da arquitetura Model/View"),
    p("Em aplicações de engenharia, os dados raramente cabem em meia dúzia de campos: são listas de ensaios, tabelas "
      "de medições, árvores de equipamentos. A arquitetura Model/View do Qt separa **onde os dados estão** (o "
      "modelo) de **como são exibidos** (a visão) e **como cada célula é desenhada e editada** (o delegado). O "
      "modelo não sabe nada de widgets; a visão pede apenas o que está visível, o que permite exibir milhões de "
      "linhas com fluidez."),
    img("Arquitetura Model/View do Qt", "f14_1_modelview.png"),
    h3("QModelIndex e QPersistentModelIndex"),
    p("Um `QModelIndex` identifica um item por linha, coluna e pai (para hierarquias). Índices são **temporários**: "
      "deixam de valer quando o modelo muda de estrutura. Para guardar uma referência que acompanhe inserções e "
      "remoções, use `QPersistentModelIndex`."),
    h3("Papéis de dados (Qt.ItemDataRole)"),
    p("Cada item fornece dados diferentes conforme o **papel** solicitado pela visão. Com isso, um único método "
      "`data()` define texto, valor de edição, alinhamento, cores, dicas e estado de marcação."),
    tab("Papéis de dados mais usados (Qt.ItemDataRole)", ["Papel", "Tipo esperado", "Uso"],
        [["DisplayRole", "str (ou número)", "Texto exibido na célula"],
         ["EditRole", "valor do editor", "Valor numérico/bruto oferecido ao editor e gravado por setData()"],
         ["ToolTipRole", "str", "Dica ao repousar o mouse"],
         ["TextAlignmentRole", "Qt.AlignmentFlag", "Alinhamento do texto (números à direita)"],
         ["ForegroundRole / BackgroundRole", "QColor ou QBrush", "Cor do texto / do fundo da célula"],
         ["FontRole", "QFont", "Fonte da célula (negrito em totais, por exemplo)"],
         ["DecorationRole", "QIcon, QPixmap ou QColor", "Ícone à esquerda do texto"],
         ["CheckStateRole", "Qt.CheckState", "Caixa de marcação na célula"],
         ["UserRole (e acima)", "qualquer", "Dados próprios da aplicação, sem exibição direta"]],
        [3000, 2500, 3571]),

    h2("Widgets de conveniência"),
    p("`QListWidget`, `QTreeWidget` e `QTableWidget` combinam visão e um modelo interno baseado em itens. São "
      "práticos para coleções pequenas, preenchidas uma vez; para dados que vêm de outra fonte ou mudam com "
      "frequência, prefira um modelo próprio (Seção 14.4)."),
    lst("c14_conveniencia.py", "Widgets de conveniência: QListWidget, QTreeWidget e QTableWidget"),
    out("c14_conveniencia"),
    h3("QListWidget e QListWidgetItem"),
    p("Cada linha é um `QListWidgetItem`, com texto, ícone, dados por papel e *flags* — como "
      "`ItemIsUserCheckable`, que acrescenta a caixa de marcação usada na listagem."),
    h3("QTreeWidget e QTreeWidgetItem"),
    p("Itens criados com outro item como pai formam a hierarquia; `setHeaderLabels()` define as colunas e "
      "`expandAll()` expande a árvore."),
    h3("QTableWidget e QTableWidgetItem"),
    p("Grava os valores com `setData(DisplayRole, valor)` em vez de `setText(str(valor))`: o tipo original é "
      "preservado e a ordenação passa a ser **numérica**, como mostra a saída (310,5 antes de 345,0)."),

    h2("Modelos prontos"),
    lst("c14_modelos_prontos.py", "Modelos prontos: QStringListModel e QStandardItemModel"),
    out("c14_modelos_prontos"),
    h3("QStringListModel"),
    p("Modelo de lista de textos, editável, ideal para alimentar `QListView`, `QComboBox` ou `QCompleter`."),
    h3("QStandardItemModel e QStandardItem"),
    p("Modelo genérico de itens (lista, tabela ou árvore) que dispensa subclasses. Cada `QStandardItem` guarda dados "
      "por papel e pode ter filhos. É um bom meio-termo entre os widgets de conveniência e um modelo próprio."),
    h3("QFileSystemModel"),
    p("Expõe o sistema de arquivos como modelo hierárquico, com leitura **assíncrona** em uma thread interna: ao "
      "definir `setRootPath()`, os itens só ficam disponíveis após o sinal `directoryLoaded`. Filtros de nome "
      "(`setNameFilters`) e de tipo (`setFilter`) controlam o que aparece."),
    lst("c14_filesystem.py", "QFileSystemModel: carregamento assíncrono de diretórios (sinal directoryLoaded)"),
    out("c14_filesystem"),
    p("Com `setNameFilterDisables(False)`, os itens que não casam com `*.csv` são ocultados em vez de apenas "
      "desabilitados — e, nessa configuração, a subpasta `fotos` também deixou de aparecer."),
    h3("QRangeModel (Qt 6.10+)"),
    p("O Qt 6.10 introduziu `QRangeModel`, que expõe uma estrutura de dados existente como modelo. No PyQt6 6.12, "
      "ele é acessível por meio das classes `QPySequenceRange` e `QPyTableRange`, que envolvem listas Python."),
    note("ATENÇÃO", "Nos testes realizados para este manual com PyQt6 6.12.0, `QRangeModel` provocou falha de "
                    "segmentação (encerramento do processo) ao associar o modelo a uma `QTableView` e, com faixas "
                    "editáveis (`editable=True`), ao encerrar o programa; com `editable=False` e sem visão associada, "
                    "funcionou. Por isso este manual não o utiliza: para dados editáveis, use um "
                    "`QAbstractTableModel` próprio (Seção 14.4.2). Reavalie o recurso em versões futuras do PyQt6."),

    h2("Modelos personalizados"),
    p("Um modelo próprio é a forma profissional de expor dados da aplicação: a lista de objetos continua sendo a "
      "fonte da verdade, e o modelo apenas a traduz para o vocabulário do Qt. A escolha da classe base depende da "
      "forma dos dados."),
    h3("QAbstractListModel"),
    p("Para listas de uma coluna: implemente `rowCount()` e `data()` (e `setData()`/`flags()` para edição). A "
      "própria classe base fornece `index()`, `parent()` e `columnCount()`."),
    h3("QAbstractTableModel"),
    p("Para tabelas: implemente `rowCount()`, `columnCount()` e `data()`; opcionalmente `headerData()`, `flags()`, "
      "`setData()`, `insertRows()` e `removeRows()`. A Listagem 14.4 implementa todos esses métodos sobre uma "
      "lista de objetos `Ensaio`."),
    lst("c14_modelo_tabela.py", "Modelo de tabela personalizado: leitura, edição, papéis e inserção/remoção"),
    out("c14_modelo_tabela"),
    h4("rowCount(), columnCount(), data() e headerData()"),
    p("`rowCount()` e `columnCount()` devem retornar 0 quando recebem um pai válido — em uma tabela, nenhum item "
      "tem filhos. `data()` responde por papel e retorna `None` para papéis que não trata; `headerData()` fornece "
      "os títulos das colunas."),
    h4("Edição: flags() e setData()"),
    p("`flags()` acrescenta `ItemIsEditable` às flags herdadas. `setData()` valida o valor, atualiza o objeto e "
      "**emite `dataChanged`**; retornar `False` recusa a edição — a pressão −10 da saída foi rejeitada sem alterar "
      "o modelo."),
    h4("Inserção e remoção: beginInsertRows()/endInsertRows() e afins"),
    p("Toda mudança de estrutura deve ser envolvida pelo par `begin...`/`end...` correspondente (`beginInsertRows`, "
      "`beginRemoveRows`, `beginMoveRows`, `beginInsertColumns`…), com os índices **inclusivos** das linhas "
      "afetadas. É assim que visões, proxies e seleções se mantêm consistentes."),
    h4("Notificações: dataChanged, layoutChanged e resets"),
    p("`dataChanged(topo, base, papéis)` informa alteração de valores; `layoutChanged` informa reordenação sem "
      "inserções; `beginResetModel()`/`endResetModel()` informam que tudo mudou (use com parcimônia, pois a visão "
      "perde seleção e rolagem)."),
    note("ATENÇÃO", "Emita `dataChanged` apenas para o que realmente mudou. Na primeira versão da Listagem 14.4, "
                    "cada edição emitia `dataChanged` para a linha inteira; com isso, o `QDataWidgetMapper` da Seção "
                    "14.9 recarregava os campos do formulário no meio da gravação e o valor editado se perdia (a "
                    "pressão voltava de 315,0 para 310,5). A versão final emite a linha inteira apenas quando muda o "
                    "estado *Aprovado*, que altera a cor de todas as células."),
    p("O `QAbstractItemModelTester` (módulo QtTest), instanciado logo após o modelo, verifica dezenas de regras de "
      "consistência a cada operação e interrompe o programa ao detectar uma violação — os modelos das Listagens "
      "14.4 e 14.5 foram exercitados sob ele."),
    h3("QAbstractItemModel para estruturas hierárquicas"),
    p("Para árvores, implementa-se também `index()` e `parent()`. A técnica usual guarda em cada índice um ponteiro "
      "para o nó Python (`createIndex(linha, coluna, no)` e `index.internalPointer()`), e cada nó conhece seu pai e "
      "sua posição entre os irmãos."),
    lst("c14_modelo_arvore.py", "Modelo hierárquico com QAbstractItemModel: index(), parent() e internalPointer"),
    out("c14_modelo_arvore"),
    note("ATENÇÃO", "O nó precisa continuar referenciado por estruturas Python (a lista `filhos` do pai) enquanto o "
                    "modelo existir: o índice guarda apenas um ponteiro, que não mantém o objeto vivo. Note também "
                    "`eq=False` na dataclass: a comparação por identidade é necessária para que `filhos.index(self)` "
                    "encontre o nó correto."),

    h2("Visões"),
    h3("QListView, QTableView, QTreeView e QColumnView"),
    p("Todas derivam de `QAbstractItemView` e compartilham seleção, edição (`setEditTriggers`), arraste e rolagem. "
      "`QTableView` oferece `setSortingEnabled`, `setAlternatingRowColors` e redimensionamento de seções; "
      "`QTreeView` acrescenta expansão, indentação e colunas; `QColumnView` apresenta hierarquias em colunas "
      "sucessivas."),
    h3("QHeaderView"),
    p("Os cabeçalhos são widgets próprios (`horizontalHeader()`, `verticalHeader()`), com modos de "
      "redimensionamento por seção (`setSectionResizeMode`: `Interactive`, `Stretch`, `ResizeToContents`, "
      "`Fixed`), ordenação por clique e `saveState()`/`restoreState()` para lembrar larguras e ordem das colunas."),

    h2("Seleção: QItemSelectionModel"),
    p("A seleção é um objeto separado (`view.selectionModel()`), que pode ser compartilhado entre visões. Seus sinais "
      "`currentChanged`, `currentRowChanged` e `selectionChanged` são a forma correta de reagir à linha ativa — por "
      "exemplo, para preencher um formulário de detalhes, como na Listagem 14.8."),

    h2("Delegados: QStyledItemDelegate"),
    p("O delegado desenha cada célula e cria o editor quando o usuário inicia a edição. O `QStyledItemDelegate` "
      "padrão escolhe o editor pelo tipo do valor de `EditRole` (`QSpinBox` para inteiros, `QDoubleSpinBox` para "
      "`float`, `QLineEdit` para texto, `QCheckBox` para booleanos)."),
    lst("c14_delegado.py", "Delegado personalizado: editor numérico com limites e texto formatado"),
    out("c14_delegado"),
    img("QTableView com o modelo da Listagem 14.4 e o delegado da Listagem 14.6", "f14_2_tabela.png", width_cm=11.0),
    h3("Editores personalizados"),
    p("Sobrescreva `createEditor()` (cria e configura o editor), `setEditorData()` (copia o valor do modelo para o "
      "editor), `setModelData()` (grava o valor do editor no modelo) e `updateEditorGeometry()`. Na saída, o valor "
      "2000 foi limitado ao máximo do editor (1035 bar) antes de chegar ao modelo."),
    h3("Pintura personalizada de células"),
    p("`displayText()` muda apenas o texto; para desenhos completos (barras de progresso, ícones de status, "
      "gráficos em miniatura), sobrescreva `paint(painter, option, index)` usando as técnicas do Capítulo 17 e "
      "`sizeHint()` para informar o tamanho desejado. A Figura 14.2 mostra o efeito combinado do modelo (cor dos "
      "reprovados, alinhamento) e do delegado (unidade *bar*)."),

    h2("Modelos proxy"),
    p("Um proxy fica entre o modelo e a visão e transforma o que a visão enxerga — ordem, filtro, forma — sem "
      "alterar os dados originais. `mapToSource()` e `mapFromSource()` convertem índices entre os dois lados."),
    lst("c14_proxy.py", "Modelos proxy: ordenação/filtragem, transposição e concatenação"),
    out("c14_proxy"),
    h3("QSortFilterProxyModel"),
    p("Ordena por coluna e papel (`setSortRole(EditRole)` garante ordenação numérica) e filtra por expressão "
      "regular (`setFilterRegularExpression`) em uma coluna. Para regras próprias, sobrescreva "
      "`filterAcceptsRow()` — combinando com a implementação base, como na listagem — e chame "
      "`invalidateRowsFilter()` quando os critérios mudarem."),
    h3("QIdentityProxyModel, QTransposeProxyModel e QConcatenateTablesProxyModel"),
    p("`QIdentityProxyModel` repassa tudo e serve de base para alterar apenas alguns papéis (por exemplo, formatar "
      "unidades). `QTransposeProxyModel` troca linhas por colunas. `QConcatenateTablesProxyModel` empilha vários "
      "modelos com as mesmas colunas, como ensaios de duas fontes diferentes."),

    h2("QDataWidgetMapper"),
    p("Liga colunas de um modelo a widgets comuns, criando formulários de detalhe que exibem e editam a linha "
      "atual. Com `ManualSubmit`, as alterações só chegam ao modelo em `submit()`; com `AutoSubmit` (padrão), "
      "chegam quando o widget perde o foco."),
    lst("c14_selecao_mapper.py", "QItemSelectionModel e QDataWidgetMapper: formulário ligado à linha selecionada"),
    out("c14_selecao_mapper"),

    h2("Validação de modelos com QAbstractItemModelTester"),
    p("Erros em modelos costumam aparecer longe da causa — uma visão que trava, uma seleção que salta de linha. "
      "Instancie o `QAbstractItemModelTester` sobre o modelo durante o desenvolvimento e nos testes automatizados "
      "(Capítulo 28): com `FailureReportingMode.Fatal`, a primeira violação interrompe a execução e aponta a regra "
      "descumprida. O objeto testador deve ser mantido em uma variável enquanto o modelo for usado."),

    h2("Exercícios do capítulo"),
    nl("Acrescente ao `ModeloEnsaios` uma coluna *Data* (`QDate`) editável com `QDateEdit` por meio de um delegado.",
       "Implemente `sort()` diretamente no modelo e compare com a ordenação via `QSortFilterProxyModel`.",
       "Crie um proxy derivado de `QIdentityProxyModel` que exiba as pressões em psi sem alterar o modelo-fonte.",
       "Construa a árvore de equipamentos com edição de nomes e inserção de filhos, validando com o "
       "`QAbstractItemModelTester`."),
)
