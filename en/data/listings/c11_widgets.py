"""Custom widget used through promotion in Qt Designer."""

from PyQt6.QtWidgets import QDoubleSpinBox


class PressureField(QDoubleSpinBox):
    """QDoubleSpinBox preconfigured for pressures in bar."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setRange(0.0, 1035.0)
        self.setDecimals(1)
        self.setSuffix(" bar")
