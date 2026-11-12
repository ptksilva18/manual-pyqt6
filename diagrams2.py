# -*- coding: utf-8 -*-
"""Diagramas didáticos das Partes III e IV (Pillow, 2x), reutilizando diagrams.py."""
from PIL import Image, ImageDraw

from diagrams import BLUE, GREEN, GREY, NAVY, ORANGE, arrow, box, label, save


def fig_20_1():
    W, H = 2000, 1080
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((20, 20, 860, 980), 24, outline=BLUE, width=4)
    d.rounded_rectangle((1140, 20, 1980, 980), 24, outline=GREEN, width=4)
    label(d, (440, 66), "Thread da GUI (principal)", 38, NAVY, bold=True)
    label(d, (1560, 66), "QThread (event loop próprio)", 38, GREEN, bold=True)
    box(d, (70, 130, 810, 310), ["Janela / Controlador", "cria QThread e worker; moveToThread()"], "blue")
    box(d, (70, 400, 810, 560), ["Slots da GUI", "ao_progresso, ao_resultado, ao_erro"], "blue")
    box(d, (70, 650, 810, 810), ["requestInterruption()", "quit() + wait() no fechamento"], "orange")
    box(d, (1190, 130, 1930, 310), ["Worker (QObject)", "executar(): laço com verificação"], "green")
    box(d, (1190, 400, 1930, 560), ["Sinais emitidos", "progresso, resultado, erro, finalizado"], "green")
    box(d, (1190, 650, 1930, 810), ["isInterruptionRequested()", "encerra o laço com segurança"], "orange")
    arrow(d, (814, 220), (1186, 220))
    label(d, (1000, 186), "started → executar", 28, GREY)
    arrow(d, (1186, 480), (814, 480), GREEN)
    label(d, (1000, 446), "conexão enfileirada", 28, GREEN)
    arrow(d, (814, 730), (1186, 730), ORANGE, dashed=True)
    label(d, (1000, 696), "pedido de parada", 28, ORANGE)
    label(d, (W / 2, 900), "Fila de eventos da thread receptora", 30, GREY)
    label(d, (W / 2, 1040), "Regra de ouro: widgets só são acessados na thread da GUI; "
          "dados cruzam threads por sinais.", 32, NAVY)
    save(im, "f20_1_worker.png")


def fig_21_1():
    W, H = 2000, 820
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    etapas = [(["Instrumento", "RS-232/485 ou USB"], "grey"),
              (["QSerialPort", "readyRead (sem bloqueio)"], "blue"),
              (["Enquadramento", "canReadLine + parse"], "green"),
              (["Modelo / buffer", "deque ou numpy"], "purple"),
              (["Gráfico em tempo real", "pyqtgraph / QtGraphs"], "orange")]
    x, w, g = 20, 330, 72
    for i, (txt, kind) in enumerate(etapas):
        box(d, (x, 230, x + w, 450), txt, kind, sz=27)
        if i:
            arrow(d, (x - g + 4, 340), (x - 4, 340))
        x += w + g
    d.rounded_rectangle((398, 140, 1178, 520), 26, outline=BLUE, width=3)
    label(d, (788, 110), "thread de aquisição (opcional, para taxas altas)", 28, BLUE)
    label(d, (1400, 610), "sinal amostra(seq, p, T) — conexão enfileirada", 28, GREEN)
    arrow(d, (1180, 565), (1620, 565), GREEN, dashed=True)
    label(d, (W / 2, 740), "A aquisição nunca bloqueia a interface; erros de porta chegam por "
          "errorOccurred.", 32, NAVY)
    save(im, "f21_1_serial.png")


def fig_24_1():
    W, H = 2000, 900
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((20, 40, 900, 760), 24, outline=BLUE, width=4)
    d.rounded_rectangle((1100, 40, 1980, 760), 24, outline=ORANGE, width=4)
    label(d, (460, 86), "Processo Python (PyQt6)", 36, NAVY, bold=True)
    label(d, (1540, 86), "Página Web (Chromium)", 36, ORANGE, bold=True)
    box(d, (70, 150, 850, 330), ["QObject Python", "pyqtProperty, pyqtSlot, pyqtSignal"], "green")
    box(d, (70, 430, 850, 600), ["QWebChannel", "registerObject(\"ponte\", obj)"], "blue")
    box(d, (1150, 150, 1930, 330), ["JavaScript da página", "ponte.calcular(x, callback)"], "orange")
    box(d, (1150, 430, 1930, 600), ["qwebchannel.js", "new QWebChannel(qt.webChannelTransport, …)"],
        "orange", sz=30)
    arrow(d, (460, 334), (460, 426))
    arrow(d, (1540, 426), (1540, 334))
    arrow(d, (854, 490), (1146, 490))
    arrow(d, (1146, 545), (854, 545))
    label(d, (1000, 456), "mensagens JSON", 28, GREY)
    label(d, (1000, 640), "QWebEnginePage.setWebChannel()", 28, GREY)
    label(d, (W / 2, 840), "Chamadas de slots são assíncronas no JavaScript: o resultado chega "
          "por callback.", 32, NAVY)
    save(im, "f24_1_webchannel.png")


def fig_27_1():
    W, H = 2000, 1180
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    camadas = [(["Apresentação — Views", "widgets, arquivos .ui, QML; sem regra de negócio"], "blue"),
               (["Presenters / ViewModels", "estado da tela, comandos, validação de entrada"], "teal"),
               (["Serviços de aplicação", "casos de uso, orquestração, threads, undo"], "green"),
               (["Domínio", "entidades e cálculos puros em Python (sem Qt)"], "orange"),
               (["Infraestrutura", "arquivos, banco de dados, rede, instrumentos"], "grey")]
    y = 30
    for i, (txt, kind) in enumerate(camadas):
        box(d, (260, y, 1740, y + 170), txt, kind, sz=36)
        if i:
            arrow(d, (1000, y - 50), (1000, y - 4))
        y += 220
    label(d, (130, 560), "depende de ↓", 30, GREY)
    label(d, (1870, 560), "testável", 30, GREEN)
    label(d, (1870, 600), "sem tela", 30, GREEN)
    label(d, (W / 2, 1140), "Dependências apontam para dentro: o domínio não importa PyQt6 "
          "nem conhece a interface.", 32, NAVY)
    save(im, "f27_1_camadas.png")



def fig_31_1():
    W, H = 2000, 1240
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    box(d, (40, 40, 1960, 220), ["janela.py — JanelaPrincipal (QMainWindow)",
                                 "ações, QTableView, QTabWidget, pyqtgraph, QDockWidget, QSettings"],
        "blue", sz=34)
    box(d, (40, 300, 620, 480), ["modelos.py", "ModeloEnsaios, ModeloLeituras"], "teal", sz=32)
    box(d, (710, 300, 1290, 480), ["servicos.py", "ServicoAnalise (QThreadPool)"], "green", sz=32)
    box(d, (1380, 300, 1960, 480), ["relatorio.py", "QTextDocument → QPdfWriter"], "green", sz=32)
    box(d, (700, 580, 1600, 760), ["dominio.py — Leitura, Criterio, Resultado, analisar()",
                                   "Python puro: regressão, compensação térmica, aceitação"],
        "orange", sz=34)
    box(d, (40, 860, 620, 1040), ["repositorio.py", "SQLite (sqlite3)"], "grey", sz=32)
    box(d, (710, 860, 1290, 1040), ["importacao.py", "CSV (; ou , e vírgula decimal)"], "grey",
        sz=30)
    box(d, (1380, 860, 1960, 1040), ["app.py", "composição, autoteste, QStandardPaths"], "purple",
        sz=30)
    for x in (330, 1000, 1670):
        arrow(d, (x, 224), (x, 296))
    arrow(d, (1000, 484), (1000, 576))
    arrow(d, (1670, 484), (1500, 576))
    arrow(d, (665, 224), (560, 856), GREY, dashed=True)
    arrow(d, (1000, 224), (1000, 296))
    arrow(d, (900, 856), (900, 764))
    arrow(d, (520, 484), (720, 600))
    arrow(d, (540, 856), (760, 764))
    d.line([(1960, 950), (1985, 950), (1985, 130)], fill=BLUE, width=4)
    arrow(d, (1985, 130), (1964, 130), BLUE)
    label(d, (W / 2, 1150), "Setas: principais dependências (quem importa quem). O domínio não importa PyQt6; "
          "app.py compõe tudo.", 32, NAVY)
    save(im, "f31_1_integrador.png")


if __name__ == "__main__":
    for fn in (fig_20_1, fig_21_1, fig_24_1, fig_27_1, fig_31_1):
        fn()
    print("diagramas (Partes III e IV) gerados")
