# runner: ticks=40 xcb
"""QVulkanInstance: instance creation, API version, layers and extensions."""

import sys

from PyQt6.QtCore import QVersionNumber
from PyQt6.QtGui import QVulkanInstance
from PyQt6.QtWidgets import QApplication


def main() -> int:
    app = QApplication(sys.argv)  # noqa: F841
    inst = QVulkanInstance()
    print("Version supported by the loader:", inst.supportedApiVersion().toString())
    inst.setApiVersion(QVersionNumber(1, 1))  # 0 is not accepted by current drivers
    layers = [
        bytes(c.name).decode() for c in inst.supportedLayers()
    ]  # name: QByteArray
    print("Available layers:", layers or "(none)")
    if "VK_LAYER_KHRONOS_validation" in layers:
        inst.setLayers(
            [b"VK_LAYER_KHRONOS_validation"]
        )  # validation during development
    if not inst.create():
        print("Vulkan unavailable on this system; code", inst.errorCode())
        return 0
    ext = sorted(bytes(e.name).decode() for e in inst.supportedExtensions())
    print(
        f"Instance created: {inst.isValid()}; API {inst.apiVersion().toString()}; "
        f"{len(ext)} extensions, e.g. {[e for e in ext if 'surface' in e][:3]}"
    )
    inst.destroy()
    return 0


if __name__ == "__main__":
    sys.exit(main())
