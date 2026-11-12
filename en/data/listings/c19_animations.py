"""QPropertyAnimation, QVariantAnimation, groups and QTimeLine."""

import sys

from PyQt6.QtCore import (
    QEasingCurve,
    QParallelAnimationGroup,
    QPauseAnimation,
    QPoint,
    QPropertyAnimation,
    QSequentialAnimationGroup,
    QTimeLine,
    QVariantAnimation,
)
from PyQt6.QtWidgets import QApplication, QLabel, QWidget

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QWidget()
    window.resize(400, 200)
    box = QLabel("alarm", window)
    box.move(10, 10)
    window.show()

    move = QPropertyAnimation(box, b"pos")  # animates the Qt property 'pos'
    move.setDuration(300)
    move.setStartValue(QPoint(10, 10))
    move.setEndValue(QPoint(250, 120))
    move.setEasingCurve(QEasingCurve.Type.OutCubic)

    # generic value, applied through a signal
    opacity = QVariantAnimation()
    opacity.setDuration(300)
    opacity.setStartValue(0.0)
    opacity.setEndValue(1.0)
    opacity_values = []
    opacity.valueChanged.connect(opacity_values.append)

    parallel = QParallelAnimationGroup()
    parallel.addAnimation(move)
    parallel.addAnimation(opacity)
    sequence = QSequentialAnimationGroup()
    sequence.addAnimation(parallel)
    sequence.addAnimation(QPauseAnimation(100))
    back = QPropertyAnimation(box, b"pos")
    back.setDuration(200)
    back.setEndValue(QPoint(10, 10))  # start = current value
    sequence.addAnimation(back)

    timeline = QTimeLine(250)  # manual frame control
    timeline.setFrameRange(0, 10)
    frames = []
    timeline.frameChanged.connect(frames.append)

    def on_finished() -> None:
        print("final position:", box.pos().x(), box.pos().y())
        print(
            "final opacity:",
            round(opacity_values[-1], 2),
            "| intermediate updates received?",
            len(opacity_values) > 2,
        )
        print("total duration of the sequence:", sequence.duration(), "ms")
        timeline.start()

    sequence.finished.connect(on_finished)
    timeline.finished.connect(
        lambda: (print("QTimeLine last frame:", frames[-1]), app.quit())
    )
    sequence.start()
    app.exec()

    curve = QEasingCurve(QEasingCurve.Type.OutBounce)
    print("OutBounce at t=0.5:", round(curve.valueForProgress(0.5), 4))
