"""Relatório PDF: HTML (QTextDocument) com gráfico Matplotlib, gravado com QPdfWriter."""

import io
from html import escape
from pathlib import Path

from matplotlib.figure import Figure
from PyQt6.QtCore import QByteArray, QMarginsF, QUrl
from PyQt6.QtGui import QImage, QPageLayout, QPageSize, QPdfWriter, QTextDocument

from .dominio import Criterio, Leitura, Resultado


def grafico_png(leituras: list[Leitura], titulo: str) -> bytes:
    fig = Figure(figsize=(6.5, 2.8), dpi=150, layout="constrained")
    ax = fig.add_subplot()
    ax.plot(
        [lt.t_min for lt in leituras],
        [lt.p_bar for lt in leituras],
        "o-",
        color="#2E75B6",
        ms=3,
        lw=1.5,
    )
    ax.set_xlabel("Tempo (min)")
    ax.set_ylabel("Pressão (bar)")
    ax.set_title(titulo + " (pressão medida)", fontsize=10)
    ax.grid(True, alpha=0.3)
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    return buf.getvalue()


def gerar_pdf(
    destino: str | Path,
    codigo: str,
    descricao: str,
    leituras: list[Leitura],
    criterio: Criterio,
    r: Resultado,
) -> Path:
    destino = Path(destino)
    situacao = (
        "<b style='color:#548235'>APROVADO</b>"
        if r.aprovado
        else "<b style='color:#C00000'>REPROVADO</b>"
    )
    linhas = "".join(
        f"<tr><td>{lt.t_min:.1f}</td><td>{lt.p_bar:.3f}</td>"
        f"<td>{lt.temp_c:.2f}</td></tr>"
        for lt in leituras
    )
    motivos = "".join(f"<li>{escape(m)}</li>" for m in r.motivos) or "<li>nenhum</li>"
    html = f"""
    <h2>Relatório de ensaio de estanqueidade — {escape(codigo)}</h2>
    <p>{escape(descricao)}</p>
    <table border="1" cellspacing="0" cellpadding="3">
      <tr><td>Pressão inicial</td><td>{r.p_inicial:.3f} bar</td></tr>
      <tr><td>Pressão final corrigida (temperatura inicial)</td>
          <td>{r.p_final_corrigida:.3f} bar</td></tr>
      <tr><td>Queda</td><td>{r.queda_bar:.3f} bar ({r.queda_pct:.3f} %)</td></tr>
      <tr><td>Taxa de queda (regressão)</td><td>{r.taxa_bar_h:.3f} bar/h</td></tr>
      <tr><td>Duração do patamar</td><td>{r.duracao_min:.0f} min</td></tr>
      <tr><td>Critério</td><td>≥ {criterio.duracao_min:.0f} min;
          ≤ {criterio.queda_max_pct} %; ≤ {criterio.taxa_max_bar_h} bar/h;
          dp/dT = {criterio.coef_temp_bar_c} bar/°C</td></tr>
      <tr><td>Resultado</td><td>{situacao}</td></tr>
    </table>
    <p>Motivos de reprovação:</p><ul>{motivos}</ul>
    <p><img src="grafico://pressao" width="600"></p>
    <h3>Leituras</h3>
    <table border="1" cellspacing="0" cellpadding="2">
      <tr><th>Tempo (min)</th><th>Pressão (bar)</th><th>Temperatura (°C)</th></tr>{linhas}
    </table>"""
    doc = QTextDocument()
    imagem = QImage.fromData(
        QByteArray(grafico_png(leituras, f"Patamar de pressão — {codigo}"))
    )
    doc.addResource(
        QTextDocument.ResourceType.ImageResource, QUrl("grafico://pressao"), imagem
    )
    doc.setHtml(html)
    escritor = QPdfWriter(str(destino))
    escritor.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
    escritor.setPageMargins(QMarginsF(15, 15, 15, 15), QPageLayout.Unit.Millimeter)
    escritor.setTitle(f"Relatório {codigo}")
    escritor.setCreator("Monitor de Ensaios")
    escritor.setResolution(300)
    doc.print(
        escritor
    )  # sem pageSize definido, print() pagina no tamanho útil da folha
    return destino
