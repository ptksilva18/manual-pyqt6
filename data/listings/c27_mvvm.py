# runner: ticks=40
"""MVVM: ViewModel com propriedades notificáveis e ligação (binding) bidirecional a
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


class VMConversor(QObject):
    """Estado e regras da tela, sem widgets: converte pressão entre bar e psi."""

    barChanged = pyqtSignal(float)
    psiChanged = pyqtSignal(float)
    alarmeChanged = pyqtSignal(bool)
    FATOR = 14.503773773
    LIMITE_BAR = 350.0

    def __init__(self) -> None:
        super().__init__()
        self._bar = 0.0

    @pyqtProperty(float, notify=barChanged)
    def bar(self) -> float:
        return self._bar

    @bar.setter
    def bar(self, valor: float) -> None:
        if abs(valor - self._bar) < 1e-9:  # evita laços de atualização entre widgets
            return
        alarme_antes = self.alarme
        self._bar = valor
        self.barChanged.emit(valor)
        self.psiChanged.emit(self.psi)
        if self.alarme != alarme_antes:
            self.alarmeChanged.emit(self.alarme)

    @pyqtProperty(float, notify=psiChanged)
    def psi(self) -> float:
        return self._bar * self.FATOR

    @psi.setter
    def psi(self, valor: float) -> None:
        self.bar = valor / self.FATOR

    @pyqtProperty(bool, notify=alarmeChanged)
    def alarme(self) -> bool:
        return self._bar > self.LIMITE_BAR


def ligar(
    sinal_vm,
    widget: QWidget,
    setter_widget: Callable,
    sinal_widget=None,
    setter_vm=None,
) -> None:
    """Liga uma propriedade do ViewModel a um widget (e, se pedido, no sentido inverso).

    A atualização vinda do ViewModel bloqueia os sinais do widget: assim o valor
    arredondado pelo widget (casas decimais) não volta ao ViewModel e não gera deriva.
    """

    def atualizar_widget(valor) -> None:
        with QSignalBlocker(widget):
            setter_widget(valor)

    sinal_vm.connect(atualizar_widget)
    if sinal_widget is not None and setter_vm is not None:
        sinal_widget.connect(setter_vm)


class TelaConversor(QWidget):
    def __init__(self, vm: VMConversor) -> None:
        super().__init__()
        self.vm = vm
        self.ed_bar = QDoubleSpinBox(decimals=3, maximum=1e5, suffix=" bar")
        self.ed_psi = QDoubleSpinBox(decimals=3, maximum=1e6, suffix=" psi")
        self.alarme = QCheckBox("Acima de 350 bar")
        self.alarme.setEnabled(False)
        self.info = QLabel()
        lay = QVBoxLayout(self)
        for w in (self.ed_bar, self.ed_psi, self.alarme, self.info):
            lay.addWidget(w)
        ligar(
            vm.barChanged,
            self.ed_bar,
            self.ed_bar.setValue,
            self.ed_bar.valueChanged,
            lambda v: setattr(vm, "bar", v),
        )
        ligar(
            vm.psiChanged,
            self.ed_psi,
            self.ed_psi.setValue,
            self.ed_psi.valueChanged,
            lambda v: setattr(vm, "psi", v),
        )
        ligar(vm.alarmeChanged, self.alarme, self.alarme.setChecked)
        vm.barChanged.connect(
            lambda v: self.info.setText(f"{v:.3f} bar = {vm.psi:.3f} psi")
        )


def main() -> int:
    app = QApplication(sys.argv)
    vm = VMConversor()
    tela = TelaConversor(vm)
    tela.show()
    tela.ed_bar.setValue(100.0)  # o usuário digita em bar
    print(
        f"bar -> psi: {tela.ed_psi.value():.3f} psi | alarme {tela.alarme.isChecked()}"
    )
    tela.ed_psi.setValue(5500.0)  # o usuário digita em psi
    print(
        f"psi -> bar: {tela.ed_bar.value():.3f} bar | campo psi permanece "
        f"{tela.ed_psi.value():.3f} | VM: {vm.psi:.6f} psi | alarme "
        f"{tela.alarme.isChecked()}"
    )
    vm.bar = 200.0  # a lógica altera o ViewModel; a tela acompanha
    print(
        f"VM -> tela: {tela.ed_bar.value():.3f} bar, {tela.ed_psi.value():.3f} psi | "
        f"alarme {tela.alarme.isChecked()} | {tela.info.text()}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
