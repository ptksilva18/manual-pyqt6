"""QStyleFactory, troca de estilo e QProxyStyle para um ajuste pontual."""

import sys

from PyQt6.QtWidgets import QApplication, QProxyStyle, QStyle, QStyleFactory


class EstiloEngenharia(QProxyStyle):
    """Herda tudo do estilo base e altera apenas o que precisar."""

    def pixelMetric(self, metrica, opcao=None, widget=None) -> int:
        if metrica == QStyle.PixelMetric.PM_ScrollBarExtent:
            return 20  # barras de rolagem mais largas
        if metrica == QStyle.PixelMetric.PM_ToolBarIconSize:
            return 32  # ícones grandes nas barras
        return super().pixelMetric(metrica, opcao, widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    print("estilos disponíveis:", QStyleFactory.keys())
    print("estilo padrão:", app.style().name())
    base = QStyleFactory.create("Fusion")
    print(
        "barra de rolagem (Fusion):",
        base.pixelMetric(QStyle.PixelMetric.PM_ScrollBarExtent),
    )
    # o proxy passa a ser o estilo global
    app.setStyle(EstiloEngenharia(base))
    st = app.style()
    print(
        "barra de rolagem (proxy): ",
        st.pixelMetric(QStyle.PixelMetric.PM_ScrollBarExtent),
    )
    print(
        "ícones de barra (proxy):  ",
        st.pixelMetric(QStyle.PixelMetric.PM_ToolBarIconSize),
    )
