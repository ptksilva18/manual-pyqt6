"""Domain: analysis of leak tests (pure Python, no Qt)."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Reading:
    t_min: float  # time since the start of stabilization (min)
    p_bar: float  # gauge pressure (bar)
    temp_c: float  # temperature of the test fluid (°C)


@dataclass(frozen=True)
class Criterion:
    duration_min: float = 60.0  # minimum hold time
    max_drop_pct: float = 0.5  # allowable drop, % of the initial pressure
    max_rate_bar_h: float = 1.0  # allowable rate of drop (linear regression)
    temp_coef_bar_c: float = 0.0  # thermal compensation dp/dT (bar/°C); 0 = none


@dataclass(frozen=True)
class Result:
    p_initial: float
    p_final_corrected: float
    drop_bar: float
    drop_pct: float
    rate_bar_h: float
    duration_min: float
    passed: bool
    reasons: tuple[str, ...] = field(default_factory=tuple)


class DataError(ValueError):
    """Inconsistent test data (fewer than 2 readings, non-increasing time...)."""


def linear_regression(x: list[float], y: list[float]) -> tuple[float, float]:
    """Least squares: returns (slope, intercept)."""
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    sxx = sum((xi - mx) ** 2 for xi in x)
    if sxx == 0.0:
        raise DataError("all readings have the same time")
    sxy = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
    a = sxy / sxx
    return a, my - a * mx


def analyze(readings: list[Reading], criterion: Criterion) -> Result:
    if len(readings) < 2:
        raise DataError("at least 2 readings are required")
    times = [rd.t_min for rd in readings]
    if any(b <= a for a, b in zip(times, times[1:])):
        raise DataError("the reading times must be strictly increasing")
    p0, t0 = readings[0].p_bar, readings[0].temp_c
    if p0 <= 0.0:
        raise DataError("the initial pressure must be positive")
    k = criterion.temp_coef_bar_c
    # Pressure corrected to the initial temperature: p_corr = p - k * (T - T0)
    p_corr = [rd.p_bar - k * (rd.temp_c - t0) for rd in readings]
    drop = p0 - p_corr[-1]
    drop_pct = 100.0 * drop / p0
    slope, _ = linear_regression(times, p_corr)  # bar/min
    rate_bar_h = -60.0 * slope  # positive when the pressure falls
    duration = times[-1] - times[0]
    reasons = []
    if duration < criterion.duration_min:
        reasons.append(
            f"hold of {duration:.0f} min < {criterion.duration_min:.0f} min required"
        )
    if drop_pct > criterion.max_drop_pct:
        reasons.append(f"drop of {drop_pct:.3f} % > {criterion.max_drop_pct:.3f} %")
    if rate_bar_h > criterion.max_rate_bar_h:
        reasons.append(
            f"rate of {rate_bar_h:.3f} bar/h > {criterion.max_rate_bar_h:.3f} bar/h"
        )
    return Result(
        p0,
        p_corr[-1],
        drop,
        drop_pct,
        rate_bar_h,
        duration,
        not reasons,
        tuple(reasons),
    )
