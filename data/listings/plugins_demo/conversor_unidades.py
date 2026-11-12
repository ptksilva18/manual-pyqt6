"""Plugin de exemplo: converte a pressão selecionada de bar para psi."""

NOME = "Conversor bar → psi"
VERSAO_API = 1


def registrar(app_api) -> None:
    app_api.adicionar_acao(
        NOME, lambda: app_api.mostrar(f"{app_api.pressao() * 14.5038:.1f} psi")
    )
