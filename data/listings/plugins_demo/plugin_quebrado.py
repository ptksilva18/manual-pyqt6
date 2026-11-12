"""Plugin com erro proposital: a aplicação deve isolá-lo e continuar."""

NOME = "Plugin quebrado"
VERSAO_API = 1


def registrar(app_api) -> None:
    raise RuntimeError("falha ao inicializar o hardware do plugin")
