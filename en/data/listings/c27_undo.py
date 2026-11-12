# runner: ticks=40
"""Command pattern with QUndoStack: commands, merging, macros, clean state, QUndoView."""

import sys

from PyQt6.QtGui import QUndoCommand, QUndoStack
from PyQt6.QtWidgets import QApplication, QUndoView


class Document:
    def __init__(self) -> None:
        self.pressures: dict[str, float] = {"PT-101": 100.0, "PT-102": 50.0}


class ChangePressure(QUndoCommand):
    ID = 1001  # commands with the same id() can be merged

    def __init__(self, doc: Document, tag: str, new: float) -> None:
        super().__init__(f"{tag} = {new:g} bar")
        self.doc, self.tag, self.new = doc, tag, new
        self.old = doc.pressures[tag]

    def redo(self) -> None:  # also called by push()
        self.doc.pressures[self.tag] = self.new

    def undo(self) -> None:
        self.doc.pressures[self.tag] = self.old

    def id(self) -> int:
        return self.ID

    def mergeWith(self, other: QUndoCommand) -> bool:
        """Merges successive edits of the same tag (e.g. turning a QDial) into a single
        step."""
        if not isinstance(other, ChangePressure) or other.tag != self.tag:
            return False
        self.new = other.new
        self.setText(f"{self.tag} = {self.new:g} bar")
        return True


def state(stack: QUndoStack, doc: Document, label: str) -> None:
    print(
        f"{label:<26} {doc.pressures} | index {stack.index()}/{stack.count()} | "
        f"clean={stack.isClean()} | undo: {stack.undoText()!r}"
    )


def main() -> int:
    app = QApplication(sys.argv)
    doc = Document()
    stack = QUndoStack()
    stack.setUndoLimit(100)
    undo_action = stack.createUndoAction(
        None, "Undo"
    )  # the text updates itself
    view = QUndoView(stack)  # visual list of the history
    view.show()

    for v in (101.0, 102.5, 104.0):  # three successive edits of one tag -> 1 command
        stack.push(ChangePressure(doc, "PT-101", v))
    state(stack, doc, "after 3 edits of PT-101:")
    stack.setClean()  # "file saved"
    stack.beginMacro("Zero all")  # several commands undone as one
    for tag in list(doc.pressures):
        stack.push(ChangePressure(doc, tag, 0.0))
    stack.endMacro()
    state(stack, doc, "after macro:")
    stack.undo()
    state(stack, doc, "undo (whole macro):")
    stack.undo()
    state(stack, doc, "undo:")
    stack.redo()
    state(stack, doc, "redo:")
    print(
        "Menu action:",
        repr(undo_action.text()),
        "| items in the QUndoView:",
        view.model().rowCount(),
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
