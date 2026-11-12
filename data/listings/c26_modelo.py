# runner: ticks=40
"""Modelo Python (QAbstractListModel) exibido em um ListView QML via roleNames()."""

import os
import sys
from dataclasses import dataclass

from PyQt6.QtCore import QAbstractListModel, QByteArray, QModelIndex, Qt, QTimer, QUrl
from PyQt6.QtQuick import QQuickView
from PyQt6.QtGui import QGuiApplication

AQUI = os.path.dirname(os.path.abspath(__file__))


@dataclass
class Poco:
    nome: str
    lamina: float
    ativo: bool


class ModeloPocos(QAbstractListModel):
    NomeRole = Qt.ItemDataRole.UserRole + 1
    LaminaRole = Qt.ItemDataRole.UserRole + 2
    AtivoRole = Qt.ItemDataRole.UserRole + 3

    def __init__(self, pocos: list[Poco]) -> None:
        super().__init__()
        self._pocos = pocos

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self._pocos)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        p = self._pocos[index.row()]
        return {
            self.NomeRole: p.nome,
            self.LaminaRole: p.lamina,
            self.AtivoRole: p.ativo,
        }.get(role)

    def roleNames(self) -> dict[int, QByteArray]:  # nomes usados no QML
        return {
            self.NomeRole: QByteArray(b"nome"),
            self.LaminaRole: QByteArray(b"lamina"),
            self.AtivoRole: QByteArray(b"ativo"),
        }

    def adicionar(self, poco: Poco) -> None:
        linha = len(self._pocos)
        self.beginInsertRows(QModelIndex(), linha, linha)
        self._pocos.append(poco)
        self.endInsertRows()

    def desativar(self, linha: int) -> None:
        self._pocos[linha].ativo = False
        idx = self.index(linha)
        self.dataChanged.emit(idx, idx, [self.AtivoRole])


def main() -> int:
    app = QGuiApplication(sys.argv)
    modelo = ModeloPocos(
        [Poco("7-ABC-001", 1350.0, True), Poco("7-ABC-002", 1420.0, True)]
    )
    vista = QQuickView()
    vista.rootContext().setContextProperty(
        "modeloPocos", modelo
    )  # antes de setSource()
    vista.setSource(QUrl.fromLocalFile(os.path.join(AQUI, "c26_modelo.qml")))
    vista.show()
    lista = vista.rootObject()
    print("Itens no ListView:", lista.property("count"))
    modelo.adicionar(Poco("7-ABC-003", 1980.0, True))
    modelo.desativar(0)
    print("Após inserir e desativar:", lista.property("count"), "itens")

    def textos() -> None:
        conteudo = lista.property("contentItem")
        delegados = [c for c in conteudo.childItems() if c.property("nome")]
        for d in sorted(delegados, key=lambda d: d.property("y")):
            print(
                "  delegate:",
                d.property("nome"),
                d.property("lamina"),
                d.property("ativo"),
            )
        app.quit()

    QTimer.singleShot(300, textos)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
