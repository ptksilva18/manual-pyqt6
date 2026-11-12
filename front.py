# -*- coding: utf-8 -*-
"""Textos de abertura (Prefácio), estrutura dos Anexos e grupos do catálogo — edição em português."""
from blocks import bl, flat, p  # noqa: F401
import anexo_b as AB
import part2_anexos as PA

FRONT_UNNUMBERED = flat(
    dict(k="hu", t="Prefácio — Como usar este manual"),
    p("Este manual conduz o leitor do primeiro `import` ao empacotamento de uma aplicação desktop profissional "
      "escrita em Python com PyQt6. O texto é progressivo: cada capítulo depende apenas dos anteriores, e cada "
      "Parte termina com exercícios e um incremento do projeto integrador."),
    p("Versão de referência: **Python ≥ 3.10**, **PyQt6 6.12.0** e **Qt 6.12 (LTS)**. Os nomes de módulos e classes "
      "citados neste manual foram conferidos por introspecção nas wheels oficiais PyQt6 6.12.0 (PyPI) para "
      "Linux, Windows e macOS."),
    p("**Como o código foi verificado.** Todas as listagens Python marcadas com ✔ foram executadas com "
      "Python 3.13, PyQt6 6.12.0 e Qt 6.12.0 em Linux, sem interação humana: a interface rodou na plataforma "
      "`offscreen` do Qt ou, quando havia OpenGL, Vulkan ou Qt Quick 3D, sob um servidor X virtual com "
      "renderização por software. Os blocos \"Saída\" reproduzem a saída real dessas execuções — tempos e "
      "valores de desempenho variam de máquina para máquina. Comportamentos inesperados encontrados nos "
      "testes estão registrados em quadros de ATENÇÃO, com a solução adotada. Listagens que exigem outra "
      "plataforma (Windows) estão marcadas com ⚠."),
    bl("**Parte I — Fundamentos** (nível Básico): ambiente, Python para GUI, QObject, sinais/slots, widgets, layouts, janela principal, diálogos e eventos.",
       "**Parte II — Interface profissional** (nível Intermediário): Qt Designer, estilos, recursos, Model/View, banco de dados, arquivos, pintura 2D, Graphics View e animação.",
       "**Parte III — Desenvolvimento avançado** (nível Avançado): concorrência, redes, visualização de dados, multimídia, Web, 3D e QML.",
       "**Parte IV — Qualidade, arquitetura e distribuição** (nível Avançado): arquitetura, testes, desempenho, acessibilidade e empacotamento.",
       "**Parte V — Projeto integrador**: aplicação técnica completa, construída de ponta a ponta.",
       "**Anexos**: catálogo completo de classes do PyQt6 6.12, referências rápidas, ferramentas e glossário."),
)

ANNEXES = flat(
    dict(k="ha", lvl=1, t="Catálogo de classes do PyQt6 6.12 por módulo"),
    p("Este anexo foi gerado automaticamente por introspecção dos arquivos de stubs (`.pyi`) das wheels oficiais "
      "PyQt6 6.12.0, PyQt6-Charts 6.12.0, PyQt6-Graphs 6.12.0, PyQt6-DataVisualization 6.12.0, PyQt6-3D 6.12.0, "
      "PyQt6-NetworkAuth 6.12.0 e PyQt6-WebEngine 6.140.0. São listadas as classes de nível de módulo — incluindo "
      "namespaces (por exemplo, `Qt`) e enums declarados no nível do módulo — e as funções de nível de módulo. "
      "Classes aninhadas e enums internos às classes não são listados separadamente. O módulo QAxContainer foi "
      "extraído da wheel para Windows."),
    dict(k="catalog"),
    dict(k="ha", lvl=1, t="Referência rápida do namespace Qt e enums frequentes"),
    AB.ANEXO_B,
    dict(k="ha", lvl=1, t="Referência rápida de Qt Style Sheets"),
    PA.ANEXO_C,
    dict(k="ha", lvl=1, t="Ferramentas de linha de comando"),
    PA.ANEXO_D,
)

CATALOG_GROUPS = [
    ("PyQt6 — núcleo", ["QtCore", "QtGui", "QtWidgets", "QtBluetooth", "QtDBus", "QtDesigner", "QtHelp",
                        "QtMultimedia", "QtMultimediaWidgets", "QtNetwork", "QtNfc", "QtOpenGL", "QtOpenGLWidgets",
                        "QtPositioning", "QtPrintSupport", "QtQml", "QtQuick", "QtQuick3D", "QtQuickWidgets",
                        "QtRemoteObjects", "QtSensors", "QtSerialPort", "QtSpatialAudio", "QtSql", "QtStateMachine",
                        "QtSvg", "QtSvgWidgets", "QtTest", "QtTextToSpeech", "QtWebChannel", "QtWebSockets", "QtXml",
                        "QAxContainer"]),
    ("PyQt6-Charts", ["QtCharts"]),
    ("PyQt6-Graphs", ["QtGraphs", "QtGraphsWidgets"]),
    ("PyQt6-DataVisualization", ["QtDataVisualization"]),
    ("PyQt6-3D", ["Qt3DCore", "Qt3DRender", "Qt3DExtras", "Qt3DInput", "Qt3DLogic", "Qt3DAnimation"]),
    ("PyQt6-NetworkAuth", ["QtNetworkAuth"]),
    ("PyQt6-WebEngine", ["QtWebEngineCore", "QtWebEngineWidgets", "QtWebEngineQuick"]),
]
