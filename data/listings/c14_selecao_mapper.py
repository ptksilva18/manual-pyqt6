"""QItemSelectionModel e QDataWidgetMapper: formulário ligado à linha selecionada."""

import sys

from PyQt6.QtCore import QItemSelectionModel
from PyQt6.QtWidgets import (
    QApplication,
    QDataWidgetMapper,
    QDoubleSpinBox,
    QFormLayout,
    QLineEdit,
    QTableView,
    QWidget,
)

from c14_modelo_tabela import Ensaio, ModeloEnsaios

if __name__ == "__main__":
    app = QApplication(sys.argv)
    modelo = ModeloEnsaios(
        [Ensaio("BOP-01", 345.0, True), Ensaio("BOP-02", 310.5, False)]
    )
    vista = QTableView()
    vista.setModel(modelo)
    vista.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)

    form = QWidget()
    tag, pressao = QLineEdit(), QDoubleSpinBox(maximum=1035.0, decimals=1)
    lay = QFormLayout(form)
    lay.addRow("Tag:", tag)
    lay.addRow("Pressão:", pressao)

    mapper = QDataWidgetMapper()
    mapper.setModel(modelo)
    mapper.addMapping(tag, 0)  # coluna 0 -> QLineEdit
    mapper.addMapping(pressao, 1)  # coluna 1 -> QDoubleSpinBox
    mapper.setSubmitPolicy(QDataWidgetMapper.SubmitPolicy.ManualSubmit)

    selecao = vista.selectionModel()
    selecao.currentRowChanged.connect(
        lambda atual, _: mapper.setCurrentIndex(atual.row())
    )
    selecao.selectionChanged.connect(
        lambda sel, _: print(
            "linhas selecionadas:", sorted({i.row() for i in sel.indexes()})
        )
    )

    flags = QItemSelectionModel.SelectionFlag
    selecao.setCurrentIndex(modelo.index(1, 0), flags.ClearAndSelect | flags.Rows)
    print("formulário mostra:", tag.text(), pressao.value())
    pressao.setValue(315.0)
    # grava o formulário no modelo
    mapper.submit()
    print("modelo após submit:", modelo.index(1, 1).data())
