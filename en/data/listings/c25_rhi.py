# runner: ticks=40 xcb
"""QRhiWidget: rendering via the QRhi abstraction (OpenGL, Vulkan, Direct3D or Metal)."""

import math
import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QColor, QRhiCommandBuffer, QRhiDepthStencilClearValue
from PyQt6.QtWidgets import QApplication, QRhiWidget


class Panel(QRhiWidget):
    """Clears the target with a color that varies over time: the QRhi "hello, world"."""

    def __init__(self) -> None:
        super().__init__()
        self.frame = 0

    def initialize(self, cb: QRhiCommandBuffer) -> None:  # resources tied to the target
        rhi = self.rhi()
        print(
            f"Requested API: {self.api().name}; backend: {rhi.backendName()}; "
            f"device: {bytes(rhi.driverInfo().deviceName).decode()}"
        )
        print(
            f"Render target: {self.renderTarget().pixelSize().width()}x"
            f"{self.renderTarget().pixelSize().height()} px"
        )

    def render(self, cb: QRhiCommandBuffer) -> None:
        t = self.frame / 30.0
        color = QColor.fromRgbF(0.15 + 0.1 * math.sin(t), 0.35, 0.55 + 0.2 * math.cos(t))
        cb.beginPass(self.renderTarget(), color, QRhiDepthStencilClearValue(1.0, 0))
        # Here would go setGraphicsPipeline(), setShaderResources(), setVertexInput()
        # and draw(), with shaders precompiled to the .qsb format (qsb tool).
        cb.endPass()
        self.frame += 1
        self.update()  # requests the next frame (continuous animation)


def main() -> int:
    app = QApplication(sys.argv)
    w = Panel()
    w.setApi(QRhiWidget.Api.OpenGL)  # per-platform default: D3D11 (Win), Metal (macOS)
    w.resize(320, 200)
    w.show()

    def finish() -> None:
        img = w.grabFramebuffer()
        print(
            f"Frames rendered: {'> 10' if w.frame > 10 else w.frame}; "
            f"center pixel {img.pixelColor(160, 100).name()}"
        )
        app.quit()

    QTimer.singleShot(1000, finish)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
