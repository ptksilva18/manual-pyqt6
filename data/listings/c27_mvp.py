# runner: ticks=40
"""MVP: domínio puro, presenter testável e duas views (widget real e falsa, para
teste)."""

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


# ---------------------------------------------------------------- domínio (sem Qt)
@dataclass(frozen=True)
class ResultadoEstanqueidade:
    queda_bar: float
    queda_percentual: float
    aprovado: bool


def avaliar_estanqueidade(
    p_inicial: float, p_final: float, limite_percentual: float
) -> ResultadoEstanqueidade:
    if p_inicial <= 0.0:
        raise ValueError("pressão inicial deve ser positiva")
    queda = p_inicial - p_final
    pct = 100.0 * queda / p_inicial
    return ResultadoEstanqueidade(queda, pct, pct <= limite_percentual)


# ---------------------------------------------------------------- contrato da view
class VisaoEstanqueidade(Protocol):
    def valores(self) -> tuple[float, float, float]: ...
    def mostrar_resultado(self, texto: str, aprovado: bool) -> None: ...
    def mostrar_erro(self, texto: str) -> None: ...


# ---------------------------------------------------------------- presenter
class Apresentador:
    """Não conhece widgets: conversa com qualquer objeto que cumpra o Protocol."""

    def __init__(self, visao: VisaoEstanqueidade) -> None:
        self.visao = visao

    def avaliar(self) -> None:
        p0, p1, limite = self.visao.valores()
        try:
            r = avaliar_estanqueidade(p0, p1, limite)
        except ValueError as exc:
            self.visao.mostrar_erro(str(exc))
            return
        estado = "APROVADO" if r.aprovado else "REPROVADO"
        self.visao.mostrar_resultado(
            f"Queda {r.queda_bar:.2f} bar ({r.queda_percentual:.3f} %) — {estado}",
            r.aprovado,
        )


# ---------------------------------------------------------------- view real (Qt)
class FormularioEstanqueidade(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.p0, self.p1, self.lim = (
            QDoubleSpinBox(decimals=2, maximum=1000.0) for _ in range(3)
        )
        self.p0.setValue(345.0)
        self.p1.setValue(344.0)
        self.lim.setValue(0.5)
        self.rotulo = QLabel()
        botao = QPushButton("Avaliar")
        form = QFormLayout(self)
        form.addRow("Pressão inicial (bar)", self.p0)
        form.addRow("Pressão final (bar)", self.p1)
        form.addRow("Queda admissível (%)", self.lim)
        form.addRow(botao)
        form.addRow(self.rotulo)
        self.apresentador = Apresentador(self)
        botao.clicked.connect(self.apresentador.avaliar)
        self.botao = botao

    def valores(self) -> tuple[float, float, float]:
        return self.p0.value(), self.p1.value(), self.lim.value()

    def mostrar_resultado(self, texto: str, aprovado: bool) -> None:
        self.rotulo.setStyleSheet(f"color: {'#548235' if aprovado else '#C00000'}")
        self.rotulo.setText(texto)

    def mostrar_erro(self, texto: str) -> None:
        self.rotulo.setStyleSheet("color: #C55A11")
        self.rotulo.setText(f"Erro: {texto}")


# ---------------------------------------------------------------- view falsa (testes)
class VisaoFalsa:
    def __init__(self, p0: float, p1: float, limite: float) -> None:
        self.entrada = (p0, p1, limite)
        self.saidas: list[str] = []

    def valores(self) -> tuple[float, float, float]:
        return self.entrada

    def mostrar_resultado(self, texto: str, aprovado: bool) -> None:
        self.saidas.append(f"resultado: {texto} (aprovado={aprovado})")

    def mostrar_erro(self, texto: str) -> None:
        self.saidas.append(f"erro: {texto}")


def main() -> int:
    for caso in ((345.0, 344.0, 0.5), (345.0, 342.0, 0.5), (0.0, 0.0, 0.5)):
        falsa = VisaoFalsa(*caso)
        Apresentador(falsa).avaliar()
        print("View falsa ", caso, "->", falsa.saidas[0])
    app = QApplication(sys.argv)
    form = FormularioEstanqueidade()
    form.show()
    form.botao.click()
    print("View real  -> rótulo:", form.rotulo.text())
    app.processEvents()
    return 0


if __name__ == "__main__":
    sys.exit(main())
