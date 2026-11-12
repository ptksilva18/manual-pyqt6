"""Argumentos de linha de comando: o Qt consome as opções que reconhece."""
import sys

from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    # Simula: python app.py -style fusion relatorio.csv --verbose
    argv = ["app.py", "-style", "fusion", "relatorio.csv", "--verbose"]
    app = QApplication(argv)
    print("lista original após o construtor:", argv)
    print("app.arguments():                 ", app.arguments())
    print("estilo em uso:", app.style().name())
