# runner: ticks=60
"""Bluetooth LE and NFC: device discovery with handling of missing
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
    adapters = QBluetoothLocalDevice.allDevices()
    print(f"Local Bluetooth adapters: {len(adapters)}")
    print(f"NFC supported on this platform: {QNearFieldManager().isSupported()}")
    agent = QBluetoothDeviceDiscoveryAgent()
    agent.setLowEnergyDiscoveryTimeout(3000)  # ms; 0 = until stop() is called
    print(
        "Supported methods:",
        QBluetoothDeviceDiscoveryAgent.supportedDiscoveryMethods(),
    )

    def found(info: QBluetoothDeviceInfo) -> None:
        if (
            info.coreConfigurations()
            & QBluetoothDeviceInfo.CoreConfiguration.LowEnergyCoreConfiguration
        ):
            print(
                f"BLE: {info.name() or '(unnamed)'} {info.address().toString()} "
                f"RSSI {info.rssi()} dBm"
            )

    def error(e: QBluetoothDeviceDiscoveryAgent.Error) -> None:
        print(f"Discovery unavailable: {e.name} — {agent.errorString()}")
        app.quit()

    agent.deviceDiscovered.connect(found)
    agent.errorOccurred.connect(error)
    agent.finished.connect(
        lambda: (
            print(
                f"Discovery finished: {len(agent.discoveredDevices())} devices"
            ),
            app.quit(),
        )
    )
    agent.start(QBluetoothDeviceDiscoveryAgent.DiscoveryMethod.LowEnergyMethod)
    QTimer.singleShot(5000, app.quit)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
