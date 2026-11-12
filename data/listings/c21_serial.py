# runner: ticks=60 serial
"""QSerialPort: aquisição de um instrumento que envia linhas ASCII
($PT,seq,pressao,temp)."""

import os
import sys

from PyQt6.QtCore import QIODevice, QObject, QTimer, pyqtSignal
from PyQt6.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt6.QtWidgets import QApplication

PORTA_PADRAO = "COM3" if sys.platform == "win32" else "/dev/ttyUSB0"


class Aquisicao(QObject):
    amostra = pyqtSignal(int, float, float)
    linha_invalida = pyqtSignal(str)

    def __init__(self, nome_porta: str) -> None:
        super().__init__()
        self.porta = QSerialPort(nome_porta, self)
        self.porta.setBaudRate(
            115200
        )  # no PyQt6 recebe int (BaudRate.Baud115200.value)
        self.porta.setDataBits(QSerialPort.DataBits.Data8)
        self.porta.setParity(QSerialPort.Parity.NoParity)
        self.porta.setStopBits(QSerialPort.StopBits.OneStop)
        self.porta.setFlowControl(QSerialPort.FlowControl.NoFlowControl)
        self.porta.readyRead.connect(self._ler)
        self.porta.errorOccurred.connect(self._erro)

    def abrir(self) -> bool:
        if not self.porta.open(QIODevice.OpenModeFlag.ReadOnly):
            print("Falha ao abrir:", self.porta.errorString())
            return False
        return True

    def _ler(self) -> None:
        while self.porta.canReadLine():
            linha = bytes(self.porta.readLine()).decode("ascii", "replace").strip()
            campos = linha.split(",")
            try:
                if campos[0] != "$PT" or len(campos) != 4:
                    raise ValueError
                self.amostra.emit(int(campos[1]), float(campos[2]), float(campos[3]))
            except ValueError:
                self.linha_invalida.emit(linha)

    def _erro(self, erro: QSerialPort.SerialPortError) -> None:
        if erro != QSerialPort.SerialPortError.NoError:
            print("Erro serial:", erro.name, self.porta.errorString())


def main() -> int:
    app = QApplication(sys.argv)
    portas = QSerialPortInfo.availablePorts()
    print(f"Portas físicas detectadas: {len(portas)}")
    for info in portas:
        print(
            f"  {info.portName()} — {info.description()} (VID {info.vendorIdentifier()})"
        )
    nome = os.environ.get("PORTA_SERIAL", PORTA_PADRAO)
    aq = Aquisicao(nome)
    if not aq.abrir():
        return 1
    print(f"Porta aberta: {aq.porta.isOpen()} | {aq.porta.baudRate()} baud, 8N1")
    serie: list[tuple[int, float, float]] = []
    aq.amostra.connect(lambda s, p, t: serie.append((s, p, t)))
    aq.linha_invalida.connect(lambda l: print("linha descartada:", l))

    def resumo() -> None:
        aq.porta.close()
        print(
            f"{len(serie)} amostras; seq {serie[0][0]}..{serie[-1][0]}; "
            f"pressão {serie[0][1]:.2f} -> {serie[-1][1]:.2f} bar; "
            f"temperatura máx. {max(t for *_, t in serie):.2f} °C"
        )
        app.quit()

    QTimer.singleShot(1800, resumo)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
