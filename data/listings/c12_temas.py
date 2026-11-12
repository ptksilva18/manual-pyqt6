"""Qt Style Sheets: temas claro e escuro, seletores, subcontroles e pseudo-estados."""

import sys

from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

BASE = """
QWidget            { font-size: 10pt; }
QGroupBox          { border: 1px solid %(borda)s; border-radius: 6px;
                     margin-top: 14px; padding: 10px 8px 8px 8px; }
QGroupBox::title   { subcontrol-origin: margin; left: 10px; padding: 0 4px;
                     color: %(destaque)s; font-weight: bold; }
QLineEdit, QDoubleSpinBox, QComboBox {
                     background: %(campo)s; color: %(texto)s;
                     border: 1px solid %(borda)s; border-radius: 4px; padding: 3px 6px; }
QLineEdit:focus, QDoubleSpinBox:focus, QComboBox:focus { border: 2px solid %(destaque)s; }
QPushButton        { background: %(botao)s; color: %(texto)s; border: 1px solid %(borda)s;
                     border-radius: 4px; padding: 5px 16px; }
QPushButton:hover  { border-color: %(destaque)s; }
QPushButton:pressed { background: %(destaque)s; color: white; }
QPushButton#primario { background: %(destaque)s; color: white; border: none; }
QPushButton[perigoso="true"] { background: #C00000; color: white; border: none; }
QWidget#raiz       { background: %(fundo)s; color: %(texto)s; }
QCheckBox          { color: %(texto)s; }
QGroupBox QLabel   { color: %(texto)s; }
"""
CLARO = dict(
    fundo="#F7F8FA",
    campo="#FFFFFF",
    texto="#1E1E1E",
    borda="#BFC5CF",
    botao="#FFFFFF",
    destaque="#2E75B6",
)
ESCURO = dict(
    fundo="#1E1F22",
    campo="#2B2D31",
    texto="#E6E6E6",
    borda="#4A4D55",
    botao="#2B2D31",
    destaque="#4E9BE0",
)


class Formulario(QWidget):
    def __init__(self) -> None:
        super().__init__(objectName="raiz")
        grupo = QGroupBox("Dados do ensaio")
        f = QFormLayout(grupo)
        f.addRow("Tag:", QLineEdit("BOP-01"))
        f.addRow("Pressão:", QDoubleSpinBox(maximum=1035.0, value=345.0, suffix=" bar"))
        combo = QComboBox()
        combo.addItems(["Hidrostático", "Funcional", "Estanqueidade"])
        f.addRow("Tipo:", combo)
        f.addRow("", QCheckBox("Registrar no diário", checked=True))
        botoes = QHBoxLayout()
        botoes.addStretch()
        excluir = QPushButton("Excluir")
        excluir.setProperty("perigoso", True)  # seletor [perigoso="true"]
        botoes.addWidget(excluir)
        botoes.addWidget(QPushButton("Cancelar"))
        # seletor #primario
        botoes.addWidget(QPushButton("Salvar", objectName="primario"))
        lay = QVBoxLayout(self)
        lay.addWidget(grupo)
        lay.addLayout(botoes)

    def aplicar_tema(self, cores: dict) -> None:
        self.setStyleSheet(BASE % cores)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    w = Formulario()
    w.aplicar_tema(ESCURO)
    w.show()
    excluir = next(b for b in w.findChildren(QPushButton) if b.text() == "Excluir")
    print("QSS aplicado (caracteres):", len(w.styleSheet()))
    print("propriedade dinâmica perigoso =", excluir.property("perigoso"))
    excluir.setProperty("perigoso", False)  # mudou: re-polir o widget
    excluir.style().unpolish(excluir)
    excluir.style().polish(excluir)
    print("re-polido após mudar a propriedade")
    sys.exit(app.exec())
