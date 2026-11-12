"""Import of readings from CSV files exported by pressure recorders."""

import csv
from pathlib import Path

from .domain import DataError, Reading


def number(text: str) -> float:
    return float(text.strip().replace(",", "."))  # accepts a decimal comma


def read_csv(path: str | Path) -> list[Reading]:
    """Columns: time_min; pressure_bar; temperature_c (separator ';' or ',')."""
    text = Path(path).read_text(encoding="utf-8-sig")
    dialect = csv.Sniffer().sniff(text.splitlines()[0], delimiters=";,")
    readings = []
    for n, line in enumerate(csv.reader(text.splitlines(), dialect), start=1):
        if n == 1 or not any(c.strip() for c in line):  # header or empty line
            continue
        try:
            t, p, temp = (number(c) for c in line[:3])
        except (ValueError, TypeError) as exc:
            raise DataError(f"line {n} invalid: {line!r}") from exc
        readings.append(Reading(t, p, temp))
    return readings
