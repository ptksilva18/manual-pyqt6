# runner: ticks=40
"""Plugins with importlib: discovery in a folder and through entry points, stable API and
isolation."""

import importlib.metadata
import importlib.util
import os
import sys
from collections.abc import Callable
from types import ModuleType

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow

HERE = os.path.dirname(os.path.abspath(__file__))
API_VERSION = 1
ENTRY_POINT_GROUP = "pyqt6_manual.plugins"


class AppAPI:
    """Stable facade offered to the plugins: they do not touch the window directly."""

    def __init__(self, window: QMainWindow) -> None:
        self._window = window
        self._menu = window.menuBar().addMenu("Plugins")
        self.messages: list[str] = []

    def add_action(self, text: str, function: Callable[[], None]) -> QAction:
        action = self._menu.addAction(text)
        action.triggered.connect(function)
        return action

    def pressure(self) -> float:
        return 345.0

    def show(self, text: str) -> None:
        self.messages.append(text)
        self._window.statusBar().showMessage(text)


def load_file(path: str) -> ModuleType:
    name = "plugin_" + os.path.splitext(os.path.basename(path))[0]
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(
        module
    )  # executes the plugin's code: trust only its origin
    return module


def discover(folder: str) -> list[ModuleType]:
    modules = []
    for file_name in sorted(os.listdir(folder)):
        if file_name.endswith(".py") and not file_name.startswith("_"):
            modules.append(load_file(os.path.join(folder, file_name)))
    for ep in importlib.metadata.entry_points(
        group=ENTRY_POINT_GROUP
    ):  # installed packages
        modules.append(ep.load())
    return modules


def activate(modules: list[ModuleType], api: AppAPI) -> None:
    for mod in modules:
        name = getattr(mod, "NAME", mod.__name__)
        if getattr(mod, "API_VERSION", None) != API_VERSION:
            print(
                f"  ignored   {name!r}: API_VERSION={getattr(mod, 'API_VERSION', None)} "
                f"(expected {API_VERSION})"
            )
            continue
        try:
            mod.register(api)
            print(f"  activated {name!r}")
        except Exception as exc:  # a faulty plugin does not bring the application down
            print(f"  failed    {name!r}: {type(exc).__name__}: {exc}")


def main() -> int:
    app = QApplication(sys.argv)
    window = QMainWindow()
    api = AppAPI(window)
    modules = discover(os.path.join(HERE, "plugins_demo"))
    print(
        f"{len(modules)} plugins found (folder + entry points "
        f"'{ENTRY_POINT_GROUP}')"
    )
    activate(modules, api)
    actions = api._menu.actions()
    print("Plugins menu:", [a.text() for a in actions])
    actions[0].trigger()  # simulates the user's click
    print("Plugin message:", api.messages[-1])
    window.show()
    app.processEvents()
    return 0


if __name__ == "__main__":
    sys.exit(main())
