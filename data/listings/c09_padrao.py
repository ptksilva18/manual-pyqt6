"""Diálogos padrão: QInputDialog, QProgressDialog e QFileDialog (não nativo)."""
import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QFileDialog, QInputDialog, QProgressDialog

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # QInputDialog estático: retorna (valor, ok).
    # O timer simula o usuário clicando em "Cancelar".
    QTimer.singleShot(0, lambda: QApplication.activeModalWidget().reject())
    valor, ok = QInputDialog.getDouble(None, "Fator de segurança", "Fator:",
                                       1.5, 1.0, 5.0, 2)
    print("getDouble ->", (valor, ok))

    # QProgressDialog para uma tarefa em etapas, com cancelamento
    prog = QProgressDialog("Processando arquivos…", "Cancelar", 0, 5)
    prog.setMinimumDuration(0)                 # aparece imediatamente
    for i in range(5):
        prog.setValue(i)
        app.processEvents()
        if prog.wasCanceled():
            break
    prog.setValue(5)
    print("valor após concluir:", prog.value(), "(autoReset reinicia para -1)",
          "| cancelado?", prog.wasCanceled())

    # QFileDialog configurado como objeto (opção: diálogo do Qt em vez do nativo)
    dlg = QFileDialog(None, "Abrir ensaio", "", "Ensaios (*.json *.csv);;Todos (*)")
    dlg.setFileMode(QFileDialog.FileMode.ExistingFile)
    dlg.setOption(QFileDialog.Option.DontUseNativeDialog, True)
    print("filtros:", dlg.nameFilters())
    QTimer.singleShot(0, dlg.reject)
    print("arquivo escolhido?", bool(dlg.exec()))
