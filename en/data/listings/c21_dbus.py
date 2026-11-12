# runner: ticks=100 dbus
"""D-Bus (Linux): service exported by one process and called by another.

Usage: python c21_dbus.py           (service; starts the client automatically)
       python c21_dbus.py --client  (client)
"""

import sys

from PyQt6.QtCore import QCoreApplication, QObject, QProcess, pyqtClassInfo, pyqtSlot
from PyQt6.QtDBus import QDBusConnection, QDBusInterface, QDBusMessage, QDBusReply

SERVICE = "org.example.Tests"
PATH = "/tests"
INTERFACE = "org.example.Tests.Control"


@pyqtClassInfo("D-Bus Interface", INTERFACE)
class Control(QObject):
    @pyqtSlot(str, result=str)
    def status(self, test: str) -> str:
        return f"{test}: in progress (stage 3/5)"

    @pyqtSlot(str, float, result=bool)
    def record(self, tag: str, value: float) -> bool:
        print(f"[service] record({tag!r}, {value})")
        return value >= 0.0


def service(app: QCoreApplication) -> int:
    bus = QDBusConnection.sessionBus()
    if not bus.isConnected():
        print("No D-Bus session bus:", bus.lastError().message())
        return 1
    control = Control()
    ok_obj = bus.registerObject(
        PATH, control, QDBusConnection.RegisterOption.ExportAllSlots
    )
    ok_srv = bus.registerService(SERVICE)
    print(f"[service] object registered: {ok_obj}; name {SERVICE} registered: {ok_srv}")
    proc = QProcess()
    proc.setProcessChannelMode(QProcess.ProcessChannelMode.ForwardedChannels)
    proc.finished.connect(lambda code, _st: app.exit(code))
    proc.start(sys.executable, [__file__, "--client"])
    return app.exec()


def client() -> int:
    bus = QDBusConnection.sessionBus()
    names = bus.interface().registeredServiceNames().value()
    print(f"[client]  service visible on the bus: {SERVICE in names}")
    iface = QDBusInterface(SERVICE, PATH, INTERFACE, bus)
    reply = QDBusReply(iface.call("status", "TH-01"))
    print(
        f"[client]  status -> valid={reply.isValid()}, value={reply.value()!r}"
    )
    msg = iface.call("record", "PT-101", 345.0)
    print(f"[client]  record -> {msg.type().name}, arguments={msg.arguments()}")
    error = iface.call("nonexistent_method")
    print(
        f"[client]  nonexistent method -> "
        f"{error.type() == QDBusMessage.MessageType.ErrorMessage}"
        f": {error.errorName()}"
    )
    return 0


if __name__ == "__main__":
    application = QCoreApplication(sys.argv)
    sys.exit(client() if "--client" in sys.argv else service(application))
