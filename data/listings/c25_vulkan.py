# runner: ticks=40 xcb
"""QVulkanInstance: criação da instância, versão da API, camadas e extensões."""

import sys

from PyQt6.QtCore import QVersionNumber
from PyQt6.QtGui import QVulkanInstance
from PyQt6.QtWidgets import QApplication


def main() -> int:
    app = QApplication(sys.argv)  # noqa: F841
    inst = QVulkanInstance()
    print("Versão suportada pelo carregador:", inst.supportedApiVersion().toString())
    inst.setApiVersion(QVersionNumber(1, 1))  # 0 não é aceito pelos drivers atuais
    camadas = [
        bytes(c.name).decode() for c in inst.supportedLayers()
    ]  # name: QByteArray
    print("Camadas disponíveis:", camadas or "(nenhuma)")
    if "VK_LAYER_KHRONOS_validation" in camadas:
        inst.setLayers(
            [b"VK_LAYER_KHRONOS_validation"]
        )  # validação durante o desenvolvimento
    if not inst.create():
        print("Vulkan indisponível neste sistema; código", inst.errorCode())
        return 0
    ext = sorted(bytes(e.name).decode() for e in inst.supportedExtensions())
    print(
        f"Instância criada: {inst.isValid()}; API {inst.apiVersion().toString()}; "
        f"{len(ext)} extensões, p.ex. {[e for e in ext if 'surface' in e][:3]}"
    )
    inst.destroy()
    return 0


if __name__ == "__main__":
    sys.exit(main())
