# runner: ticks=40 xcb
"""Qt 3D (deprecated since Qt 6.8): entities, components and a Qt3DWindow."""

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
    window = Qt3DWindow()  # QWindow; in Widgets: QWidget.createWindowContainer(window)
    window.defaultFrameGraph().setClearColor(QColor("#1E2F40"))
    root = QEntity()
    box = QEntity(
        root
    )  # entity = set of components (mesh, material, transform)
    mesh = QCuboidMesh()
    mesh.setXExtent(2.0)
    material = QPhongMaterial(root)
    material.setDiffuse(QColor("#C55A11"))
    transform = QTransform()
    transform.setRotation(QQuaternion.fromEulerAngles(20.0, 30.0, 0.0))
    for comp in (mesh, material, transform):
        box.addComponent(comp)
    camera = window.camera()
    camera.lens().setPerspectiveProjection(45.0, 16 / 9, 0.1, 100.0)
    camera.setPosition(QVector3D(0.0, 0.0, 6.0))
    camera.setViewCenter(QVector3D(0.0, 0.0, 0.0))
    controller = QOrbitCameraController(root)
    controller.setCamera(camera)
    window.setRootEntity(root)
    container = QWidget.createWindowContainer(window)
    container.resize(480, 270)
    container.show()
    components = [type(c).__name__ for c in box.components()]
    print("Components of the entity:", components)
    print("Children of the root:", [type(f).__name__ for f in root.childNodes()])
    QTimer.singleShot(800, app.quit)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
