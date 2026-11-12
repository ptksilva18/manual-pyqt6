# -*- coding: utf-8 -*-
"""Parte III — Capítulos 23 a 26 (Step 4)."""
from blocks import ST_AVA, bl, ch, flat, h2, h3, img, lst, nl, note, out, p, snip, tab

CAP23 = flat(
    ch("Multimídia e integração com o sistema", ST_AVA, [
        "Reproduzir e capturar áudio e vídeo.",
        "Utilizar síntese de voz, posicionamento e sensores.",
        "Integrar a aplicação à bandeja do sistema e ao desktop.",
    ]),
    p("Os recursos deste capítulo dependem de hardware (placa de som, câmera, GNSS, sensores) e de serviços do "
      "sistema operacional. As listagens foram executadas em um servidor Linux **sem** esses dispositivos; por "
      "isso, além do caminho principal, elas mostram como detectar a ausência de recursos e degradar com "
      "elegância — requisito de qualquer aplicação profissional."),
    h2("QtMultimedia"),
    p("A API de multimídia do Qt 6 foi reprojetada em relação ao Qt 5: o reprodutor (`QMediaPlayer`) não tem "
      "mais saída implícita, e a captura é organizada em torno de uma sessão (`QMediaCaptureSession`) que "
      "liga entradas (câmera, microfone, tela) a saídas (visualização, foto, gravador). Nas wheels "
      "PyQt6-Qt6 6.12 para Linux, o único plugin de multimídia é o baseado em **FFmpeg** (verificado), que "
      "decodifica e codifica os formatos usuais sem depender de codecs do sistema."),
    h3("Reprodução: QMediaPlayer, QAudioOutput e QVideoWidget"),
    p("`QMediaPlayer` controla a mídia (`setSource`, `play`, `pause`, `stop`, `setPosition`) e informa o "
      "andamento por `mediaStatusChanged`, `playbackStateChanged`, `durationChanged` e `positionChanged`. O "
      "som só sai se houver um `QAudioOutput` associado; o vídeo exige `setVideoOutput()` com um "
      "`QVideoWidget` (Widgets), um `QGraphicsVideoItem` (Graphics View) ou um `QVideoSink` (quadros para "
      "processamento próprio). `QAudioDecoder` decodifica o arquivo em memória, sem reproduzir — útil para "
      "análise de sinais."),
    lst("c23_audio.py", "Reprodução e decodificação de áudio com QMediaPlayer e QAudioDecoder"),
    out("c23_audio"),
    p("Mesmo sem saída de áudio, o player percorreu todos os estados até `EndOfMedia`, e o decodificador "
      "entregou as 22 050 amostras (0,5 s a 44,1 kHz) com o pico esperado — a diferença de uma unidade vem do "
      "truncamento na geração do seno."),
    note("ATENÇÃO", "No ambiente de teste (contêiner Linux com bibliotecas do PipeWire, mas sem servidor de "
                    "áudio em execução), `QMediaDevices.audioOutputs()` encerrou o processo com falha de "
                    "segmentação. Definir `QT_AUDIO_BACKEND=pulseaudio` (variável reconhecida pela biblioteca "
                    "Qt Multimedia 6.12) contornou o problema. Em máquinas de usuário com áudio funcional, isso "
                    "não é necessário; o registro serve para diagnóstico em servidores de teste."),
    h3("Captura: QCamera, QMediaCaptureSession, QImageCapture e QMediaRecorder"),
    p("A sessão de captura é o ponto central: `setCamera()`, `setAudioInput()`, `setImageCapture()`, "
      "`setRecorder()` e `setVideoOutput()`. O `QMediaRecorder` grava no contêiner e com os codecs "
      "escolhidos em `QMediaFormat`; `QMediaFormat().supportedFileFormats(Encode)` informa o que o backend "
      "consegue gravar. Sem microfone nem câmera, a Listagem 23.2 usa `QAudioBufferInput` (Qt 6.8+), que "
      "permite ao próprio programa fornecer as amostras — por exemplo, sinais sintetizados ou vindos de um "
      "instrumento."),
    lst("c23_gravacao.py", "Captura e gravação: QMediaCaptureSession, QMediaRecorder e QAudioBufferInput"),
    out("c23_gravacao"),
    note("ATENÇÃO", "No PyQt6 6.12, conectar `QMediaRecorder.recorderStateChanged` ou "
                    "`QMediaRecorder.errorOccurred` falha com `TypeError` (\"No such signal\"): a assinatura do "
                    "sinal não é encontrada. A Listagem 23.2 contorna o problema consultando `recorderState()` "
                    "e `error()` com um `QTimer`. Os sinais de `QMediaPlayer` funcionam normalmente."),
    h3("Efeitos sonoros: QSoundEffect"),
    p("Para sons curtos de baixa latência (cliques, alarmes), `QSoundEffect` carrega um arquivo WAV não "
      "comprimido para a memória e o toca repetidamente com `play()`, com controle de volume e de repetições "
      "(`setLoopCount`). Sem dispositivo de saída, seu `status()` vai para `Error` — trate esse estado em vez "
      "de supor que o som foi tocado."),
    h3("Dispositivos: QMediaDevices"),
    p("`QMediaDevices` lista câmeras (`videoInputs`), microfones (`audioInputs`) e saídas (`audioOutputs`), "
      "informa os padrões do sistema e emite sinais quando dispositivos são conectados ou removidos "
      "(`audioOutputsChanged`, `videoInputsChanged`). Reaja a esses sinais para trocar de dispositivo sem "
      "reiniciar a aplicação."),

    h2("Áudio espacial: QtSpatialAudio"),
    p("O QtSpatialAudio posiciona fontes sonoras em 3D em torno de um ouvinte, com atenuação por distância, "
      "oclusão e reverberação de salas — útil em simuladores e treinamento. A unidade de posição é definida "
      "por `distanceScale` (o padrão é centímetros; `DistanceScaleMeter` faz as posições valerem metros)."),
    lst("c23_espacial.py", "QtSpatialAudio: motor, ouvinte, sala e fonte posicionada"),
    out("c23_espacial"),
    note("ATENÇÃO", "Destrua fontes, salas e ouvinte antes do `QAudioEngine`. No teste, deixar a ordem de "
                    "destruição ao coletor de lixo do Python encerrou o processo com falha de segmentação na "
                    "saída; os `del` explícitos da Listagem 23.3 resolveram. Observe também que `setLoops()` "
                    "recebe `int` no PyQt6 (`QSpatialSound.Loops.Infinite.value`)."),

    h2("Síntese de voz: QTextToSpeech"),
    p("`QTextToSpeech` converte texto em fala usando o motor do sistema (`availableEngines()`; no Linux, por "
      "exemplo, o speech-dispatcher). Vozes e idiomas dependem do motor e do que está instalado no sistema; "
      "escolha a voz por idioma com `availableVoices()`/`availableLocales()` e trate a ausência. `say()` "
      "interrompe a fala atual; `enqueue()` (Qt 6.6+) acrescenta à fila. A Listagem 23.4 usa o motor `mock`, "
      "distribuído com o Qt para testes, que simula a fala de forma determinística."),
    lst("c23_voz.py", "QTextToSpeech: motores, vozes, idiomas e fila de falas"),
    out("c23_voz"),

    h2("Posicionamento: QtPositioning"),
    p("O QtPositioning obtém posição de fontes do sistema (`QGeoPositionInfoSource.createDefaultSource()`) ou "
      "de receptores GNSS que falam **NMEA 0183**, por porta serial, socket ou arquivo "
      "(`QNmeaPositionInfoSource`). `QGeoCoordinate` resolve geodésia básica sobre o elipsoide WGS 84: "
      "`distanceTo()`, `azimuthTo()` e `atDistanceAndAzimuth()`. Formas como `QGeoCircle`, `QGeoRectangle` e "
      "`QGeoPolygon` testam pertinência (`contains`) — por exemplo, zonas de exclusão em torno de uma "
      "unidade marítima."),
    lst("c23_posicao.py", "QtPositioning: registro NMEA em modo simulação, distância, azimute e zona"),
    out("c23_posicao"),
    p("O registro `trajeto.nmea` (sentenças GGA e RMC com *checksums* válidos) descreve uma embarcação a "
      "8,1 nós no rumo 48°; os 29,1 m percorridos em 7 s (4,16 m/s ≈ 8,1 nós) e o azimute de 47,9° conferem "
      "com os dados. Em `SimulationMode`, a fonte respeita os horários das sentenças; em campo, use "
      "`RealTimeMode` com o dispositivo do receptor."),

    h2("Sensores: QtSensors"),
    p("O QtSensors dá acesso a acelerômetro, giroscópio, magnetômetro, luz ambiente, proximidade e outros, "
      "conforme os backends da plataforma (Android, iOS e, no Linux, `iio-sensor-proxy`). Em computadores de "
      "mesa, é comum não haver backend: `QSensor.sensorTypes()` volta vazio e `connectToBackend()` retorna "
      "`False`, como na Listagem 23.6. Filtros (`QSensorFilter` e subclasses) decidem quais leituras chegam "
      "à aplicação."),
    lst("c23_sensores.py", "QtSensors: descoberta de backends, filtros e tratamento de ausência"),
    out("c23_sensores"),

    h2("Integração com o desktop"),
    lst("c23_desktop.py", "Bandeja do sistema, QDesktopServices e permissões"),
    out("c23_desktop"),
    h3("QSystemTrayIcon e notificações"),
    p("Aplicações de monitoramento costumam viver na bandeja do sistema, com menu de contexto e "
      "notificações (`showMessage`). Verifique `isSystemTrayAvailable()` — em alguns ambientes Linux (e em "
      "servidores sem desktop, como o de teste) não há bandeja — e chame "
      "`setQuitOnLastWindowClosed(False)` para que fechar a última janela não encerre o programa."),
    h3("QDesktopServices: abrir URLs e arquivos"),
    p("`QDesktopServices.openUrl()` abre URLs e arquivos no aplicativo padrão do sistema (navegador, leitor "
      "de PDF, cliente de e-mail com `mailto:`). `setUrlHandler(esquema, objeto, \"slot\")` desvia URLs de um "
      "esquema próprio para dentro da aplicação, como `engapp://` na listagem. Para que **outros programas** "
      "abram esse esquema, é preciso registrá-lo no sistema operacional (registro do Windows, arquivo "
      "`.desktop` no Linux, `Info.plist` no macOS)."),
    h3("Permissões de aplicação (QPermission)"),
    p("Desde o Qt 6.5, `QCoreApplication.checkPermission()` e `requestPermission()` tratam permissões de "
      "câmera, microfone, localização, Bluetooth, contatos e calendário de forma portável. Em plataformas com "
      "sistema de permissões (macOS, iOS, Android), o pedido abre o diálogo do sistema e exige as declarações "
      "correspondentes no `Info.plist` ou no manifesto; no Linux e no Windows de desktop, como mostra a saída, "
      "o resultado costuma ser `Granted` imediatamente. Escreva o código como se o pedido pudesse ser negado."),

    h2("Exercícios do capítulo"),
    nl("Crie um reprodutor com `QVideoWidget`, barra de posição e controle de volume.",
       "Grave em FLAC um sinal sintetizado com `QAudioBufferInput` e confira o arquivo com `QAudioDecoder`.",
       "Use `QNmeaPositionInfoSource` com uma `QSerialPort` (Capítulo 21) para ler um receptor GNSS real.",
       "Implemente uma zona de exclusão poligonal (`QGeoPolygon`) e emita um alarme sonoro ao entrar nela.",
       "Transforme o monitor de ensaios em aplicação de bandeja com notificações de fim de etapa."),
)

CAP24 = flat(
    ch("Web, documentos e ajuda integrada", ST_AVA, [
        "Embutir um navegador Chromium na aplicação.",
        "Criar uma ponte bidirecional entre Python e JavaScript.",
        "Oferecer ajuda pesquisável e integração com COM/ActiveX.",
    ]),
    p("O **Qt WebEngine** embute o Chromium e é distribuído no pacote **PyQt6-WebEngine** (versão 6.140.0 na "
      "referência deste manual). O motor roda em processos auxiliares (`QtWebEngineProcess`), como um "
      "navegador comum. Importe `PyQt6.QtWebEngineWidgets` antes de criar a `QApplication`."),
    note("NOTA", "As listagens deste capítulo foram executadas como usuário root em um contêiner; nesse caso o "
                 "Chromium exige a opção `--no-sandbox`, passada pela variável de ambiente "
                 "`QTWEBENGINE_CHROMIUM_FLAGS`. Em produção, execute a aplicação como usuário comum e mantenha "
                 "o *sandbox* ativo."),
    h2("QtWebEngineWidgets: QWebEngineView"),
    p("`QWebEngineView` é o widget de exibição; o conteúdo e o comportamento ficam na `QWebEnginePage` "
      "associada. Além de `load(QUrl)`, `setHtml(html, baseUrl)` exibe HTML gerado pelo Python — relatórios, "
      "tabelas, gráficos em bibliotecas JavaScript — com `baseUrl` resolvendo caminhos relativos. "
      "`runJavaScript(codigo, callback)` executa JavaScript na página e devolve o resultado de forma "
      "assíncrona."),
    lst("c24_webengine.py", "QWebEngineView: HTML, JavaScript, console, controle de navegação e PDF"),
    out("c24_webengine"),
    bl("`javaScriptConsoleMessage()` encaminha o `console.log` da página para o Python — essencial para "
       "depurar.",
       "`acceptNavigationRequest()` permite bloquear navegação para fora do conteúdo da aplicação. Uma "
       "navegação recusada também emite `loadFinished(False)` (verificado): sem a proteção de "
       "`carregado()`, o exemplo repetiria o clique indefinidamente.",
       "`printToPdf(caminho)` gera PDF do conteúdo renderizado, com o resultado em `pdfPrintingFinished`."),
    h2("QtWebEngineCore"),
    h3("QWebEnginePage e QWebEngineProfile"),
    p("O **perfil** guarda cache, cookies, armazenamento local, configurações e tratadores. "
      "`QWebEngineProfile()` sem nome é *off-the-record* (nada vai para o disco); com nome, os dados persistem "
      "em `persistentStoragePath()`. Várias páginas podem compartilhar um perfil, e cada página deve ser "
      "destruída antes do seu perfil — daí o `del pagina` ao final da Listagem 24.2."),
    h3("Interceptação de requisições e esquemas de URL"),
    p("`QWebEngineUrlRequestInterceptor.interceptRequest()` examina toda requisição da página e pode "
      "bloqueá-la ou acrescentar cabeçalhos; ele roda fora da thread da GUI e deve ser rápido. Um esquema "
      "próprio (`engapp://`) é registrado com `QWebEngineUrlScheme.registerScheme()` **antes** da "
      "`QApplication` e atendido por um `QWebEngineUrlSchemeHandler`, que responde com dados gerados pelo "
      "Python — documentação embarcada, relatórios montados a partir de um banco, arquivos de um pacote."),
    lst("c24_esquemas.py", "Perfil próprio, esquema engapp://, interceptor e download"),
    out("c24_esquemas"),
    h3("Downloads e impressão em PDF"),
    p("Downloads chegam ao sinal `downloadRequested` do perfil como `QWebEngineDownloadRequest`; defina a "
      "pasta e o nome e chame `accept()` — sem isso, o download é cancelado. O progresso é acompanhado por "
      "`receivedBytesChanged` e o fim por `isFinishedChanged`. Para PDF da própria página, `printToPdf()` "
      "(Listagem 24.1); para impressão em impressora, `QWebEngineView.print(QPrinter)`."),

    h2("QtWebChannel: ponte Python ↔ JavaScript"),
    p("O **QWebChannel** publica objetos Python para o JavaScript da página: propriedades são lidas como "
      "atributos, slots viram funções (com retorno entregue por *callback*) e sinais podem ser conectados a "
      "funções JavaScript. Do lado da página, a biblioteca `qwebchannel.js` — embutida no Qt, no recurso "
      "`:/qtwebchannel/qwebchannel.js` — cria o canal a partir de `qt.webChannelTransport`. Na Listagem 24.4, "
      "o script é injetado com `QWebEngineScript` antes do código da página."),
    lst("c24_webchannel.html", "Página que usa a ponte: propriedade, slot com retorno e sinal", lang="html",
        nota="✔ Página carregada e executada pela Listagem 24.4 (executada e verificada)."),
    lst("c24_webchannel.py", "QWebChannel: objeto Python publicado para o JavaScript"),
    out("c24_webchannel"),
    img("Ponte QWebChannel entre Python e JavaScript", "f24_1_webchannel.png", 15.0),
    note("ATENÇÃO", "Tudo o que é publicado no canal pode ser chamado por qualquer script da página. Publique "
                    "apenas objetos de fachada com operações seguras e valide os argumentos no Python, como se "
                    "viessem de um usuário externo."),

    h2("Visualização de PDF: alternativas e disponibilidade (QtPdf não incluído nas wheels 6.12)"),
    p("Os módulos `QtPdf` e `QtPdfWidgets` não fazem parte das wheels PyQt6 6.12.0 nem PyQt6-WebEngine "
      "6.140.0 (verificado por inspeção dos módulos instalados). As alternativas, em ordem de simplicidade:"),
    bl("**Visualizador do Chromium**: `QWebEngineView` exibe PDFs com navegação, zoom e busca quando "
       "`PluginsEnabled` e `PdfViewerEnabled` estão ativos (Listagem 24.5).",
       "**Aplicativo padrão do sistema**: `QDesktopServices.openUrl(QUrl.fromLocalFile(caminho))`.",
       "**Renderização própria**: bibliotecas como `pypdfium2` convertem páginas em imagens para um "
       "`QLabel` ou `QGraphicsView`. Verifique a licença de cada biblioteca antes de distribuí-la "
       "(Capítulo 30)."),
    lst("c24_pdf.py", "Exibição de PDF com o visualizador embutido do QWebEngineView"),
    out("c24_pdf"),

    h2("Ajuda integrada: QtHelp e QHelpEngine"),
    p("O QtHelp oferece documentação pesquisável dentro da aplicação, no mesmo formato do Qt Assistant. O "
      "fluxo tem três etapas: escrever páginas HTML e um projeto `.qhp` (sumário, palavras-chave e arquivos); "
      "compilá-lo com `qhelpgenerator` em um arquivo `.qch`; e registrá-lo em tempo de execução em uma "
      "coleção (`.qhc`) com `QHelpEngine`. Os widgets prontos — `contentWidget()`, `indexWidget()` e os da "
      "busca — compõem a janela de ajuda."),
    lst("resources/ajuda/manual.qhp", "Projeto de ajuda (.qhp): sumário, palavras-chave e arquivos",
        lang="xml", nota="✔ Compilado com qhelpgenerator; o .qch resultante é usado pela Listagem 24.7."),
    lst("c24_ajuda.py", "QtHelp: registro do .qch, índice, conteúdo, exibição e busca"),
    out("c24_ajuda"),
    bl("O `qhelpgenerator` não acompanha as wheels do PyQt6. No teste, usou-se o do pacote "
       "`qt6-documentation-tools` do Ubuntu (Qt 6.4), e o `.qch` foi lido normalmente pelo QtHelp 6.12.",
       "No Qt 6, `QHelpEngineCore` é **somente leitura por padrão**: sem `setReadOnly(False)`, "
       "`registerDocumentation()` retorna `False` com o erro \"Cannot register namespace\" (verificado).",
       "As páginas usam URLs `qthelp://namespace/pasta/arquivo`; o `QTextBrowser` precisa de "
       "`loadResource()` reimplementado para lê-las com `fileData()`.",
       "A busca de texto completo exige indexação (`reindexDocumentation()`); no Qt 6, `search()` recebe a "
       "consulta como texto."),

    h2("Automação COM/ActiveX no Windows: QAxContainer"),
    p("O módulo `QAxContainer`, presente apenas nas wheels do PyQt6 para Windows, controla objetos COM e "
      "controles ActiveX: Microsoft Office, sistemas legados de supervisão, instrumentos com driver COM. "
      "`QAxObject(\"ProgID\")` cria o objeto; `querySubObject()` navega pela hierarquia; `dynamicCall()` "
      "chama métodos com assinatura no estilo Qt; propriedades COM são lidas e gravadas com `property()` e "
      "`setProperty()`; o sinal `exception` informa erros COM."),
    lst("c24_activex.py.win", "QAxContainer: exportação de resultados para o Microsoft Excel via COM",
        nota="⚠ Não executado no ambiente de teste (Linux): requer Windows com Microsoft Excel. Os nomes de "
             "classes, métodos e sinais foram conferidos no arquivo de stubs QAxContainer.pyi da wheel "
             "PyQt6 6.12.0 para Windows."),
    p("A gravação é feita célula a célula, uma chamada COM por valor — simples e suportada por qualquer versão "
      "do Excel, porém lenta para grandes volumes. Para milhares de linhas, gere o arquivo diretamente com "
      "uma biblioteca de planilhas (por exemplo, `openpyxl`) ou exporte CSV, e use a automação COM apenas "
      "para o que exige o Excel em execução (macros, gráficos dinâmicos, impressão)."),

    h2("Exercícios do capítulo"),
    nl("Gere um relatório HTML a partir de um `QSqlQueryModel` (Capítulo 15), exiba-o em `QWebEngineView` e "
       "exporte-o para PDF.",
       "Acrescente à ponte da Listagem 24.4 um slot que receba um objeto JSON e valide seus campos.",
       "Use um gráfico JavaScript (por exemplo, uma biblioteca de gráficos servida pelo esquema `engapp://`) "
       "alimentado por um sinal Python a cada segundo.",
       "Monte uma janela de ajuda com sumário, índice e busca usando os widgets do `QHelpEngine`.",
       "No Windows, leia uma planilha de entrada com `QAxObject` e importe os dados para um modelo Qt."),
)

CAP25 = flat(
    ch("OpenGL, Vulkan e 3D", ST_AVA, [
        "Renderizar com OpenGL dentro de widgets.",
        "Conhecer as opções de 3D do Qt e seu estado atual.",
        "Escolher entre Qt Quick 3D, Qt 3D (obsoleto) e renderização de baixo nível.",
    ]),
    p("Todos os exemplos deste capítulo exigem aceleração gráfica. Foram executados sob X11 virtual (Xvfb) "
      "com o Mesa (OpenGL 4.5 e Vulkan por software: llvmpipe e lavapipe). Na plataforma `offscreen` não há "
      "contexto OpenGL, e `QOpenGLWidget` informa \"not supported on this platform\"."),
    h2("QOpenGLWidget e o módulo QtOpenGL"),
    p("`QOpenGLWidget` renderiza em um *framebuffer object* e é composto com os demais widgets, convivendo "
      "com layouts, sobreposições e QSS. As classes auxiliares do módulo `QtOpenGL` — "
      "`QOpenGLShaderProgram`, `QOpenGLBuffer`, `QOpenGLVertexArrayObject`, `QOpenGLTexture`, "
      "`QOpenGLFramebufferObject` — encapsulam os objetos do OpenGL. A versão e o perfil do contexto são "
      "pedidos com `QSurfaceFormat.setDefaultFormat()` **antes** de criar a `QApplication`."),
    h3("initializeGL(), resizeGL() e paintGL()"),
    bl("`initializeGL()`: uma vez, com o contexto corrente — compile shaders e crie buffers e texturas.",
       "`resizeGL(w, h)`: a cada redimensionamento — ajuste projeção e razão de aspecto.",
       "`paintGL()`: a cada quadro — desenhe. Para animar, chame `update()`; nunca chame `paintGL()` "
       "diretamente.",
       "Fora desses métodos, chame `makeCurrent()`/`doneCurrent()` antes de usar funções do OpenGL."),
    lst("c25_opengl.py", "QOpenGLWidget com OpenGL 4.1 Core: shaders, VBO, VAO e uniform"),
    out("c25_opengl"),
    img("Triângulo renderizado com OpenGL 4.1 Core em um QOpenGLWidget", "f25_1_opengl.png", 9.0),
    h3("Shaders, buffers e texturas"),
    p("No perfil *Core*, todo desenho passa por shaders GLSL. O VAO memoriza o VBO e o leiaute dos atributos "
      "(`setAttributeBuffer(local, tipo, deslocamento, componentes, passo)`); uniforms como a matriz "
      "`mvp` (`QMatrix4x4`) são definidos com `setUniformValue()`. Texturas vêm de `QImage` com "
      "`QOpenGLTexture(imagem.mirrored())` — o OpenGL espera a origem no canto inferior esquerdo."),
    note("ATENÇÃO", "O PyQt6 traz apenas as tabelas de funções OpenGL 2.0, 2.1 e 4.1 Core. Pedir a tabela do "
                    "contexto efetivamente criado (4.5 no teste) gera `TypeError: QOpenGLFunctions_4_5_Core is "
                    "not supported by PyQt6` (verificado); peça 4.1 Core explicitamente, como na listagem. O "
                    "PyQt6 também não exporta as constantes `GL_*`: use os valores da especificação ou o pacote "
                    "PyOpenGL."),

    h2("QRhiWidget e a abstração de hardware de renderização (QRhi)"),
    p("O **QRhi** (*Rendering Hardware Interface*) é a camada que o Qt 6 usa para desenhar Qt Quick, Qt Quick "
      "3D e QtGraphs sobre a API nativa de cada plataforma: Direct3D 11/12, Metal, Vulkan ou OpenGL. "
      "`QRhiWidget` (Qt 6.7+) expõe essa camada aos Widgets: `initialize()` cria recursos e `render()` grava "
      "comandos em um `QRhiCommandBuffer`. Os shaders são escritos em GLSL Vulkan e pré-compilados para o "
      "formato `.qsb` pela ferramenta `qsb`, que não acompanha as wheels do PyQt6 (está, por exemplo, no "
      "PySide6, como `pyside6-qsb`, e no Qt SDK)."),
    lst("c25_rhi.py", "QRhiWidget: passe de renderização com limpeza animada"),
    out("c25_rhi"),
    p("Um pipeline completo acrescenta, em `initialize()`, `rhi.newBuffer()` para os vértices, "
      "`rhi.newShaderResourceBindings()` para uniforms e texturas e `rhi.newGraphicsPipeline()` com os "
      "estágios `QShader.fromSerialized(dados_qsb)`; em `render()`, `setGraphicsPipeline()`, "
      "`setShaderResources()`, `setVertexInput()` e `draw()` entre `beginPass()` e `endPass()`. O ganho em "
      "relação ao OpenGL puro é a portabilidade: o mesmo código usa Direct3D no Windows e Metal no macOS."),

    h2("Vulkan: QVulkanInstance"),
    p("Para Vulkan direto, o ponto de partida é `QVulkanInstance`: versão da API, camadas (como a de "
      "validação `VK_LAYER_KHRONOS_validation`, quando instalada) e extensões. A instância é associada a uma "
      "janela com `QWindow.setVulkanInstance()`. Para a maioria das aplicações Python, o Vulkan é usado "
      "indiretamente — via QRhi —, e não chamado diretamente."),
    lst("c25_vulkan.py", "QVulkanInstance: versão, camadas, extensões e criação"),
    out("c25_vulkan"),
    p("Defina a versão da API antes de `create()`: no teste, sem `setApiVersion()`, o carregador recusou "
      "`apiVersion = 0` e a instância não foi criada."),

    h2("Qt Quick 3D com Python"),
    p("O **Qt Quick 3D** é a pilha 3D recomendada pela Qt: cenas declaradas em QML (`View3D`, câmeras, luzes, "
      "`Model` com malhas e materiais PBR), renderizadas pelo QRhi, com importação de modelos glTF pela "
      "ferramenta `balsam`. O Python controla a cena por propriedades e pode gerar geometria própria "
      "subclassificando `QQuick3DGeometry` (módulo `QtQuick3D`)."),
    lst("c25_quick3d.qml", "Cena Qt Quick 3D: câmera, luz, modelos e propriedade controlada pelo Python",
        lang="qml", nota="✔ Arquivo carregado e renderizado pela Listagem 25.5 (executada e verificada)."),
    lst("c25_quick3d.py", "Qt Quick 3D em QQuickWidget, controlado pelo Python"),
    out("c25_quick3d"),
    img("Cena Qt Quick 3D renderizada em um QQuickWidget", "f25_2_quick3d.png", 10.0),

    h2("Qt 3D (obsoleto desde Qt 6.8)"),
    h3("Qt3DCore, Qt3DRender, Qt3DExtras, Qt3DInput, Qt3DLogic e Qt3DAnimation"),
    p("O Qt 3D organiza a cena em **entidades** compostas por **componentes** (malha, material, "
      "transformação), com *frame graph* configurável e aspectos de entrada, lógica e animação. Ainda está "
      "no pacote PyQt6-3D 6.12, mas é obsoleto desde o Qt 6.8 e não deve ser escolhido para projetos novos."),
    lst("c25_qt3d.py", "Qt 3D: entidade, malha, material, transformação e câmera"),
    out("c25_qt3d"),
    h3("Estratégia de migração"),
    bl("Reescreva a cena em Qt Quick 3D: `QEntity` + componentes viram `Model` com `source`/`geometry` e "
       "`materials`; `QTransform` vira `position`, `eulerRotation` e `scale`.",
       "Malhas procedurais (`QCuboidMesh`, `QSphereMesh`...) correspondem às primitivas `#Cube`, `#Sphere`, "
       "`#Cylinder`, `#Cone` e `#Rectangle`; malhas de arquivo são convertidas com `balsam`.",
       "`QPhongMaterial` aproxima-se de `DefaultMaterial`; prefira `PrincipledMaterial` (PBR).",
       "Controladores de câmera: `OrbitCameraController` e `WasdController` (módulo QtQuick3D.Helpers).",
       "Para visualização científica de dados, avalie primeiro o QtGraphs (Capítulo 22)."),

    h2("Exercícios do capítulo"),
    nl("Acrescente uma textura carregada de `QImage` ao triângulo da Listagem 25.1.",
       "Compile um par de shaders com `pyside6-qsb` e desenhe um triângulo com `QRhiWidget`.",
       "Gere uma superfície com `QQuick3DGeometry` a partir de uma malha NumPy e exiba-a em Qt Quick 3D.",
       "Migre a cena da Listagem 25.6 para Qt Quick 3D, mantendo a câmera orbital."),
)

CAP26 = flat(
    ch("QML e Qt Quick com Python", ST_AVA, [
        "Decidir entre Qt Widgets e Qt Quick para cada projeto.",
        "Expor objetos, propriedades e modelos Python ao QML.",
        "Combinar QML e Widgets na mesma aplicação.",
    ]),
    h2("Qt Widgets versus Qt Quick"),
    tab("Qt Widgets versus Qt Quick", ["Critério", "Qt Widgets", "Qt Quick (QML)"],
        [["Paradigma", "Imperativo, em Python", "Declarativo (QML) + lógica em Python"],
         ["Aparência", "Nativa do desktop; QSS", "Livre, animada, fluida; estilos do Quick Controls"],
         ["Renderização", "Raster (CPU), com OpenGL opcional", "Grafo de cena acelerado (QRhi)"],
         ["Formulários e tabelas densos", "Excelente (Model/View maduro)", "Possível, com mais trabalho"],
         ["Toque, animação, telas embarcadas", "Limitado", "Excelente"],
         ["Gráficos e 3D modernos", "Via QQuickWidget", "Nativo (QtGraphs, Quick 3D)"],
         ["Ferramentas", "Qt Designer", "Qt Design Studio, qmllint, qmlls"]],
        [2600, 3100, 3371]),
    p("Não é uma escolha exclusiva: aplicações técnicas costumam ter o corpo em Widgets (formulários, tabelas, "
      "árvores) e componentes visuais em QML embutidos com `QQuickWidget` (Seção 26.5)."),

    h2("QQmlApplicationEngine e QQuickView"),
    p("`QQmlApplicationEngine` carrega um QML cuja raiz é uma janela (`Window`/`ApplicationWindow`). "
      "`QQuickView` é uma janela que exibe um item QML qualquer, com `rootContext()` para propriedades de "
      "contexto. Em ambos, verifique erros: `engine.rootObjects()` vazio ou `view.status() == Error` indicam "
      "falha, e o sinal `warnings` traz as mensagens com arquivo e linha."),

    h2("Expondo Python ao QML"),
    lst("c26_main.qml", "Interface QML que usa um singleton e um tipo definidos em Python", lang="qml",
        nota="✔ Arquivo carregado pela Listagem 26.2 (executada e verificada)."),
    lst("c26_engine.py", "QQmlApplicationEngine com singleton, tipo registrado, propriedades e sinais"),
    out("c26_engine"),
    h3("Propriedades de contexto e objetos singleton"),
    p("Há duas formas de entregar um objeto Python pronto ao QML. `rootContext().setContextProperty(\"nome\", "
      "obj)` (Listagem 26.4) é simples, mas o nome é resolvido dinamicamente e as ferramentas (qmllint, "
      "qmlls) não o conhecem. `qmlRegisterSingletonInstance(uri, maior, menor, \"Nome\", obj)` registra o "
      "objeto em um módulo (`import Engenharia 1.0`), com nome conhecido — a forma recomendada. Em ambos os "
      "casos, mantenha uma referência Python ao objeto enquanto o QML o usar."),
    h3("pyqtProperty com sinal notify"),
    p("O QML só atualiza *bindings* quando a propriedade tem sinal de notificação: declare "
      "`pyqtProperty(tipo, notify=sinal)` e emita o sinal a cada mudança. Na listagem, trocar a unidade "
      "emite `unidadeChanged`, e o rótulo de pressão — que lê `Calculadora.unidade` — é reavaliado "
      "automaticamente (2944,70 psi para 2000 m). Slots com `@pyqtSlot(..., result=tipo)` podem ser "
      "chamados do QML e devolver valores."),
    h3("Registro de tipos: qmlRegisterType() e funções correlatas"),
    p("`qmlRegisterType(Classe, uri, maior, menor, \"Nome\")` permite **instanciar** a classe Python dentro "
      "do QML (`Tanque { diametro: 3.0 }`). As funções correlatas são `qmlRegisterSingletonType`, "
      "`qmlRegisterUncreatableType` (tipo visível, mas não instanciável, para enums e tipos anexados) e "
      "`qmlRegisterAnonymousType`."),
    note("ATENÇÃO", "Para obter no Python um objeto criado pelo QML a partir de um tipo Python, declare na "
                    "raiz `property QtObject nome: id`. No teste, `property alias` para o mesmo objeto "
                    "chegou ao Python como `sip.voidptr` inutilizável, e `findChild()` não o encontrou — "
                    "objetos não visuais declarados em uma `ApplicationWindow` não são filhos QObject dela."),

    h2("Modelos Python em QML"),
    p("Qualquer `QAbstractItemModel` do Capítulo 14 serve a `ListView`, `TableView`, `Repeater` e afins. O "
      "QML não usa colunas nem `DisplayRole`: ele acessa **papéis por nome**, definidos em `roleNames()`. "
      "No delegate, declare cada papel como `required property` — a forma recomendada no Qt 6, que torna as "
      "dependências explícitas e verificáveis."),
    lst("c26_modelo.qml", "ListView com delegate que usa required properties", lang="qml",
        nota="✔ Arquivo carregado pela Listagem 26.4 (executada e verificada)."),
    lst("c26_modelo.py", "QAbstractListModel com roleNames() exibido em QML"),
    out("c26_modelo"),
    p("As notificações do modelo (`beginInsertRows`/`endInsertRows`, `dataChanged` com a lista de papéis) "
      "atualizam a lista sem recriar os delegates existentes: o terceiro poço apareceu e o primeiro passou a "
      "inativo."),

    h2("QQuickWidget: QML dentro de aplicações Widgets"),
    p("`QQuickWidget` é um widget que exibe uma cena QML: entra em layouts, recebe foco e pode ser capturado "
      "com `grab()`. A comunicação nos dois sentidos usa propriedades (`rootObject().setProperty`) e sinais "
      "declarados em QML, conectados diretamente no Python (`raiz.alarme.connect(...)`)."),
    lst("c26_indicador.qml", "Indicador circular em QML com propriedade, sinal e animação", lang="qml",
        nota="✔ Arquivo carregado pela Listagem 26.6 (executada e verificada)."),
    lst("c26_qquickwidget.py", "QQuickWidget em uma janela Widgets com QSlider e sinal QML"),
    out("c26_qquickwidget"),
    img("Componente QML (indicador) controlado por um QSlider em janela Widgets", "f26_1_qquickwidget.png", 9.5),
    note("DICA", "`QQuickWidget` desenha em uma textura e a compõe com os widgets, o que tem custo. Para uma "
                 "cena QML grande e independente, `QWidget.createWindowContainer(QQuickView)` é mais eficiente, "
                 "com a restrição de que nada pode ser sobreposto à janela embutida."),

    h2("Qt Quick Controls e estilos"),
    p("Os Qt Quick Controls (`Button`, `SpinBox`, `ApplicationWindow`...) têm estilos intercambiáveis. O "
      "PyQt6 não inclui o módulo `QtQuickControls2` (não há `QQuickStyle`); o estilo é escolhido pela variável "
      "de ambiente `QT_QUICK_CONTROLS_STYLE`, pelo arquivo `qtquickcontrols2.conf` empacotado com o QML ou "
      "pelo argumento de linha de comando `-style`. A Listagem 26.2 rodou com `Fusion`."),
    tab("Estilos do Qt Quick Controls presentes nas wheels PyQt6-Qt6 6.12 (Linux)",
        ["Estilo", "Características"],
        [["Basic", "Leve e neutro; base para estilos próprios"],
         ["Fusion", "Aparência de desktop, igual ao estilo Fusion dos Widgets"],
         ["Material", "Google Material Design, com temas claro/escuro e cor de destaque"],
         ["Universal", "Diretrizes de design da Microsoft (Universal)"],
         ["FluentWinUI3", "Aparência do Windows 11 (WinUI 3)"],
         ["Imagine", "Baseado em imagens (9-patch) fornecidas pelo projeto"],
         ["Native", "Seleciona o estilo nativo da plataforma (Windows, macOS, iOS)"]],
        [2200, 6871]),

    h2("Exercícios do capítulo"),
    nl("Acrescente à Listagem 26.2 um `TextField` com validação numérica ligado a `Tanque.nivel`.",
       "Exiba o modelo `ModeloPocos` em uma `TableView` QML com duas colunas.",
       "Implemente o indicador da Listagem 26.5 como `QQuickPaintedItem` em Python e compare.",
       "Rode a Listagem 26.2 com os estilos Material e Universal e compare as capturas."),
)
