"""JSON (json module, QJsonDocument) and XML (QXmlStreamWriter/Reader, QtXml DOM)."""

import json

from PyQt6.QtCore import QByteArray, QJsonDocument, QXmlStreamReader, QXmlStreamWriter
from PyQt6.QtXml import QDomDocument

test = {
    "tag": "BOP-01",
    "pressure_bar": 345.0,
    "passed": True,
    "readings": [344.8, 345.1, 345.0],
}

# Python's json: the simplest
text = json.dumps(test, ensure_ascii=False, indent=2)
print("json.loads ok?", json.loads(text) == test)

doc = QJsonDocument.fromJson(QByteArray(text.encode("utf-8")))
print(
    "QJsonDocument is an object?",
    doc.isObject(),
    "| tag:",
    doc.object()["tag"].toString(),
)

output = QByteArray()
w = QXmlStreamWriter(output)
w.setAutoFormatting(True)
w.writeStartDocument()
w.writeStartElement("test")
w.writeAttribute("tag", test["tag"])
for v in test["readings"]:
    w.writeTextElement("reading", f"{v:.1f}")
w.writeEndElement()
w.writeEndDocument()
xml = bytes(output).decode("utf-8")
print(xml.strip())

# sequential reading (streaming)
r = QXmlStreamReader(xml)
readings = []
while not r.atEnd():
    if (
        r.readNext() == QXmlStreamReader.TokenType.StartElement
        and r.name() == "reading"
    ):
        readings.append(float(r.readElementText()))
print("stream reader:", readings, "| error?", r.hasError())

dom = QDomDocument()
# complete tree in memory
result = dom.setContent(xml)
print(
    "DOM loaded?",
    bool(result),
    "| tag attribute:",
    dom.documentElement().attribute("tag"),
    "| no. of <reading>:",
    dom.elementsByTagName("reading").count(),
)
