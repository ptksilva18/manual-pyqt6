"""QMessageBox: métodos estáticos e caixa personalizada."""
import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QMessageBox

SB = QMessageBox.StandardButton


def confirmar_exclusao(parent=None) -> bool:
    resposta = QMessageBox.question(
        parent, "Excluir registro",
        "Excluir o ensaio selecionado?\nEsta operação não pode ser desfeita.",
        SB.Yes | SB.No, defaultButton=SB.No)          # 'Não' como padrão: mais seguro
    return resposta == SB.Yes


def perguntar_salvar(parent=None) -> str:
    caixa = QMessageBox(parent)
    caixa.setIcon(QMessageBox.Icon.Warning)
    caixa.setWindowTitle("Alterações não salvas")
    caixa.setText("O documento foi modificado.")
    caixa.setInformativeText("Deseja salvar as alterações?")
    caixa.setStandardButtons(SB.Save | SB.Discard | SB.Cancel)
    caixa.setDefaultButton(SB.Save)
    caixa.setDetailedText("Arquivo: ensaio_345bar.json\nÚltima gravação: 10:42")
    QTimer.singleShot(0, caixa.button(SB.Discard).click)   # simula o usuário
    resultado = SB(caixa.exec())
    return resultado.name


if __name__ == "__main__":
    app = QApplication(sys.argv)
    QTimer.singleShot(0, lambda: QApplication.activeModalWidget().close())  # simula Esc
    print("confirmou exclusão?", confirmar_exclusao())
    print("escolha ao salvar:", perguntar_salvar())
