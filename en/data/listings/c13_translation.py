"""Internationalization: tr(), the application's QTranslator and Qt's own translations."""

import sys
from pathlib import Path

from PyQt6.QtCore import QCoreApplication, QLibraryInfo, QLocale, QTranslator
from PyQt6.QtWidgets import QApplication, QDialogButtonBox, QLabel, QWidget

HERE = Path(__file__).resolve().parent


class Panel(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.title = QLabel()
        self.retranslate()

    def retranslate(self) -> None:
        self.setWindowTitle(self.tr("Pipe check"))
        self.title.setText(self.tr("Test pressure: %1 bar").replace("%1", "345"))


def message_outside_a_class() -> str:
    return QCoreApplication.translate("Report", "Report generated")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    p = Panel()
    print(
        "before:", p.windowTitle(), "|", p.title.text(), "|", message_outside_a_class()
    )

    app_tr = QTranslator()  # the application's translations (its own .qm)
    print("app loaded?", app_tr.load(str(HERE / "c13_engcalc_pt_BR.qm")))
    qt_tr = QTranslator()  # translations of Qt's internal texts
    qt_dir = QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)
    print("qtbase loaded?", qt_tr.load(QLocale("pt_BR"), "qtbase", "_", qt_dir))
    app.installTranslator(app_tr)
    app.installTranslator(qt_tr)

    p.retranslate()  # the texts must be set again
    print(
        "after:", p.windowTitle(), "|", p.title.text(), "|", message_outside_a_class()
    )
    box = QDialogButtonBox(
        QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
    )
    print("Qt's buttons:", [b.text() for b in box.buttons()])
