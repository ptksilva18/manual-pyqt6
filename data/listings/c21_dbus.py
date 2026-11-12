# runner: ticks=100 dbus
"""D-Bus (Linux): serviço exportado por um processo e chamado por outro.

Uso: python c21_dbus.py            (serviço; inicia o cliente automaticamente)
     python c21_dbus.py --cliente  (cliente)
"""

import sys

from PyQt6.QtCore import QCoreApplication, QObject, QProcess, pyqtClassInfo, pyqtSlot
from PyQt6.QtDBus import QDBusConnection, QDBusInterface, QDBusMessage, QDBusReply

SERVICO = "br.manual.Ensaios"
CAMINHO = "/ensaios"
INTERFACE = "br.manual.Ensaios.Controle"


@pyqtClassInfo("D-Bus Interface", INTERFACE)
class Controle(QObject):
    @pyqtSlot(str, result=str)
    def status(self, ensaio: str) -> str:
        return f"{ensaio}: em andamento (estágio 3/5)"

    @pyqtSlot(str, float, result=bool)
    def registrar(self, tag: str, valor: float) -> bool:
        print(f"[serviço] registrar({tag!r}, {valor})")
        return valor >= 0.0


def servico(app: QCoreApplication) -> int:
    barramento = QDBusConnection.sessionBus()
    if not barramento.isConnected():
        print("Sem barramento de sessão D-Bus:", barramento.lastError().message())
        return 1
    controle = Controle()
    ok_obj = barramento.registerObject(
        CAMINHO, controle, QDBusConnection.RegisterOption.ExportAllSlots
    )
    ok_srv = barramento.registerService(SERVICO)
    print(f"[serviço] objeto registrado: {ok_obj}; nome {SERVICO} registrado: {ok_srv}")
    proc = QProcess()
    proc.setProcessChannelMode(QProcess.ProcessChannelMode.ForwardedChannels)
    proc.finished.connect(lambda codigo, _st: app.exit(codigo))
    proc.start(sys.executable, [__file__, "--cliente"])
    return app.exec()


def cliente() -> int:
    barramento = QDBusConnection.sessionBus()
    nomes = barramento.interface().registeredServiceNames().value()
    print(f"[cliente] serviço visível no barramento: {SERVICO in nomes}")
    iface = QDBusInterface(SERVICO, CAMINHO, INTERFACE, barramento)
    resposta = QDBusReply(iface.call("status", "TH-01"))
    print(
        f"[cliente] status -> válido={resposta.isValid()}, valor={resposta.value()!r}"
    )
    msg = iface.call("registrar", "PT-101", 345.0)
    print(f"[cliente] registrar -> {msg.type().name}, argumentos={msg.arguments()}")
    erro = iface.call("metodo_inexistente")
    print(
        f"[cliente] método inexistente -> "
        f"{erro.type() == QDBusMessage.MessageType.ErrorMessage}"
        f": {erro.errorName()}"
    )
    return 0


if __name__ == "__main__":
    aplicacao = QCoreApplication(sys.argv)
    sys.exit(cliente() if "--cliente" in sys.argv else servico(aplicacao))
