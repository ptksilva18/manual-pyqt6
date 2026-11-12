"""Domínio: análise de ensaios de estanqueidade (Python puro, sem Qt)."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Leitura:
    t_min: float  # tempo desde o início da estabilização (min)
    p_bar: float  # pressão manométrica (bar)
    temp_c: float  # temperatura do fluido de teste (°C)


@dataclass(frozen=True)
class Criterio:
    duracao_min: float = 60.0  # tempo mínimo de patamar
    queda_max_pct: float = 0.5  # queda admissível, % da pressão inicial
    taxa_max_bar_h: float = 1.0  # taxa admissível de queda (regressão linear)
    coef_temp_bar_c: float = 0.0  # compensação térmica dp/dT (bar/°C); 0 = sem


@dataclass(frozen=True)
class Resultado:
    p_inicial: float
    p_final_corrigida: float
    queda_bar: float
    queda_pct: float
    taxa_bar_h: float
    duracao_min: float
    aprovado: bool
    motivos: tuple[str, ...] = field(default_factory=tuple)


class ErroDados(ValueError):
    """Dados de ensaio inconsistentes (menos de 2 leituras, tempo não crescente...)."""


def regressao_linear(x: list[float], y: list[float]) -> tuple[float, float]:
    """Mínimos quadrados: devolve (inclinação, intercepto)."""
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    sxx = sum((xi - mx) ** 2 for xi in x)
    if sxx == 0.0:
        raise ErroDados("todas as leituras têm o mesmo tempo")
    sxy = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
    a = sxy / sxx
    return a, my - a * mx


def analisar(leituras: list[Leitura], criterio: Criterio) -> Resultado:
    if len(leituras) < 2:
        raise ErroDados("são necessárias pelo menos 2 leituras")
    tempos = [lt.t_min for lt in leituras]
    if any(b <= a for a, b in zip(tempos, tempos[1:])):
        raise ErroDados("os tempos das leituras devem ser estritamente crescentes")
    p0, t0 = leituras[0].p_bar, leituras[0].temp_c
    if p0 <= 0.0:
        raise ErroDados("a pressão inicial deve ser positiva")
    k = criterio.coef_temp_bar_c
    # Pressão corrigida para a temperatura inicial: p_corr = p - k * (T - T0)
    p_corr = [lt.p_bar - k * (lt.temp_c - t0) for lt in leituras]
    queda = p0 - p_corr[-1]
    queda_pct = 100.0 * queda / p0
    inclinacao, _ = regressao_linear(tempos, p_corr)  # bar/min
    taxa_bar_h = -60.0 * inclinacao  # positiva quando a pressão cai
    duracao = tempos[-1] - tempos[0]
    motivos = []
    if duracao < criterio.duracao_min:
        motivos.append(
            f"patamar de {duracao:.0f} min < {criterio.duracao_min:.0f} min exigidos"
        )
    if queda_pct > criterio.queda_max_pct:
        motivos.append(f"queda de {queda_pct:.3f} % > {criterio.queda_max_pct:.3f} %")
    if taxa_bar_h > criterio.taxa_max_bar_h:
        motivos.append(
            f"taxa de {taxa_bar_h:.3f} bar/h > {criterio.taxa_max_bar_h:.3f} bar/h"
        )
    return Resultado(
        p0,
        p_corr[-1],
        queda,
        queda_pct,
        taxa_bar_h,
        duracao,
        not motivos,
        tuple(motivos),
    )
