"""Plugin written for an earlier version of the plugin API."""

NAME = "Legacy exporter"
API_VERSION = 0


def register(app_api) -> None:
    app_api.add_action(NAME, lambda: None)
