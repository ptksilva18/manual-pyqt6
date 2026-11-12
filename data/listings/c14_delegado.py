"""Delegado personalizado: editor numérico com limites e texto formatado."""

import sys

from PyQt6.QtCore import QLocale, QModelIndex, Qt
from PyQt6.QtWidgets import (
    QApplication,
    QDoubleSpinBox,
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QTableView,
)

from c14_modelo_tabela import Ensaio, ModeloEnsaios


class DelegadoPressao(QStyledItemDelegate):
    """Edita pressões com QDoubleSpinBox e exibe com unidade e separador do idioma."""

    def __init__(self, maximo: float, parent=None) -> None:
        super().__init__(parent)
        self.maximo = maximo

    def createEditor(self, parent, opcao: QStyleOptionViewItem, index: QModelIndex):
        ed = QDoubleSpinBox(parent)
        ed.setRange(0.1, self.maximo)
        ed.setDecimals(1)
        ed.setSuffix(" bar")
        ed.setFrame(False)
        return ed

    def setEditorData(self, editor: QDoubleSpinBox, index: QModelIndex) -> None:
        # valor numérico do modelo
        editor.setValue(index.data(Qt.ItemDataRole.EditRole))

    def setModelData(self, editor: QDoubleSpinBox, modelo, index: QModelIndex) -> None:
        # confirma o texto digitado
        editor.interpretText()
        modelo.setData(index, editor.value(), Qt.ItemDataRole.EditRole)

    def updateEditorGeometry(self, editor, opcao: QStyleOptionViewItem, index) -> None:
        editor.setGeometry(opcao.rect)

    def displayText(self, valor, locale: QLocale) -> str:
        try:
            return f"{locale.toString(float(valor), 'f', 1)} bar"
        except (TypeError, ValueError):
            return str(valor)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    modelo = ModeloEnsaios(
        [Ensaio("BOP-01", 345.0, True), Ensaio("BOP-02", 310.5, False)]
    )
    vista = QTableView()
    vista.setModel(modelo)
    delegado = DelegadoPressao(maximo=1035.0, parent=vista)
    # só na coluna de pressão
    vista.setItemDelegateForColumn(1, delegado)
    vista.show()

    idx = modelo.index(0, 1)
    br = QLocale(QLocale.Language.Portuguese, QLocale.Country.Brazil)
    print(
        "texto exibido (pt_BR):",
        delegado.displayText(idx.data(Qt.ItemDataRole.EditRole), br),
    )
    opcao = QStyleOptionViewItem()
    editor = delegado.createEditor(vista.viewport(), opcao, idx)  # o que a view faria
    delegado.setEditorData(editor, idx)
    print(
        "editor iniciado com:",
        editor.value(),
        "| faixa:",
        editor.minimum(),
        "-",
        editor.maximum(),
    )
    # acima do máximo: limitado
    editor.setValue(2000.0)
    delegado.setModelData(editor, modelo, idx)
    print("valor gravado no modelo:", modelo.index(0, 1).data(Qt.ItemDataRole.EditRole))
    sys.exit(app.exec())
