"""Herança e super(): uma subclasse de QWidget com parâmetros próprios."""
import sys

from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget


class PainelTitulado(QWidget):
    """Painel com um título fixo; aceita 'parent' como qualquer QWidget."""

    def __init__(self, titulo: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)              # inicializa a parte C++ do QWidget
        self.titulo = titulo                  # atributo Python comum
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"<b>{titulo}</b>"))

    def descricao(self) -> str:
        return f"{type(self).__name__}('{self.titulo}')"


class PainelResultado(PainelTitulado):
    """Especialização: acrescenta um rótulo de valor."""

    def __init__(self, titulo: str, unidade: str, parent: QWidget | None = None) -> None:
        super().__init__(titulo, parent)      # reaproveita a inicialização da base
        self.unidade = unidade
        self.valor = QLabel(f"— {unidade}")
        self.layout().addWidget(self.valor)

    def mostrar(self, x: float) -> None:
        self.valor.setText(f"{x:.2f} {self.unidade}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    painel = PainelResultado("Pressão de teste", "bar")
    painel.mostrar(345.0)
    print(painel.descricao())
    print("MRO:", [c.__name__ for c in type(painel).__mro__][:4])
    print("Texto exibido:", painel.valor.text())
