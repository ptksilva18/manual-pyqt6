"""Example plugin: converts the selected pressure from bar to psi."""

NAME = "bar → psi converter"
API_VERSION = 1


def register(app_api) -> None:
    app_api.add_action(
        NAME, lambda: app_api.show(f"{app_api.pressure() * 14.5038:.1f} psi")
    )
