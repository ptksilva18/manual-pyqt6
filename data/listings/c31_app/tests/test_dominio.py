"""Testes do domínio: valores calculados à mão e verificação cruzada com NumPy."""

import numpy as np
import pytest

from ensaios.dominio import Criterio, ErroDados, Leitura, analisar, regressao_linear
from ensaios.importacao import ler_csv


def test_regressao_coincide_com_numpy():
    x = [0.0, 5.0, 10.0, 20.0, 40.0, 60.0]
    y = [345.0, 344.98, 344.97, 344.93, 344.88, 344.80]
    a, b = regressao_linear(x, y)
    a_np, b_np = np.polyfit(x, y, 1)
    assert a == pytest.approx(a_np, rel=1e-12)
    assert b == pytest.approx(b_np, rel=1e-12)


def test_queda_linear_calculada_a_mao():
    # 345 bar caindo 0,6 bar/h por 60 min: queda 0,6 bar = 0,1739 % (0,6/345)
    leituras = [Leitura(t, 345.0 - 0.01 * t, 20.0) for t in range(0, 61, 10)]
    r = analisar(leituras, Criterio(queda_max_pct=0.5, taxa_max_bar_h=1.0))
    assert r.queda_bar == pytest.approx(0.6)
    assert r.queda_pct == pytest.approx(100 * 0.6 / 345.0)
    assert r.taxa_bar_h == pytest.approx(0.6)
    assert r.aprovado and r.motivos == ()


def test_compensacao_termica():
    # Sobe 0,5 bar só por aquecimento de 2 °C com dp/dT = 0,25 bar/°C: queda real nula
    leituras = [Leitura(0.0, 345.0, 20.0), Leitura(60.0, 345.5, 22.0)]
    r = analisar(leituras, Criterio(coef_temp_bar_c=0.25))
    assert r.p_final_corrigida == pytest.approx(345.0)
    assert r.queda_bar == pytest.approx(0.0, abs=1e-12)


def test_reprovacoes_acumulam_motivos():
    leituras = [Leitura(0.0, 345.0, 20.0), Leitura(30.0, 342.0, 20.0)]
    r = analisar(
        leituras, Criterio(duracao_min=60.0, queda_max_pct=0.5, taxa_max_bar_h=1.0)
    )
    assert not r.aprovado
    assert len(r.motivos) == 3  # patamar curto, queda e taxa


@pytest.mark.parametrize(
    "leituras, mensagem",
    [
        ([Leitura(0.0, 345.0, 20.0)], "pelo menos 2"),
        ([Leitura(0.0, 345.0, 20.0), Leitura(0.0, 344.0, 20.0)], "crescentes"),
        ([Leitura(0.0, 0.0, 20.0), Leitura(1.0, 0.0, 20.0)], "positiva"),
    ],
)
def test_dados_invalidos(leituras, mensagem):
    with pytest.raises(ErroDados, match=mensagem):
        analisar(leituras, Criterio())


def test_csv_com_virgula_decimal(tmp_path):
    arq = tmp_path / "x.csv"
    arq.write_text(
        "tempo_min;pressao_bar;temperatura_c\n0;345,0;20,5\n\n10;344,9;20,6\n",
        encoding="utf-8",
    )
    assert ler_csv(arq) == [Leitura(0.0, 345.0, 20.5), Leitura(10.0, 344.9, 20.6)]


def test_csv_invalido_informa_linha(tmp_path):
    arq = tmp_path / "x.csv"
    arq.write_text("t;p;T\n0;345;20\n10;abc;20\n", encoding="utf-8")
    with pytest.raises(ErroDados, match="linha 3"):
        ler_csv(arq)
