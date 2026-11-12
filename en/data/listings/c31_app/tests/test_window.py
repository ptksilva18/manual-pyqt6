"""Interface tests with pytest-qt: full workflow and error handling."""

from pathlib import Path

import pytest
from PyQt6.QtWidgets import QMessageBox

from leaktest.domain import Criterion
from leaktest.repository import Repository
from leaktest.services import AnalysisService
from leaktest.window import MainWindow

CSV = Path(__file__).resolve().parent.parent / "data" / "TH-01.csv"


@pytest.fixture
def window(qtbot, tmp_path):
    repo = Repository(tmp_path / "test.sqlite")
    w = MainWindow(repo, AnalysisService())
    qtbot.addWidget(w)
    yield w
    w.service.wait()
    repo.close()


def test_actions_disabled_without_test(window):
    assert not window.act_import.isEnabled()
    assert not window.act_analyze.isEnabled()
    assert not window.act_report.isEnabled()


def test_full_workflow(window, qtbot, tmp_path):
    window.new_test("TH-01", "service line", Criterion(temp_coef_bar_c=0.25))
    assert window.import_csv(str(CSV))
    assert window.readings_model.rowCount() == 13
    with qtbot.waitSignal(window.service.completed, timeout=5000) as blocker:
        window.act_analyze.trigger()
    result = blocker.args[1]
    assert result.passed
    assert result.drop_bar == pytest.approx(0.224, abs=0.001)
    assert "PASSED" in window.panel.text()
    assert window.act_report.isEnabled()
    pdf = window.report(str(tmp_path / "r.pdf"))
    assert pdf.read_bytes()[:5] == b"%PDF-"


def test_repeated_code_shows_warning(window, monkeypatch):
    warnings = []
    monkeypatch.setattr(QMessageBox, "warning", lambda *a: warnings.append(a[2]))
    window.new_test("TH-02")
    assert window.new_test("TH-02") is None
    assert "UNIQUE" in warnings[0]
    assert window.tests_model.rowCount() == 1


def test_invalid_csv_keeps_readings(window, monkeypatch, tmp_path):
    errors = []
    monkeypatch.setattr(QMessageBox, "critical", lambda *a: errors.append(a[2]))
    window.new_test("TH-03")
    bad = tmp_path / "bad.csv"
    bad.write_text("t;p;T\n0;x;1\n", encoding="utf-8")
    assert not window.import_csv(str(bad))
    assert "line 2" in errors[0]
    assert window.readings_model.rowCount() == 0
