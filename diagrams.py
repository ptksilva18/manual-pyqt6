# -*- coding: utf-8 -*-
"""Diagramas didáticos da Parte I (desenhados com Pillow, 2x)."""
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, "data", "figs")
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FM = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
NAVY, BLUE, LBLUE, GREEN, ORANGE, GREY = (31, 56, 100), (46, 117, 182), (234, 241, 250), (84, 130, 53), (197, 90, 17), (90, 90, 90)
PALE = {"blue": (234, 241, 250), "green": (238, 245, 233), "orange": (251, 239, 230), "grey": (242, 242, 242),
        "purple": (240, 234, 247), "teal": (230, 244, 244)}
EDGE = {"blue": BLUE, "green": GREEN, "orange": ORANGE, "grey": (130, 130, 130), "purple": (112, 48, 160),
        "teal": (0, 128, 128)}


def font(sz, bold=False, mono=False):
    return ImageFont.truetype(FM if mono else (FB if bold else F), sz)


def box(d, xy, lines, kind="blue", title_bold=True, sz=34, align="center", radius=18, width=4):
    x0, y0, x1, y1 = xy
    d.rounded_rectangle(xy, radius=radius, fill=PALE[kind], outline=EDGE[kind], width=width)
    avail = (x1 - x0) - 40
    tmp = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    while sz > 18 and max(tmp.textlength(ln, font=font(sz, bold=(i == 0 and title_bold)))
                          for i, ln in enumerate(lines)) > avail:
        sz -= 1
    fonts = [font(sz, bold=(i == 0 and title_bold)) for i in range(len(lines))]
    hs = [f.size + 10 for f in fonts]
    y = (y0 + y1) / 2 - sum(hs) / 2 + 4
    for ln, f, h in zip(lines, fonts, hs):
        col = NAVY if f is fonts[0] and title_bold else (50, 50, 50)
        if align == "center":
            d.text(((x0 + x1) / 2, y + h / 2), ln, font=f, fill=col, anchor="mm")
        else:
            d.text((x0 + 28, y + h / 2), ln, font=f, fill=col, anchor="lm")
        y += h


def arrow(d, p0, p1, color=NAVY, width=5, head=22, dashed=False):
    x0, y0 = p0
    x1, y1 = p1
    ang = math.atan2(y1 - y0, x1 - x0)
    xe, ye = x1 - head * 0.8 * math.cos(ang), y1 - head * 0.8 * math.sin(ang)
    if dashed:
        L = math.hypot(xe - x0, ye - y0)
        n = int(L // 26)
        for i in range(0, n, 2):
            a, b = i / n, min((i + 1) / n, 1)
            d.line([(x0 + (xe - x0) * a, y0 + (ye - y0) * a), (x0 + (xe - x0) * b, y0 + (ye - y0) * b)],
                   fill=color, width=width)
    else:
        d.line([(x0, y0), (xe, ye)], fill=color, width=width)
    pts = [(x1, y1),
           (x1 - head * math.cos(ang - 0.42), y1 - head * math.sin(ang - 0.42)),
           (x1 - head * math.cos(ang + 0.42), y1 - head * math.sin(ang + 0.42))]
    d.polygon(pts, fill=color)


def label(d, xy, text, sz=28, color=GREY, anchor="mm", bold=False):
    d.text(xy, text, font=font(sz, bold), fill=color, anchor=anchor)


def save(img, name):
    img.save(os.path.join(FIG, name), dpi=(300, 300))


# ------------------------------------------------------------------ 1.1 ----
def fig_1_1():
    W, H = 1900, 1160
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    camadas = [
        (["Sua aplicação Python", "classes, sinais e slots, lógica de negócio (.py)"], "green"),
        (["PyQt6 — bindings gerados com SIP", "módulos de extensão QtCore, QtGui, QtWidgets… + PyQt6-sip"], "blue"),
        (["Bibliotecas Qt 6 (C++)", "Qt6Core, Qt6Gui, Qt6Widgets… distribuídas no pacote PyQt6-Qt6"], "blue"),
        (["Plugins de plataforma do Qt", "windows · cocoa (macOS) · xcb / wayland (Linux) · offscreen"], "orange"),
        (["Sistema operacional", "Windows · macOS · Linux"], "grey"),
    ]
    x0, x1, h, gap, y = 220, 1610, 170, 52, 40
    for i, (ln, k) in enumerate(camadas):
        box(d, (x0, y, x1, y + h), ln, k, sz=36)
        if i < len(camadas) - 1:
            arrow(d, ((x0 + x1) / 2, y + h + 4), ((x0 + x1) / 2, y + h + gap - 4))
        y += h + gap
    # chaves laterais
    d.line([(1650, 40), (1680, 40), (1680, 40 + 2 * h + gap), (1650, 40 + 2 * h + gap)], fill=GREEN, width=5)
    label(d, (1790, 40 + h + gap / 2), "Python", 38, GREEN, bold=True)
    yc = 40 + 2 * (h + gap)
    d.line([(1650, yc), (1680, yc), (1680, yc + 2 * h + gap), (1650, yc + 2 * h + gap)], fill=BLUE, width=5)
    label(d, (1790, yc + h + gap / 2), "C++", 38, BLUE, bold=True)
    label(d, (110, 40 + h + gap / 2 - 10), "chamadas", 32, GREY)
    label(d, (110, 40 + h + gap / 2 + 34), "↓ ↑", 36, GREY)
    label(d, (110, 40 + h + gap / 2 + 80), "sinais", 32, GREY)
    save(im, "f1_1_arquitetura.png")


# ------------------------------------------------------------------ 1.2 ----
def fig_1_2():
    W, H = 1980, 1500
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    grupos = [
        ("Núcleo", "green", ["QtCore", "QtGui", "QtWidgets"]),
        ("Dados e documentos", "blue", ["QtSql", "QtXml", "QtPrintSupport", "QtSvg · QtSvgWidgets"]),
        ("Rede e dispositivos", "blue", ["QtNetwork · QtWebSockets", "QtNetworkAuth*", "QtRemoteObjects · QtDBus",
                                          "QtSerialPort", "QtBluetooth · QtNfc"]),
        ("Multimídia e sistema", "teal", ["QtMultimedia(+Widgets)", "QtSpatialAudio", "QtTextToSpeech",
                                           "QtPositioning · QtSensors"]),
        ("Gráficos 2D/3D", "orange", ["QtOpenGL(+Widgets)", "QtGraphs* · QtGraphsWidgets*", "QtQuick3D",
                                       "QtCharts* (obsoleto)", "QtDataVisualization* (obsoleto)", "Qt3D* (obsoleto)"]),
        ("Web", "purple", ["QtWebEngineCore*", "QtWebEngineWidgets*", "QtWebEngineQuick*", "QtWebChannel"]),
        ("QML / Qt Quick", "purple", ["QtQml", "QtQuick", "QtQuickWidgets"]),
        ("Ferramentas e qualidade", "grey", ["QtTest · QtDesigner · QtHelp", "QtStateMachine",
                                              "uic (pyuic6) · lupdate (pylupdate6)", "QAxContainer (Windows)"]),
    ]
    cols, cw, ch_, gx, gy, x_ini, y_ini = 3, 630, 450, 30, 35, 15, 15
    for i, (tit, k, mods) in enumerate(grupos):
        c, r = i % cols, i // cols
        x0 = x_ini + c * (cw + gx)
        y0 = y_ini + r * (ch_ + gy)
        d.rounded_rectangle((x0, y0, x0 + cw, y0 + ch_), radius=18, fill=PALE[k], outline=EDGE[k], width=4)
        d.rounded_rectangle((x0, y0, x0 + cw, y0 + 76), radius=18, fill=EDGE[k])
        d.rectangle((x0, y0 + 50, x0 + cw, y0 + 76), fill=EDGE[k])
        label(d, (x0 + cw / 2, y0 + 39), tit, 34, (255, 255, 255), bold=True)
        yy = y0 + 112
        for m in mods:
            col = (150, 150, 150) if "obsoleto" in m else (40, 40, 40)
            label(d, (x0 + 22, yy), m, 32, col, anchor="lm")
            yy += 55
    x0, y0 = x_ini + 2 * (cw + gx), y_ini + 2 * (ch_ + gy)
    d.rounded_rectangle((x0, y0, x0 + cw, y0 + ch_), radius=18, fill="white", outline=(190, 190, 190), width=3)
    for i, t in enumerate(["Legenda", "* módulo de pacote add-on", "   (instalado com pip à parte)",
                           "cinza = obsoleto no Qt 6", "   (evitar em código novo)"]):
        label(d, (x0 + 26, y0 + 60 + i * 62), t, 34 if i == 0 else 31, NAVY if i == 0 else GREY,
              anchor="lm", bold=(i == 0))
    save(im, "f1_2_mapa_modulos.png")


# ------------------------------------------------------------------ 2.1 ----
def fig_2_1():
    linhas = [
        "calc-engenharia/",
        "├── pyproject.toml            # metadados, dependências, entry points",
        "├── README.md",
        "├── src/",
        "│   └── calc_engenharia/",
        "│       ├── __init__.py",
        "│       ├── __main__.py       # ponto de entrada: main()",
        "│       ├── app.py            # cria QApplication e a janela principal",
        "│       ├── ui/               # janelas, diálogos e arquivos .ui",
        "│       ├── models/           # modelos de dados (Model/View)",
        "│       ├── services/         # cálculos e regras de negócio (sem Qt)",
        "│       └── resources/        # ícones, folhas de estilo .qss, traduções",
        "├── tests/",
        "│   └── test_janela.py        # testes (pytest-qt)",
        "└── docs/",
    ]
    f = font(34, mono=True)
    W, H = 1640, 60 + len(linhas) * 54 + 40
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((10, 10, W - 10, H - 10), radius=18, fill=(248, 250, 252), outline=BLUE, width=4)
    y = 50
    for ln in linhas:
        if "#" in ln:
            a, b = ln.split("#", 1)
            d.text((60, y), a, font=f, fill=(30, 30, 30))
            d.text((60 + d.textlength(a, font=f), y), "#" + b, font=f, fill=(0, 128, 0))
        else:
            d.text((60, y), ln, font=f, fill=NAVY if ln.endswith("/") else (30, 30, 30))
        y += 54
    save(im, "f2_1_estrutura.png")


# ------------------------------------------------------------------ 4.2 ----
def fig_4_2():
    W, H = 2000, 1180
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    bw, bh, y0 = 600, 170, 30
    xs = [20, 700, 1380]
    top = [(["1. QApplication(sys.argv)", "um objeto por processo"], "green"),
           (["2. Criar widgets", "janela, layouts, conexões"], "blue"),
           (["3. janela.show()", "agenda a exibição"], "blue")]
    for (ln, k), x in zip(top, xs):
        box(d, (x, y0, x + bw, y0 + bh), ln, k, sz=36)
    for i in range(2):
        arrow(d, (xs[i] + bw + 6, y0 + bh / 2), (xs[i + 1] - 6, y0 + bh / 2))
    cx, cy, r = 1000, 600, 210
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=ORANGE, width=8)
    label(d, (cx, cy - 30), "4. app.exec()", 42, ORANGE, bold=True)
    label(d, (cx, cy + 30), "event loop", 36, ORANGE)
    arrow(d, (xs[2] + bw / 2, y0 + bh + 6), (cx + 110, cy - r - 12))
    etapas = [("aguarda evento", (cx - r - 470, cy - 150)), ("despacha ao objeto", (cx + r + 40, cy - 150)),
              ("executa handlers/slots", (cx + r + 40, cy + 80)), ("repinta a tela", (cx - r - 470, cy + 80))]
    for t, (x, y) in etapas:
        d.rounded_rectangle((x, y, x + 430, y + 76), radius=14, fill=PALE["orange"], outline=ORANGE, width=3)
        label(d, (x + 215, y + 38), t, 34, (60, 60, 60))
    for ang in (-60, 30, 120, 210):
        a0, a1 = math.radians(ang), math.radians(ang + 25)
        arrow(d, (cx + r * math.cos(a0), cy + r * math.sin(a0)),
              (cx + r * math.cos(a1), cy + r * math.sin(a1)), ORANGE, width=6, head=30)
    yb = 970
    bottom = [(["5. quit() / última janela", "o loop termina"], "grey"),
              (["6. sinal aboutToQuit", "salvar configurações"], "grey"),
              (["7. sys.exit(código)", "código de saída ao SO"], "green")]
    for (ln, k), x in zip(bottom, xs):
        box(d, (x, yb, x + bw, yb + bh), ln, k, sz=36)
    arrow(d, (cx - 110, cy + r + 8), (xs[0] + bw / 2, yb - 6))
    for i in range(2):
        arrow(d, (xs[i] + bw + 6, yb + bh / 2), (xs[i + 1] - 6, yb + bh / 2))
    save(im, "f4_2_ciclo.png")


# ------------------------------------------------------------------ 5.1 ----
def fig_5_1():
    W, H = 2000, 900
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    root = (720, 30, 1280, 200)
    box(d, root, ["QWidget", "objectName = \"janela\""], "green", sz=38)
    filhos = [(["QVBoxLayout", "layoutPrincipal"], "grey"), (["QLineEdit", "campoVazao"], "blue"),
              (["QLineEdit", "campoPressao"], "blue"), (["QPushButton", "botaoCalcular"], "blue")]
    bw, gap, y = 465, 25, 420
    x = (W - (4 * bw + 3 * gap)) / 2
    for ln, k in filhos:
        box(d, (x, y, x + bw, y + 160), ln, k, sz=38)
        arrow(d, ((root[0] + root[2]) / 2, root[3] + 6), (x + bw / 2, y - 6), width=4)
        x += bw + gap
    label(d, (360, 115), "filho.parent() → pai", 34, GREY)
    label(d, (1640, 115), "pai.children() → filhos", 34, GREY)
    label(d, (W / 2, 670), "Destruir o pai destrói automaticamente todos os filhos.", 38, NAVY)
    label(d, (W / 2, 740), "layout.addWidget(w) reparenta w para o widget dono do layout.", 34, GREY)
    label(d, (W / 2, 805), "Widgets complexos têm filhos internos (o QLineEdit cria objetos auxiliares).", 34, GREY)
    save(im, "f5_1_arvore.png")


# ------------------------------------------------------------------ 5.2 ----
def fig_5_2():
    W, H = 2000, 1000
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((20, 120, 660, 880), radius=20, fill=PALE["green"], outline=GREEN, width=4)
    label(d, (340, 180), "Sensor (emissor)", 40, NAVY, bold=True)
    for t, y in (("leituraMudou(float)", 370), ("alarme(str, float)", 620)):
        d.rounded_rectangle((60, y - 55, 620, y + 55), radius=14, fill="white", outline=GREEN, width=3)
        label(d, (340, y), t, 36, (40, 40, 40))
    label(d, (340, 800), "self.alarme.emit(tag, v)", 32, GREY)
    alvos = [(["Painel.exibir(v)", "método com @pyqtSlot"], 220, "blue"),
             (["lambda v: print(...)", "qualquer callable"], 480, "blue"),
             (["Painel.registrar_alarme", "recebe (str, float)"], 740, "orange")]
    for ln, y, k in alvos:
        box(d, (1260, y - 95, 1980, y + 95), ln, k, sz=36)
    arrow(d, (622, 370), (1254, 220))
    arrow(d, (622, 370), (1254, 480))
    arrow(d, (622, 620), (1254, 740))
    for (x, y) in ((900, 255), (960, 470), (900, 625)):
        label(d, (x, y), "connect()", 32, GREY)
    label(d, (W / 2, 55), "Um sinal pode ter vários receptores; um slot pode receber vários sinais.", 36, NAVY)
    label(d, (W / 2, 945), "O emissor não conhece os receptores: baixo acoplamento.", 34, GREY)
    save(im, "f5_2_sinais.png")


# ----------------------------------------------------------------- 10.1 ----
def fig_10_1():
    W, H = 2000, 1000
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    l1 = [(["Sistema operacional", "evento nativo"], "grey"), (["Plugin de plataforma", "converte em QEvent"], "orange"),
          (["Fila de eventos", "event loop"], "orange"), (["QApplication.notify()", "entrega ao objeto"], "blue")]
    l2 = [(["Filtros da aplicação", "app.installEventFilter"], "purple"),
          (["Filtros do objeto", "eventFilter()"], "purple"),
          (["QWidget.event()", "despachante geral"], "blue"), (["Handler específico", "mousePressEvent()…"], "green")]
    bw, bh, gap = 460, 180, 40
    y1, y2 = 40, 450
    xs = [20 + i * (bw + gap) for i in range(4)]
    for (ln, k), x in zip(l1, xs):
        box(d, (x, y1, x + bw, y1 + bh), ln, k, sz=36)
    for (ln, k), x in zip(l2, xs):
        box(d, (x, y2, x + bw, y2 + bh), ln, k, sz=36)
    for i in range(3):
        arrow(d, (xs[i] + bw + 4, y1 + bh / 2), (xs[i + 1] - 4, y1 + bh / 2))
        arrow(d, (xs[i] + bw + 4, y2 + bh / 2), (xs[i + 1] - 4, y2 + bh / 2))
    arrow(d, (xs[3] + bw / 2, y1 + bh + 4), (xs[0] + bw / 2, y2 - 4))
    arrow(d, (xs[1] + bw / 2, y2 + bh + 4), (xs[1] + bw / 2, y2 + bh + 110), (192, 0, 0), dashed=True)
    label(d, (xs[1] + bw / 2, y2 + bh + 150), "retorna True: evento consumido", 33, (192, 0, 0))
    arrow(d, (xs[3] + bw / 2, y2 + bh + 4), (xs[3] + bw / 2, y2 + bh + 110), GREEN, dashed=True)
    label(d, (xs[3] + bw / 2 - 40, y2 + bh + 150), "ignore(): sobe ao widget pai", 33, GREEN)
    label(d, (W / 2, H - 45), "Eventos de entrada ignorados sobem pela árvore de widgets até alguém aceitar.", 35, NAVY)
    save(im, "f10_1_eventos.png")



# ----------------------------------------------------------------- 13.1 ----
def fig_13_1():
    W, H = 2000, 760
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    etapas = [(["Código-fonte", "self.tr(\"Pipe check\")"], "green"),
              (["pylupdate6", "extrai os textos"], "orange"),
              (["arquivo .ts (XML)", "traduções a preencher"], "blue"),
              (["Qt Linguist", "o tradutor preenche"], "orange"),
              (["lrelease", "compila"], "orange"),
              (["arquivo .qm", "binário compacto"], "blue")]
    bw, bh, gap = 600, 170, 70
    pos = [(30, 40), (700, 40), (1370, 40), (1370, 300), (700, 300), (30, 300)]
    for (ln, k), (x, y) in zip(etapas, pos):
        box(d, (x, y, x + bw, y + bh), ln, k, sz=36)
    arrow(d, (630 + 4, 125), (700 - 4, 125))
    arrow(d, (1300 + 4, 125), (1370 - 4, 125))
    arrow(d, (1670, 210 + 4), (1670, 300 - 4))
    arrow(d, (1370 - 4, 385), (1300 + 4, 385))
    arrow(d, (700 - 4, 385), (630 + 4, 385))
    box(d, (30, 560, 1300, 720), ["QTranslator.load(\"app_pt_BR.qm\") + app.installTranslator()",
                                  "tr() passa a devolver o texto traduzido em tempo de execução"], "green", sz=34)
    arrow(d, (330, 470 + 4), (330, 560 - 4))
    box(d, (1370, 560, 1970, 720), ["qtbase_pt_BR.qm", "textos internos do Qt"], "grey", sz=34)
    arrow(d, (1370 - 4, 640), (1300 + 4, 640))
    save(im, "f13_1_traducao.png")


# ----------------------------------------------------------------- 14.1 ----
def fig_14_1():
    W, H = 2000, 980
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    box(d, (20, 330, 380, 530), ["Dados", "lista, BD, DataFrame"], "grey", sz=38)
    box(d, (500, 330, 900, 530), ["Modelo", "QAbstractItemModel"], "green", sz=38)
    box(d, (1020, 330, 1440, 530), ["Proxy (opcional)", "QSortFilterProxyModel"], "purple", sz=36)
    box(d, (1560, 330, 1980, 530), ["Visão", "QTableView / QTreeView"], "blue", sz=36)
    arrow(d, (384, 430), (496, 430))
    arrow(d, (904, 410), (1016, 410))
    arrow(d, (1016, 455), (904, 455))
    arrow(d, (1444, 410), (1556, 410))
    arrow(d, (1556, 455), (1444, 455))
    label(d, (960, 300), "dados / sinais", 28, GREY)
    label(d, (1500, 300), "índices", 28, GREY)
    box(d, (1560, 40, 1980, 220), ["Delegado", "pinta e edita células"], "orange", sz=36)
    arrow(d, (1770, 224), (1770, 326))
    box(d, (1560, 690, 1980, 870), ["QItemSelectionModel", "itens selecionados"], "teal", sz=34)
    arrow(d, (1770, 534), (1770, 686))
    box(d, (500, 690, 1440, 870), ["Sinais do modelo: dataChanged, rowsInserted,",
                                    "rowsRemoved, layoutChanged, modelReset"], "green", sz=34, title_bold=False)
    arrow(d, (700, 534), (700, 686), GREEN, dashed=True)
    label(d, (W / 2, 950), "Uma mesma fonte de dados pode alimentar várias visões, cada uma com seu proxy e delegado.",
          32, NAVY)
    save(im, "f14_1_modelview.png")


if __name__ == "__main__":
    for fn in (fig_1_1, fig_1_2, fig_2_1, fig_4_2, fig_5_1, fig_5_2, fig_10_1, fig_13_1, fig_14_1):
        fn()
    print("diagramas gerados")
