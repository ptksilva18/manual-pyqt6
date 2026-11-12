"""Widget personalizado usado por promoção no Qt Designer."""

from PyQt6.QtWidgets import QDoubleSpinBox


class CampoPressao(QDoubleSpinBox):
    """QDoubleSpinBox pré-configurado para pressões em bar."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setRange(0.0, 1035.0)
        self.setDecimals(1)
        self.setSuffix(" bar")
