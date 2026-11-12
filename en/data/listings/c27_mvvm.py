# runner: ticks=40
"""MVVM: ViewModel with notifiable properties and two-way binding to
widgets."""

import sys
from collections.abc import Callable

from PyQt6.QtCore import QObject, QSignalBlocker, pyqtProperty, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QDoubleSpinBox,
    QLabel,
    QVBoxLayout,
    QWidget,
)


class ConverterVM(QObject):
    """Screen state and rules, without widgets: converts pressure between bar and psi."""

    barChanged = pyqtSignal(float)
    psiChanged = pyqtSignal(float)
    alarmChanged = pyqtSignal(bool)
    FACTOR = 14.503773773
    LIMIT_BAR = 350.0

    def __init__(self) -> None:
        super().__init__()
        self._bar = 0.0

    @pyqtProperty(float, notify=barChanged)
    def bar(self) -> float:
        return self._bar

    @bar.setter
    def bar(self, value: float) -> None:
        if abs(value - self._bar) < 1e-9:  # avoids update loops between widgets
            return
        alarm_before = self.alarm
        self._bar = value
        self.barChanged.emit(value)
        self.psiChanged.emit(self.psi)
        if self.alarm != alarm_before:
            self.alarmChanged.emit(self.alarm)

    @pyqtProperty(float, notify=psiChanged)
    def psi(self) -> float:
        return self._bar * self.FACTOR

    @psi.setter
    def psi(self, value: float) -> None:
        self.bar = value / self.FACTOR

    @pyqtProperty(bool, notify=alarmChanged)
    def alarm(self) -> bool:
        return self._bar > self.LIMIT_BAR


def bind(
    vm_signal,
    widget: QWidget,
    widget_setter: Callable,
    widget_signal=None,
    vm_setter=None,
) -> None:
    """Binds a ViewModel property to a widget (and, if requested, in the other direction).

    An update coming from the ViewModel blocks the widget's signals: this way the value
    rounded by the widget (decimal places) does not go back to the ViewModel and causes no
    drift.
    """

    def update_widget(value) -> None:
        with QSignalBlocker(widget):
            widget_setter(value)

    vm_signal.connect(update_widget)
    if widget_signal is not None and vm_setter is not None:
        widget_signal.connect(vm_setter)


class ConverterScreen(QWidget):
    def __init__(self, vm: ConverterVM) -> None:
        super().__init__()
        self.vm = vm
        self.ed_bar = QDoubleSpinBox(decimals=3, maximum=1e5, suffix=" bar")
        self.ed_psi = QDoubleSpinBox(decimals=3, maximum=1e6, suffix=" psi")
        self.alarm = QCheckBox("Above 350 bar")
        self.alarm.setEnabled(False)
        self.info = QLabel()
        lay = QVBoxLayout(self)
        for w in (self.ed_bar, self.ed_psi, self.alarm, self.info):
            lay.addWidget(w)
        bind(
            vm.barChanged,
            self.ed_bar,
            self.ed_bar.setValue,
            self.ed_bar.valueChanged,
            lambda v: setattr(vm, "bar", v),
        )
        bind(
            vm.psiChanged,
            self.ed_psi,
            self.ed_psi.setValue,
            self.ed_psi.valueChanged,
            lambda v: setattr(vm, "psi", v),
        )
        bind(vm.alarmChanged, self.alarm, self.alarm.setChecked)
        vm.barChanged.connect(
            lambda v: self.info.setText(f"{v:.3f} bar = {vm.psi:.3f} psi")
        )


def main() -> int:
    app = QApplication(sys.argv)
    vm = ConverterVM()
    screen = ConverterScreen(vm)
    screen.show()
    screen.ed_bar.setValue(100.0)  # the user types in bar
    print(
        f"bar -> psi: {screen.ed_psi.value():.3f} psi | alarm {screen.alarm.isChecked()}"
    )
    screen.ed_psi.setValue(5500.0)  # the user types in psi
    print(
        f"psi -> bar: {screen.ed_bar.value():.3f} bar | psi field stays "
        f"{screen.ed_psi.value():.3f} | VM: {vm.psi:.6f} psi | alarm "
        f"{screen.alarm.isChecked()}"
    )
    vm.bar = 200.0  # the logic changes the ViewModel; the screen follows
    print(
        f"VM -> screen: {screen.ed_bar.value():.3f} bar, "
        f"{screen.ed_psi.value():.3f} psi | "
        f"alarm {screen.alarm.isChecked()} | {screen.info.text()}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
