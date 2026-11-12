"""Diálogo personalizado com QDialogButtonBox e validação antes de accept()."""
import sys
from dataclasses import dataclass

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QApplication, QDialog, QDialogButtonBox, QDoubleSpinBox, QFormLayout, QLabel,
    QLineEdit, QVBoxLayout,
)


@dataclass
class Ensaio:
    tag: str
    pressao_bar: float
    duracao_min: float


class DialogoEnsaio(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Novo ensaio hidrostático")
        self.tag = QLineEdit(placeholderText="ex.: BOP-01")
        self.pressao = QDoubleSpinBox(maximum=1035.0, decimals=1, suffix=" bar")
        self.duracao = QDoubleSpinBox(maximum=240.0, decimals=0, suffix=" min", value=15)
        self.erro = QLabel(styleSheet="color: #C00000")
        form = QFormLayout()
        form.addRow("Tag:", self.tag)
        form.addRow("Pressão de teste:", self.pressao)
        form.addRow("Duração:", self.duracao)
        botoes = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok
                                  | QDialogButtonBox.StandardButton.Cancel)
        botoes.accepted.connect(self.accept)           # accept() validará os dados
        botoes.rejected.connect(self.reject)
        lay = QVBoxLayout(self)
        lay.addLayout(form)
        lay.addWidget(self.erro)
        lay.addWidget(botoes)

    def accept(self) -> None:                           # reimplementação: valida antes
        if not self.tag.text().strip():
            self.erro.setText("Informe a tag do equipamento.")
            self.tag.setFocus()
            return                                      # mantém o diálogo aberto
        if self.pressao.value() <= 0:
            self.erro.setText("A pressão de teste deve ser positiva.")
            return
        super().accept()

    def resultado(self) -> Ensaio:
        return Ensaio(self.tag.text().strip(), self.pressao.value(), self.duracao.value())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = DialogoEnsaio()

    def simular_usuario() -> None:                      # roteiro de demonstração
        dlg.accept()                                     # 1ª tentativa: sem tag
        print("mensagem:", dlg.erro.text())
        dlg.tag.setText("BOP-01")
        dlg.pressao.setValue(1034.2)
        dlg.accept()                                     # 2ª tentativa: válida

    QTimer.singleShot(0, simular_usuario)
    if dlg.exec() == QDialog.DialogCode.Accepted:
        print("aceito:", dlg.resultado())
