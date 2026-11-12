"""PDF report: HTML (QTextDocument) with a Matplotlib chart, written with QPdfWriter."""

import io
from html import escape
from pathlib import Path

from matplotlib.figure import Figure
from PyQt6.QtCore import QByteArray, QMarginsF, QUrl
from PyQt6.QtGui import QImage, QPageLayout, QPageSize, QPdfWriter, QTextDocument

from .domain import Criterion, Reading, Result


def chart_png(readings: list[Reading], title: str) -> bytes:
    fig = Figure(figsize=(6.5, 2.8), dpi=150, layout="constrained")
    ax = fig.add_subplot()
    ax.plot(
        [rd.t_min for rd in readings],
        [rd.p_bar for rd in readings],
        "o-",
        color="#2E75B6",
        ms=3,
        lw=1.5,
    )
    ax.set_xlabel("Time (min)")
    ax.set_ylabel("Pressure (bar)")
    ax.set_title(title + " (measured pressure)", fontsize=10)
    ax.grid(True, alpha=0.3)
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    return buf.getvalue()


def make_pdf(
    target: str | Path,
    code: str,
    description: str,
    readings: list[Reading],
    criterion: Criterion,
    r: Result,
) -> Path:
    target = Path(target)
    status = (
        "<b style='color:#548235'>PASSED</b>"
        if r.passed
        else "<b style='color:#C00000'>FAILED</b>"
    )
    rows = "".join(
        f"<tr><td>{rd.t_min:.1f}</td><td>{rd.p_bar:.3f}</td>"
        f"<td>{rd.temp_c:.2f}</td></tr>"
        for rd in readings
    )
    reasons = "".join(f"<li>{escape(m)}</li>" for m in r.reasons) or "<li>none</li>"
    html = f"""
    <h2>Leak test report — {escape(code)}</h2>
    <p>{escape(description)}</p>
    <table border="1" cellspacing="0" cellpadding="3">
      <tr><td>Initial pressure</td><td>{r.p_initial:.3f} bar</td></tr>
      <tr><td>Final pressure corrected (initial temperature)</td>
          <td>{r.p_final_corrected:.3f} bar</td></tr>
      <tr><td>Drop</td><td>{r.drop_bar:.3f} bar ({r.drop_pct:.3f} %)</td></tr>
      <tr><td>Rate of drop (regression)</td><td>{r.rate_bar_h:.3f} bar/h</td></tr>
      <tr><td>Hold duration</td><td>{r.duration_min:.0f} min</td></tr>
      <tr><td>Criterion</td><td>≥ {criterion.duration_min:.0f} min;
          ≤ {criterion.max_drop_pct} %; ≤ {criterion.max_rate_bar_h} bar/h;
          dp/dT = {criterion.temp_coef_bar_c} bar/°C</td></tr>
      <tr><td>Result</td><td>{status}</td></tr>
    </table>
    <p>Reasons for failure:</p><ul>{reasons}</ul>
    <p><img src="chart://pressure" width="600"></p>
    <h3>Readings</h3>
    <table border="1" cellspacing="0" cellpadding="2">
      <tr><th>Time (min)</th><th>Pressure (bar)</th><th>Temperature (°C)</th></tr>{rows}
    </table>"""
    doc = QTextDocument()
    image = QImage.fromData(
        QByteArray(chart_png(readings, f"Pressure hold — {code}"))
    )
    doc.addResource(
        QTextDocument.ResourceType.ImageResource, QUrl("chart://pressure"), image
    )
    doc.setHtml(html)
    writer = QPdfWriter(str(target))
    writer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
    writer.setPageMargins(QMarginsF(15, 15, 15, 15), QPageLayout.Unit.Millimeter)
    writer.setTitle(f"Report {code}")
    writer.setCreator("Leak Test Monitor")
    writer.setResolution(300)
    doc.print(
        writer
    )  # with no pageSize set, print() paginates to the printable area of the sheet
    return target
