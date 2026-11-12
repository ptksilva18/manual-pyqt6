# Índice das listagens do MAN-PYQT6-001

Correspondência entre o número de cada listagem no manual e o arquivo neste diretório.

- **✔ executada** — rodada por [`runner.py`](../../runner.py); a saída real fica em `../outputs/<nome>.txt`.
- **✔ (indireta)** — arquivo carregado ou executado por outra listagem, conforme a nota.
- **⚠** — não executada no ambiente de teste (Linux): exige Windows.
- **apoio** — arquivo de apoio (modelo de configuração, interface `.ui` ou tradução `.ts`) mostrado no manual; quando outra listagem o usa, o capítulo indica.

| Listagem | Título | Arquivo | Verificação |
|---|---|---|---|
| 2.1 | Script de verificação da instalação do PyQt6 e dos add-ons | [`c02_verifica.py`](c02_verifica.py) | ✔ executada |
| 2.2 | Modelo de pyproject.toml para aplicação PyQt6 | [`c02_pyproject.toml`](c02_pyproject.toml) | apoio |
| 3.1 | Herança e super(): uma subclasse de QWidget com parâmetros próprios | [`c03_heranca.py`](c03_heranca.py) | ✔ executada |
| 3.2 | Mixin Python puro combinado com uma única classe Qt | [`c03_mixin.py`](c03_mixin.py) | ✔ executada |
| 3.3 | @property (Python) versus pyqtProperty (visível ao sistema de metaobjetos) | [`c03_property.py`](c03_property.py) | ✔ executada |
| 3.4 | Armadilha clássica: lambda em laço conectado a clicked(bool) | [`c03_lambda.py`](c03_lambda.py) | ✔ executada |
| 3.5 | Decoradores: um decorador próprio empilhado com @pyqtSlot | [`c03_decorador.py`](c03_decorador.py) | ✔ executada |
| 3.6 | dataclass + Enum alimentando um QComboBox (dado associado com userData) | [`c03_dataclass_enum.py`](c03_dataclass_enum.py) | ✔ executada |
| 3.7 | Exceções em slots: excepthook global mantém a aplicação viva | [`c03_excecoes.py`](c03_excecoes.py) | ✔ executada |
| 4.1 | Primeira aplicação PyQt6 | [`c04_primeira.py`](c04_primeira.py) | ✔ executada |
| 4.2 | Argumentos de linha de comando: o Qt consome as opções que reconhece | [`c04_argumentos.py`](c04_argumentos.py) | ✔ executada |
| 4.3 | Janela principal como subclasse de QMainWindow | [`c04_mainwindow.py`](c04_mainwindow.py) | ✔ executada |
| 4.4 | Metadados, aboutToQuit e quitOnLastWindowClosed | [`c04_ciclo_vida.py`](c04_ciclo_vida.py) | ✔ executada |
| 5.1 | Árvore de objetos: pai-filho, objectName, findChild/findChildren e destroyed | [`c05_arvore.py`](c05_arvore.py) | ✔ executada |
| 5.2 | Ciclo de vida C++ x Python: referência para objeto C++ já destruído | [`c05_vida_cpp.py`](c05_vida_cpp.py) | ✔ executada |
| 5.3 | Sinais personalizados: declaração, argumentos, sobrecarga e conexões | [`c05_sinais.py`](c05_sinais.py) | ✔ executada |
| 5.4 | Tipos de conexão, UniqueConnection, SingleShotConnection e bloqueio de sinais | [`c05_conexoes.py`](c05_conexoes.py) | ✔ executada |
| 5.5 | Propriedades dinâmicas e introspecção com QMetaObject | [`c05_meta.py`](c05_meta.py) | ✔ executada |
| 5.6 | QTimer (periódico e singleShot), QElapsedTimer e QBasicTimer | [`c05_timers.py`](c05_timers.py) | ✔ executada |
| 5.7 | Tipos de valor do QtCore: geometria, datas e URLs | [`c05_tipos.py`](c05_tipos.py) | ✔ executada |
| 6.1 | Galeria dos widgets fundamentais | [`c06_galeria.py`](c06_galeria.py) | ✔ executada |
| 6.2 | Botões checáveis, QButtonGroup exclusivo e QDialogButtonBox | [`c06_botoes.py`](c06_botoes.py) | ✔ executada |
| 6.3 | QLineEdit: validadores, máscara, modo de eco e autocompletar | [`c06_lineedit.py`](c06_lineedit.py) | ✔ executada |
| 6.4 | Sincronizando QSlider e QDoubleSpinBox; QComboBox com dados associados | [`c06_numericos.py`](c06_numericos.py) | ✔ executada |
| 7.1 | QHBoxLayout e QVBoxLayout: margens, espaçamento, stretch e alinhamento | [`c07_caixas.py`](c07_caixas.py) | ✔ executada |
| 7.2 | QGridLayout: teclado numérico com células mescladas (row/column span) | [`c07_grade.py`](c07_grade.py) | ✔ executada |
| 7.3 | QFormLayout: rótulos e campos alinhados, com políticas de quebra e crescimento | [`c07_formulario.py`](c07_formulario.py) | ✔ executada |
| 7.4 | Composição com layouts aninhados | [`c07_composicao.py`](c07_composicao.py) | ✔ executada |
| 7.5 | QStackedWidget, QSplitter e QScrollArea | [`c07_pilha_divisor.py`](c07_pilha_divisor.py) | ✔ executada |
| 8.1 | Janela principal completa: ações, menus, barra de ferramentas, docks e QSettings | [`c08_janela_principal.py`](c08_janela_principal.py) | ✔ executada |
| 8.2 | QSplashScreen durante a inicialização | [`c08_splash.py`](c08_splash.py) | ✔ executada |
| 9.1 | QMessageBox: métodos estáticos e caixa personalizada | [`c09_messagebox.py`](c09_messagebox.py) | ✔ executada |
| 9.2 | Diálogos padrão: QInputDialog, QProgressDialog e QFileDialog (não nativo) | [`c09_padrao.py`](c09_padrao.py) | ✔ executada |
| 9.3 | Diálogo personalizado com QDialogButtonBox e validação antes de accept() | [`c09_dialogo.py`](c09_dialogo.py) | ✔ executada |
| 9.4 | QWizard com campos registrados (registerField) e páginas encadeadas | [`c09_wizard.py`](c09_wizard.py) | ✔ executada |
| 10.1 | Reimplementação de manipuladores de eventos (mouse, teclado, janela) | [`c10_manipuladores.py`](c10_manipuladores.py) | ✔ executada |
| 10.2 | Filtro de eventos: um objeto observa e intercepta eventos de outro | [`c10_filtro.py`](c10_filtro.py) | ✔ executada |
| 10.3 | Eventos personalizados: registerEventType, postEvent (assíncrono) e sendEvent | [`c10_evento_proprio.py`](c10_evento_proprio.py) | ✔ executada |
| 10.4 | Arrastar e soltar: alvo que aceita apenas arquivos .csv | [`c10_arrastar_soltar.py`](c10_arrastar_soltar.py) | ✔ executada |
| 10.5 | Área de transferência: texto, dados MIME e notificação de mudança | [`c10_clipboard.py`](c10_clipboard.py) | ✔ executada |
| 11.1 | Arquivo .ui produzido pelo Qt Designer (XML) | [`c11_dados_poco.ui`](c11_dados_poco.ui) | apoio |
| 11.2 | Carga dinâmica de um arquivo .ui com uic.loadUi() | [`c11_loadui.py`](c11_loadui.py) | ✔ executada |
| 11.3 | Código gerado pelo pyuic6 6.12.0 a partir da Listagem 11.1 | [`ui_dados_poco.py`](ui_dados_poco.py) | ✔ executada |
| 11.4 | Código gerado pelo pyuic6: integração por composição e por herança múltipla | [`c11_composicao_ui.py`](c11_composicao_ui.py) | ✔ executada |
| 11.5 | Widget personalizado usado por promoção no Qt Designer | [`c11_widgets.py`](c11_widgets.py) | ✔ executada |
| 11.6 | Trecho <customwidgets> de um .ui com widget promovido | [`c11_promovido.ui`](c11_promovido.ui) | apoio |
| 11.7 | Promoção de widget: o .ui referencia CampoPressao, definido em c11_widgets.py | [`c11_promocao.py`](c11_promocao.py) | ✔ executada |
| 11.8 | Plugin de widget para o Qt Designer escrito em Python (módulo QtDesigner) | [`c11_plugin.py`](c11_plugin.py) | ✔ executada |
| 12.1 | QStyleFactory, troca de estilo e QProxyStyle para um ajuste pontual | [`c12_estilos.py`](c12_estilos.py) | ✔ executada |
| 12.2 | QPalette: tema escuro programático e esquema de cores do sistema | [`c12_paleta.py`](c12_paleta.py) | ✔ executada |
| 12.3 | Qt Style Sheets: temas claro e escuro, seletores, subcontroles e pseudo-estados | [`c12_temas.py`](c12_temas.py) | ✔ executada |
| 12.4 | Fontes embarcadas (QFontDatabase) e ícones (QIcon a partir de SVG) | [`c12_fontes_icones.py`](c12_fontes_icones.py) | ✔ executada |
| 12.5 | High-DPI: política de arredondamento e pixmaps com devicePixelRatio | [`c12_highdpi.py`](c12_highdpi.py) | ✔ executada |
| 13.1 | Recursos sem pyrcc: caminhos relativos ao pacote e prefixos de busca do QDir | [`c13_recursos.py`](c13_recursos.py) | ✔ executada |
| 13.2 | QSettings em formato INI: tipos, grupos, arrays e valores padrão | [`c13_settings.py`](c13_settings.py) | ✔ executada |
| 13.3 | QStandardPaths, QDir e QFileInfo: onde guardar cada tipo de arquivo | [`c13_caminhos.py`](c13_caminhos.py) | ✔ executada |
| 13.4 | Internacionalização: tr(), QTranslator da aplicação e traduções do próprio Qt | [`c13_traducao.py`](c13_traducao.py) | ✔ executada |
| 13.5 | Arquivo .ts gerado pelo pylupdate6 e traduzido | [`c13_calceng_pt_BR.ts`](c13_calceng_pt_BR.ts) | apoio |
| 13.6 | QLocale: formatação e leitura de números, datas e moeda por idioma | [`c13_locale.py`](c13_locale.py) | ✔ executada |
| 13.7 | Mensagens do Qt redirecionadas ao módulo logging (qInstallMessageHandler) | [`c13_log.py`](c13_log.py) | ✔ executada |
| 14.1 | Widgets de conveniência: QListWidget, QTreeWidget e QTableWidget | [`c14_conveniencia.py`](c14_conveniencia.py) | ✔ executada |
| 14.2 | Modelos prontos: QStringListModel e QStandardItemModel | [`c14_modelos_prontos.py`](c14_modelos_prontos.py) | ✔ executada |
| 14.3 | QFileSystemModel: carregamento assíncrono de diretórios (sinal directoryLoaded) | [`c14_filesystem.py`](c14_filesystem.py) | ✔ executada |
| 14.4 | Modelo de tabela personalizado: leitura, edição, papéis e inserção/remoção | [`c14_modelo_tabela.py`](c14_modelo_tabela.py) | ✔ executada |
| 14.5 | Modelo hierárquico com QAbstractItemModel: index(), parent() e internalPointer | [`c14_modelo_arvore.py`](c14_modelo_arvore.py) | ✔ executada |
| 14.6 | Delegado personalizado: editor numérico com limites e texto formatado | [`c14_delegado.py`](c14_delegado.py) | ✔ executada |
| 14.7 | Modelos proxy: ordenação/filtragem, transposição e concatenação | [`c14_proxy.py`](c14_proxy.py) | ✔ executada |
| 14.8 | QItemSelectionModel e QDataWidgetMapper: formulário ligado à linha selecionada | [`c14_selecao_mapper.py`](c14_selecao_mapper.py) | ✔ executada |
| 15.1 | QtSql com SQLite: conexão, DDL, consultas preparadas, transações e erros | [`c15_sqlite.py`](c15_sqlite.py) | ✔ executada |
| 15.2 | Modelos SQL: QSqlQueryModel, QSqlTableModel (edição) e QSqlRelationalTableModel | [`c15_modelos_sql.py`](c15_modelos_sql.py) | ✔ executada |
| 16.1 | QSaveFile + QTextStream (texto) e QDataStream (binário versionado) | [`c16_arquivos.py`](c16_arquivos.py) | ✔ executada |
| 16.2 | JSON (módulo json e QJsonDocument) e XML (QXmlStreamWriter/Reader e QtXml DOM) | [`c16_json_xml.py`](c16_json_xml.py) | ✔ executada |
| 16.3 | CSV com o módulo csv e com pandas, exibido em QTableView por um modelo genérico | [`c16_csv_pandas.py`](c16_csv_pandas.py) | ✔ executada |
| 16.4 | QFileSystemWatcher e QProcess (execução síncrona e assíncrona) | [`c16_watcher_processo.py`](c16_watcher_processo.py) | ✔ executada |
| 16.5 | QCommandLineParser: opções, valores, argumentos posicionais e --help | [`c16_linha_comando.py`](c16_linha_comando.py) | ✔ executada |
| 17.1 | QPainter em um QImage: canetas, pincéis, gradientes, caminhos, transformações e texto | [`c17_primitivas.py`](c17_primitivas.py) | ✔ executada |
| 17.2 | QImage (pixels), QPixmap (exibição), QFontMetrics (texto) e QStylePainter | [`c17_imagens.py`](c17_imagens.py) | ✔ executada |
| 17.3 | Widget personalizado: manômetro analógico desenhado com QPainter | [`c17_manometro.py`](c17_manometro.py) | ✔ executada |
| 17.4 | Impressão em PDF (QPrinter), QPdfWriter, QSvgGenerator e QSvgRenderer | [`c17_impressao_svg.py`](c17_impressao_svg.py) | ✔ executada |
| 18.1 | Graphics View: cena com itens padrão e personalizados, duas visões, colisão e zoom | [`c18_cena.py`](c18_cena.py) | ✔ executada |
| 19.1 | QPropertyAnimation, QVariantAnimation, grupos e QTimeLine | [`c19_animacoes.py`](c19_animacoes.py) | ✔ executada |
| 19.2 | QStateMachine: estados, transições por sinal, propriedades atribuídas e histórico | [`c19_maquina_estados.py`](c19_maquina_estados.py) | ✔ executada |
| 20.1 | Responsividade do event loop: cálculo na thread da GUI versus em worker | [`c20_bloqueio.py`](c20_bloqueio.py) | ✔ executada |
| 20.2 | Padrão worker com moveToThread(): progresso, resultado, erro e cancelamento | [`c20_worker.py`](c20_worker.py) | ✔ executada |
| 20.3 | Subclasse de QThread: run() na nova thread, slots na thread de origem | [`c20_qthread_sub.py`](c20_qthread_sub.py) | ✔ executada |
| 20.4 | QThreadPool com QRunnable, sinais auxiliares e callables | [`c20_pool.py`](c20_pool.py) | ✔ executada |
| 20.5 | Sincronização: QMutex, QReadWriteLock, QWaitCondition e QSemaphore | [`c20_sync.py`](c20_sync.py) | ✔ executada |
| 20.6 | Tipos de conexão entre threads e QMetaObject.invokeMethod | [`c20_sinais_threads.py`](c20_sinais_threads.py) | ✔ executada |
| 20.7 | concurrent.futures com processos e threads integrados ao Qt | [`c20_futures.py`](c20_futures.py) | ✔ executada |
| 20.8 | asyncio sobre o event loop do Qt com qasync | [`c20_asyncio.py`](c20_asyncio.py) | ✔ executada |
| 21.1 | HTTP com QNetworkAccessManager: GET/POST JSON, erros, timeout e progresso | [`c21_http.py`](c21_http.py) | ✔ executada |
| 21.2 | TCP com QTcpServer e QTcpSocket: protocolo de linhas e enquadramento | [`c21_tcp.py`](c21_tcp.py) | ✔ executada |
| 21.3 | UDP com QUdpSocket e datagramas binários | [`c21_udp.py`](c21_udp.py) | ✔ executada |
| 21.4 | TLS com QSslServer e QSslSocket: verificação de certificado e de nome | [`c21_tls.py`](c21_tls.py) | ✔ executada |
| 21.5 | WebSockets: servidor e cliente trocando JSON e dados binários | [`c21_websocket.py`](c21_websocket.py) | ✔ executada |
| 21.6 | OAuth 2.0 Authorization Code + PKCE com QOAuth2AuthorizationCodeFlow | [`c21_oauth.py`](c21_oauth.py) | ✔ executada |
| 21.7 | QtRemoteObjects: fonte e réplica dinâmica em processos distintos | [`c21_remoteobjects.py`](c21_remoteobjects.py) | ✔ executada |
| 21.8 | D-Bus: serviço exportado e cliente em outro processo | [`c21_dbus.py`](c21_dbus.py) | ✔ executada |
| 21.9 | QSerialPort: aquisição de linhas ASCII de um instrumento | [`c21_serial.py`](c21_serial.py) | ✔ executada |
| 21.10 | Bluetooth LE e NFC: descoberta com tratamento de ausência de hardware | [`c21_bluetooth.py`](c21_bluetooth.py) | ✔ executada |
| 22.1 | GraphsView em QML: tema, eixos, série de linha e de dispersão | [`c22_graphs2d.qml`](c22_graphs2d.qml) | ✔ (indireta): Arquivo carregado e renderizado pela Listagem 22.2 (executada e verificada) |
| 22.2 | QtGraphs 2D alimentado pelo Python em um QQuickWidget | [`c22_graphs2d.py`](c22_graphs2d.py) | ✔ executada |
| 22.3 | Superfície 3D com Q3DSurfaceWidgetItem, gradiente de cores e câmera | [`c22_graphs3d.py`](c22_graphs3d.py) | ✔ executada |
| 22.4 | QtCharts: linha, spline, dispersão, eixo logarítmico, barras e pizza | [`c22_qtcharts.py`](c22_qtcharts.py) | ✔ executada |
| 22.5 | Matplotlib embutido com barra de navegação e redesenho por parâmetros | [`c22_matplotlib.py`](c22_matplotlib.py) | ✔ executada |
| 22.6 | pyqtgraph: osciloscópio com buffer circular e QTimer | [`c22_pyqtgraph.py`](c22_pyqtgraph.py) | ✔ executada |
| 22.7 | Custo por quadro (dados + pintura) de pyqtgraph, QtCharts e Matplotlib | [`c22_desempenho.py`](c22_desempenho.py) | ✔ executada |
| 23.1 | Reprodução e decodificação de áudio com QMediaPlayer e QAudioDecoder | [`c23_audio.py`](c23_audio.py) | ✔ executada |
| 23.2 | Captura e gravação: QMediaCaptureSession, QMediaRecorder e QAudioBufferInput | [`c23_gravacao.py`](c23_gravacao.py) | ✔ executada |
| 23.3 | QtSpatialAudio: motor, ouvinte, sala e fonte posicionada | [`c23_espacial.py`](c23_espacial.py) | ✔ executada |
| 23.4 | QTextToSpeech: motores, vozes, idiomas e fila de falas | [`c23_voz.py`](c23_voz.py) | ✔ executada |
| 23.5 | QtPositioning: registro NMEA em modo simulação, distância, azimute e zona | [`c23_posicao.py`](c23_posicao.py) | ✔ executada |
| 23.6 | QtSensors: descoberta de backends, filtros e tratamento de ausência | [`c23_sensores.py`](c23_sensores.py) | ✔ executada |
| 23.7 | Bandeja do sistema, QDesktopServices e permissões | [`c23_desktop.py`](c23_desktop.py) | ✔ executada |
| 24.1 | QWebEngineView: HTML, JavaScript, console, controle de navegação e PDF | [`c24_webengine.py`](c24_webengine.py) | ✔ executada |
| 24.2 | Perfil próprio, esquema engapp://, interceptor e download | [`c24_esquemas.py`](c24_esquemas.py) | ✔ executada |
| 24.3 | Página que usa a ponte: propriedade, slot com retorno e sinal | [`c24_webchannel.html`](c24_webchannel.html) | ✔ (indireta): Página carregada e executada pela Listagem 24.4 (executada e verificada) |
| 24.4 | QWebChannel: objeto Python publicado para o JavaScript | [`c24_webchannel.py`](c24_webchannel.py) | ✔ executada |
| 24.5 | Exibição de PDF com o visualizador embutido do QWebEngineView | [`c24_pdf.py`](c24_pdf.py) | ✔ executada |
| 24.6 | Projeto de ajuda (.qhp): sumário, palavras-chave e arquivos | [`resources/ajuda/manual.qhp`](resources/ajuda/manual.qhp) | ✔ (indireta): Compilado com qhelpgenerator; o .qch resultante é usado pela Listagem 24.7 |
| 24.7 | QtHelp: registro do .qch, índice, conteúdo, exibição e busca | [`c24_ajuda.py`](c24_ajuda.py) | ✔ executada |
| 24.8 | QAxContainer: exportação de resultados para o Microsoft Excel via COM | [`c24_activex.py.win`](c24_activex.py.win) | ⚠ Não executado no ambiente de teste (Linux): requer Windows com Microsoft Excel |
| 25.1 | QOpenGLWidget com OpenGL 4.1 Core: shaders, VBO, VAO e uniform | [`c25_opengl.py`](c25_opengl.py) | ✔ executada |
| 25.2 | QRhiWidget: passe de renderização com limpeza animada | [`c25_rhi.py`](c25_rhi.py) | ✔ executada |
| 25.3 | QVulkanInstance: versão, camadas, extensões e criação | [`c25_vulkan.py`](c25_vulkan.py) | ✔ executada |
| 25.4 | Cena Qt Quick 3D: câmera, luz, modelos e propriedade controlada pelo Python | [`c25_quick3d.qml`](c25_quick3d.qml) | ✔ (indireta): Arquivo carregado e renderizado pela Listagem 25.5 (executada e verificada) |
| 25.5 | Qt Quick 3D em QQuickWidget, controlado pelo Python | [`c25_quick3d.py`](c25_quick3d.py) | ✔ executada |
| 25.6 | Qt 3D: entidade, malha, material, transformação e câmera | [`c25_qt3d.py`](c25_qt3d.py) | ✔ executada |
| 26.1 | Interface QML que usa um singleton e um tipo definidos em Python | [`c26_main.qml`](c26_main.qml) | ✔ (indireta): Arquivo carregado pela Listagem 26.2 (executada e verificada) |
| 26.2 | QQmlApplicationEngine com singleton, tipo registrado, propriedades e sinais | [`c26_engine.py`](c26_engine.py) | ✔ executada |
| 26.3 | ListView com delegate que usa required properties | [`c26_modelo.qml`](c26_modelo.qml) | ✔ (indireta): Arquivo carregado pela Listagem 26.4 (executada e verificada) |
| 26.4 | QAbstractListModel com roleNames() exibido em QML | [`c26_modelo.py`](c26_modelo.py) | ✔ executada |
| 26.5 | Indicador circular em QML com propriedade, sinal e animação | [`c26_indicador.qml`](c26_indicador.qml) | ✔ (indireta): Arquivo carregado pela Listagem 26.6 (executada e verificada) |
| 26.6 | QQuickWidget em uma janela Widgets com QSlider e sinal QML | [`c26_qquickwidget.py`](c26_qquickwidget.py) | ✔ executada |
| 27.1 | MVP: domínio puro, presenter e duas views (widget e falsa) | [`c27_mvp.py`](c27_mvp.py) | ✔ executada |
| 27.2 | MVVM: ViewModel com propriedades notificáveis e ligação bidirecional | [`c27_mvvm.py`](c27_mvvm.py) | ✔ executada |
| 27.3 | Arquivo de configuração TOML da aplicação | [`c27_config.toml`](c27_config.toml) | ✔ (indireta): Lido pela Listagem 27.4 (executada e verificada) |
| 27.4 | Injeção de dependências: configuração tipada, raiz de composição e repositórios | [`c27_di.py`](c27_di.py) | ✔ executada |
| 27.5 | QUndoStack: comandos, fusão, macros, estado limpo e QUndoView | [`c27_undo.py`](c27_undo.py) | ✔ executada |
| 27.6 | Plugin de exemplo (pasta plugins_demo) | [`plugins_demo/conversor_unidades.py`](plugins_demo/conversor_unidades.py) | ✔ (indireta): Carregado e executado pela Listagem 27.7 (executada e verificada) |
| 27.7 | Descoberta, validação de versão e isolamento de plugins | [`c27_plugins.py`](c27_plugins.py) | ✔ executada |
| 27.8 | sys.excepthook e threading.excepthook com relatório de erro | [`c27_excecoes.py`](c27_excecoes.py) | ✔ executada |
| 28.1 | Widget sob teste: calculadora de pressão hidrostática | [`c28_calculadora.py`](c28_calculadora.py) | ✔ executada |
| 28.2 | QtTest com unittest: teclado, mouse, QSignalSpy e QAbstractItemModelTester | [`c28_qtest.py`](c28_qtest.py) | ✔ executada |
| 28.3 | Testes com pytest-qt: qtbot, waitSignal, assertNotEmitted e parametrização | [`c28_test_calculadora.py`](c28_test_calculadora.py) | ✔ executada |
| 28.4 | GitHub Actions: matriz de sistemas e versões do Python com testes headless | [`c28_ci.yml`](c28_ci.yml) | ✔ (indireta): Sintaxe YAML validada com parser; comandos equivalentes aos executados neste capítulo |
| 28.5 | Execução da suíte com pytest-cov, como em integração contínua | [`c28_cobertura.py`](c28_cobertura.py) | ✔ executada |
| 28.6 | Regressão visual: comparação com imagem de referência | [`c28_regressao_visual.py`](c28_regressao_visual.py) | ✔ executada |
| 29.1 | cProfile e QElapsedTimer: modelo lento versus modelo com cache | [`c29_desempenho.py`](c29_desempenho.py) | ✔ executada |
| 29.2 | QLoggingCategory, regras de filtro, manipulador de mensagens e QT_DEBUG_PLUGINS | [`c29_depuracao.py`](c29_depuracao.py) | ✔ executada |
| 29.3 | Objetos C++ destruídos, temporários, objetos sem referência e faulthandler | [`c29_memoria.py`](c29_memoria.py) | ✔ executada |
| 29.4 | Nomes acessíveis, buddies, ordem de tabulação, contraste e preferências | [`c29_acessibilidade.py`](c29_acessibilidade.py) | ✔ executada |
| 30.1 | Aplicação a empacotar: recursos, tema, tradução e autoteste | [`c30_app/app_ensaios.py`](c30_app/app_ensaios.py) | ✔ (indireta): Empacotada e executada pela Listagem 30.3 (executada e verificada) |
| 30.2 | Arquivo .spec do PyInstaller (onedir, dados e exclusões) | [`c30_app/app_ensaios.spec`](c30_app/app_ensaios.spec) | ✔ (indireta): Usado pela Listagem 30.3 (executada e verificada) |
| 30.3 | Empacotamento com PyInstaller e execução do resultado congelado | [`c30_empacotar.py`](c30_empacotar.py) | ✔ executada |
| 30.4 | Script do Inno Setup para a pasta gerada pelo PyInstaller | [`c30_instalador.iss`](c30_instalador.iss) | ⚠ Não executado no ambiente de teste (Linux): requer Inno Setup 6.3+ no Windows |
| 31.1 | app.py — raiz de composição, pastas de dados e autoteste | [`c31_app/ensaios/app.py`](c31_app/ensaios/app.py) | ✔ (indireta): Executado pela Listagem 31.13 (testes, autoteste do código-fonte e do executável congelado) |
| 31.2 | janela.py — janela principal, ações e integração dos componentes | [`c31_app/ensaios/janela.py`](c31_app/ensaios/janela.py) | ✔ (indireta): Executado pela Listagem 31.13 (testes, autoteste do código-fonte e do executável congelado) |
| 31.3 | dados/TH-01.csv — leituras de exemplo | [`c31_app/dados/TH-01.csv`](c31_app/dados/TH-01.csv) | ✔ (indireta): Lido pelo autoteste e pelos testes da Listagem 31.11 |
| 31.4 | dominio.py — regras de análise em Python puro | [`c31_app/ensaios/dominio.py`](c31_app/ensaios/dominio.py) | ✔ (indireta): Executado pela Listagem 31.13 (testes, autoteste do código-fonte e do executável congelado) |
| 31.5 | importacao.py — leitura de CSV com detecção de separador | [`c31_app/ensaios/importacao.py`](c31_app/ensaios/importacao.py) | ✔ (indireta): Executado pela Listagem 31.13 (testes, autoteste do código-fonte e do executável congelado) |
| 31.6 | repositorio.py — persistência em SQLite | [`c31_app/ensaios/repositorio.py`](c31_app/ensaios/repositorio.py) | ✔ (indireta): Executado pela Listagem 31.13 (testes, autoteste do código-fonte e do executável congelado) |
| 31.7 | modelos.py — modelos de tabela para ensaios e leituras | [`c31_app/ensaios/modelos.py`](c31_app/ensaios/modelos.py) | ✔ (indireta): Executado pela Listagem 31.13 (testes, autoteste do código-fonte e do executável congelado) |
| 31.8 | servicos.py — análise em QThreadPool com resultado por sinal | [`c31_app/ensaios/servicos.py`](c31_app/ensaios/servicos.py) | ✔ (indireta): Executado pela Listagem 31.13 (testes, autoteste do código-fonte e do executável congelado) |
| 31.9 | relatorio.py — HTML + Matplotlib → QTextDocument → PDF | [`c31_app/ensaios/relatorio.py`](c31_app/ensaios/relatorio.py) | ✔ (indireta): Executado pela Listagem 31.13 (testes, autoteste do código-fonte e do executável congelado) |
| 31.10 | tests/test_dominio.py — testes do domínio e da importação | [`c31_app/tests/test_dominio.py`](c31_app/tests/test_dominio.py) | ✔ (indireta): Executado pela Listagem 31.13 (testes, autoteste do código-fonte e do executável congelado) |
| 31.11 | tests/test_janela.py — testes de interface com pytest-qt | [`c31_app/tests/test_janela.py`](c31_app/tests/test_janela.py) | ✔ (indireta): Executado pela Listagem 31.13 (testes, autoteste do código-fonte e do executável congelado) |
| 31.12 | monitor_ensaios.spec — empacotamento com PyInstaller | [`c31_app/monitor_ensaios.spec`](c31_app/monitor_ensaios.spec) | ✔ (indireta): Executado pela Listagem 31.13 (testes, autoteste do código-fonte e do executável congelado) |
| 31.13 | Roteiro de entrega: testes, autoteste, empacotamento e reteste do executável | [`c31_entrega.py`](c31_entrega.py) | ✔ executada |
