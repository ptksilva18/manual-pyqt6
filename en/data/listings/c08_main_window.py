"""Complete main window: actions, menus, toolbar, docks and QSettings."""
import sys

from PyQt6.QtCore import QSettings, Qt
from PyQt6.QtGui import QAction, QActionGroup, QKeySequence
from PyQt6.QtWidgets import (
    QApplication, QDockWidget, QLabel, QListWidget, QMainWindow, QMenu, QStyle,
    QTabWidget, QTextEdit, QToolBar,
)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Test Log [*]")            # [*]: modification indicator
        self.resize(820, 520)
        self._create_actions()
        self._create_menus()
        self._create_toolbar()
        self._create_central_area()
        self._create_docks()
        self._create_status_bar()
        self._restore_state()

    # --------------------------------------------------------------- actions --
    def _create_actions(self) -> None:
        st = self.style()
        self.new_action = QAction(st.standardIcon(QStyle.StandardPixmap.SP_FileIcon),
                                  "&New", self)
        self.new_action.setShortcut(QKeySequence.StandardKey.New)      # Ctrl+N
        self.new_action.setStatusTip("Creates a new test record")
        self.new_action.triggered.connect(self.new_record)

        save_icon = st.standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton)
        self.save_action = QAction(save_icon, "&Save", self)
        self.save_action.setShortcut(QKeySequence.StandardKey.Save)    # Ctrl+S
        self.save_action.triggered.connect(self.save)

        self.quit_action = QAction("&Quit", self)
        self.quit_action.setShortcut(QKeySequence("Ctrl+Q"))
        self.quit_action.triggered.connect(self.close)

        self.wrap_action = QAction("&Word wrap", self, checkable=True, checked=True)
        self.wrap_action.toggled.connect(self._toggle_wrap)

        self.unit_group = QActionGroup(self)                             # exclusive
        for name in ("SI", "Imperial"):
            a = QAction(name, self, checkable=True, checked=(name == "SI"))
            self.unit_group.addAction(a)
        self.unit_group.triggered.connect(
            lambda a: self.statusBar().showMessage(f"Units: {a.text()}", 3000))

    # ----------------------------------------------------------------- menus --
    def _create_menus(self) -> None:
        file_menu = self.menuBar().addMenu("&File")
        file_menu.addActions([self.new_action, self.save_action])
        file_menu.addSeparator()
        file_menu.addAction(self.quit_action)
        view = self.menuBar().addMenu("&View")
        view.addAction(self.wrap_action)
        units = view.addMenu("&Units")                                   # submenu
        units.addActions(self.unit_group.actions())
        self.panels_menu = view.addMenu("&Panels")

    def _create_toolbar(self) -> None:
        bar = QToolBar("Main", objectName="mainToolBar")            # for saveState
        bar.addActions([self.new_action, self.save_action])
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, bar)

    # ---------------------------------------------------------- central area --
    def _create_central_area(self) -> None:
        self.tabs = QTabWidget(documentMode=True, tabsClosable=True)
        self.tabs.tabCloseRequested.connect(self.tabs.removeTab)
        self.setCentralWidget(self.tabs)
        self.new_record()

    def _create_docks(self) -> None:
        dock = QDockWidget("Equipment", self, objectName="equipmentDock")
        items = QListWidget()
        items.addItems(["BOP 18¾\" 15 ksi", "Drilling riser", "HPU 5000 psi"])
        items.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        items.customContextMenuRequested.connect(
            lambda pos: self._context_menu(items, pos))
        dock.setWidget(items)
        dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea
                             | Qt.DockWidgetArea.RightDockWidgetArea)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock)
        self.panels_menu.addAction(dock.toggleViewAction())              # show/hide

    def _create_status_bar(self) -> None:
        self.lines_label = QLabel("Lines: 0")
        self.statusBar().addPermanentWidget(self.lines_label)            # right side
        self.statusBar().showMessage("Ready", 2000)

    # ----------------------------------------------------------------- slots --
    def new_record(self) -> None:
        editor = QTextEdit()
        editor.textChanged.connect(lambda: self.setWindowModified(True))
        editor.textChanged.connect(lambda: self.lines_label.setText(
            f"Lines: {editor.document().blockCount()}"))
        index = self.tabs.addTab(editor, f"Test {self.tabs.count() + 1}")
        self.tabs.setCurrentIndex(index)

    def save(self) -> None:
        self.setWindowModified(False)
        self.statusBar().showMessage("Record saved", 2000)

    def _toggle_wrap(self, on: bool) -> None:
        mode = (QTextEdit.LineWrapMode.WidgetWidth if on
                else QTextEdit.LineWrapMode.NoWrap)
        for i in range(self.tabs.count()):
            self.tabs.widget(i).setLineWrapMode(mode)

    def _context_menu(self, items: QListWidget, pos) -> None:
        item = items.itemAt(pos)
        if item is None:
            return
        menu = QMenu(self)
        menu.addAction(f"Open data sheet of {item.text()}")
        menu.exec(items.viewport().mapToGlobal(pos))

    # ----------------------------------------------------------- persistence --
    def _restore_state(self) -> None:
        s = QSettings("Engineering", "TestLog")
        geom, state = s.value("geometry"), s.value("state")
        geom_ok = geom is not None and self.restoreGeometry(geom)
        state_ok = state is not None and self.restoreState(state)
        self.state_restored = bool(geom_ok and state_ok)

    def closeEvent(self, event) -> None:
        s = QSettings("Engineering", "TestLog")
        s.setValue("geometry", self.saveGeometry())
        s.setValue("state", self.saveState())
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    QSettings("Engineering", "TestLog").clear()             # demonstration: 1st run
    w1 = MainWindow()
    w1.show()
    print("1st opening — state restored?", w1.state_restored)
    w1.tabs.currentWidget().setPlainText("Hydrostatic test\n345 bar for 15 min")
    print("title:", w1.windowTitle(), "| modified?", w1.isWindowModified())
    w1.save_action.trigger()
    print("after saving — modified?", w1.isWindowModified())
    print("menus:", [a.text() for a in w1.menuBar().actions()])
    w1.close()                                               # stores geometry and state
    w2 = MainWindow()
    print("2nd opening — state restored?", w2.state_restored)
    w2.show()
    sys.exit(app.exec())
