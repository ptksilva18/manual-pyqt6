# -*- coding: utf-8 -*-
"""Conteúdo dos Anexos C (QSS) e D (ferramentas) — Step 3."""
from blocks import flat, nl, note, out, p, snip, tab

ANEXO_C = flat(
    p("Este anexo resume a sintaxe das Qt Style Sheets usada no Capítulo 12. Todas as propriedades da Tabela C.4 "
      "foram verificadas no Qt 6.12: aplicadas a uma janela com widgets de vários tipos, nenhuma gerou o aviso "
      "*Unknown property*, emitido pelo Qt quando o nome de uma propriedade é inválido."),
    tab("Seletores", ["Seletor", "Exemplo", "Seleciona"],
        [["Universal", "`*`", "Todos os widgets"],
         ["Tipo", "`QPushButton`", "Instâncias da classe e de subclasses"],
         ["Classe exata", "`.QPushButton`", "Apenas a classe, sem subclasses"],
         ["ID", "`#primario` ou `QPushButton#primario`", "objectName igual a primario"],
         ["Propriedade", "`[perigoso=\"true\"]`", "Valor de propriedade Qt ou dinâmica"],
         ["Descendente", "`QGroupBox QLabel`", "Em qualquer nível dentro do primeiro"],
         ["Filho direto", "`QGroupBox > QLabel`", "Filho imediato"],
         ["Agrupamento", "`QLineEdit, QComboBox`", "Aplica a mesma regra a vários seletores"]],
        [1900, 3471, 3700]),
    tab("Pseudo-estados frequentes", ["Pseudo-estado", "Condição", "Pseudo-estado", "Condição"],
        [[":hover", "Mouse sobre o widget", ":checked / :unchecked", "Estado marcado"],
         [":pressed", "Botão pressionado", ":indeterminate", "Terceiro estado (tristate)"],
         [":focus", "Widget com foco de teclado", ":selected", "Item selecionado (visões, abas)"],
         [":disabled / :enabled", "Habilitação", ":read-only", "Campo somente leitura"],
         [":default", "Botão padrão do diálogo", ":editable", "QComboBox editável"],
         [":flat", "Botão plano", ":open / :closed", "Menu ou combo aberto / fechado"],
         [":horizontal / :vertical", "Orientação", ":first / :last", "Primeira / última aba ou item"],
         [":alternate", "Linha alternada (alternatingRowColors)", ":!estado", "Negação, ex.: :!enabled"]],
        [1900, 2636, 1900, 2635]),
    tab("Subcontroles frequentes", ["Widget", "Subcontroles"],
        [["QGroupBox", "::title, ::indicator (quando checável)"],
         ["QCheckBox, QRadioButton", "::indicator"],
         ["QComboBox", "::drop-down, ::down-arrow"],
         ["QSpinBox, QDoubleSpinBox", "::up-button, ::down-button, ::up-arrow, ::down-arrow"],
         ["QSlider", "::groove, ::handle, ::add-page, ::sub-page"],
         ["QScrollBar", "::handle, ::add-line, ::sub-line, ::add-page, ::sub-page"],
         ["QProgressBar", "::chunk"],
         ["QTabWidget / QTabBar", "::pane, ::tab-bar / ::tab, ::close-button"],
         ["QHeaderView", "::section"],
         ["Visões (QListView, QTreeView…)", "::item, ::branch (QTreeView)"],
         ["QPushButton / QToolButton", "::menu-indicator, ::menu-button"],
         ["QMenu", "::item, ::separator, ::indicator"]],
        [3200, 5871]),
    tab("Propriedades verificadas no Qt 6.12", ["Grupo", "Propriedades"],
        [["Cores", "color, background, background-color, selection-color, selection-background-color, "
                   "alternate-background-color, gridline-color, placeholder-text-color"],
         ["Borda e caixa", "border, border-width, border-style, border-color, border-radius, border-image, margin, "
                           "padding, outline"],
         ["Dimensões", "width, height, min-width, min-height, max-width, max-height, icon-size, spacing"],
         ["Texto e fonte", "font, font-family, font-size, font-weight, font-style, text-align, text-decoration, "
                           "lineedit-password-character"],
         ["Imagens", "image, background-image, background-position, background-repeat"],
         ["Subcontroles", "subcontrol-origin, subcontrol-position, position, left, top, right, bottom"],
         ["Outras", "opacity (dicas de ferramenta), qproperty-<nome> (define uma propriedade Qt)"]],
        [1900, 7171]),
    p("O prefixo `qproperty-` define propriedades Qt do widget a partir da folha de estilo, por exemplo "
      "`QLabel { qproperty-alignment: AlignCenter; }`. A regra é aplicada uma única vez, quando o estilo é polido."),
    snip('''/* Tema mínimo coerente (trecho) */
QWidget              { font-size: 10pt; }
QLineEdit, QComboBox { border: 1px solid #BFC5CF; border-radius: 4px; padding: 3px 6px; }
QLineEdit:focus      { border: 2px solid #2E75B6; }
QPushButton          { padding: 5px 16px; border-radius: 4px; }
QPushButton:hover    { border: 1px solid #2E75B6; }
QPushButton#primario { background: #2E75B6; color: white; border: none; }
QProgressBar::chunk  { background-color: #2E75B6; }
QTableView           { gridline-color: #D9D9D9; alternate-background-color: #F2F6FB; }''', lang="text"),
    note("DICA", "Para depurar uma folha de estilo, aplique-a a um único widget (`w.setStyleSheet`) antes de "
                 "aplicá-la à aplicação inteira, e observe o console: propriedades inválidas geram *Unknown "
                 "property* e erros de sintaxe geram *Could not parse stylesheet*."),
)

ANEXO_D_TAB = tab("Ferramentas de linha de comando para projetos PyQt6",
                  ["Comando", "Função", "Origem", "Cap."],
                  [["pyuic6", "Converte arquivos .ui do Qt Designer em código Python", "PyQt6 (instalado com o pacote)", "11"],
                   ["pylupdate6", "Extrai textos traduzíveis de .py e .ui para arquivos .ts", "PyQt6 (instalado com o pacote)", "13"],
                   ["designer", "Editor visual de formulários (Qt Designer)", "Ferramentas do Qt ou pyside6-designer", "11"],
                   ["linguist", "Editor de traduções (.ts) para tradutores", "Ferramentas do Qt ou pyside6-linguist", "13"],
                   ["lrelease", "Compila .ts em .qm", "Ferramentas do Qt ou pyside6-lrelease", "13"]],
                  [1600, 3671, 2900, 900])

ANEXO_D = flat(
    p("O PyQt6 instala apenas `pyuic6` e `pylupdate6` (registrados como *entry points* do pacote, verificado na "
      "versão 6.12.0). As demais ferramentas pertencem ao Qt e podem ser obtidas pelo instalador oficial, pelos "
      "pacotes da distribuição Linux ou pelo pacote PySide6-Essentials 6.12.0, que inclui `pyside6-designer`, "
      "`pyside6-linguist` e `pyside6-lrelease` (este usado no Capítulo 13). Ferramentas do Qt operam sobre "
      "arquivos (`.ui`, `.ts`, `.qm`) independentes do binding, por isso podem ser usadas em projetos PyQt6."),
    ANEXO_D_TAB,
    out("tool_pyuic6", "Saída de pyuic6 --help (PyQt6 6.12.0)"),
    out("tool_pylupdate6", "Saída de pylupdate6 --help (PyQt6 6.12.0)"),
    p("Fluxos típicos:"),
    snip('''# Interface: gerar o módulo a partir do .ui (repetir a cada alteração no Designer)
pyuic6 ui/dados_poco.ui -o src/calc_engenharia/ui/ui_dados_poco.py

# Tradução: extrair -> traduzir no Linguist -> compilar
pylupdate6 src/ --ts resources/traducoes/calceng_pt_BR.ts
linguist resources/traducoes/calceng_pt_BR.ts
lrelease resources/traducoes/calceng_pt_BR.ts -qm resources/traducoes/calceng_pt_BR.qm''', lang="text"),
)
