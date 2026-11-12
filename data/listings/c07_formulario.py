"""QFormLayout: rótulos e campos alinhados, com políticas de quebra e crescimento."""
import sys

from PyQt6.QtWidgets import (
    QApplication, QComboBox, QDoubleSpinBox, QFormLayout, QLineEdit, QSpinBox, QWidget,
)


class DadosPoco(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("QFormLayout")
        f = QFormLayout(self)
        f.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapLongRows)
        f.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        self.nome = QLineEdit()
        f.addRow("&Nome do poço:", self.nome)            # & cria atalho Alt+N (buddy)
        f.addRow("Lâmina d'água:", QDoubleSpinBox(maximum=3500.0, suffix=" m"))
        f.addRow("Nº de colunas:", QSpinBox(minimum=1, maximum=8))
        tipo = QComboBox()
        tipo.addItems(["Produtor", "Injetor", "Exploratório"])
        f.addRow("Tipo:", tipo)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    d = DadosPoco()
    d.show()
    f = d.layout()
    print("linhas:", f.rowCount())
    rotulo = f.labelForField(d.nome)
    print("rótulo do campo nome:", rotulo.text())
    print("buddy é o campo?", rotulo.buddy() is d.nome)
    sys.exit(app.exec())
