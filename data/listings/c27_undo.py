# runner: ticks=40
"""Command pattern com QUndoStack: comandos, fusão, macros, estado limpo e QUndoView."""

import sys

from PyQt6.QtGui import QUndoCommand, QUndoStack
from PyQt6.QtWidgets import QApplication, QUndoView


class Documento:
    def __init__(self) -> None:
        self.pressoes: dict[str, float] = {"PT-101": 100.0, "PT-102": 50.0}


class AlterarPressao(QUndoCommand):
    ID = 1001  # comandos com o mesmo id() podem ser fundidos

    def __init__(self, doc: Documento, tag: str, novo: float) -> None:
        super().__init__(f"{tag} = {novo:g} bar")
        self.doc, self.tag, self.novo = doc, tag, novo
        self.antigo = doc.pressoes[tag]

    def redo(self) -> None:  # chamado também por push()
        self.doc.pressoes[self.tag] = self.novo

    def undo(self) -> None:
        self.doc.pressoes[self.tag] = self.antigo

    def id(self) -> int:
        return self.ID

    def mergeWith(self, outro: QUndoCommand) -> bool:
        """Funde edições sucessivas da mesma tag (ex.: girar um QDial) em um único
        passo."""
        if not isinstance(outro, AlterarPressao) or outro.tag != self.tag:
            return False
        self.novo = outro.novo
        self.setText(f"{self.tag} = {self.novo:g} bar")
        return True


def estado(pilha: QUndoStack, doc: Documento, rotulo: str) -> None:
    print(
        f"{rotulo:<28} {doc.pressoes} | índice {pilha.index()}/{pilha.count()} | "
        f"limpo={pilha.isClean()} | desfazer: {pilha.undoText()!r}"
    )


def main() -> int:
    app = QApplication(sys.argv)
    doc = Documento()
    pilha = QUndoStack()
    pilha.setUndoLimit(100)
    acao_desfazer = pilha.createUndoAction(
        None, "Desfazer"
    )  # texto se atualiza sozinho
    vista = QUndoView(pilha)  # lista visual do histórico
    vista.show()

    for v in (101.0, 102.5, 104.0):  # três edições seguidas da mesma tag -> 1 comando
        pilha.push(AlterarPressao(doc, "PT-101", v))
    estado(pilha, doc, "após 3 edições de PT-101:")
    pilha.setClean()  # "arquivo salvo"
    pilha.beginMacro("Zerar todos")  # vários comandos desfeitos como um só
    for tag in list(doc.pressoes):
        pilha.push(AlterarPressao(doc, tag, 0.0))
    pilha.endMacro()
    estado(pilha, doc, "após macro:")
    pilha.undo()
    estado(pilha, doc, "undo (macro inteira):")
    pilha.undo()
    estado(pilha, doc, "undo:")
    pilha.redo()
    estado(pilha, doc, "redo:")
    print(
        "Ação de menu:",
        repr(acao_desfazer.text()),
        "| itens na QUndoView:",
        vista.model().rowCount(),
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
