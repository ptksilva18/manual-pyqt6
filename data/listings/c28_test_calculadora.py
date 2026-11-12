# runner: ticks=300 timeout=120
"""Testes da calculadora com pytest-qt (fixture qtbot). Execute: pytest
c28_test_calculadora.py"""

import os
import sys

import pytest
from PyQt6.QtCore import Qt

from c28_calculadora import Calculadora, pressao_bar


@pytest.fixture
def calc(qtbot):
    w = Calculadora()
    qtbot.addWidget(w)  # o qtbot fecha e destrói o widget ao fim do teste
    return w


def test_dominio_valor_conhecido():
    assert pressao_bar(0.0) == pytest.approx(1.01325)
    assert pressao_bar(1000.0) == pytest.approx(102.03, abs=0.01)


def test_dominio_rejeita_negativo():
    with pytest.raises(ValueError):
        pressao_bar(-1.0)


def test_digitar_e_clicar(calc, qtbot):
    qtbot.keyClicks(calc.entrada, "1350")
    with qtbot.waitSignal(calc.calculado, timeout=1000) as bloqueio:
        qtbot.mouseClick(calc.botao, Qt.MouseButton.LeftButton)
    assert bloqueio.args[0] == pytest.approx(137.37, abs=0.01)
    assert calc.resultado.text() == "137.37"


def test_enter_dispara_calculo(calc, qtbot):
    qtbot.keyClicks(calc.entrada, "2000")
    with qtbot.waitSignal(calc.calculado, timeout=1000):
        qtbot.keyPress(calc.entrada, Qt.Key.Key_Return)
    assert calc.resultado.text() == "203.03"


def test_validador_bloqueia_texto(calc, qtbot):
    qtbot.keyClicks(calc.entrada, "abc")
    assert calc.entrada.text() == ""  # o QDoubleValidator recusou as teclas
    with qtbot.assertNotEmitted(calc.calculado):
        qtbot.mouseClick(calc.botao, Qt.MouseButton.LeftButton)
    assert calc.resultado.text() == "entrada inválida"


@pytest.mark.parametrize(
    "prof, esperado", [("0", "1.01"), ("500", "51.52"), ("3000", "304.04")]
)
def test_varios_valores(calc, qtbot, prof, esperado):
    qtbot.keyClicks(calc.entrada, prof)
    calc.botao.click()
    qtbot.waitUntil(lambda: calc.resultado.text() == esperado, timeout=1000)


if __name__ == "__main__":
    os.chdir(
        os.path.dirname(os.path.abspath(__file__))
    )  # ids de teste relativos à pasta
    sys.exit(
        pytest.main(
            [os.path.basename(__file__), "-v", "--no-header", "-p", "no:cacheprovider"]
        )
    )
