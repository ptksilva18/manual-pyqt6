"""QStateMachine: states, signal transitions, assigned properties and history."""

import sys

from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from PyQt6.QtStateMachine import QFinalState, QHistoryState, QState, QStateMachine
from PyQt6.QtWidgets import QApplication, QLabel


class Panel(QObject):
    start = pyqtSignal()
    pause = pyqtSignal()
    resume = pyqtSignal()
    complete = pyqtSignal()
    advance = pyqtSignal()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui, label = Panel(), QLabel()
    m = QStateMachine()

    idle = QState(m)
    # compound state (with substates)
    test = QState(m)
    pressurizing = QState(test)
    stabilizing = QState(test)
    test.setInitialState(pressurizing)
    history = QHistoryState(test)  # remembers the active substate
    paused = QState(m)
    done = QFinalState(m)

    idle.assignProperty(label, "text", "Idle")  # properties per state
    pressurizing.assignProperty(label, "text", "Pressurizing")
    stabilizing.assignProperty(label, "text", "Stabilizing")
    paused.assignProperty(label, "text", "Paused")

    idle.addTransition(ui.start, test)
    pressurizing.addTransition(ui.advance, stabilizing)
    test.addTransition(ui.pause, paused)
    paused.addTransition(ui.resume, history)  # back to the previous substate
    test.addTransition(ui.complete, done)
    m.setInitialState(idle)

    for name, state in (
        ("idle", idle),
        ("pressurizing", pressurizing),
        ("stabilizing", stabilizing),
        ("paused", paused),
    ):
        state.entered.connect(
            lambda n=name: print("entered:", n, "| label:", label.text())
        )
    m.finished.connect(lambda: (print("machine finished"), app.quit()))

    script = [ui.start, ui.advance, ui.pause, ui.resume, ui.complete]
    for i, signal in enumerate(script, start=1):
        QTimer.singleShot(50 * i, signal.emit)
    # asynchronous: runs in the event loop
    m.start()
    app.exec()
