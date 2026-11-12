"""Command-line arguments: Qt consumes the options it recognizes."""
import sys

from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    # Simulates: python app.py -style fusion report.csv --verbose
    argv = ["app.py", "-style", "fusion", "report.csv", "--verbose"]
    app = QApplication(argv)
    print("original list after the constructor:", argv)
    print("app.arguments():                    ", app.arguments())
    print("style in use:", app.style().name())
