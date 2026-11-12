"""Background analysis service (QThreadPool) with the result delivered by signal."""

from PyQt6.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal

from .domain import Criterion, DataError, Reading, analyze


class _Signals(QObject):
    completed = pyqtSignal(int, object)  # test_id, Result
    failed = pyqtSignal(int, str)


class _Task(QRunnable):
    def __init__(
        self,
        test_id: int,
        readings: list[Reading],
        criterion: Criterion,
        signals: _Signals,
    ) -> None:
        super().__init__()
        self.args = (test_id, readings, criterion)
        self.signals = signals

    def run(self) -> None:  # runs in a pool thread: no widgets here
        test_id, readings, criterion = self.args
        try:
            self.signals.completed.emit(test_id, analyze(readings, criterion))
        except DataError as exc:
            self.signals.failed.emit(test_id, str(exc))


class AnalysisService(QObject):
    completed = pyqtSignal(int, object)
    failed = pyqtSignal(int, str)

    def __init__(self) -> None:
        super().__init__()
        self.pool = QThreadPool()
        self.pool.setMaxThreadCount(2)
        self._signals = (
            _Signals()
        )  # lives in the GUI thread: the emissions arrive queued
        self._signals.completed.connect(self.completed)
        self._signals.failed.connect(self.failed)

    def analyze(
        self, test_id: int, readings: list[Reading], criterion: Criterion
    ) -> None:
        self.pool.start(_Task(test_id, list(readings), criterion, self._signals))

    def wait(self, ms: int = 5000) -> bool:
        return self.pool.waitForDone(ms)
