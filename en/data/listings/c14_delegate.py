"""Custom delegate: numeric editor with limits and formatted text."""

import sys

from PyQt6.QtCore import QLocale, QModelIndex, Qt
from PyQt6.QtWidgets import (
    QApplication,
    QDoubleSpinBox,
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QTableView,
)

from c14_table_model import PressureTest, TestModel


class PressureDelegate(QStyledItemDelegate):
    """Edits pressures with a QDoubleSpinBox; shows unit and locale separator."""

    def __init__(self, maximum: float, parent=None) -> None:
        super().__init__(parent)
        self.maximum = maximum

    def createEditor(self, parent, option: QStyleOptionViewItem, index: QModelIndex):
        ed = QDoubleSpinBox(parent)
        ed.setRange(0.1, self.maximum)
        ed.setDecimals(1)
        ed.setSuffix(" bar")
        ed.setFrame(False)
        return ed

    def setEditorData(self, editor: QDoubleSpinBox, index: QModelIndex) -> None:
        # numeric value from the model
        editor.setValue(index.data(Qt.ItemDataRole.EditRole))

    def setModelData(self, editor: QDoubleSpinBox, model, index: QModelIndex) -> None:
        # confirms the typed text
        editor.interpretText()
        model.setData(index, editor.value(), Qt.ItemDataRole.EditRole)

    def updateEditorGeometry(self, editor, option: QStyleOptionViewItem, index) -> None:
        editor.setGeometry(option.rect)

    def displayText(self, value, locale: QLocale) -> str:
        try:
            return f"{locale.toString(float(value), 'f', 1)} bar"
        except (TypeError, ValueError):
            return str(value)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    model = TestModel(
        [PressureTest("BOP-01", 345.0, True), PressureTest("BOP-02", 310.5, False)]
    )
    view = QTableView()
    view.setModel(model)
    delegate = PressureDelegate(maximum=1035.0, parent=view)
    # only in the pressure column
    view.setItemDelegateForColumn(1, delegate)
    view.show()

    idx = model.index(0, 1)
    br = QLocale(QLocale.Language.Portuguese, QLocale.Country.Brazil)
    print(
        "displayed text (pt_BR):",
        delegate.displayText(idx.data(Qt.ItemDataRole.EditRole), br),
    )
    option = QStyleOptionViewItem()
    editor = delegate.createEditor(view.viewport(), option, idx)  # what the view would do
    delegate.setEditorData(editor, idx)
    print(
        "editor started with:",
        editor.value(),
        "| range:",
        editor.minimum(),
        "-",
        editor.maximum(),
    )
    # above the maximum: clamped
    editor.setValue(2000.0)
    delegate.setModelData(editor, model, idx)
    print("value stored in the model:", model.index(0, 1).data(Qt.ItemDataRole.EditRole))
    sys.exit(app.exec())
