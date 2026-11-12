# runner: ticks=40
"""QQuickWidget: componente QML dentro de uma janela Widgets, com comunicação nos dois
sentidos."""

import os
import sys

from PyQt6.QtCore import Qt, QTimer, QUrl
from PyQt6.QtQuickWidgets import QQuickWidget
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QSlider,
    QVBoxLayout,
    QWidget,
)

AQUI = os.path.dirname(os.path.abspath(__file__))


class Janela(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Widgets + QML")
        self.indicador = QQuickWidget()
        self.indicador.setResizeMode(QQuickWidget.ResizeMode.SizeRootObjectToView)
        self.indicador.setClearColor(Qt.GlobalColor.white)
        self.indicador.setSource(
            QUrl.fromLocalFile(os.path.join(AQUI, "c26_indicador.qml"))
        )
        self.raiz = self.indicador.rootObject()
        self.controle = QSlider(Qt.Orientation.Vertical)
        self.controle.setRange(0, 400)
        self.status = QLabel("Normal")
        self.controle.valueChanged.connect(
            lambda v: self.raiz.setProperty("valor", float(v))
        )
        self.raiz.alarme.connect(self.ao_alarme)  # sinal declarado em QML
        lay = QHBoxLayout()
        lay.addWidget(self.indicador, 1)
        lay.addWidget(self.controle)
        coluna = QVBoxLayout()
        coluna.addLayout(lay)
        coluna.addWidget(self.status)
        central = QWidget()
        central.setLayout(coluna)
        self.setCentralWidget(central)

    def ao_alarme(self, valor: float) -> None:
        self.status.setText(f"ALARME: {valor:.0f} bar acima de 80 % do fundo de escala")


def main() -> int:
    app = QApplication(sys.argv)
    janela = Janela()
    janela.resize(420, 300)
    janela.show()
    print("Status do QML:", janela.indicador.status().name)
    janela.controle.setValue(250)

    def depois() -> None:
        print(
            "valor no QML:",
            janela.raiz.property("valor"),
            "| status:",
            janela.status.text(),
        )
        janela.controle.setValue(345)
        QTimer.singleShot(400, fim)

    def fim() -> None:
        print(
            "valor no QML:",
            janela.raiz.property("valor"),
            "| status:",
            janela.status.text(),
        )
        if os.environ.get("CAPTURA"):
            janela.grab().save(os.environ["CAPTURA"])
        app.quit()

    QTimer.singleShot(400, depois)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
