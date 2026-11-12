"""Script de entrada para o PyInstaller (equivale a "python -m ensaios")."""

import sys

from ensaios.app import main

if __name__ == "__main__":
    sys.exit(main(sys.argv))
