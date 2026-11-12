# runner: ticks=40
"""MVP: pure domain, testable presenter and two views (real widget and fake one, for
testing)."""

import sys
from dataclasses import dataclass
from typing import Protocol

from PyQt6.QtWidgets import (
    QApplication,
    QDoubleSpinBox,
    QFormLayout,
    QLabel,
    QPushButton,
    QWidget,
)


# ---------------------------------------------------------------- domain (no Qt)
@dataclass(frozen=True)
class LeakTestResult:
    drop_bar: float
    drop_percent: float
    passed: bool


def evaluate_leak_test(
    p_initial: float, p_final: float, limit_percent: float
) -> LeakTestResult:
    if p_initial <= 0.0:
        raise ValueError("initial pressure must be positive")
    drop = p_initial - p_final
    pct = 100.0 * drop / p_initial
    return LeakTestResult(drop, pct, pct <= limit_percent)


# ---------------------------------------------------------------- view contract
class LeakTestView(Protocol):
    def values(self) -> tuple[float, float, float]: ...
    def show_result(self, text: str, passed: bool) -> None: ...
    def show_error(self, text: str) -> None: ...


# ---------------------------------------------------------------- presenter
class Presenter:
    """Knows no widgets: talks to any object that fulfills the Protocol."""

    def __init__(self, view: LeakTestView) -> None:
        self.view = view

    def evaluate(self) -> None:
        p0, p1, limit = self.view.values()
        try:
            r = evaluate_leak_test(p0, p1, limit)
        except ValueError as exc:
            self.view.show_error(str(exc))
            return
        status = "PASSED" if r.passed else "FAILED"
        self.view.show_result(
            f"Drop {r.drop_bar:.2f} bar ({r.drop_percent:.3f} %) — {status}",
            r.passed,
        )


# ---------------------------------------------------------------- real view (Qt)
class LeakTestForm(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.p0, self.p1, self.lim = (
            QDoubleSpinBox(decimals=2, maximum=1000.0) for _ in range(3)
        )
        self.p0.setValue(345.0)
        self.p1.setValue(344.0)
        self.lim.setValue(0.5)
        self.label = QLabel()
        button = QPushButton("Evaluate")
        form = QFormLayout(self)
        form.addRow("Initial pressure (bar)", self.p0)
        form.addRow("Final pressure (bar)", self.p1)
        form.addRow("Allowable drop (%)", self.lim)
        form.addRow(button)
        form.addRow(self.label)
        self.presenter = Presenter(self)
        button.clicked.connect(self.presenter.evaluate)
        self.button = button

    def values(self) -> tuple[float, float, float]:
        return self.p0.value(), self.p1.value(), self.lim.value()

    def show_result(self, text: str, passed: bool) -> None:
        self.label.setStyleSheet(f"color: {'#548235' if passed else '#C00000'}")
        self.label.setText(text)

    def show_error(self, text: str) -> None:
        self.label.setStyleSheet("color: #C55A11")
        self.label.setText(f"Error: {text}")


# ---------------------------------------------------------------- fake view (tests)
class FakeView:
    def __init__(self, p0: float, p1: float, limit: float) -> None:
        self.inputs = (p0, p1, limit)
        self.outputs: list[str] = []

    def values(self) -> tuple[float, float, float]:
        return self.inputs

    def show_result(self, text: str, passed: bool) -> None:
        self.outputs.append(f"result: {text} (passed={passed})")

    def show_error(self, text: str) -> None:
        self.outputs.append(f"error: {text}")


def main() -> int:
    for case in ((345.0, 344.0, 0.5), (345.0, 342.0, 0.5), (0.0, 0.0, 0.5)):
        fake = FakeView(*case)
        Presenter(fake).evaluate()
        print("Fake view ", case, "->", fake.outputs[0])
    app = QApplication(sys.argv)
    form = LeakTestForm()
    form.show()
    form.button.click()
    print("Real view  -> label:", form.label.text())
    app.processEvents()
    return 0


if __name__ == "__main__":
    sys.exit(main())
