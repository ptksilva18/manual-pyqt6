# -*- coding: utf-8 -*-
"""Anexo B — Referência rápida do namespace Qt e enums frequentes (Step 4).

Os nomes e valores são obtidos por introspecção do PyQt6 instalado no momento da
geração (6.12.0); qualquer membro inexistente interrompe a geração (assert).
Somente as descrições são texto editorial.
"""
import enum

from PyQt6 import QtCore
from PyQt6.QtCore import QEvent, QIODevice, Qt
from PyQt6.QtGui import QFont, QPainter
from PyQt6.QtWidgets import (QAbstractItemView, QDialogButtonBox, QHeaderView, QLineEdit,
                             QMessageBox, QSizePolicy)

from blocks import flat, p, tab

VERSAO = QtCore.PYQT_VERSION_STR


def _valor(membro: enum.Enum) -> str:
    v = membro.value
    if isinstance(membro, enum.Flag) and v > 9:
        return f"0x{v:X}"
    return str(v)


def tabela_enum(enum_cls, itens, titulo: str):
    """itens: [(nome_do_membro, descricao)]; o nome qualificado é montado por introspecção."""
    qual = f"{enum_cls.__qualname__}"
    linhas = []
    for nome, desc in itens:
        assert hasattr(enum_cls, nome), f"{qual}.{nome} não existe no PyQt6 {VERSAO}"
        linhas.append([f"{qual}.{nome}", _valor(getattr(enum_cls, nome)), desc])
    return tab(titulo, ["Membro (nome completo no PyQt6)", "Valor", "Uso"], linhas, [4100, 1000, 3971],
               font=16)


def _procurar(classe, nome_curto: str) -> str:
    """Encontra o enum de 'classe' que contém o membro 'nome_curto' (migração PyQt5 -> PyQt6)."""
    achados = []
    for atributo in dir(classe):
        obj = getattr(classe, atributo)
        if isinstance(obj, type) and issubclass(obj, enum.Enum) and nome_curto in obj.__members__:
            achados.append(f"{obj.__qualname__}.{nome_curto}")
    assert len(achados) == 1, f"{classe.__name__}.{nome_curto}: {achados}"
    return achados[0]


MIGRACAO = [(Qt, "AlignCenter"), (Qt, "AlignRight"), (Qt, "Horizontal"), (Qt, "Checked"),
            (Qt, "UserRole"), (Qt, "DisplayRole"), (Qt, "ItemIsEditable"), (Qt, "LeftButton"),
            (Qt, "ControlModifier"), (Qt, "Key_Return"), (Qt, "WA_DeleteOnClose"),
            (Qt, "FramelessWindowHint"), (Qt, "AscendingOrder"), (Qt, "KeepAspectRatio"),
            (Qt, "SmoothTransformation"), (Qt, "CustomContextMenu"), (Qt, "StrongFocus"),
            (Qt, "QueuedConnection"), (QSizePolicy, "Expanding"), (QMessageBox, "Yes"),
            (QDialogButtonBox, "Ok"), (QAbstractItemView, "SelectRows"),
            (QAbstractItemView, "NoEditTriggers"), (QHeaderView, "Stretch"),
            (QPainter, "Antialiasing"), (QFont, "Bold"), (QEvent, "KeyPress"),
            (QIODevice, "ReadOnly"), (QLineEdit, "Password")]

ANEXO_B = flat(
    p(f"Este anexo reúne os enums mais usados no dia a dia, com o **nome completo exigido pelo PyQt6** "
      f"(Capítulo 1, Seção 1.5.1) e o valor numérico. Nomes e valores foram extraídos por introspecção do "
      f"PyQt6 {VERSAO} durante a geração do documento; apenas a coluna \"Uso\" é texto editorial. Flags "
      f"(combináveis com `|`) aparecem com valor hexadecimal."),

    dict(k="ha", lvl=2, t="Migração de nomes curtos (PyQt5) para nomes completos (PyQt6)"),
    tab("Nomes de enums: PyQt5 versus PyQt6 (gerado por introspecção)", ["PyQt5", "PyQt6"],
        [[f"{c.__name__}.{n}", _procurar(c, n)] for c, n in MIGRACAO], [3300, 5771], font=16),
    p("Algumas classes herdam enums de uma classe base: `QIODevice.OpenModeFlag.ReadOnly`, usado nos "
      "capítulos anteriores, é o mesmo membro definido em `QIODeviceBase`, que a tabela mostra. Para localizar "
      "o nome completo de qualquer membro, a mesma busca usada nesta tabela pode ser feita no console: percorra `dir(Classe)`, filtre os atributos que são subclasses de `enum.Enum` e procure o "
      "nome em `__members__`."),

    dict(k="ha", lvl=2, t="Alinhamento, orientação e ordenação"),
    tabela_enum(Qt.AlignmentFlag, [
        ("AlignLeft", "Alinha à esquerda (horizontal)"),
        ("AlignRight", "Alinha à direita; recomendado para números em tabelas"),
        ("AlignHCenter", "Centraliza na horizontal"),
        ("AlignJustify", "Justifica o texto (quando suportado)"),
        ("AlignTop", "Alinha ao topo (vertical)"),
        ("AlignBottom", "Alinha à base"),
        ("AlignVCenter", "Centraliza na vertical"),
        ("AlignCenter", "AlignHCenter | AlignVCenter"),
    ], "Qt.AlignmentFlag"),
    tabela_enum(Qt.Orientation, [
        ("Horizontal", "Layouts, barras de rolagem, cabeçalhos (headerData), splitters"),
        ("Vertical", "Idem, no eixo vertical"),
    ], "Qt.Orientation"),
    tabela_enum(Qt.SortOrder, [
        ("AscendingOrder", "Ordem crescente (sort(), sortByColumn())"),
        ("DescendingOrder", "Ordem decrescente"),
    ], "Qt.SortOrder"),

    dict(k="ha", lvl=2, t="Model/View: papéis, flags de item e seleção"),
    tabela_enum(Qt.ItemDataRole, [
        ("DisplayRole", "Texto exibido (str)"),
        ("DecorationRole", "Ícone ou cor exibida (QIcon, QColor, QPixmap)"),
        ("EditRole", "Valor para edição (geralmente o dado bruto)"),
        ("ToolTipRole", "Texto da dica de ferramenta"),
        ("StatusTipRole", "Texto para a barra de status"),
        ("WhatsThisRole", "Ajuda \"O que é isto?\""),
        ("FontRole", "Fonte do item (QFont)"),
        ("TextAlignmentRole", "Alinhamento (Qt.AlignmentFlag)"),
        ("BackgroundRole", "Fundo (QBrush/QColor)"),
        ("ForegroundRole", "Cor do texto (QBrush/QColor)"),
        ("CheckStateRole", "Estado da caixa de seleção (Qt.CheckState)"),
        ("SizeHintRole", "Tamanho sugerido (QSize)"),
        ("UserRole", "Primeiro papel livre para dados da aplicação (UserRole + n)"),
    ], "Qt.ItemDataRole"),
    tabela_enum(Qt.ItemFlag, [
        ("NoItemFlags", "Nenhuma propriedade"),
        ("ItemIsSelectable", "Pode ser selecionado"),
        ("ItemIsEditable", "Pode ser editado (exige setData())"),
        ("ItemIsDragEnabled", "Pode ser arrastado"),
        ("ItemIsDropEnabled", "Aceita itens soltos sobre ele"),
        ("ItemIsUserCheckable", "Usuário pode marcar/desmarcar"),
        ("ItemIsEnabled", "Interage com o usuário"),
        ("ItemIsAutoTristate", "Estado calculado a partir dos filhos (árvores)"),
        ("ItemNeverHasChildren", "Otimização: nunca terá filhos"),
        ("ItemIsUserTristate", "Usuário pode alternar entre os três estados"),
    ], "Qt.ItemFlag"),
    tabela_enum(Qt.CheckState, [
        ("Unchecked", "Desmarcado"),
        ("PartiallyChecked", "Parcialmente marcado (tristate)"),
        ("Checked", "Marcado"),
    ], "Qt.CheckState"),
    tabela_enum(Qt.MatchFlag, [
        ("MatchExactly", "Igualdade exata (QVariant)"),
        ("MatchContains", "Contém o texto"),
        ("MatchStartsWith", "Começa com o texto"),
        ("MatchRegularExpression", "Expressão regular"),
        ("MatchCaseSensitive", "Diferencia maiúsculas e minúsculas"),
        ("MatchRecursive", "Busca também nos filhos (árvores)"),
    ], "Qt.MatchFlag (findItems(), QAbstractItemModel.match())"),

    dict(k="ha", lvl=2, t="Janelas, widgets e foco"),
    tabela_enum(Qt.WindowType, [
        ("Widget", "Padrão de QWidget (janela se não tiver pai)"),
        ("Window", "Força janela de nível superior"),
        ("Dialog", "Janela de diálogo"),
        ("Tool", "Janela de ferramentas (flutuante, fica sobre a principal)"),
        ("ToolTip", "Janela de dica"),
        ("SplashScreen", "Tela de abertura"),
        ("FramelessWindowHint", "Sem moldura do sistema"),
        ("WindowStaysOnTopHint", "Sempre visível sobre as demais"),
        ("CustomizeWindowHint", "Ativa a personalização dos botões da moldura"),
        ("WindowMinimizeButtonHint", "Botão minimizar"),
        ("WindowMaximizeButtonHint", "Botão maximizar"),
        ("WindowCloseButtonHint", "Botão fechar"),
    ], "Qt.WindowType"),
    tabela_enum(Qt.WidgetAttribute, [
        ("WA_DeleteOnClose", "Destrói o widget ao fechar (deleteLater automático)"),
        ("WA_TranslucentBackground", "Fundo translúcido (janelas sem moldura)"),
        ("WA_StyledBackground", "Pinta o fundo pela folha de estilo em subclasses de QWidget"),
        ("WA_OpaquePaintEvent", "paintEvent() pinta tudo: o Qt não limpa o fundo"),
        ("WA_TransparentForMouseEvents", "Eventos de mouse passam para o widget de baixo"),
        ("WA_Hover", "Gera eventos de hover (pseudo-estado :hover em QSS)"),
        ("WA_QuitOnClose", "Fechar o widget pode encerrar a aplicação"),
    ], "Qt.WidgetAttribute (setAttribute())"),
    tabela_enum(Qt.FocusPolicy, [
        ("NoFocus", "Não recebe foco"),
        ("TabFocus", "Recebe foco pelo Tab"),
        ("ClickFocus", "Recebe foco pelo clique"),
        ("StrongFocus", "Tab e clique"),
        ("WheelFocus", "Tab, clique e roda do mouse"),
    ], "Qt.FocusPolicy"),
    tabela_enum(Qt.ContextMenuPolicy, [
        ("DefaultContextMenu", "Chama contextMenuEvent()"),
        ("ActionsContextMenu", "Mostra as QActions do widget"),
        ("CustomContextMenu", "Emite customContextMenuRequested(QPoint)"),
        ("NoContextMenu", "Repassa ao widget pai"),
    ], "Qt.ContextMenuPolicy"),
    tabela_enum(Qt.DockWidgetArea, [
        ("LeftDockWidgetArea", "Área esquerda da QMainWindow"),
        ("RightDockWidgetArea", "Área direita"),
        ("TopDockWidgetArea", "Área superior"),
        ("BottomDockWidgetArea", "Área inferior"),
        ("AllDockWidgetAreas", "Qualquer área (setAllowedAreas())"),
    ], "Qt.DockWidgetArea"),

    dict(k="ha", lvl=2, t="Entrada: teclado e mouse"),
    tabela_enum(Qt.KeyboardModifier, [
        ("NoModifier", "Nenhum modificador"),
        ("ShiftModifier", "Shift"),
        ("ControlModifier", "Ctrl (Command no macOS)"),
        ("AltModifier", "Alt (Option no macOS)"),
        ("MetaModifier", "Tecla Windows/Super (Control no macOS)"),
        ("KeypadModifier", "Tecla do teclado numérico"),
    ], "Qt.KeyboardModifier"),
    tabela_enum(Qt.MouseButton, [
        ("NoButton", "Nenhum botão (eventos de movimento)"),
        ("LeftButton", "Botão esquerdo"),
        ("RightButton", "Botão direito"),
        ("MiddleButton", "Botão do meio (roda)"),
        ("BackButton", "Botão \"voltar\" (lateral)"),
        ("ForwardButton", "Botão \"avançar\" (lateral)"),
    ], "Qt.MouseButton"),
    tabela_enum(Qt.Key, [
        ("Key_Return", "Enter do teclado principal"),
        ("Key_Enter", "Enter do teclado numérico"),
        ("Key_Escape", "Esc"),
        ("Key_Tab", "Tab"),
        ("Key_Backspace", "Backspace"),
        ("Key_Delete", "Delete"),
        ("Key_Left", "Seta para a esquerda (Up, Right e Down análogas)"),
        ("Key_Home", "Home"),
        ("Key_PageUp", "Page Up"),
        ("Key_F1", "F1 (F2 a F35 seguem a sequência)"),
        ("Key_A", "Letras: Key_A a Key_Z (mesmo código para maiúscula e minúscula)"),
        ("Key_0", "Dígitos: Key_0 a Key_9"),
    ], "Qt.Key (keyPressEvent(), QTest.keyClick())"),
    tabela_enum(Qt.CursorShape, [
        ("ArrowCursor", "Seta padrão"),
        ("PointingHandCursor", "Mão (elementos clicáveis)"),
        ("IBeamCursor", "Edição de texto"),
        ("WaitCursor", "Ocupado (use com QApplication.setOverrideCursor)"),
        ("BusyCursor", "Ocupado, mas ainda interativo"),
        ("CrossCursor", "Cruz (seleção de pontos em gráficos)"),
        ("SizeAllCursor", "Mover"),
        ("ForbiddenCursor", "Ação não permitida"),
    ], "Qt.CursorShape"),

    dict(k="ha", lvl=2, t="Pintura e imagens"),
    tabela_enum(Qt.PenStyle, [
        ("NoPen", "Sem contorno"),
        ("SolidLine", "Linha contínua"),
        ("DashLine", "Tracejada"),
        ("DotLine", "Pontilhada"),
        ("DashDotLine", "Traço-ponto (eixos e linhas de centro)"),
        ("CustomDashLine", "Padrão definido em QPen.setDashPattern()"),
    ], "Qt.PenStyle"),
    tabela_enum(Qt.BrushStyle, [
        ("NoBrush", "Sem preenchimento"),
        ("SolidPattern", "Preenchimento sólido"),
        ("Dense4Pattern", "Retícula de densidade média (Dense1 a Dense7)"),
        ("HorPattern", "Hachura horizontal"),
        ("BDiagPattern", "Hachura diagonal (cortes em desenhos técnicos)"),
        ("DiagCrossPattern", "Hachura cruzada diagonal"),
    ], "Qt.BrushStyle"),
    tabela_enum(Qt.AspectRatioMode, [
        ("IgnoreAspectRatio", "Distorce para preencher o tamanho"),
        ("KeepAspectRatio", "Cabe no tamanho, mantendo a proporção"),
        ("KeepAspectRatioByExpanding", "Cobre o tamanho, mantendo a proporção (pode cortar)"),
    ], "Qt.AspectRatioMode (QPixmap.scaled(), QImage.scaled())"),
    tabela_enum(Qt.TransformationMode, [
        ("FastTransformation", "Vizinho mais próximo: rápido, serrilhado"),
        ("SmoothTransformation", "Bilinear: suave; use para exibição"),
    ], "Qt.TransformationMode"),
    tabela_enum(Qt.TextFormat, [
        ("PlainText", "Texto puro"),
        ("RichText", "Subconjunto de HTML"),
        ("AutoText", "Detecta automaticamente (padrão do QLabel)"),
        ("MarkdownText", "Markdown (CommonMark e GitHub)"),
    ], "Qt.TextFormat"),
)
