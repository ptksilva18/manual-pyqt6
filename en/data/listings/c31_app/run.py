"""Entry script for PyInstaller (equivalent to "python -m leaktest")."""

import sys

from leaktest.app import main

if __name__ == "__main__":
    sys.exit(main(sys.argv))
