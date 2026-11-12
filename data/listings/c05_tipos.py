"""Tipos de valor do QtCore: geometria, datas e URLs."""
from PyQt6.QtCore import QDate, QDateTime, QPoint, QRect, QSize, Qt, QTime, QUrl

p = QPoint(10, 20) + QPoint(5, 5)
r = QRect(QPoint(0, 0), QSize(200, 100))
print("QPoint soma:", p.x(), p.y())
print("QRect contém (150, 50)?", r.contains(QPoint(150, 50)))
print("centro:", r.center().x(), r.center().y())
print("right():", r.right(), "| width():", r.width())
t = r.translated(10, 10).topLeft()
print("deslocado (10, 10):", t.x(), t.y())
s = QSize(1920, 1080).scaled(QSize(800, 800), Qt.AspectRatioMode.KeepAspectRatio)
print("QSize escalado mantendo proporção:", s.width(), "x", s.height())

d = QDate(2026, 11, 11)
print("data ISO:", d.toString(Qt.DateFormat.ISODate))
print("+90 dias:", d.addDays(90).toString("dd/MM/yyyy"))
print("dia da semana (1=seg):", d.dayOfWeek())
inicio = QDateTime(d, QTime(8, 0))
fim = QDateTime(d.addDays(1), QTime(17, 30))
print("duração (h):", inicio.secsTo(fim) / 3600)

u = QUrl("https://doc.qt.io/qt-6/qobject.html#signals")
print("host:", u.host(), "| caminho:", u.path(), "| fragmento:", u.fragment())
print("arquivo local:", QUrl.fromLocalFile("/dados/ensaio.csv").toString())
