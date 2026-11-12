"""QStyleFactory, switching styles and QProxyStyle for a targeted adjustment."""

import sys

from PyQt6.QtWidgets import QApplication, QProxyStyle, QStyle, QStyleFactory


class EngineeringStyle(QProxyStyle):
    """Inherits everything from the base style and changes only what it needs."""

    def pixelMetric(self, metric, option=None, widget=None) -> int:
        if metric == QStyle.PixelMetric.PM_ScrollBarExtent:
            return 20  # wider scroll bars
        if metric == QStyle.PixelMetric.PM_ToolBarIconSize:
            return 32  # large toolbar icons
        return super().pixelMetric(metric, option, widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    print("available styles:", QStyleFactory.keys())
    print("default style:", app.style().name())
    base = QStyleFactory.create("Fusion")
    print(
        "scroll bar (Fusion):",
        base.pixelMetric(QStyle.PixelMetric.PM_ScrollBarExtent),
    )
    # the proxy becomes the global style
    app.setStyle(EngineeringStyle(base))
    st = app.style()
    print(
        "scroll bar (proxy): ",
        st.pixelMetric(QStyle.PixelMetric.PM_ScrollBarExtent),
    )
    print(
        "toolbar icons (proxy):",
        st.pixelMetric(QStyle.PixelMetric.PM_ToolBarIconSize),
    )
