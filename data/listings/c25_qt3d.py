# runner: ticks=40 xcb
"""Qt 3D (obsoleto desde Qt 6.8): entidades, componentes e janela Qt3DWindow."""

import sys

from PyQt6.Qt3DCore import QEntity, QTransform
from PyQt6.Qt3DExtras import (
    QCuboidMesh,
    QOrbitCameraController,
    QPhongMaterial,
    Qt3DWindow,
)
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QColor, QQuaternion, QVector3D
from PyQt6.QtWidgets import QApplication, QWidget


def main() -> int:
    app = QApplication(sys.argv)
    janela = Qt3DWindow()  # QWindow; em Widgets: QWidget.createWindowContainer(janela)
    janela.defaultFrameGraph().setClearColor(QColor("#1E2F40"))
    raiz = QEntity()
    caixa = QEntity(
        raiz
    )  # entidade = conjunto de componentes (malha, material, transformação)
    malha = QCuboidMesh()
    malha.setXExtent(2.0)
    material = QPhongMaterial(raiz)
    material.setDiffuse(QColor("#C55A11"))
    transf = QTransform()
    transf.setRotation(QQuaternion.fromEulerAngles(20.0, 30.0, 0.0))
    for comp in (malha, material, transf):
        caixa.addComponent(comp)
    camera = janela.camera()
    camera.lens().setPerspectiveProjection(45.0, 16 / 9, 0.1, 100.0)
    camera.setPosition(QVector3D(0.0, 0.0, 6.0))
    camera.setViewCenter(QVector3D(0.0, 0.0, 0.0))
    controle = QOrbitCameraController(raiz)
    controle.setCamera(camera)
    janela.setRootEntity(raiz)
    recipiente = QWidget.createWindowContainer(janela)
    recipiente.resize(480, 270)
    recipiente.show()
    componentes = [type(c).__name__ for c in caixa.components()]
    print("Componentes da entidade:", componentes)
    print("Filhos da raiz:", [type(f).__name__ for f in raiz.childNodes()])
    QTimer.singleShot(800, app.quit)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
