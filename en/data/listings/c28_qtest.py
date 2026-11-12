# runner: ticks=300 timeout=120
"""QtTest with unittest: QTest (keyboard/mouse), QSignalSpy, QAbstractItemModelTester."""

import sys
import unittest

from PyQt6.QtCore import QAbstractTableModel, QModelIndex, QPoint, Qt
from PyQt6.QtTest import QAbstractItemModelTester, QSignalSpy, QTest
from PyQt6.QtWidgets import QApplication

from c28_calculator import Calculator

app = QApplication.instance() or QApplication(sys.argv)


class ReadingsModel(QAbstractTableModel):
    def __init__(self) -> None:
        super().__init__()
        self.rows = [["PT-101", 345.0], ["PT-102", 98.7]]

    def rowCount(self, parent=QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self.rows)

    def columnCount(self, parent=QModelIndex()) -> int:
        return 0 if parent.isValid() else 2

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid() and role in (
            Qt.ItemDataRole.DisplayRole,
            Qt.ItemDataRole.EditRole,
        ):
            return self.rows[index.row()][index.column()]
        return None

    def add(self, tag: str, value: float) -> None:
        n = len(self.rows)
        self.beginInsertRows(QModelIndex(), n, n)
        self.rows.append([tag, value])
        self.endInsertRows()


class CalculatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.calc = Calculator()
        self.calc.show()
        QTest.qWaitForWindowExposed(self.calc)

    def tearDown(self) -> None:
        self.calc.close()
        self.calc.deleteLater()

    def test_keyboard_and_mouse(self) -> None:
        spy = QSignalSpy(
            self.calc.computed
        )  # records each emission and its arguments
        QTest.keyClicks(self.calc.entry, "2000")
        QTest.mouseClick(
            self.calc.button,
            Qt.MouseButton.LeftButton,
            Qt.KeyboardModifier.NoModifier,
            QPoint(5, 5),
        )
        self.assertEqual(len(spy), 1)
        self.assertAlmostEqual(spy[0][0], 203.03, places=2)
        self.assertEqual(self.calc.result.text(), "203.03")

    def test_enter_key(self) -> None:
        spy = QSignalSpy(self.calc.computed)
        QTest.keyClicks(self.calc.entry, "100")
        QTest.keyClick(self.calc.entry, Qt.Key.Key_Return)
        self.assertEqual(len(spy), 1)  # returnPressed is emitted synchronously

    def test_backspace_fixes_typing(self) -> None:
        QTest.keyClicks(self.calc.entry, "13500")
        QTest.keyClick(self.calc.entry, Qt.Key.Key_Backspace)
        self.assertEqual(self.calc.entry.text(), "1350")


class ModelTests(unittest.TestCase):
    def test_model_honors_contract(self) -> None:
        model = ReadingsModel()
        # Fatal: any violation of the QAbstractItemModel contract aborts the test.
        tester = QAbstractItemModelTester(
            model, QAbstractItemModelTester.FailureReportingMode.Fatal
        )
        model.add("TT-201", 61.2)
        self.assertEqual(model.rowCount(), 3)
        del tester


if __name__ == "__main__":
    unittest.main(
        argv=[sys.argv[0], "-v"],
        testRunner=unittest.TextTestRunner(stream=sys.stdout, verbosity=2),
        exit=False,
    )
