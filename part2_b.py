# -*- coding: utf-8 -*-
"""Parte II — Capítulos 15 a 19 (Step 3)."""
from blocks import ST_INT, bl, ch, flat, h2, h3, h4, img, lst, nl, note, out, p, snip, tab

CAP15 = flat(
    ch("Banco de dados com QtSql", ST_INT, [
        "Conectar-se a bancos SQLite, PostgreSQL, MySQL e ODBC.",
        "Executar consultas seguras com parâmetros e transações.",
        "Exibir e editar tabelas com os modelos SQL.",
    ]),
    h2("QSqlDatabase e drivers"),
    p("O QtSql oferece uma API única para vários bancos, por meio de **drivers** (plugins). `QSqlDatabase.drivers()` "
      "lista os disponíveis; `addDatabase(driver, nome)` cria uma conexão nomeada. O SQLite não exige servidor nem "
      "biblioteca externa — é a escolha natural para dados locais de ferramentas desktop."),
    tab("Drivers SQL do Qt e disponibilidade", ["Driver", "Banco de dados", "Plugin nas wheels PyQt6-Qt6 6.12.0",
                                                "Observação"],
        [["QSQLITE", "SQLite 3", "Linux e Windows", "Embutido; não requer biblioteca externa"],
         ["QPSQL", "PostgreSQL", "Linux e Windows", "Requer a biblioteca cliente libpq"],
         ["QMYSQL / QMARIADB", "MySQL / MariaDB", "Linux (ausente na wheel Windows)", "Requer a biblioteca cliente MySQL/MariaDB"],
         ["QODBC", "Fontes ODBC (SQL Server etc.)", "Linux e Windows", "Requer driver ODBC configurado"],
         ["QOCI", "Oracle", "Linux e Windows", "Requer Oracle Instant Client"],
         ["QIBASE", "Firebird / InterBase", "Linux e Windows", "Requer a biblioteca cliente"],
         ["QMIMER", "Mimer SQL", "Linux e Windows", "Requer a biblioteca cliente"]],
        [1700, 2000, 2571, 2800]),
    p("A coluna de disponibilidade foi verificada inspecionando as pastas `plugins/sqldrivers` das wheels "
      "PyQt6-Qt6 6.12.0 para Linux x86-64 e Windows x64. Um plugin presente ainda depende da biblioteca cliente do "
      "banco instalada no sistema; caso contrário, `open()` falha e `lastError()` explica o motivo."),
    lst("c15_sqlite.py", "QtSql com SQLite: conexão, DDL, consultas preparadas, transações e erros"),
    out("c15_sqlite"),

    h2("QSqlQuery"),
    h3("Consultas preparadas e parâmetros (bindValue)"),
    p("Nunca monte SQL concatenando textos digitados pelo usuário: use `prepare()` com marcadores nomeados "
      "(`:tag`) ou posicionais (`?`) e `bindValue()`/`addBindValue()`. Além de impedir injeção de SQL, consultas "
      "preparadas são mais rápidas quando repetidas em laço. Sempre verifique o retorno de `exec()` — a listagem "
      "centraliza isso na função `executar()`."),
    h3("Transações"),
    p("`transaction()`, `commit()` e `rollback()` agrupam operações: ou todas são gravadas, ou nenhuma. Além da "
      "consistência, inserir milhares de linhas dentro de uma transação é ordens de grandeza mais rápido no "
      "SQLite."),
    h3("Tratamento de erros com QSqlError"),
    p("`lastError()` retorna um `QSqlError` com o tipo, o texto do driver (`driverText`), o texto do banco "
      "(`databaseText`) e o código nativo (`nativeErrorCode`). A classificação do tipo varia entre drivers — na "
      "saída, a violação de `UNIQUE` no SQLite foi classificada como `ConnectionError` —, por isso, para decidir o "
      "que fazer, confie no código nativo e no texto do banco."),
    note("ATENÇÃO", "Para fechar uma conexão nomeada, finalize e descarte todas as consultas e o objeto "
                    "`QSqlDatabase` antes de chamar `QSqlDatabase.removeDatabase(nome)`, como no final da Listagem "
                    "15.1; caso contrário, o Qt avisa que a conexão ainda está em uso."),

    h2("Modelos SQL"),
    lst("c15_modelos_sql.py", "Modelos SQL: QSqlQueryModel, QSqlTableModel (edição) e QSqlRelationalTableModel"),
    out("c15_modelos_sql"),
    h3("QSqlQueryModel"),
    p("Modelo somente leitura para o resultado de qualquer `SELECT`, pronto para uma `QTableView`. Para colunas "
      "calculadas ou formatação, combine com um proxy (Capítulo 14)."),
    h3("QSqlTableModel e estratégias de edição"),
    p("Modelo editável de uma tabela. A **estratégia de edição** define quando as alterações vão para o banco: "
      "`OnFieldChange` (a cada campo), `OnRowChange` (ao mudar de linha) ou `OnManualSubmit` (apenas em "
      "`submitAll()`, com `revertAll()` para descartar). A última é a mais adequada a formulários com botões "
      "*Salvar*/*Cancelar*. `setFilter()` e `setSort()` restringem e ordenam a consulta."),
    h3("QSqlRelationalTableModel e QSqlRelationalDelegate"),
    p("Resolve chaves estrangeiras: `setRelation(coluna, QSqlRelation(tabela, chave, exibição))` faz a coluna "
      "`tipo_id` exibir o nome do tipo, e o `QSqlRelationalDelegate` oferece um `QComboBox` com as opções válidas "
      "durante a edição."),

    h2("Integração com o banco via ORM (SQLAlchemy) versus QtSql"),
    p("Bibliotecas como o **SQLAlchemy** mapeiam tabelas para classes Python, geram SQL portável e cuidam de "
      "migrações de esquema (com o Alembic), mas não conversam diretamente com as visões do Qt. O **QtSql** "
      "integra-se nativamente ao Model/View, porém trabalha em SQL e com tipos do Qt. Uma regra prática: para "
      "telas centradas em tabelas editáveis, QtSql; para regras de negócio complexas, muitos relacionamentos e "
      "código compartilhado com serviços sem interface, um ORM na camada de serviços, exposto à interface por "
      "modelos próprios (Capítulo 14)."),

    h2("Exercícios do capítulo"),
    nl("Crie um banco SQLite em arquivo (em `QStandardPaths.StandardLocation.AppDataLocation`) com as tabelas de ensaio e tipo.",
       "Implemente busca por tag com consulta preparada e `LIKE`, exibindo o resultado em `QSqlQueryModel`.",
       "Monte uma tela com `QSqlTableModel` em `OnManualSubmit` e botões *Salvar* e *Descartar*.",
       "Meça o tempo para inserir 10 000 linhas com e sem transação e explique a diferença."),
)

CAP16 = flat(
    ch("Arquivos, dados e processos", ST_INT, [
        "Ler e gravar arquivos de texto e binários com segurança.",
        "Trabalhar com JSON, XML e CSV.",
        "Monitorar arquivos e executar processos externos.",
    ]),
    h2("QFile, QTextStream, QDataStream e QSaveFile"),
    p("O Python já oferece `open()` e `pathlib`, suficientes na maioria dos casos. As classes do Qt são úteis quando "
      "se quer integração com o restante da API (prefixos de busca, `QIODevice` em rede e processos) ou recursos "
      "específicos, como a **gravação atômica** do `QSaveFile`: os dados vão para um arquivo temporário e só "
      "substituem o original em `commit()` — uma queda de energia no meio da gravação não corrompe o arquivo "
      "existente."),
    lst("c16_arquivos.py", "QSaveFile + QTextStream (texto) e QDataStream (binário versionado)"),
    out("c16_arquivos"),
    p("Dois detalhes da saída: o `QTextStream` escreveu `345.0` como `345`, pois usa por padrão a notação mais curta "
      "— formate números explicitamente quando o formato importar; e o arquivo binário tem exatamente 48 bytes "
      "(4 do número mágico, 16 da string em UTF-16 com prefixo de tamanho, 4 da contagem e 3 × 8 dos `double`). "
      "Fixar `setVersion()` garante que arquivos gravados hoje sejam lidos por versões futuras do Qt."),

    h2("JSON: QJsonDocument versus módulo json"),
    p("Para JSON, o módulo `json` do Python é a escolha mais simples e idiomática. `QJsonDocument` interessa quando o "
      "JSON chega como `QByteArray` de uma resposta de rede (Capítulo 21) ou precisa ser repassado a APIs do Qt."),
    lst("c16_json_xml.py", "JSON (módulo json e QJsonDocument) e XML (QXmlStreamWriter/Reader e QtXml DOM)"),
    out("c16_json_xml"),

    h2("XML"),
    h3("QXmlStreamReader e QXmlStreamWriter (QtCore)"),
    p("Leitura e escrita sequenciais (*streaming*): consomem pouca memória e servem para arquivos grandes. São a "
      "API recomendada pela Qt para XML."),
    h3("DOM com o módulo QtXml"),
    p("`QDomDocument` carrega a árvore inteira em memória e permite navegação e alteração livres — conveniente para "
      "arquivos pequenos de configuração. Para novos códigos de leitura, prefira o stream reader."),

    h2("CSV e integração com pandas"),
    p("O módulo `csv` resolve arquivos simples. Para análise, o **pandas** lê e converte tipos de uma vez — "
      "inclusive decimais com vírgula (`decimal=\",\"`) e datas — e um modelo genérico de poucas linhas exibe "
      "qualquer `DataFrame` em uma `QTableView`."),
    lst("c16_csv_pandas.py", "CSV com o módulo csv e com pandas, exibido em QTableView por um modelo genérico"),
    out("c16_csv_pandas"),
    p("Com o módulo `csv`, os valores chegam como texto (`'345,0'`); com o pandas, já como `float64` e "
      "`datetime64`. A saída foi obtida com o pandas 3.0.5, em que colunas de texto passam a ter o tipo `str`."),

    h2("QFileSystemWatcher"),
    p("Observa arquivos e pastas e emite `fileChanged`/`directoryChanged` quando mudam — útil para recarregar "
      "parâmetros editados externamente ou detectar novos arquivos de aquisição. Alguns editores salvam criando um "
      "arquivo novo e renomeando-o; nesse caso, o arquivo deixa de ser observado e deve ser readicionado no slot."),
    lst("c16_watcher_processo.py", "QFileSystemWatcher e QProcess (execução síncrona e assíncrona)"),
    out("c16_watcher_processo"),

    h2("QProcess: execução de programas externos"),
    h3("Execução síncrona e assíncrona"),
    p("`QProcess` executa programas externos — solvers, conversores, scripts. O modo **síncrono** "
      "(`waitForFinished()`) bloqueia o event loop e só é aceitável para comandos rápidos. O modo **assíncrono** "
      "mantém a interface responsiva: a saída chega por `readyReadStandardOutput` e o término por "
      "`finished(código, status)`. Passe programa e argumentos separadamente (`setProgram`/`setArguments`), sem "
      "montar linhas de comando com textos do usuário."),
    h3("Captura de stdout/stderr e códigos de saída"),
    p("`readAllStandardOutput()` e `readAllStandardError()` retornam `QByteArray`; decodifique com a codificação "
      "do programa chamado. O código de saída 3 da listagem chegou em `finished` com status `NormalExit`: o status "
      "indica se o processo terminou normalmente ou falhou (`CrashExit`), e o código, o resultado informado por ele. "
      "Falhas ao iniciar (programa inexistente) chegam por `errorOccurred`. A saída pode chegar em vários "
      "trechos, um `readyReadStandardOutput` para cada; por isso o slot da listagem ignora trechos vazios. Em "
      "programas reais, acumule os trechos e processe linha a linha (`canReadLine()`/`readLine()`)."),

    h2("QCommandLineParser"),
    p("Para aplicações que aceitam argumentos — abrir um arquivo, rodar em lote, escolher unidades —, o "
      "`QCommandLineParser` gera `--help` e `--version` automaticamente, valida opções e separa argumentos "
      "posicionais. `parse()` apenas analisa; `process()` também trata `--help`/`--version` e encerra o programa."),
    lst("c16_linha_comando.py", "QCommandLineParser: opções, valores, argumentos posicionais e --help"),
    out("c16_linha_comando"),
    note("NOTA", "Na saída, `--version pedido? True`: a opção `-v` da linha simulada foi interpretada como "
                 "`--version`, registrada por `addVersionOption()`. Ao criar opções próprias, evite letras já usadas "
                 "pelas opções padrão (`-h`, `-v`)."),

    h2("Exercícios do capítulo"),
    nl("Grave os ensaios da Listagem 14.4 em JSON com `QSaveFile` e recarregue-os ao abrir a aplicação.",
       "Leia um CSV de medições com pandas e exiba-o em uma `QTableView` com ordenação por proxy.",
       "Execute um script Python externo com `QProcess` assíncrono e mostre sua saída em um `QPlainTextEdit`.",
       "Monitore uma pasta e liste automaticamente os novos arquivos `.csv` que aparecerem nela."),
)

CAP17 = flat(
    ch("Gráficos 2D com QPainter, impressão e SVG", ST_INT, [
        "Desenhar formas, textos e imagens com QPainter.",
        "Criar widgets personalizados com paintEvent().",
        "Gerar impressões, PDFs e arquivos SVG.",
    ]),
    h2("O sistema de pintura: QPainter, QPaintDevice e QPaintEngine"),
    p("`QPainter` desenha em qualquer `QPaintDevice`: um widget (dentro de `paintEvent`), um `QImage`, um "
      "`QPixmap`, uma impressora, um `QPdfWriter` ou um `QSvgGenerator`. O mesmo código de desenho serve a todos — "
      "o `QPaintEngine` de cada dispositivo traduz as chamadas. Isso permite, por exemplo, reaproveitar a pintura de "
      "um gráfico na tela e no relatório PDF."),
    lst("c17_primitivas.py", "QPainter em um QImage: canetas, pincéis, gradientes, caminhos, transformações e texto"),
    out("c17_primitivas"),
    img("Primitivas desenhadas pela Listagem 17.1", "f17_1_primitivas.png", width_cm=9.0),

    h2("Canetas, pincéis e gradientes"),
    h3("QPen e QBrush"),
    p("A **caneta** (`QPen`) define contornos e linhas: cor, espessura, estilo (`SolidLine`, `DashLine`…), "
      "terminação (`PenCapStyle`) e junção. O **pincel** (`QBrush`) define o preenchimento: cor sólida, padrão, "
      "gradiente ou textura. `Qt.PenStyle.NoPen` e `Qt.BrushStyle.NoBrush` desligam cada um."),
    h3("QLinearGradient, QRadialGradient e QConicalGradient"),
    p("Gradientes são definidos por pontos de parada (`setColorAt(posição, cor)`) e usados como pincel. O linear "
      "varia ao longo de uma reta; o radial, a partir de um centro; o cônico, ao redor de um centro (útil em "
      "indicadores circulares)."),

    h2("Formas, caminhos e transformações"),
    h3("Primitivas de desenho"),
    p("`drawLine`, `drawRect`, `drawRoundedRect`, `drawEllipse`, `drawArc`, `drawPie`, `drawPolygon`, "
      "`drawPolyline`, `drawPoint` e `drawText` cobrem a maioria das necessidades. Use as versões com tipos de ponto "
      "flutuante (`QPointF`, `QRectF`) junto com `RenderHint.Antialiasing` para traços precisos e suaves."),
    h3("QPainterPath"),
    p("Um caminho combina segmentos de reta, curvas de Bézier, arcos e subcaminhos em uma forma única, que pode ser "
      "preenchida, contornada, usada para recorte (`setClipPath`) ou para detecção de colisão no Capítulo 18."),
    h3("QTransform e sistemas de coordenadas"),
    p("`translate`, `rotate` e `scale` alteram o sistema de coordenadas do pintor. Envolva transformações em "
      "`save()`/`restore()` para não afetar o restante do desenho — como no leque de linhas da Listagem 17.1. O "
      "manômetro da Seção 17.6 usa a mesma técnica para desenhar em coordenadas lógicas de −100 a 100, "
      "independentemente do tamanho do widget."),

    h2("Texto: QFont, QFontMetrics e QStaticText"),
    p("`QFontMetrics` mede texto antes de desenhá-lo — largura (`horizontalAdvance`), altura de linha, retângulo "
      "ocupado — e abrevia textos longos com `elidedText()`. `QStaticText` guarda o leiaute de um texto que não "
      "muda, acelerando repinturas frequentes."),
    lst("c17_imagens.py", "QImage (pixels), QPixmap (exibição), QFontMetrics (texto) e QStylePainter"),
    out("c17_imagens"),

    h2("Imagens: QImage, QPixmap, QPicture e QBitmap"),
    p("`QImage` é independente de hardware e dá acesso direto aos pixels — use-o para processar, gerar e salvar "
      "imagens, inclusive fora da thread da interface. `QPixmap` é otimizado para exibição na tela e deve ser criado "
      "e usado na thread da interface. `QBitmap` é um pixmap monocromático (máscaras); `QPicture` grava comandos de "
      "pintura para reproduzi-los depois. Converta com `QPixmap.fromImage()` e `pixmap.toImage()`."),

    h2("Widgets personalizados com paintEvent()"),
    p("Um widget próprio herda de `QWidget`, guarda seu estado em propriedades, desenha tudo em `paintEvent()` e "
      "chama `update()` quando o estado muda. `update()` apenas **agenda** a repintura — várias chamadas seguidas "
      "resultam em uma única pintura, no próximo ciclo do event loop. Nunca chame `paintEvent()` diretamente."),
    h3("Exemplo: manômetro analógico"),
    lst("c17_manometro.py", "Widget personalizado: manômetro analógico desenhado com QPainter"),
    out("c17_manometro"),
    img("Widget personalizado de manômetro desenhado com QPainter", "f17_2_manometro.png", width_cm=12.0),
    p("O manômetro expõe `valor` como `pyqtProperty` com sinal de notificação — por isso pode ser animado no "
      "Capítulo 19 e conectado a qualquer sinal numérico. `sizeHint()` e `minimumSizeHint()` informam ao layout os "
      "tamanhos desejados. Na escala, o formato `:g` evita que valores como 1,5 ou 4,5 sejam arredondados para "
      "inteiros — erro presente na primeira versão da listagem e detectado na revisão da Figura 17.2."),
    h3("QStylePainter e opções de estilo"),
    p("Para widgets que imitam controles padrão (um botão com desenho extra, por exemplo), `QStylePainter` com uma "
      "`QStyleOption` preenchida (`initFrom(self)`) desenha as partes padrão pelo estilo atual — mantendo a "
      "aparência coerente com o restante da aplicação e com as folhas de estilo."),

    h2("Impressão com QtPrintSupport"),
    h3("QPrinter, QPrintDialog e QPageSetupDialog"),
    p("`QPrinter` é um dispositivo de pintura: o mesmo `QPainter` desenha nele. `QPrintDialog` deixa o usuário "
      "escolher impressora e páginas; `QPageSetupDialog`, papel e margens. Configurado com "
      "`setOutputFormat(PdfFormat)`, o `QPrinter` grava um PDF em vez de imprimir."),
    h3("QPrintPreviewDialog e QPrintPreviewWidget"),
    p("A pré-visualização chama, pelo sinal `paintRequested(QPrinter)`, a mesma função de desenho usada na "
      "impressão — escreva o desenho do relatório uma única vez, recebendo o dispositivo como parâmetro."),
    snip('''from PyQt6.QtPrintSupport import QPrintPreviewDialog

previa = QPrintPreviewDialog(self)
# assinatura do slot: def desenhar_relatorio(self, printer: QPrinter) -> None
previa.paintRequested.connect(self.desenhar_relatorio)
previa.exec()'''),
    lst("c17_impressao_svg.py", "Impressão em PDF (QPrinter), QPdfWriter, QSvgGenerator e QSvgRenderer"),
    out("c17_impressao_svg"),

    h2("Geração de PDF com QPdfWriter"),
    p("`QPdfWriter` gera PDF sem depender do subsistema de impressão, com controle de resolução, leiaute de página, "
      "título e metadados. As coordenadas estão em unidades do dispositivo: a 300 dpi, uma folha A4 inteira mede "
      "cerca de 2 480 × 3 508 unidades, e `width()`/`height()` já descontam as margens do leiaute — calcule as "
      "posições sempre a partir desses valores (2 125 × 3 154 na saída da Listagem 17.4, com margens de 15 mm). "
      "Informe a unidade das margens explicitamente (`QPageLayout.Unit.Millimeter`): o padrão é ponto tipográfico."),

    h2("SVG: QSvgRenderer, QSvgGenerator e QSvgWidget"),
    p("`QSvgGenerator` é um dispositivo que grava os comandos do `QPainter` como SVG vetorial — ideal para figuras "
      "de relatório. `QSvgRenderer` desenha um SVG em qualquer dispositivo, em qualquer escala, e `QSvgWidget` "
      "(módulo QtSvgWidgets) o exibe diretamente em um layout."),

    h2("Exercícios do capítulo"),
    nl("Acrescente ao manômetro uma marca para o valor máximo registrado, reiniciável com duplo clique.",
       "Crie um widget de gráfico de barras simples com eixos e rótulos usando apenas `QPainter`.",
       "Gere um relatório PDF de duas páginas com cabeçalho, tabela de ensaios e a imagem do manômetro.",
       "Exporte o desenho da Listagem 17.1 para SVG e reabra-o com `QSvgWidget`."),
)

CAP18 = flat(
    ch("Graphics View Framework", ST_INT, [
        "Modelar cenas 2D com milhares de itens interativos.",
        "Criar itens personalizados com detecção de colisão.",
        "Implementar zoom, pan e efeitos gráficos.",
    ]),
    h2("Cena, visão e itens"),
    p("O Graphics View Framework separa a **cena** (`QGraphicsScene`), que contém e gerencia os itens, das "
      "**visões** (`QGraphicsView`), que a exibem com zoom, rotação e rolagem próprios. É a ferramenta indicada para "
      "diagramas interativos, sinóticos de processo, editores de layout e mapas com muitos objetos, graças a um "
      "índice espacial que localiza rapidamente os itens visíveis."),
    lst("c18_cena.py", "Graphics View: cena com itens padrão e personalizados, duas visões, colisão e zoom"),
    out("c18_cena"),
    img("Uma QGraphicsScene exibida por duas QGraphicsView com transformações distintas", "f18_1_cena.png"),

    h2("Itens padrão"),
    p("A cena oferece métodos de conveniência para itens prontos: `addRect`, `addEllipse`, `addLine`, `addPath`, "
      "`addPolygon`, `addPixmap`, `addText` e `addSimpleText`. Cada item tem posição (`setPos`), ordem de "
      "empilhamento (`setZValue`), transformação própria e flags de interação."),

    h2("Itens personalizados: boundingRect(), shape() e paint()"),
    p("Um item próprio herda de `QGraphicsItem` — ou de `QGraphicsObject`, quando precisa de sinais e propriedades "
      "(por exemplo, para animação). Três métodos são essenciais: `boundingRect()` delimita a área que o item pode "
      "pintar (incluindo a espessura do contorno); `shape()` define a forma exata usada em cliques e colisões; e "
      "`paint()` desenha o item em suas coordenadas locais."),

    h2("Sistemas de coordenadas e transformações"),
    p("Há três sistemas: o do **item** (local), o da **cena** e o da **visão** (pixels do widget). Conversões são "
      "feitas com `mapToScene`/`mapFromScene` (itens e visões) e `mapToItem`. Transformar a visão (`scale`, "
      "`rotate`) não altera a cena; transformar um item afeta apenas ele e seus filhos."),

    h2("Interação"),
    h3("Seleção, movimentação e flags de item"),
    p("Flags como `ItemIsMovable` e `ItemIsSelectable` habilitam o arraste e a seleção com o mouse, sem código "
      "adicional. Com `ItemSendsGeometryChanges`, o item recebe `itemChange()` antes de cada mudança de posição e "
      "pode ajustá-la — na listagem, as válvulas se encaixam em uma grade de 10 unidades (`setPos(213, 127)` "
      "resultou em `(210, 130)`)."),
    h3("Detecção de colisão"),
    p("`collidingItems()` retorna os itens que se sobrepõem a um item, usando `shape()` por padrão; "
      "`cena.items(região)` e `cena.itemAt(ponto, transformação)` localizam itens por posição. Como a forma da "
      "válvula é um polígono, a colisão considera o desenho real, e não apenas o retângulo envolvente."),

    h2("Zoom, pan e navegação"),
    p("Zoom é uma escala da visão (`scale()`), normalmente aplicada na roda do mouse, como em `VisaoZoom`; ancore no "
      "cursor com `setTransformationAnchor(ViewportAnchor.AnchorUnderMouse)`. O arraste da área visível (*pan*) é "
      "habilitado com `setDragMode(DragMode.ScrollHandDrag)`; `fitInView()` enquadra uma região inteira."),

    h2("Widgets na cena: QGraphicsProxyWidget e QGraphicsWidget"),
    p("`cena.addWidget(widget)` insere um widget comum na cena por meio de um `QGraphicsProxyWidget` — o campo de "
      "texto da Figura 18.1 continua editável e acompanha as transformações da visão. `QGraphicsWidget` é a base "
      "para itens com geometria gerenciada por layouts da própria cena (`QGraphicsLinearLayout`, "
      "`QGraphicsGridLayout`)."),

    h2("Efeitos: QGraphicsBlurEffect, QGraphicsDropShadowEffect, QGraphicsOpacityEffect e QGraphicsColorizeEffect"),
    p("Efeitos gráficos se aplicam a itens e também a widgets comuns (`setGraphicsEffect`): desfoque, sombra, "
      "opacidade e colorização. Cada item ou widget aceita um único efeito. São processados por software e têm "
      "custo de desempenho: evite-os em itens numerosos ou animados continuamente."),

    h2("Exercícios do capítulo"),
    nl("Acrescente ligações (linhas) entre válvulas que acompanhem o movimento dos itens.",
       "Mostre em uma barra de status as coordenadas de cena do cursor, usando `mapToScene`.",
       "Implemente um minimapa: uma segunda visão com `fitInView` da cena inteira e um retângulo da área visível.",
       "Destaque em vermelho as válvulas que colidirem com outra durante o arraste."),
)

CAP19 = flat(
    ch("Animações e máquinas de estado", ST_INT, [
        "Animar propriedades de widgets com curvas de suavização.",
        "Compor animações sequenciais e paralelas.",
        "Modelar comportamentos com QtStateMachine.",
    ]),
    h2("Framework de animação"),
    p("Animações tornam mudanças de estado compreensíveis — um painel que desliza, um alarme que pisca, um ponteiro "
      "que se move até o novo valor. O framework do Qt anima **propriedades** ao longo do tempo, integrado ao event "
      "loop, sem threads nem laços manuais."),
    lst("c19_animacoes.py", "QPropertyAnimation, QVariantAnimation, grupos e QTimeLine"),
    out("c19_animacoes"),
    h3("QPropertyAnimation e QVariantAnimation"),
    p("`QPropertyAnimation(objeto, b\"propriedade\")` interpola uma propriedade Qt — embutida (`pos`, `geometry`, "
      "`size`, `windowOpacity`) ou declarada com `pyqtProperty`, como o `valor` do manômetro do Capítulo 17. "
      "Define-se duração, valor inicial (opcional: na ausência, usa o valor atual) e final. `QVariantAnimation` "
      "interpola valores sem alvo e entrega cada passo pelo sinal `valueChanged`, para aplicação livre."),
    h3("Curvas de suavização: QEasingCurve"),
    p("A curva de suavização transforma o progresso do tempo em progresso do valor. Curvas `Out` desaceleram no "
      "final (naturais para movimentos de chegada); `InOut` aceleram e desaceleram; `Bounce`, `Elastic` e `Back` "
      "ultrapassam ou oscilam em torno do valor final. A Figura 19.1 foi gerada com os valores calculados pelo "
      "próprio `QEasingCurve.valueForProgress()`."),
    img("Curvas de suavização (QEasingCurve) mais usadas", "f19_1_easing.png", width_cm=14.0),
    h3("Grupos: QSequentialAnimationGroup, QParallelAnimationGroup e QPauseAnimation"),
    p("Grupos compõem animações: paralelas (executadas juntas), sequenciais (uma após a outra) e pausas. Grupos "
      "podem conter grupos, e a duração total é calculada automaticamente — 600 ms na saída (300 do paralelo, 100 de "
      "pausa e 200 do retorno). O sinal `finished` encadeia ações ao término."),

    h2("QTimeLine"),
    p("`QTimeLine` fornece apenas a linha do tempo — valores de 0 a 1 (`valueChanged`) ou números de quadro "
      "(`frameChanged`) — para animações em que o próprio código decide o que fazer a cada passo, como trocar "
      "imagens de uma sequência."),

    h2("Máquinas de estado com QtStateMachine"),
    p("Interfaces com modos (parado, ensaiando, pausado, concluído) tendem a acumular `if`s espalhados pelos slots. "
      "Uma **máquina de estados** explicita os estados, as transições permitidas e o que muda em cada estado. No "
      "Qt 6, o framework está no módulo **QtStateMachine** (no Qt 5 fazia parte do QtCore)."),
    lst("c19_maquina_estados.py", "QStateMachine: estados, transições por sinal, propriedades atribuídas e histórico"),
    out("c19_maquina_estados"),
    h3("QStateMachine, QState e QFinalState"),
    p("Estados podem ser compostos: `ensaio` contém `pressurizando` e `estabilizando`, com estado inicial próprio. "
      "Ao entrar em um `QFinalState` de nível superior, a máquina termina e emite `finished`. A máquina é "
      "assíncrona: inicia com `start()` e processa as transições no event loop."),
    h3("Transições: QSignalTransition, QEventTransition, QKeyEventTransition e QMouseEventTransition"),
    p("`estado.addTransition(sinal, destino)` cria uma `QSignalTransition`. Há também transições disparadas por "
      "eventos (`QEventTransition`), teclas (`QKeyEventTransition`) e mouse (`QMouseEventTransition`). Uma transição "
      "definida em um estado composto vale para todos os seus subestados — como `pausar` e `concluir` na listagem."),
    h3("Estados históricos: QHistoryState"),
    p("Um `QHistoryState` lembra qual subestado estava ativo ao sair do estado composto. Na saída, o ensaio foi "
      "pausado durante `estabilizando` e, ao retomar pelo histórico, voltou a `estabilizando` — e não ao estado "
      "inicial `pressurizando`."),
    h3("Animações associadas a transições"),
    p("`assignProperty(objeto, \"propriedade\", valor)` define valores aplicados ao entrar em cada estado. Com "
      "`transicao.addAnimation(QPropertyAnimation(...))` ou `maquina.addDefaultAnimation(...)`, essas mudanças "
      "passam a ser animadas — combinando os dois frameworks deste capítulo."),

    h2("Exercícios do capítulo"),
    nl("Anime o `valor` do manômetro do Capítulo 17 com `QPropertyAnimation` e curva `OutCubic`.",
       "Faça um rótulo de alarme piscar indefinidamente com `QSequentialAnimationGroup` e `setLoopCount(-1)`.",
       "Modele com `QStateMachine` os estados de uma conexão serial (desconectado, conectando, conectado, erro).",
       "Associe animações de cor às transições da máquina da Listagem 19.2 usando `assignProperty`."),
)
