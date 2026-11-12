# runner: ticks=40
"""Python model (QAbstractListModel) displayed in a QML ListView through roleNames()."""

import os
import sys
from dataclasses import dataclass

from PyQt6.QtCore import QAbstractListModel, QByteArray, QModelIndex, Qt, QTimer, QUrl
from PyQt6.QtQuick import QQuickView
from PyQt6.QtGui import QGuiApplication

HERE = os.path.dirname(os.path.abspath(__file__))


@dataclass
class Well:
    name: str
    water_depth: float
    active: bool


class WellModel(QAbstractListModel):
    NameRole = Qt.ItemDataRole.UserRole + 1
    WaterDepthRole = Qt.ItemDataRole.UserRole + 2
    ActiveRole = Qt.ItemDataRole.UserRole + 3

    def __init__(self, wells: list[Well]) -> None:
        super().__init__()
        self._wells = wells

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self._wells)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        w = self._wells[index.row()]
        return {
            self.NameRole: w.name,
            self.WaterDepthRole: w.water_depth,
            self.ActiveRole: w.active,
        }.get(role)

    def roleNames(self) -> dict[int, QByteArray]:  # names used in QML
        return {
            self.NameRole: QByteArray(b"name"),
            self.WaterDepthRole: QByteArray(b"waterDepth"),
            self.ActiveRole: QByteArray(b"active"),
        }

    def add(self, well: Well) -> None:
        row = len(self._wells)
        self.beginInsertRows(QModelIndex(), row, row)
        self._wells.append(well)
        self.endInsertRows()

    def deactivate(self, row: int) -> None:
        self._wells[row].active = False
        idx = self.index(row)
        self.dataChanged.emit(idx, idx, [self.ActiveRole])


def main() -> int:
    app = QGuiApplication(sys.argv)
    model = WellModel(
        [Well("7-ABC-001", 1350.0, True), Well("7-ABC-002", 1420.0, True)]
    )
    view = QQuickView()
    view.rootContext().setContextProperty(
        "wellModel", model
    )  # before setSource()
    view.setSource(QUrl.fromLocalFile(os.path.join(HERE, "c26_model.qml")))
    view.show()
    list_view = view.rootObject()
    print("Items in the ListView:", list_view.property("count"))
    model.add(Well("7-ABC-003", 1980.0, True))
    model.deactivate(0)
    print("After inserting and deactivating:", list_view.property("count"), "items")

    def texts() -> None:
        content = list_view.property("contentItem")
        delegates = [c for c in content.childItems() if c.property("name")]
        for d in sorted(delegates, key=lambda d: d.property("y")):
            print(
                "  delegate:",
                d.property("name"),
                d.property("waterDepth"),
                d.property("active"),
            )
        app.quit()

    QTimer.singleShot(300, texts)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
