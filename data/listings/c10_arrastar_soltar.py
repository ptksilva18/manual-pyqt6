"""Arrastar e soltar: alvo que aceita apenas arquivos .csv."""
import sys

from PyQt6.QtCore import QMimeData, QPointF, Qt, QUrl
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
from PyQt6.QtWidgets import QApplication, QLabel


class AlvoCSV(QLabel):
    def __init__(self) -> None:
        super().__init__("Solte um arquivo .csv aqui")
        self.setAcceptDrops(True)                         # habilita o recebimento
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    @staticmethod
    def _csv(mime: QMimeData) -> list[str]:
        return [u.toLocalFile() for u in mime.urls()
                if u.isLocalFile() and u.toLocalFile().lower().endswith(".csv")]

    def dragEnterEvent(self, e: QDragEnterEvent) -> None:
        if e.mimeData().hasUrls() and self._csv(e.mimeData()):
            e.acceptProposedAction()                      # cursor indica "pode soltar"
        else:
            e.ignore()

    def dropEvent(self, e: QDropEvent) -> None:
        arquivos = self._csv(e.mimeData())
        self.setText("\n".join(arquivos))
        e.acceptProposedAction()


def simular(alvo: QLabel, caminho: str) -> None:
    """Gera os eventos que o sistema enviaria durante um arraste real."""
    mime = QMimeData()
    mime.setUrls([QUrl.fromLocalFile(caminho)])
    acao, botoes = Qt.DropAction.CopyAction, Qt.MouseButton.LeftButton
    entrar = QDragEnterEvent(alvo.rect().center(), acao, mime, botoes,
                             Qt.KeyboardModifier.NoModifier)
    QApplication.sendEvent(alvo, entrar)
    print(f"{caminho}: aceito? {entrar.isAccepted()}")
    if entrar.isAccepted():
        soltar = QDropEvent(QPointF(alvo.rect().center()), acao, mime, botoes,
                            Qt.KeyboardModifier.NoModifier)
        QApplication.sendEvent(alvo, soltar)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    alvo = AlvoCSV()
    alvo.show()
    simular(alvo, "/dados/relatorio.pdf")
    simular(alvo, "/dados/ensaio_bop.csv")
    print("rótulo:", alvo.text())
