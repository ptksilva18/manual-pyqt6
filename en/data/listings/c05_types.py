"""QtCore value types: geometry, dates and URLs."""
from PyQt6.QtCore import QDate, QDateTime, QPoint, QRect, QSize, Qt, QTime, QUrl

p = QPoint(10, 20) + QPoint(5, 5)
r = QRect(QPoint(0, 0), QSize(200, 100))
print("QPoint sum:", p.x(), p.y())
print("QRect contains (150, 50)?", r.contains(QPoint(150, 50)))
print("center:", r.center().x(), r.center().y())
print("right():", r.right(), "| width():", r.width())
t = r.translated(10, 10).topLeft()
print("translated (10, 10):", t.x(), t.y())
s = QSize(1920, 1080).scaled(QSize(800, 800), Qt.AspectRatioMode.KeepAspectRatio)
print("QSize scaled keeping the aspect ratio:", s.width(), "x", s.height())

d = QDate(2026, 11, 11)
print("ISO date:", d.toString(Qt.DateFormat.ISODate))
print("+90 days:", d.addDays(90).toString("yyyy-MM-dd"))
print("day of the week (1=Mon):", d.dayOfWeek())
start = QDateTime(d, QTime(8, 0))
end = QDateTime(d.addDays(1), QTime(17, 30))
print("duration (h):", start.secsTo(end) / 3600)

u = QUrl("https://doc.qt.io/qt-6/qobject.html#signals")
print("host:", u.host(), "| path:", u.path(), "| fragment:", u.fragment())
print("local file:", QUrl.fromLocalFile("/data/test.csv").toString())
