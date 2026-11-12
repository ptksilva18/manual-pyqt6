# runner: ticks=40
"""Acessibilidade: nomes e descrições, buddies, ordem de tabulação, contraste e
preferências."""

import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import (
    QApplication,
    QDoubleSpinBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QWidget,
)


def luminancia(cor: QColor) -> float:
    """Luminância relativa (WCAG 2.x) a partir de sRGB."""

    def canal(c: float) -> float:
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    return (
        0.2126 * canal(cor.redF())
        + 0.7152 * canal(cor.greenF())
        + 0.0722 * canal(cor.blueF())
    )


def contraste(a: QColor, b: QColor) -> float:
    l1, l2 = sorted((luminancia(a), luminancia(b)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def main() -> int:
    app = QApplication(sys.argv)
    form = QWidget()
    tag, pressao, salvar = QLineEdit(), QDoubleSpinBox(), QPushButton("&Salvar")
    rot_tag, rot_p = QLabel("&Tag do sensor:"), QLabel("&Pressão (bar):")
    rot_tag.setBuddy(
        tag
    )  # Alt+T leva o foco ao campo; leitores de tela associam o rótulo
    rot_p.setBuddy(pressao)
    pressao.setAccessibleName("Pressão do ensaio")
    pressao.setAccessibleDescription("Pressão de teste em bar, entre 0 e 1000")
    salvar.setAccessibleDescription("Grava o ensaio no banco de dados")
    lay = QFormLayout(form)
    lay.addRow(rot_tag, tag)
    lay.addRow(rot_p, pressao)
    lay.addRow(salvar)
    QWidget.setTabOrder(tag, pressao)
    QWidget.setTabOrder(pressao, salvar)
    form.show()

    def proximo(w: QWidget) -> QWidget:
        """Mesma regra do Tab: aceita TabFocus, visível, sem focusProxy."""
        w = w.nextInFocusChain()
        while (
            not w.focusPolicy().value & Qt.FocusPolicy.TabFocus.value
            or w.focusProxy() is not None
            or not w.isVisible()
        ):
            w = w.nextInFocusChain()
        return w

    def nome(
        w: QWidget,
    ) -> str:  # o QLineEdit interno representa o spin box que o contém
        dono = w.parentWidget()
        return type(dono if dono is not None and dono.focusProxy() is w else w).__name__

    cadeia, w = [], tag
    for _ in range(4):
        cadeia.append(nome(w))
        w = proximo(w)
    print("Ordem de tabulação:", " -> ".join(cadeia))
    print("Nome acessível do campo de pressão:", repr(pressao.accessibleName()))

    pal = app.palette()
    texto, fundo = pal.color(QPalette.ColorRole.WindowText), pal.color(
        QPalette.ColorRole.Window
    )
    print(
        f"Contraste texto/fundo da paleta: {contraste(texto, fundo):.1f}:1 (AA exige "
        ">= 4.5:1)"
    )
    for nome, cor in (
        ("cinza #999999", QColor("#999999")),
        ("cinza #595959", QColor("#595959")),
    ):
        print(f"Texto {nome} sobre branco: {contraste(cor, QColor('white')):.2f}:1")
    dicas = app.styleHints().accessibility()
    print(
        "Preferência de contraste do sistema:",
        dicas.contrastPreference().name,
        "| movimento:",
        dicas.motionPreference().name,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
