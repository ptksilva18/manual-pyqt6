# runner: ticks=40 xcb
"""QRhiWidget: renderização pela abstração QRhi (OpenGL, Vulkan, Direct3D ou Metal)."""

import math
import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QColor, QRhiCommandBuffer, QRhiDepthStencilClearValue
from PyQt6.QtWidgets import QApplication, QRhiWidget


class Painel(QRhiWidget):
    """Limpa o alvo com uma cor que varia no tempo: o "olá, mundo" do QRhi."""

    def __init__(self) -> None:
        super().__init__()
        self.quadro = 0

    def initialize(self, cb: QRhiCommandBuffer) -> None:  # recursos ligados ao alvo
        rhi = self.rhi()
        print(
            f"API pedida: {self.api().name}; backend: {rhi.backendName()}; "
            f"dispositivo: {bytes(rhi.driverInfo().deviceName).decode()}"
        )
        print(
            f"Alvo de renderização: {self.renderTarget().pixelSize().width()}x"
            f"{self.renderTarget().pixelSize().height()} px"
        )

    def render(self, cb: QRhiCommandBuffer) -> None:
        t = self.quadro / 30.0
        cor = QColor.fromRgbF(0.15 + 0.1 * math.sin(t), 0.35, 0.55 + 0.2 * math.cos(t))
        cb.beginPass(self.renderTarget(), cor, QRhiDepthStencilClearValue(1.0, 0))
        # Aqui entrariam setGraphicsPipeline(), setShaderResources(), setVertexInput()
        # e draw(), com shaders pré-compilados no formato .qsb (ferramenta qsb).
        cb.endPass()
        self.quadro += 1
        self.update()  # pede o próximo quadro (animação contínua)


def main() -> int:
    app = QApplication(sys.argv)
    w = Painel()
    w.setApi(QRhiWidget.Api.OpenGL)  # padrão por plataforma: D3D11 (Win), Metal (macOS)
    w.resize(320, 200)
    w.show()

    def fim() -> None:
        img = w.grabFramebuffer()
        print(
            f"Quadros renderizados: {'> 10' if w.quadro > 10 else w.quadro}; "
            f"pixel central {img.pixelColor(160, 100).name()}"
        )
        app.quit()

    QTimer.singleShot(1000, fim)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
