# runner: ticks=300 timeout=120
"""QtTest com unittest: QTest (teclado/mouse), QSignalSpy e QAbstractItemModelTester."""

import sys
import unittest

from PyQt6.QtCore import QAbstractTableModel, QModelIndex, QPoint, Qt
from PyQt6.QtTest import QAbstractItemModelTester, QSignalSpy, QTest
from PyQt6.QtWidgets import QApplication

from c28_calculadora import Calculadora

app = QApplication.instance() or QApplication(sys.argv)


class ModeloLeituras(QAbstractTableModel):
    def __init__(self) -> None:
        super().__init__()
        self.linhas = [["PT-101", 345.0], ["PT-102", 98.7]]

    def rowCount(self, parent=QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self.linhas)

    def columnCount(self, parent=QModelIndex()) -> int:
        return 0 if parent.isValid() else 2

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid() and role in (
            Qt.ItemDataRole.DisplayRole,
            Qt.ItemDataRole.EditRole,
        ):
            return self.linhas[index.row()][index.column()]
        return None

    def adicionar(self, tag: str, valor: float) -> None:
        n = len(self.linhas)
        self.beginInsertRows(QModelIndex(), n, n)
        self.linhas.append([tag, valor])
        self.endInsertRows()


class TestesCalculadora(unittest.TestCase):
    def setUp(self) -> None:
        self.calc = Calculadora()
        self.calc.show()
        QTest.qWaitForWindowExposed(self.calc)

    def tearDown(self) -> None:
        self.calc.close()
        self.calc.deleteLater()

    def test_teclado_e_mouse(self) -> None:
        espiao = QSignalSpy(
            self.calc.calculado
        )  # registra cada emissão e seus argumentos
        QTest.keyClicks(self.calc.entrada, "2000")
        QTest.mouseClick(
            self.calc.botao,
            Qt.MouseButton.LeftButton,
            Qt.KeyboardModifier.NoModifier,
            QPoint(5, 5),
        )
        self.assertEqual(len(espiao), 1)
        self.assertAlmostEqual(espiao[0][0], 203.03, places=2)
        self.assertEqual(self.calc.resultado.text(), "203.03")

    def test_tecla_enter(self) -> None:
        espiao = QSignalSpy(self.calc.calculado)
        QTest.keyClicks(self.calc.entrada, "100")
        QTest.keyClick(self.calc.entrada, Qt.Key.Key_Return)
        self.assertEqual(len(espiao), 1)  # returnPressed é emitido de forma síncrona

    def test_backspace_corrige_digitacao(self) -> None:
        QTest.keyClicks(self.calc.entrada, "13500")
        QTest.keyClick(self.calc.entrada, Qt.Key.Key_Backspace)
        self.assertEqual(self.calc.entrada.text(), "1350")


class TestesModelo(unittest.TestCase):
    def test_modelo_respeita_contrato(self) -> None:
        modelo = ModeloLeituras()
        # Fatal: qualquer violação do contrato de QAbstractItemModel aborta o teste.
        testador = QAbstractItemModelTester(
            modelo, QAbstractItemModelTester.FailureReportingMode.Fatal
        )
        modelo.adicionar("TT-201", 61.2)
        self.assertEqual(modelo.rowCount(), 3)
        del testador


if __name__ == "__main__":
    unittest.main(
        argv=[sys.argv[0], "-v"],
        testRunner=unittest.TextTestRunner(stream=sys.stdout, verbosity=2),
        exit=False,
    )
