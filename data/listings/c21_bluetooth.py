# runner: ticks=60
"""Bluetooth LE e NFC: descoberta de dispositivos com tratamento de ausência de
hardware."""

import sys

from PyQt6.QtBluetooth import (
    QBluetoothDeviceDiscoveryAgent,
    QBluetoothDeviceInfo,
    QBluetoothLocalDevice,
)
from PyQt6.QtCore import QTimer
from PyQt6.QtNfc import QNearFieldManager
from PyQt6.QtWidgets import QApplication


def main() -> int:
    app = QApplication(sys.argv)
    adaptadores = QBluetoothLocalDevice.allDevices()
    print(f"Adaptadores Bluetooth locais: {len(adaptadores)}")
    print(f"NFC suportado nesta plataforma: {QNearFieldManager().isSupported()}")
    agente = QBluetoothDeviceDiscoveryAgent()
    agente.setLowEnergyDiscoveryTimeout(3000)  # ms; 0 = até chamar stop()
    print(
        "Métodos suportados:",
        QBluetoothDeviceDiscoveryAgent.supportedDiscoveryMethods(),
    )

    def encontrado(info: QBluetoothDeviceInfo) -> None:
        if (
            info.coreConfigurations()
            & QBluetoothDeviceInfo.CoreConfiguration.LowEnergyCoreConfiguration
        ):
            print(
                f"BLE: {info.name() or '(sem nome)'} {info.address().toString()} "
                f"RSSI {info.rssi()} dBm"
            )

    def erro(e: QBluetoothDeviceDiscoveryAgent.Error) -> None:
        print(f"Descoberta indisponível: {e.name} — {agente.errorString()}")
        app.quit()

    agente.deviceDiscovered.connect(encontrado)
    agente.errorOccurred.connect(erro)
    agente.finished.connect(
        lambda: (
            print(
                f"Descoberta concluída: {len(agente.discoveredDevices())} dispositivos"
            ),
            app.quit(),
        )
    )
    agente.start(QBluetoothDeviceDiscoveryAgent.DiscoveryMethod.LowEnergyMethod)
    QTimer.singleShot(5000, app.quit)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
