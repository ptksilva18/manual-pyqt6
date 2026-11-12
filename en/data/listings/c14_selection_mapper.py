"""QItemSelectionModel and QDataWidgetMapper: a form bound to the selected row."""

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

from c14_table_model import PressureTest, TestModel

if __name__ == "__main__":
    app = QApplication(sys.argv)
    model = TestModel(
        [PressureTest("BOP-01", 345.0, True), PressureTest("BOP-02", 310.5, False)]
    )
    view = QTableView()
    view.setModel(model)
    view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)

    form = QWidget()
    tag, pressure = QLineEdit(), QDoubleSpinBox(maximum=1035.0, decimals=1)
    lay = QFormLayout(form)
    lay.addRow("Tag:", tag)
    lay.addRow("Pressure:", pressure)

    mapper = QDataWidgetMapper()
    mapper.setModel(model)
    mapper.addMapping(tag, 0)  # column 0 -> QLineEdit
    mapper.addMapping(pressure, 1)  # column 1 -> QDoubleSpinBox
    mapper.setSubmitPolicy(QDataWidgetMapper.SubmitPolicy.ManualSubmit)

    selection = view.selectionModel()
    selection.currentRowChanged.connect(
        lambda current, _: mapper.setCurrentIndex(current.row())
    )
    selection.selectionChanged.connect(
        lambda sel, _: print("selected rows:", sorted({i.row() for i in sel.indexes()}))
    )

    flags = QItemSelectionModel.SelectionFlag
    selection.setCurrentIndex(model.index(1, 0), flags.ClearAndSelect | flags.Rows)
    print("the form shows:", tag.text(), pressure.value())
    pressure.setValue(315.0)
    # writes the form into the model
    mapper.submit()
    print("model after submit:", model.index(1, 1).data())
