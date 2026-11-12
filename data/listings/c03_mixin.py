"""Mixin Python puro combinado com uma única classe Qt."""
import sys

from PyQt6.QtWidgets import QApplication, QLineEdit


class RegistroMixin:
    """Mixin sem base Qt: acrescenta um histórico de mensagens."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)     # repassa adiante (cooperativo)
        self._historico: list[str] = []

    def registrar(self, msg: str) -> None:
        self._historico.append(msg)

    @property
    def historico(self) -> tuple[str, ...]:
        return tuple(self._historico)


class CampoAuditado(RegistroMixin, QLineEdit):
    """Herda de UMA classe Qt (QLineEdit) e de um mixin Python."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.textChanged.connect(lambda t: self.registrar(f"texto={t!r}"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    campo = CampoAuditado()
    campo.setText("ABC")
    campo.setText("ABCD")
    print(campo.historico)
    print("É QLineEdit?", isinstance(campo, QLineEdit))
