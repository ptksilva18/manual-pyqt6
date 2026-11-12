"""Plugin escrito para uma versão anterior da API de plugins."""

NOME = "Exportador legado"
VERSAO_API = 0


def registrar(app_api) -> None:
    app_api.adicionar_acao(NOME, lambda: None)
