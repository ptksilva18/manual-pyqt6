"""Main window: list of tests, readings, chart, result and actions."""

from pathlib import Path

import pyqtgraph as pg
from PyQt6.QtCore import QSettings, Qt
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtWidgets import (
    QDockWidget,
    QFileDialog,
    QInputDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QSplitter,
    QTableView,
    QTabWidget,
)

from . import __version__
from .csv_import import read_csv
from .domain import Criterion, DataError, Result
from .models import ReadingsModel, TestListModel
from .report import make_pdf
from .repository import Repository
from .services import AnalysisService


class MainWindow(QMainWindow):
    def __init__(self, repo: Repository, service: AnalysisService) -> None:
        super().__init__()
        self.repo, self.service = repo, service
        self.result: Result | None = None
        self.setWindowTitle(f"Leak Test Monitor {__version__}")
        self.tests_model, self.readings_model = TestListModel(), ReadingsModel()
        self.tests_table = QTableView()
        self.tests_table.setModel(self.tests_model)
        self.tests_table.setSelectionBehavior(
            QTableView.SelectionBehavior.SelectRows
        )
        self.tests_table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.tests_table.horizontalHeader().setStretchLastSection(True)
        self.readings_table = QTableView()
        self.readings_table.setModel(self.readings_model)
        self.chart = pg.PlotWidget(background="w")
        self.chart.setLabel("bottom", "Time (min)")
        self.chart.setLabel("left", "Pressure (bar)")
        self.chart.showGrid(x=True, y=True, alpha=0.3)
        self.curve = self.chart.plot(
            pen=pg.mkPen("#2E75B6", width=2),
            symbol="o",
            symbolSize=5,
            symbolBrush="#2E75B6",
        )
        tabs = QTabWidget()
        tabs.addTab(self.chart, "Chart")
        tabs.addTab(self.readings_table, "Readings")
        splitter = QSplitter()
        splitter.addWidget(self.tests_table)
        splitter.addWidget(tabs)
        splitter.setStretchFactor(1, 3)
        self.setCentralWidget(splitter)
        self.panel = QLabel("Select a test.")
        self.panel.setObjectName("resultPanel")
        self.panel.setWordWrap(True)
        self.panel.setMargin(8)
        dock = QDockWidget("Result", self)
        dock.setObjectName("resultDock")
        dock.setWidget(self.panel)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, dock)
        self._create_actions()
        self.service.completed.connect(self._on_completed)
        self.service.failed.connect(self._on_failed)
        self.tests_table.selectionModel().currentRowChanged.connect(
            self._on_selected
        )
        self.statusBar().showMessage("Ready")
        self.reload()

    def _create_actions(self) -> None:
        toolbar = self.addToolBar("Test")
        toolbar.setObjectName("testToolbar")
        menu = self.menuBar().addMenu("&Test")
        defs = [
            (
                "act_new",
                "&New test...",
                QKeySequence.StandardKey.New,
                self.new_test,
            ),
            (
                "act_import",
                "&Import CSV...",
                QKeySequence("Ctrl+I"),
                self.import_csv,
            ),
            ("act_analyze", "&Analyze", QKeySequence("F5"), self.analyze),
            (
                "act_report",
                "PDF &report...",
                QKeySequence("Ctrl+P"),
                self.report,
            ),
        ]
        for name, text, shortcut, slot in defs:
            action = QAction(text, self)
            action.setShortcut(shortcut)
            action.triggered.connect(slot)
            setattr(self, name, action)
            menu.addAction(action)
            toolbar.addAction(action)
        self._update_actions()

    def _update_actions(self) -> None:
        has_test = self.current_test() is not None
        has_readings = self.readings_model.rowCount() > 0
        self.act_import.setEnabled(has_test)
        self.act_analyze.setEnabled(has_test and has_readings)
        self.act_report.setEnabled(self.result is not None)

    # ------------------------------------------------------------- state
    def current_test(self) -> int | None:
        idx = self.tests_table.selectionModel().currentIndex()
        return self.tests_model.test_id(idx.row()) if idx.isValid() else None

    def reload(self, select: int | None = None) -> None:
        self.tests_model.reload(self.repo.list_tests())
        for row in range(self.tests_model.rowCount()):
            if self.tests_model.test_id(row) == select:
                self.tests_table.selectRow(row)

    def _on_selected(self, current, _previous) -> None:
        self.result = None
        tid = self.current_test()
        readings = self.repo.readings(tid) if tid is not None else []
        self.readings_model.set_readings(readings)
        self.curve.setData([rd.t_min for rd in readings], [rd.p_bar for rd in readings])
        self.panel.setText(
            "Readings loaded." if readings else "Test without readings."
        )
        self._update_actions()

    # ------------------------------------------------------------- actions
    def new_test(
        self,
        code: str | None = None,
        description: str = "",
        criterion: Criterion | None = None,
    ) -> int | None:
        if code is None:
            code, ok = QInputDialog.getText(self, "New test", "Test code:")
            if not ok or not code.strip():
                return None
        try:
            tid = self.repo.create_test(
                code.strip(), description, criterion or Criterion()
            )
        except Exception as exc:  # sqlite3.IntegrityError: repeated code
            QMessageBox.warning(self, "New test", f"Could not create it: {exc}")
            return None
        self.reload(select=tid)
        return tid

    def import_csv(self, path: str | None = None) -> bool:
        tid = self.current_test()
        if tid is None:
            return False
        if path is None:
            path, _ = QFileDialog.getOpenFileName(
                self, "Import readings", "", "CSV (*.csv)"
            )
            if not path:
                return False
        try:
            readings = read_csv(path)
        except (OSError, DataError) as exc:
            QMessageBox.critical(self, "Import CSV", str(exc))
            return False
        self.repo.replace_readings(tid, readings)
        self._on_selected(None, None)
        self.statusBar().showMessage(
            f"{len(readings)} readings imported from " f"{Path(path).name}", 5000
        )
        return True

    def analyze(self) -> None:
        tid = self.current_test()
        if tid is None:
            return
        self.act_analyze.setEnabled(False)
        self.statusBar().showMessage("Analyzing...")
        self.service.analyze(
            tid, self.readings_model.readings(), self.repo.criterion(tid)
        )

    def _on_completed(self, tid: int, r: Result) -> None:
        if tid != self.current_test():  # the user switched tests during the analysis
            return
        self.result = r
        color = "#548235" if r.passed else "#C00000"
        text = (
            f"<b style='color:{color}'>{'PASSED' if r.passed else 'FAILED'}</b> — "
            f"drop {r.drop_bar:.3f} bar ({r.drop_pct:.3f} %), "
            f"rate {r.rate_bar_h:.3f} bar/h, hold {r.duration_min:.0f} min"
        )
        if r.reasons:
            text += "<br>" + "; ".join(r.reasons)
        self.panel.setText(text)
        self.statusBar().showMessage("Analysis completed", 5000)
        self._update_actions()

    def _on_failed(self, tid: int, message: str) -> None:
        self.panel.setText(f"<b style='color:#C55A11'>Invalid data:</b> {message}")
        self.statusBar().showMessage("Analysis not performed", 5000)
        self._update_actions()

    def report(self, target: str | None = None) -> Path | None:
        tid = self.current_test()
        if tid is None or self.result is None:
            return None
        idx = self.tests_table.selectionModel().currentIndex()
        code = self.tests_model.index(idx.row(), 0).data()
        description = self.tests_model.index(idx.row(), 1).data()
        if target is None:
            target, _ = QFileDialog.getSaveFileName(
                self, "Save report", f"{code}.pdf", "PDF (*.pdf)"
            )
            if not target:
                return None
        return make_pdf(
            target,
            code,
            description,
            self.readings_model.readings(),
            self.repo.criterion(tid),
            self.result,
        )

    # ------------------------------------------------------------- window state
    def restore(self, cfg: QSettings) -> None:
        geometry, state = cfg.value("window/geometry"), cfg.value("window/state")
        if geometry is not None:
            self.restoreGeometry(geometry)
        if state is not None:
            self.restoreState(state)

    def closeEvent(self, event) -> None:
        cfg = QSettings()
        cfg.setValue("window/geometry", self.saveGeometry())
        cfg.setValue("window/state", self.saveState())
        self.service.wait()
        super().closeEvent(event)
