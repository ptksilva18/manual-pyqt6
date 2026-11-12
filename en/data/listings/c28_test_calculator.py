# runner: ticks=300 timeout=120
"""Tests of the calculator with pytest-qt (qtbot fixture). Run: pytest
c28_test_calculator.py"""

import os
import sys

import pytest
from PyQt6.QtCore import Qt

from c28_calculator import Calculator, pressure_bar


@pytest.fixture
def calc(qtbot):
    w = Calculator()
    qtbot.addWidget(w)  # qtbot closes and destroys the widget at the end of the test
    return w


def test_domain_known_value():
    assert pressure_bar(0.0) == pytest.approx(1.01325)
    assert pressure_bar(1000.0) == pytest.approx(102.03, abs=0.01)


def test_domain_rejects_negative():
    with pytest.raises(ValueError):
        pressure_bar(-1.0)


def test_type_and_click(calc, qtbot):
    qtbot.keyClicks(calc.entry, "1350")
    with qtbot.waitSignal(calc.computed, timeout=1000) as blocker:
        qtbot.mouseClick(calc.button, Qt.MouseButton.LeftButton)
    assert blocker.args[0] == pytest.approx(137.37, abs=0.01)
    assert calc.result.text() == "137.37"


def test_enter_triggers_computation(calc, qtbot):
    qtbot.keyClicks(calc.entry, "2000")
    with qtbot.waitSignal(calc.computed, timeout=1000):
        qtbot.keyPress(calc.entry, Qt.Key.Key_Return)
    assert calc.result.text() == "203.03"


def test_validator_blocks_text(calc, qtbot):
    qtbot.keyClicks(calc.entry, "abc")
    assert calc.entry.text() == ""  # the QDoubleValidator rejected the keys
    with qtbot.assertNotEmitted(calc.computed):
        qtbot.mouseClick(calc.button, Qt.MouseButton.LeftButton)
    assert calc.result.text() == "invalid input"


@pytest.mark.parametrize(
    "depth, expected", [("0", "1.01"), ("500", "51.52"), ("3000", "304.04")]
)
def test_several_values(calc, qtbot, depth, expected):
    qtbot.keyClicks(calc.entry, depth)
    calc.button.click()
    qtbot.waitUntil(lambda: calc.result.text() == expected, timeout=1000)


if __name__ == "__main__":
    os.chdir(
        os.path.dirname(os.path.abspath(__file__))
    )  # test ids relative to the folder
    sys.exit(
        pytest.main(
            [os.path.basename(__file__), "-v", "--no-header", "-p", "no:cacheprovider"]
        )
    )
