# -*- coding: utf-8 -*-
"""Dados tabulares verificados (PyQt6 6.12.0) usados no texto."""

# ---------------------------------------------------------------------------
# Tabela 1.2 - mapa de modulos (dados verificados nas wheels PyQt6 6.12.0)
# ---------------------------------------------------------------------------
MODULE_ROWS = [
    # modulo, pacote pip, finalidade, situacao/observacao, capitulo
    ["QtCore", "PyQt6", "Núcleo não gráfico: QObject, sinais/slots, event loop, threads, arquivos, modelos", "Essencial", "5, 13, 16, 20"],
    ["QtGui", "PyQt6", "Integração com o sistema de janelas, pintura 2D, fontes, imagens, ações, eventos de entrada", "Essencial", "8, 12, 17"],
    ["QtWidgets", "PyQt6", "Widgets clássicos de desktop, layouts, diálogos, Graphics View", "Essencial", "6–10, 14, 18"],
    ["QtSql", "PyQt6", "Acesso a bancos de dados e modelos SQL", "Ativo", "15"],
    ["QtPrintSupport", "PyQt6", "Impressão, visualização de impressão e diálogos de página", "Ativo", "17"],
    ["QtSvg / QtSvgWidgets", "PyQt6", "Renderização e geração de SVG; widget de exibição SVG", "Ativo", "17"],
    ["QtNetwork", "PyQt6", "HTTP, TCP/UDP, SSL/TLS, DNS", "Ativo", "21"],
    ["QtWebSockets", "PyQt6", "Cliente e servidor WebSocket (RFC 6455)", "Ativo", "21"],
    ["QtSerialPort", "PyQt6", "Portas seriais físicas e virtuais (instrumentação)", "Ativo", "21"],
    ["QtBluetooth / QtNfc", "PyQt6", "Conectividade Bluetooth e NFC", "Ativo (dependente de plataforma)", "21"],
    ["QtDBus", "PyQt6", "Comunicação entre processos via D-Bus", "Ativo (Linux/Unix)", "21"],
    ["QtRemoteObjects", "PyQt6", "Compartilhamento de QObjects entre processos/máquinas", "Ativo", "21"],
    ["QtMultimedia / QtMultimediaWidgets", "PyQt6", "Áudio, vídeo, câmera, captura; widget de vídeo", "Ativo", "23"],
    ["QtSpatialAudio", "PyQt6", "Som espacial 3D", "Ativo", "23"],
    ["QtTextToSpeech", "PyQt6", "Síntese de voz", "Ativo", "23"],
    ["QtPositioning", "PyQt6", "Posicionamento (GNSS, Wi-Fi, NMEA)", "Ativo", "23"],
    ["QtSensors", "PyQt6", "Acesso a sensores do dispositivo", "Ativo", "23"],
    ["QtOpenGL / QtOpenGLWidgets", "PyQt6", "Integração OpenGL; QOpenGLWidget", "Ativo", "25"],
    ["QtQml / QtQuick", "PyQt6", "Motor QML e Qt Quick", "Ativo", "26"],
    ["QtQuickWidgets", "PyQt6", "QQuickWidget: QML embutido em aplicações Widgets", "Ativo", "26"],
    ["QtQuick3D", "PyQt6", "Integração Python com Qt Quick 3D", "Ativo (pilha 3D recomendada)", "25"],
    ["QtStateMachine", "PyQt6", "Máquinas de estado hierárquicas", "Ativo", "19"],
    ["QtHelp", "PyQt6", "Documentação pesquisável integrada à aplicação", "Ativo", "24"],
    ["QtWebChannel", "PyQt6", "Ponte entre QObjects e JavaScript", "Ativo", "24"],
    ["QtDesigner", "PyQt6", "Plugins de widgets para o Qt Designer", "Ativo", "11"],
    ["QtTest", "PyQt6", "Testes de GUI: QTest, QSignalSpy, QAbstractItemModelTester", "Ativo", "28"],
    ["QtXml", "PyQt6", "Interface DOM para XML", "Ativo", "16"],
    ["QAxContainer", "PyQt6 (só Windows)", "Controles ActiveX e objetos COM", "Ativo (Windows)", "24"],
    ["uic / lupdate", "PyQt6", "Subpacotes: carga de .ui (pyuic6) e extração de traduções (pylupdate6)", "Ferramentas", "11, 13"],
    ["sip", "PyQt6 (PyQt6-sip)", "Módulo de suporte dos bindings (sip.isdeleted, sip.delete…)", "Infraestrutura", "29"],
    ["QtCharts", "PyQt6-Charts", "Gráficos 2D sobre Graphics View", "Obsoleto desde Qt 6.10 (usar QtGraphs)", "22"],
    ["QtGraphs / QtGraphsWidgets", "PyQt6-Graphs", "Gráficos 2D (via QML) e 3D; itens 3D para Widgets", "Ativo (substituto de Charts/DataVisualization)", "22"],
    ["QtDataVisualization", "PyQt6-DataVisualization", "Gráficos 3D de barras, dispersão e superfície", "Obsoleto desde Qt 6.10 (usar QtGraphs)", "22"],
    ["Qt3DCore, Qt3DRender, Qt3DExtras, Qt3DInput, Qt3DLogic, Qt3DAnimation", "PyQt6-3D", "Framework Qt 3D", "Obsoleto desde Qt 6.8 (preferir Qt Quick 3D)", "25"],
    ["QtNetworkAuth", "PyQt6-NetworkAuth", "OAuth 1.0 e OAuth 2.0", "Ativo", "21"],
    ["QtWebEngineCore / QtWebEngineWidgets / QtWebEngineQuick", "PyQt6-WebEngine", "Navegador baseado em Chromium", "Ativo", "24"],
]

PYQT5_TO_6 = [
    ["Enums", "Qt.AlignCenter", "Qt.AlignmentFlag.AlignCenter (nome totalmente qualificado é obrigatório)"],
    ["Event loop", "app.exec_() / dialog.exec_()", "app.exec() / dialog.exec() (exec_ foi removido)"],
    ["Ações e atalhos", "QtWidgets.QAction, QShortcut, QActionGroup", "Movidos para QtGui"],
    ["Undo/Redo", "QtWidgets.QUndoStack, QUndoCommand, QUndoGroup", "Movidos para QtGui (QUndoView permanece em QtWidgets)"],
    ["Modelo de arquivos", "QtWidgets.QFileSystemModel", "Movido para QtGui"],
    ["Telas", "QDesktopWidget", "Removido; usar QScreen (QGuiApplication.primaryScreen(), screens())"],
    ["Expressões regulares", "QRegExp", "Removido; usar QRegularExpression"],
    ["Métricas de fonte", "QFontMetrics.width()", "Removido; usar horizontalAdvance()"],
    ["Eventos de mouse", "event.pos() (QPoint)", "event.position() (QPointF); pos() ainda existe, mas é obsoleto no Qt 6"],
    ["OpenGL", "QtWidgets.QOpenGLWidget", "Movido para QtOpenGLWidgets"],
    ["SVG", "QtSvg.QSvgWidget", "Movido para QtSvgWidgets"],
    ["Multimídia", "QMediaPlayer com saída implícita", "API reprojetada: QMediaPlayer + QAudioOutput + QVideoWidget/QVideoSink"],
    ["High-DPI", "AA_EnableHighDpiScaling necessário", "Escalonamento High-DPI sempre ativo"],
    ["Recursos", "pyrcc5", "Sem pyrcc6: usar arquivos/importlib.resources ou QDir.addSearchPath()"],
]

CONVENTIONS = [
    ["Texto corrido", "Calibri 11 pt, justificado", "Explicações conceituais"],
    ["`Código em linha`", "Consolas, fundo cinza", "Nomes de classes, métodos, variáveis: `QWidget.show()`"],
    ["Listagem de código", "Bloco Consolas 8 pt com barra lateral azul", "Programas completos, numerados como Listagem N.M"],
    ["**Negrito**", "Destaque", "Termos-chave na primeira ocorrência"],
    ["*Itálico*", "Ênfase", "Termos em inglês e títulos de obras"],
    ["Quadro NOTA / DICA / ATENÇÃO", "Caixa com barra colorida", "Informações complementares, boas práticas e armadilhas"],
    ["Saída", "Título \"Saída\" seguido de bloco Consolas", "Saída real capturada na execução da listagem anterior"],
    ["✔ linha verde após a listagem", "Itálico verde", "Código executado e verificado, ou arquivo carregado por listagem verificada"],
    ["⚠ linha laranja após a listagem", "Itálico laranja", "Código que exige plataforma indisponível no ambiente de teste (p.ex. Windows)"],
]

