from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget

from backend import *

app = QApplication([])
dlg = uic.loadUi("app.ui")

def get_weather():
    if dlg.knn.isChecked():
        ac = (return_accurancy_score()[0])*100
        pred = return_predicted_labels()[0]
        ac = int(ac)
        ac = str(ac) + '%'
        dlg.procent.setText(ac)

    elif dlg.reg.isChecked():
        ac = (return_accurancy_score()[1])*100
        pred = return_predicted_labels()[1]
        ac = int(ac)
        ac = str(ac) + '%'
        dlg.procent.setText(ac)

    elif dlg.svn.isChecked():
        ac = (return_accurancy_score()[2])*100
        pred = return_predicted_labels()[2]
        ac = int(ac)
        ac = str(ac) + '%'
        dlg.procent.setText(ac)

dlg.next.clicked.connect(get_weather)
dlg.show()
app.exec()