# runner: ticks=40
"""Accessibility: names and descriptions, buddies, tab order, contrast and
preferences."""

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


def luminance(color: QColor) -> float:
    """Relative luminance (WCAG 2.x) from sRGB."""

    def channel(c: float) -> float:
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    return (
        0.2126 * channel(color.redF())
        + 0.7152 * channel(color.greenF())
        + 0.0722 * channel(color.blueF())
    )


def contrast(a: QColor, b: QColor) -> float:
    l1, l2 = sorted((luminance(a), luminance(b)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def main() -> int:
    app = QApplication(sys.argv)
    form = QWidget()
    tag, pressure, save = QLineEdit(), QDoubleSpinBox(), QPushButton("&Save")
    lbl_tag, lbl_p = QLabel("&Tag of the sensor:"), QLabel("&Pressure (bar):")
    lbl_tag.setBuddy(
        tag
    )  # Alt+T moves the focus to the field; screen readers associate the label
    lbl_p.setBuddy(pressure)
    pressure.setAccessibleName("Test pressure")
    pressure.setAccessibleDescription("Test pressure in bar, between 0 and 1000")
    save.setAccessibleDescription("Saves the test to the database")
    lay = QFormLayout(form)
    lay.addRow(lbl_tag, tag)
    lay.addRow(lbl_p, pressure)
    lay.addRow(save)
    QWidget.setTabOrder(tag, pressure)
    QWidget.setTabOrder(pressure, save)
    form.show()

    def next_widget(w: QWidget) -> QWidget:
        """Same rule as Tab: accepts TabFocus, visible, no focusProxy."""
        w = w.nextInFocusChain()
        while (
            not w.focusPolicy().value & Qt.FocusPolicy.TabFocus.value
            or w.focusProxy() is not None
            or not w.isVisible()
        ):
            w = w.nextInFocusChain()
        return w

    def widget_name(
        w: QWidget,
    ) -> str:  # the inner QLineEdit stands for the spin box that contains it
        owner = w.parentWidget()
        proxied = owner is not None and owner.focusProxy() is w
        return type(owner if proxied else w).__name__

    chain, w = [], tag
    for _ in range(4):
        chain.append(widget_name(w))
        w = next_widget(w)
    print("Tab order:", " -> ".join(chain))
    print("Accessible name of the pressure field:", repr(pressure.accessibleName()))

    pal = app.palette()
    text, background = pal.color(QPalette.ColorRole.WindowText), pal.color(
        QPalette.ColorRole.Window
    )
    print(
        f"Palette text/background contrast: {contrast(text, background):.1f}:1 "
        "(AA requires >= 4.5:1)"
    )
    for label, color in (
        ("gray #999999", QColor("#999999")),
        ("gray #595959", QColor("#595959")),
    ):
        print(f"Text {label} on white: {contrast(color, QColor('white')):.2f}:1")
    hints = app.styleHints().accessibility()
    print(
        "System contrast preference:",
        hints.contrastPreference().name,
        "| motion:",
        hints.motionPreference().name,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
