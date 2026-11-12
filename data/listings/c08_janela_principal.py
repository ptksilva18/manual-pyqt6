"""Janela principal completa: ações, menus, barra de ferramentas, docks e QSettings."""
import sys

from PyQt6.QtCore import QSettings, Qt
from PyQt6.QtGui import QAction, QActionGroup, QKeySequence
from PyQt6.QtWidgets import (
    QApplication, QDockWidget, QLabel, QListWidget, QMainWindow, QMenu, QStyle,
    QTabWidget, QTextEdit, QToolBar,
)


class JanelaPrincipal(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Diário de Ensaios [*]")   # [*]: indicador de alteração
        self.resize(820, 520)
        self._criar_acoes()
        self._criar_menus()
        self._criar_barra_ferramentas()
        self._criar_area_central()
        self._criar_docks()
        self._criar_barra_status()
        self._restaurar_estado()

    # ----------------------------------------------------------------- ações --
    def _criar_acoes(self) -> None:
        st = self.style()
        self.acao_novo = QAction(st.standardIcon(QStyle.StandardPixmap.SP_FileIcon),
                                 "&Novo", self)
        self.acao_novo.setShortcut(QKeySequence.StandardKey.New)       # Ctrl+N
        self.acao_novo.setStatusTip("Cria um novo registro de ensaio")
        self.acao_novo.triggered.connect(self.novo_registro)

        icone_salvar = st.standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton)
        self.acao_salvar = QAction(icone_salvar, "&Salvar", self)
        self.acao_salvar.setShortcut(QKeySequence.StandardKey.Save)     # Ctrl+S
        self.acao_salvar.triggered.connect(self.salvar)

        self.acao_sair = QAction("Sai&r", self)
        self.acao_sair.setShortcut(QKeySequence("Ctrl+Q"))
        self.acao_sair.triggered.connect(self.close)

        self.acao_quebra = QAction("&Quebra de linha", self, checkable=True, checked=True)
        self.acao_quebra.toggled.connect(self._alternar_quebra)

        self.grupo_unidades = QActionGroup(self)                         # exclusivo
        for nome in ("SI", "Imperial"):
            a = QAction(nome, self, checkable=True, checked=(nome == "SI"))
            self.grupo_unidades.addAction(a)
        self.grupo_unidades.triggered.connect(
            lambda a: self.statusBar().showMessage(f"Unidades: {a.text()}", 3000))

    # ----------------------------------------------------------------- menus --
    def _criar_menus(self) -> None:
        arquivo = self.menuBar().addMenu("&Arquivo")
        arquivo.addActions([self.acao_novo, self.acao_salvar])
        arquivo.addSeparator()
        arquivo.addAction(self.acao_sair)
        exibir = self.menuBar().addMenu("&Exibir")
        exibir.addAction(self.acao_quebra)
        unidades = exibir.addMenu("&Unidades")                           # submenu
        unidades.addActions(self.grupo_unidades.actions())
        self.menu_paineis = exibir.addMenu("&Painéis")

    def _criar_barra_ferramentas(self) -> None:
        barra = QToolBar("Principal", objectName="barraPrincipal")  # p/ saveState
        barra.addActions([self.acao_novo, self.acao_salvar])
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, barra)

    # ----------------------------------------------------- área central ------
    def _criar_area_central(self) -> None:
        self.abas = QTabWidget(documentMode=True, tabsClosable=True)
        self.abas.tabCloseRequested.connect(self.abas.removeTab)
        self.setCentralWidget(self.abas)
        self.novo_registro()

    def _criar_docks(self) -> None:
        dock = QDockWidget("Equipamentos", self, objectName="dockEquipamentos")
        lista = QListWidget()
        lista.addItems(["BOP 18¾\" 15 ksi", "Riser de perfuração", "HPU 5000 psi"])
        lista.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        lista.customContextMenuRequested.connect(
            lambda pos: self._menu_contexto(lista, pos))
        dock.setWidget(lista)
        dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea
                             | Qt.DockWidgetArea.RightDockWidgetArea)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock)
        self.menu_paineis.addAction(dock.toggleViewAction())             # mostrar/ocultar

    def _criar_barra_status(self) -> None:
        self.rotulo_linhas = QLabel("Linhas: 0")
        self.statusBar().addPermanentWidget(self.rotulo_linhas)          # lado direito
        self.statusBar().showMessage("Pronto", 2000)

    # ------------------------------------------------------------- slots -----
    def novo_registro(self) -> None:
        editor = QTextEdit()
        editor.textChanged.connect(lambda: self.setWindowModified(True))
        editor.textChanged.connect(lambda: self.rotulo_linhas.setText(
            f"Linhas: {editor.document().blockCount()}"))
        indice = self.abas.addTab(editor, f"Ensaio {self.abas.count() + 1}")
        self.abas.setCurrentIndex(indice)

    def salvar(self) -> None:
        self.setWindowModified(False)
        self.statusBar().showMessage("Registro salvo", 2000)

    def _alternar_quebra(self, ligado: bool) -> None:
        modo = (QTextEdit.LineWrapMode.WidgetWidth if ligado
                else QTextEdit.LineWrapMode.NoWrap)
        for i in range(self.abas.count()):
            self.abas.widget(i).setLineWrapMode(modo)

    def _menu_contexto(self, lista: QListWidget, pos) -> None:
        item = lista.itemAt(pos)
        if item is None:
            return
        menu = QMenu(self)
        menu.addAction(f"Abrir ficha de {item.text()}")
        menu.exec(lista.viewport().mapToGlobal(pos))

    # --------------------------------------------------------- persistência --
    def _restaurar_estado(self) -> None:
        s = QSettings("Engenharia", "DiarioEnsaios")
        geom, estado = s.value("geometria"), s.value("estado")
        ok_geom = geom is not None and self.restoreGeometry(geom)
        ok_estado = estado is not None and self.restoreState(estado)
        self.estado_restaurado = bool(ok_geom and ok_estado)

    def closeEvent(self, event) -> None:
        s = QSettings("Engenharia", "DiarioEnsaios")
        s.setValue("geometria", self.saveGeometry())
        s.setValue("estado", self.saveState())
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    QSettings("Engenharia", "DiarioEnsaios").clear()        # demonstração: 1ª execução
    j1 = JanelaPrincipal()
    j1.show()
    print("1ª abertura — estado restaurado?", j1.estado_restaurado)
    j1.abas.currentWidget().setPlainText("Teste hidrostático\n345 bar por 15 min")
    print("título:", j1.windowTitle(), "| modificado?", j1.isWindowModified())
    j1.acao_salvar.trigger()
    print("após salvar — modificado?", j1.isWindowModified())
    print("menus:", [a.text() for a in j1.menuBar().actions()])
    j1.close()                                               # grava geometria e estado
    j2 = JanelaPrincipal()
    print("2ª abertura — estado restaurado?", j2.estado_restaurado)
    j2.show()
    sys.exit(app.exec())
