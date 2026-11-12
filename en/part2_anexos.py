# -*- coding: utf-8 -*-
"""Content of Annexes C (QSS) and D (tools) — English edition."""
from blocks import flat, nl, note, out, p, snip, tab

ANEXO_C = flat(
    p("This annex summarizes the Qt Style Sheets syntax used in Chapter 12. Every property in Table C.4 was "
      "verified on Qt 6.12: applied to a window with widgets of several types, none produced the *Unknown property* "
      "warning, which Qt emits when the name of a property is invalid."),
    tab("Selectors", ["Selector", "Example", "Selects"],
        [["Universal", "`*`", "All widgets"],
         ["Type", "`QPushButton`", "Instances of the class and of its subclasses"],
         ["Exact class", "`.QPushButton`", "Only the class, without subclasses"],
         ["ID", "`#primary` or `QPushButton#primary`", "objectName equal to primary"],
         ["Property", "`[dangerous=\"true\"]`", "Value of a Qt or dynamic property"],
         ["Descendant", "`QGroupBox QLabel`", "At any level inside the first one"],
         ["Direct child", "`QGroupBox > QLabel`", "Immediate child"],
         ["Grouping", "`QLineEdit, QComboBox`", "Applies the same rule to several selectors"]],
        [1900, 3471, 3700]),
    tab("Frequent pseudo-states", ["Pseudo-state", "Condition", "Pseudo-state", "Condition"],
        [[":hover", "Mouse over the widget", ":checked / :unchecked", "Checked state"],
         [":pressed", "Button pressed", ":indeterminate", "Third state (tristate)"],
         [":focus", "Widget with keyboard focus", ":selected", "Selected item (views, tabs)"],
         [":disabled / :enabled", "Enabled state", ":read-only", "Read-only field"],
         [":default", "Default button of the dialog", ":editable", "Editable QComboBox"],
         [":flat", "Flat button", ":open / :closed", "Menu or combo open / closed"],
         [":horizontal / :vertical", "Orientation", ":first / :last", "First / last tab or item"],
         [":alternate", "Alternate row (alternatingRowColors)", ":!state", "Negation, e.g. :!enabled"]],
        [1900, 2636, 1900, 2635]),
    tab("Frequent subcontrols", ["Widget", "Subcontrols"],
        [["QGroupBox", "::title, ::indicator (when checkable)"],
         ["QCheckBox, QRadioButton", "::indicator"],
         ["QComboBox", "::drop-down, ::down-arrow"],
         ["QSpinBox, QDoubleSpinBox", "::up-button, ::down-button, ::up-arrow, ::down-arrow"],
         ["QSlider", "::groove, ::handle, ::add-page, ::sub-page"],
         ["QScrollBar", "::handle, ::add-line, ::sub-line, ::add-page, ::sub-page"],
         ["QProgressBar", "::chunk"],
         ["QTabWidget / QTabBar", "::pane, ::tab-bar / ::tab, ::close-button"],
         ["QHeaderView", "::section"],
         ["Views (QListView, QTreeView…)", "::item, ::branch (QTreeView)"],
         ["QPushButton / QToolButton", "::menu-indicator, ::menu-button"],
         ["QMenu", "::item, ::separator, ::indicator"]],
        [3200, 5871]),
    tab("Properties verified on Qt 6.12", ["Group", "Properties"],
        [["Colors", "color, background, background-color, selection-color, selection-background-color, "
                    "alternate-background-color, gridline-color, placeholder-text-color"],
         ["Border and box", "border, border-width, border-style, border-color, border-radius, border-image, margin, "
                            "padding, outline"],
         ["Dimensions", "width, height, min-width, min-height, max-width, max-height, icon-size, spacing"],
         ["Text and font", "font, font-family, font-size, font-weight, font-style, text-align, text-decoration, "
                           "lineedit-password-character"],
         ["Images", "image, background-image, background-position, background-repeat"],
         ["Subcontrols", "subcontrol-origin, subcontrol-position, position, left, top, right, bottom"],
         ["Others", "opacity (tooltips), qproperty-<name> (sets a Qt property)"]],
        [1900, 7171]),
    p("The `qproperty-` prefix sets Qt properties of the widget from the style sheet, for example "
      "`QLabel { qproperty-alignment: AlignCenter; }`. The rule is applied only once, when the style is polished."),
    snip('''/* Minimal consistent theme (excerpt) */
QWidget              { font-size: 10pt; }
QLineEdit, QComboBox { border: 1px solid #BFC5CF; border-radius: 4px; padding: 3px 6px; }
QLineEdit:focus      { border: 2px solid #2E75B6; }
QPushButton          { padding: 5px 16px; border-radius: 4px; }
QPushButton:hover    { border: 1px solid #2E75B6; }
QPushButton#primary  { background: #2E75B6; color: white; border: none; }
QProgressBar::chunk  { background-color: #2E75B6; }
QTableView           { gridline-color: #D9D9D9; alternate-background-color: #F2F6FB; }''', lang="text"),
    note("TIP", "To debug a style sheet, apply it to a single widget (`w.setStyleSheet`) before applying it to the "
                "whole application, and watch the console: invalid properties produce *Unknown property* and syntax "
                "errors produce *Could not parse stylesheet*."),
)

ANEXO_D_TAB = tab("Command-line tools for PyQt6 projects",
                  ["Command", "Purpose", "Origin", "Ch."],
                  [["pyuic6", "Converts Qt Designer .ui files into Python code", "PyQt6 (installed with the package)", "11"],
                   ["pylupdate6", "Extracts translatable texts from .py and .ui into .ts files", "PyQt6 (installed with the package)", "13"],
                   ["designer", "Visual form editor (Qt Designer)", "Qt tools or pyside6-designer", "11"],
                   ["linguist", "Translation (.ts) editor for translators", "Qt tools or pyside6-linguist", "13"],
                   ["lrelease", "Compiles .ts into .qm", "Qt tools or pyside6-lrelease", "13"]],
                  [1600, 3671, 2900, 900])

ANEXO_D = flat(
    p("PyQt6 installs only `pyuic6` and `pylupdate6` (registered as *entry points* of the package, verified on "
      "version 6.12.0). The other tools belong to Qt and can be obtained from the official installer, from the "
      "Linux distribution packages or from the PySide6-Essentials 6.12.0 package, which includes "
      "`pyside6-designer`, `pyside6-linguist` and `pyside6-lrelease` (the latter used in Chapter 13). Qt tools work "
      "on files (`.ui`, `.ts`, `.qm`) that are independent of the binding, so they can be used in PyQt6 projects."),
    ANEXO_D_TAB,
    out("tool_pyuic6", "Output of pyuic6 --help (PyQt6 6.12.0)"),
    out("tool_pylupdate6", "Output of pylupdate6 --help (PyQt6 6.12.0)"),
    p("Typical workflows:"),
    snip('''# Interface: generate the module from the .ui (repeat at every change in Designer)
pyuic6 ui/well_data.ui -o src/eng_calc/ui/ui_well_data.py

# Translation: extract -> translate in Linguist -> compile
pylupdate6 src/ --ts resources/translations/engcalc_pt_BR.ts
linguist resources/translations/engcalc_pt_BR.ts
lrelease resources/translations/engcalc_pt_BR.ts \\
    -qm resources/translations/engcalc_pt_BR.qm''', lang="text"),
)
