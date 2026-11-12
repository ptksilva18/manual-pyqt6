"""Plugin with a deliberate error: the application must isolate it and carry on."""

NAME = "Broken plugin"
API_VERSION = 1


def register(app_api) -> None:
    raise RuntimeError("failed to initialize the plugin hardware")
