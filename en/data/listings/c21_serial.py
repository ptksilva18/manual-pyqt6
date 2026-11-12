# runner: ticks=60 serial
"""QSerialPort: acquisition from an instrument that sends ASCII lines
($PT,seq,pressure,temp)."""

import os
import sys

from PyQt6.QtCore import QIODevice, QObject, QTimer, pyqtSignal
from PyQt6.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt6.QtWidgets import QApplication

DEFAULT_PORT = "COM3" if sys.platform == "win32" else "/dev/ttyUSB0"


class Acquisition(QObject):
    sample = pyqtSignal(int, float, float)
    invalid_line = pyqtSignal(str)

    def __init__(self, port_name: str) -> None:
        super().__init__()
        self.port = QSerialPort(port_name, self)
        self.port.setBaudRate(
            115200
        )  # in PyQt6 it takes an int (BaudRate.Baud115200.value)
        self.port.setDataBits(QSerialPort.DataBits.Data8)
        self.port.setParity(QSerialPort.Parity.NoParity)
        self.port.setStopBits(QSerialPort.StopBits.OneStop)
        self.port.setFlowControl(QSerialPort.FlowControl.NoFlowControl)
        self.port.readyRead.connect(self._read)
        self.port.errorOccurred.connect(self._error)

    def open(self) -> bool:
        if not self.port.open(QIODevice.OpenModeFlag.ReadOnly):
            print("Failed to open:", self.port.errorString())
            return False
        return True

    def _read(self) -> None:
        while self.port.canReadLine():
            line = bytes(self.port.readLine()).decode("ascii", "replace").strip()
            fields = line.split(",")
            try:
                if fields[0] != "$PT" or len(fields) != 4:
                    raise ValueError
                self.sample.emit(int(fields[1]), float(fields[2]), float(fields[3]))
            except ValueError:
                self.invalid_line.emit(line)

    def _error(self, error: QSerialPort.SerialPortError) -> None:
        if error != QSerialPort.SerialPortError.NoError:
            print("Serial error:", error.name, self.port.errorString())


def main() -> int:
    app = QApplication(sys.argv)
    ports = QSerialPortInfo.availablePorts()
    print(f"Physical ports detected: {len(ports)}")
    for info in ports:
        print(
            f"  {info.portName()} — {info.description()} (VID {info.vendorIdentifier()})"
        )
    name = os.environ.get("SERIAL_PORT", DEFAULT_PORT)
    acq = Acquisition(name)
    if not acq.open():
        return 1
    print(f"Port open: {acq.port.isOpen()} | {acq.port.baudRate()} baud, 8N1")
    series: list[tuple[int, float, float]] = []
    acq.sample.connect(lambda s, p, t: series.append((s, p, t)))
    acq.invalid_line.connect(lambda l: print("line discarded:", l))

    def summary() -> None:
        acq.port.close()
        print(
            f"{len(series)} samples; seq {series[0][0]}..{series[-1][0]}; "
            f"pressure {series[0][1]:.2f} -> {series[-1][1]:.2f} bar; "
            f"max. temperature {max(t for *_, t in series):.2f} °C"
        )
        app.quit()

    QTimer.singleShot(1800, summary)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
