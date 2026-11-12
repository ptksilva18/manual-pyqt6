import sys, json
from PyQt6.QtCore import qInstallMessageHandler
msgs=[]
qInstallMessageHandler(lambda t,c,m: msgs.append(m))
from PyQt6.QtWidgets import *
app=QApplication([])
w=QWidget(); l=QVBoxLayout(w)
ws=[QPushButton('a'),QCheckBox('b'),QComboBox(),QSpinBox(),QSlider(),QProgressBar(),QTabWidget(),QTableView(),QGroupBox('g'),QLineEdit(),QLabel('x'),QTextEdit()]
for c in ws: l.addWidget(c)
w.show(); app.processEvents()
props = {
 "background":"#FFFFFF","background-color":"#FFFFFF","color":"#1E1E1E","border":"1px solid #BFBFBF",
 "border-radius":"4px","border-color":"#2E75B6","border-width":"2px","border-style":"solid",
 "padding":"4px 8px","margin":"2px","min-width":"80px","min-height":"24px","max-width":"300px","max-height":"40px",
 "font":"bold 10pt","font-size":"10pt","font-weight":"bold","font-family":"Calibri","font-style":"italic",
 "selection-color":"white","selection-background-color":"#2E75B6","alternate-background-color":"#F2F6FB",
 "gridline-color":"#D9D9D9","image":"none","spacing":"6px","text-align":"left","outline":"none",
 "subcontrol-origin":"margin","subcontrol-position":"top left","icon-size":"24px","height":"20px","width":"20px",
 "placeholder-text-color":"#888888","qproperty-alignment":"AlignCenter","opacity":"200","border-image":"none",
 "lineedit-password-character":"9679","text-decoration":"underline","background-image":"none","background-position":"center",
 "background-repeat":"no-repeat","position":"relative","left":"2px","top":"2px","right":"2px","bottom":"2px",
}
res={}
for k,v in props.items():
    msgs.clear()
    sel = "QLabel" if k.startswith("qproperty") else "*"
    app.setStyleSheet(f"{sel} {{ {k}: {v}; }}")
    for c in w.findChildren(QWidget): c.style().unpolish(c); c.style().polish(c); c.ensurePolished()
    app.processEvents()
    res[k] = [m for m in msgs if 'Unknown' in m or 'parse' in m]
bad={k:v for k,v in res.items() if v}
print("propriedades testadas:", len(props), "| rejeitadas:", bad)
