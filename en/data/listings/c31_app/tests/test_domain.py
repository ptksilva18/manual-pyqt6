"""Domain tests: values computed by hand and cross-check against NumPy."""

import numpy as np
import pytest

from leaktest.csv_import import read_csv
from leaktest.domain import Criterion, DataError, Reading, analyze, linear_regression


def test_regression_matches_numpy():
    x = [0.0, 5.0, 10.0, 20.0, 40.0, 60.0]
    y = [345.0, 344.98, 344.97, 344.93, 344.88, 344.80]
    a, b = linear_regression(x, y)
    a_np, b_np = np.polyfit(x, y, 1)
    assert a == pytest.approx(a_np, rel=1e-12)
    assert b == pytest.approx(b_np, rel=1e-12)


def test_linear_drop_computed_by_hand():
    # 345 bar falling 0.6 bar/h for 60 min: drop 0.6 bar = 0.1739 % (0.6/345)
    readings = [Reading(t, 345.0 - 0.01 * t, 20.0) for t in range(0, 61, 10)]
    r = analyze(readings, Criterion(max_drop_pct=0.5, max_rate_bar_h=1.0))
    assert r.drop_bar == pytest.approx(0.6)
    assert r.drop_pct == pytest.approx(100 * 0.6 / 345.0)
    assert r.rate_bar_h == pytest.approx(0.6)
    assert r.passed and r.reasons == ()


def test_thermal_compensation():
    # Rises 0.5 bar only from 2 °C of heating with dp/dT = 0.25 bar/°C: no real drop
    readings = [Reading(0.0, 345.0, 20.0), Reading(60.0, 345.5, 22.0)]
    r = analyze(readings, Criterion(temp_coef_bar_c=0.25))
    assert r.p_final_corrected == pytest.approx(345.0)
    assert r.drop_bar == pytest.approx(0.0, abs=1e-12)


def test_failures_accumulate_reasons():
    readings = [Reading(0.0, 345.0, 20.0), Reading(30.0, 342.0, 20.0)]
    r = analyze(
        readings, Criterion(duration_min=60.0, max_drop_pct=0.5, max_rate_bar_h=1.0)
    )
    assert not r.passed
    assert len(r.reasons) == 3  # short hold, drop and rate


@pytest.mark.parametrize(
    "readings, message",
    [
        ([Reading(0.0, 345.0, 20.0)], "at least 2"),
        ([Reading(0.0, 345.0, 20.0), Reading(0.0, 344.0, 20.0)], "increasing"),
        ([Reading(0.0, 0.0, 20.0), Reading(1.0, 0.0, 20.0)], "positive"),
    ],
)
def test_invalid_data(readings, message):
    with pytest.raises(DataError, match=message):
        analyze(readings, Criterion())


def test_csv_with_decimal_comma(tmp_path):
    f = tmp_path / "x.csv"
    f.write_text(
        "time_min;pressure_bar;temperature_c\n0;345,0;20,5\n\n10;344,9;20,6\n",
        encoding="utf-8",
    )
    assert read_csv(f) == [Reading(0.0, 345.0, 20.5), Reading(10.0, 344.9, 20.6)]


def test_invalid_csv_reports_line(tmp_path):
    f = tmp_path / "x.csv"
    f.write_text("t;p;T\n0;345;20\n10;abc;20\n", encoding="utf-8")
    with pytest.raises(DataError, match="line 3"):
        read_csv(f)
