"""QCommandLineParser: opções, valores, argumentos posicionais e --help."""

import sys

from PyQt6.QtCore import QCommandLineOption, QCommandLineParser
from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    sys.argv = ["calceng", "--unidades", "psi", "-v", "ensaio_bop.json"]  # simulação
    app = QApplication(sys.argv)
    app.setApplicationName("calceng")
    app.setApplicationVersion("0.1.0")

    parser = QCommandLineParser()
    parser.setApplicationDescription("Calculadora de engenharia")
    parser.addHelpOption()  # -h / --help
    parser.addVersionOption()  # -v / --version
    unidades = QCommandLineOption(
        ["u", "unidades"], "Sistema de unidades.", "nome", "bar"
    )
    detalhado = QCommandLineOption(["d", "detalhado"], "Saída detalhada.")
    parser.addOptions([unidades, detalhado])
    parser.addPositionalArgument("arquivo", "Arquivo de ensaio a abrir.")
    # parse() não encerra; process() sim
    parser.parse(app.arguments())

    print("unidades:", parser.value(unidades))
    print("detalhado:", parser.isSet(detalhado))
    print("--version pedido?", parser.isSet("version"))
    print("posicionais:", parser.positionalArguments())
    print(parser.helpText().strip().splitlines()[0])
