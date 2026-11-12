"""Armadilha clássica: lambda em laço conectado a clicked(bool)."""
import sys
from functools import partial

from PyQt6.QtWidgets import QApplication, QPushButton

registro: list[str] = []


def ao_clicar(indice: int) -> None:
    registro.append(f"botão {indice}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    botoes = [QPushButton(f"B{i}") for i in range(3)]

    for i, b in enumerate(botoes):
        # ERRADO: clicked envia 'checked' (bool), que sobrescreve o valor default i
        b.clicked.connect(lambda i=i: registro.append(f"errado: {i!r}"))
        # CERTO (1): reservar o primeiro parâmetro para 'checked'
        b.clicked.connect(lambda checked=False, i=i: ao_clicar(i))
        # CERTO (2): functools.partial fixa o argumento antecipadamente
        b.clicked.connect(partial(registro.append, f"partial: {i}"))

    for b in botoes:
        b.click()                      # simula o clique (emite clicked)
    print("\n".join(registro))
