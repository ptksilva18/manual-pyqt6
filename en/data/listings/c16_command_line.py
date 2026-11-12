"""QCommandLineParser: options, values, positional arguments and --help."""

import sys

from PyQt6.QtCore import QCommandLineOption, QCommandLineParser
from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    sys.argv = ["engcalc", "--units", "psi", "-v", "bop_test.json"]  # simulation
    app = QApplication(sys.argv)
    app.setApplicationName("engcalc")
    app.setApplicationVersion("0.1.0")

    parser = QCommandLineParser()
    parser.setApplicationDescription("Engineering calculator")
    parser.addHelpOption()  # -h / --help
    parser.addVersionOption()  # -v / --version
    units = QCommandLineOption(["u", "units"], "Unit system.", "name", "bar")
    verbose = QCommandLineOption(["d", "detailed"], "Detailed output.")
    parser.addOptions([units, verbose])
    parser.addPositionalArgument("file", "Test file to open.")
    # parse() does not exit; process() does
    parser.parse(app.arguments())

    print("units:", parser.value(units))
    print("detailed:", parser.isSet(verbose))
    print("--version requested?", parser.isSet("version"))
    print("positional:", parser.positionalArguments())
    print(parser.helpText().strip().splitlines()[0])
