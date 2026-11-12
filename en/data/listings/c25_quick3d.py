# runner: ticks=40 xcb
"""Qt Quick 3D controlled by Python: QML scene in a QQuickWidget, properties, 3D nodes."""

import os
import sys

from PyQt6.QtCore import QTimer, QUrl
from PyQt6.QtQuick3D import QQuick3DObject
from PyQt6.QtQuickWidgets import QQuickWidget
from PyQt6.QtWidgets import QApplication

HERE = os.path.dirname(os.path.abspath(__file__))


def main() -> int:
    app = QApplication(sys.argv)
    view = QQuickWidget()
    view.setResizeMode(QQuickWidget.ResizeMode.SizeRootObjectToView)
    view.setSource(QUrl.fromLocalFile(os.path.join(HERE, "c25_quick3d.qml")))
    if view.status() != QQuickWidget.Status.Ready:
        print([e.toString() for e in view.errors()])
        return 1
    root = view.rootObject()  # the View3D (a QQuickItem)
    lid = root.findChild(QQuick3DObject, "lid")
    print(
        f"Root: {root.metaObject().className()}; node 'lid': "
        f"{lid.metaObject().className()}"
    )
    print("Lid position:", lid.property("position"))
    view.resize(520, 360)
    view.show()
    steps = [0]

    def animate() -> None:
        steps[0] += 1
        root.setProperty(
            "lidAngle", 10.0 * steps[0]
        )  # the QML binding updates the scene

    timer = QTimer()
    timer.timeout.connect(animate)
    timer.start(40)

    def finish() -> None:
        timer.stop()
        img = view.grabFramebuffer()
        print(
            f"lidAngle = {root.property('lidAngle'):.0f}°; "
            f"capture {img.width()}x{img.height()}, center "
            f"{img.pixelColor(260, 200).name()}"
        )
        if os.environ.get("CAPTURE"):
            img.save(os.environ["CAPTURE"])
        app.quit()

    QTimer.singleShot(1200, finish)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
