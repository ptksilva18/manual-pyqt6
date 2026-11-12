"""QWizard with registered fields (registerField) and chained pages."""
import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QApplication, QComboBox, QFormLayout, QLabel, QLineEdit, QVBoxLayout, QWizard,
    QWizardPage,
)


class ProjectPage(QWizardPage):
    def __init__(self) -> None:
        super().__init__()
        self.setTitle("Project")
        self.setSubTitle("Identify the project.")
        name = QLineEdit()
        form = QFormLayout(self)
        form.addRow("Name*:", name)
        self.registerField("name*", name)          # '*' = mandatory: enables "Next"


class UnitsPage(QWizardPage):
    def __init__(self) -> None:
        super().__init__()
        self.setTitle("Units")
        combo = QComboBox()
        combo.addItems(["SI", "Imperial"])
        form = QFormLayout(self)
        form.addRow("System:", combo)
        self.registerField("units", combo, "currentText")


class SummaryPage(QWizardPage):
    def __init__(self) -> None:
        super().__init__()
        self.setTitle("Summary")
        self.text = QLabel()
        QVBoxLayout(self).addWidget(self.text)

    def initializePage(self) -> None:              # called when entering the page
        self.text.setText(f"Project: {self.field('name')}\n"
                          f"Units: {self.field('units')}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    wiz = QWizard()
    wiz.setWindowTitle("New project")
    for page in (ProjectPage(), UnitsPage(), SummaryPage()):
        wiz.addPage(page)

    def script() -> None:
        next_button = wiz.button(QWizard.WizardButton.NextButton)
        print("Next enabled without a name?", next_button.isEnabled())
        wiz.page(0).findChild(QLineEdit).setText("Riser check")
        print("Next enabled with a name?", next_button.isEnabled())
        wiz.next()
        wiz.page(1).findChild(QComboBox).setCurrentText("Imperial")
        wiz.next()
        print(wiz.currentPage().text.text())
        wiz.accept()

    QTimer.singleShot(0, script)
    print("completed?", wiz.exec() == 1)
