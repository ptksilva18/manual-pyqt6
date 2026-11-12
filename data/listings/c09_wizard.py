"""QWizard com campos registrados (registerField) e páginas encadeadas."""
import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QApplication, QComboBox, QFormLayout, QLabel, QLineEdit, QVBoxLayout, QWizard,
    QWizardPage,
)


class PaginaProjeto(QWizardPage):
    def __init__(self) -> None:
        super().__init__()
        self.setTitle("Projeto")
        self.setSubTitle("Identifique o projeto.")
        nome = QLineEdit()
        form = QFormLayout(self)
        form.addRow("Nome*:", nome)
        self.registerField("nome*", nome)          # '*' = obrigatório: habilita "Avançar"


class PaginaUnidades(QWizardPage):
    def __init__(self) -> None:
        super().__init__()
        self.setTitle("Unidades")
        combo = QComboBox()
        combo.addItems(["SI", "Imperial"])
        form = QFormLayout(self)
        form.addRow("Sistema:", combo)
        self.registerField("unidades", combo, "currentText")


class PaginaResumo(QWizardPage):
    def __init__(self) -> None:
        super().__init__()
        self.setTitle("Resumo")
        self.texto = QLabel()
        QVBoxLayout(self).addWidget(self.texto)

    def initializePage(self) -> None:              # chamado ao entrar na página
        self.texto.setText(f"Projeto: {self.field('nome')}\n"
                           f"Unidades: {self.field('unidades')}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    wiz = QWizard()
    wiz.setWindowTitle("Novo projeto")
    for pagina in (PaginaProjeto(), PaginaUnidades(), PaginaResumo()):
        wiz.addPage(pagina)

    def roteiro() -> None:
        avancar = wiz.button(QWizard.WizardButton.NextButton)
        print("Avançar habilitado sem nome?", avancar.isEnabled())
        wiz.page(0).findChild(QLineEdit).setText("Verificação de riser")
        print("Avançar habilitado com nome?", avancar.isEnabled())
        wiz.next()
        wiz.page(1).findChild(QComboBox).setCurrentText("Imperial")
        wiz.next()
        print(wiz.currentPage().texto.text())
        wiz.accept()

    QTimer.singleShot(0, roteiro)
    print("concluído?", wiz.exec() == 1)
