"""QPropertyAnimation, QVariantAnimation, grupos e QTimeLine."""

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
    janela = QWidget()
    janela.resize(400, 200)
    caixa = QLabel("alarme", janela)
    caixa.move(10, 10)
    janela.show()

    mover = QPropertyAnimation(caixa, b"pos")  # anima a propriedade Qt 'pos'
    mover.setDuration(300)
    mover.setStartValue(QPoint(10, 10))
    mover.setEndValue(QPoint(250, 120))
    mover.setEasingCurve(QEasingCurve.Type.OutCubic)

    # valor genérico, aplicado por sinal
    opacidade = QVariantAnimation()
    opacidade.setDuration(300)
    opacidade.setStartValue(0.0)
    opacidade.setEndValue(1.0)
    valores_opac = []
    opacidade.valueChanged.connect(valores_opac.append)

    paralelo = QParallelAnimationGroup()
    paralelo.addAnimation(mover)
    paralelo.addAnimation(opacidade)
    sequencia = QSequentialAnimationGroup()
    sequencia.addAnimation(paralelo)
    sequencia.addAnimation(QPauseAnimation(100))
    volta = QPropertyAnimation(caixa, b"pos")
    volta.setDuration(200)
    volta.setEndValue(QPoint(10, 10))  # início = valor atual
    sequencia.addAnimation(volta)

    linha = QTimeLine(250)  # controle manual de quadros
    linha.setFrameRange(0, 10)
    quadros = []
    linha.frameChanged.connect(quadros.append)

    def ao_terminar() -> None:
        print("posição final:", caixa.pos().x(), caixa.pos().y())
        print(
            "opacidade final:",
            round(valores_opac[-1], 2),
            "| atualizações intermediárias recebidas?",
            len(valores_opac) > 2,
        )
        print("duração total da sequência:", sequencia.duration(), "ms")
        linha.start()

    sequencia.finished.connect(ao_terminar)
    linha.finished.connect(
        lambda: (print("QTimeLine último quadro:", quadros[-1]), app.quit())
    )
    sequencia.start()
    app.exec()

    curva = QEasingCurve(QEasingCurve.Type.OutBounce)
    print("OutBounce em t=0.5:", round(curva.valueForProgress(0.5), 4))
