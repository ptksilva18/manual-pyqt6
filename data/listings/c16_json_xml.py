"""JSON (módulo json e QJsonDocument) e XML (QXmlStreamWriter/Reader e QtXml DOM)."""

import json

from PyQt6.QtCore import QByteArray, QJsonDocument, QXmlStreamReader, QXmlStreamWriter
from PyQt6.QtXml import QDomDocument

ensaio = {
    "tag": "BOP-01",
    "pressao_bar": 345.0,
    "aprovado": True,
    "leituras": [344.8, 345.1, 345.0],
}

# json do Python: o mais simples
texto = json.dumps(ensaio, ensure_ascii=False, indent=2)
print("json.loads ok?", json.loads(texto) == ensaio)

doc = QJsonDocument.fromJson(QByteArray(texto.encode("utf-8")))
print(
    "QJsonDocument é objeto?", doc.isObject(), "| tag:", doc.object()["tag"].toString()
)

saida = QByteArray()
w = QXmlStreamWriter(saida)
w.setAutoFormatting(True)
w.writeStartDocument()
w.writeStartElement("ensaio")
w.writeAttribute("tag", ensaio["tag"])
for v in ensaio["leituras"]:
    w.writeTextElement("leitura", f"{v:.1f}")
w.writeEndElement()
w.writeEndDocument()
xml = bytes(saida).decode("utf-8")
print(xml.strip())

# leitura sequencial (streaming)
r = QXmlStreamReader(xml)
leituras = []
while not r.atEnd():
    if (
        r.readNext() == QXmlStreamReader.TokenType.StartElement
        and r.name() == "leitura"
    ):
        leituras.append(float(r.readElementText()))
print("stream reader:", leituras, "| erro?", r.hasError())

dom = QDomDocument()
# árvore completa em memória
resultado = dom.setContent(xml)
print(
    "DOM carregado?",
    bool(resultado),
    "| atributo tag:",
    dom.documentElement().attribute("tag"),
    "| nº de <leitura>:",
    dom.elementsByTagName("leitura").count(),
)
