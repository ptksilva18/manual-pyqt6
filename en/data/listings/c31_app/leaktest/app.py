"""Entry point: python -m leaktest [--selftest FOLDER]."""

import sys
from pathlib import Path

from PyQt6.QtCore import QSettings, QStandardPaths, QTimer
from PyQt6.QtWidgets import QApplication

from . import __version__
from .domain import Criterion
from .repository import Repository
from .services import AnalysisService
from .window import MainWindow


def data_folder() -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / "data"
    return Path(__file__).resolve().parent.parent / "data"


def selftest(window: MainWindow, output: Path, app: QApplication) -> None:
    """Full non-interactive script: create, import, analyze (in a thread) and generate
    the PDF."""
    criterion = Criterion(
        duration_min=60.0, max_drop_pct=0.5, max_rate_bar_h=1.0, temp_coef_bar_c=0.25
    )  # thermal compensation of the trapped fluid
    tid = window.new_test(
        "TH-01", "Leak test of the service line", criterion
    )
    print(
        f"test created: id={tid}; tests in the list: {window.tests_model.rowCount()}"
    )
    window.import_csv(str(data_folder() / "TH-01.csv"))
    print(
        f"readings: {window.readings_model.rowCount()}; "
        f"Analyze action enabled: {window.act_analyze.isEnabled()}"
    )

    def completed(_tid, r) -> None:
        print(
            f"result: passed={r.passed}, drop={r.drop_bar:.3f} bar "
            f"({r.drop_pct:.3f} %), rate={r.rate_bar_h:.3f} bar/h, "
            f"p_final_corrected={r.p_final_corrected:.3f} bar"
        )
        pdf = window.report(str(output / "TH-01.pdf"))
        print(
            f"report: {pdf.name}, {pdf.stat().st_size} bytes, "
            f"header {pdf.read_bytes()[:5]!r}"
        )
        print(
            "panel:", window.panel.text().split(" — ")[0].split(">")[1].split("<")[0]
        )
        if "--capture" in sys.argv:  # image of the window for the documentation
            window.grab().save(sys.argv[sys.argv.index("--capture") + 1])
        QTimer.singleShot(0, window.close)

    window.service.completed.connect(completed)
    window.act_analyze.trigger()


def main(argv: list[str]) -> int:
    app = QApplication(argv)
    app.setOrganizationName("PyQt6Manual")
    app.setApplicationName("LeakTestMonitor")
    app.setApplicationVersion(__version__)
    if "--selftest" in argv:
        output = Path(argv[argv.index("--selftest") + 1])
        QSettings.setDefaultFormat(QSettings.Format.IniFormat)
        QSettings.setPath(
            QSettings.Format.IniFormat, QSettings.Scope.UserScope, str(output)
        )
        database = output / "leaktests.sqlite"
    else:
        data = Path(
            QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.AppDataLocation
            )
        )
        data.mkdir(parents=True, exist_ok=True)
        database = data / "leaktests.sqlite"
    repo = Repository(database)
    window = MainWindow(repo, AnalysisService())
    window.restore(QSettings())
    window.resize(1000, 640)
    window.show()
    if "--selftest" in argv:
        QTimer.singleShot(0, lambda: selftest(window, output, app))
    code = app.exec()
    repo.close()
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv))
