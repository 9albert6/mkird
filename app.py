from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget

from backend import *

app = QApplication([])
dlg = uic.loadUi("app.ui")


def get_weather():
    global licznik
    if dlg.knn.isChecked():
        ac = (return_accurancy_score()[0])*100
        pred = return_predicted_labels()[0]
        ac = int(ac)
        ac = str(ac) + '%'
        dlg.procent.setText(ac)
        if pred[licznik] == 0:
            dlg.sun.setHidden(False)
            dlg.rain.setHidden(True)
        else:
            dlg.rain.setHidden(False)
            dlg.sun.setHidden(True)


    elif dlg.reg.isChecked():
        ac = (return_accurancy_score()[1])*100
        pred = return_predicted_labels()[1]
        ac = int(ac)
        ac = str(ac) + '%'
        dlg.procent.setText(ac)
        if pred[licznik] == 0:
            dlg.sun.setHidden(False)
            dlg.rain.setHidden(True)
        else:
            dlg.rain.setHidden(False)
            dlg.sun.setHidden(True)

    elif dlg.svn.isChecked():
        ac = (return_accurancy_score()[2])*100
        pred = return_predicted_labels()[2]
        ac = int(ac)
        ac = str(ac) + '%'
        dlg.procent.setText(ac)
        if pred[licznik] == 0:
            dlg.sun.setHidden(False)
            dlg.rain.setHidden(True)
        else:
            dlg.rain.setHidden(False)
            dlg.sun.setHidden(True)

licznik = 0 

def add_data():
    global licznik
    data = return_datetime()
    dlg.data.setText(data[licznik])
    licznik += 1

def add_data_back():
    global licznik
    licznik -= 2
    data = return_datetime()
    dlg.data.setText(data[licznik])
    licznik += 1
    

dlg.start.clicked.connect(get_weather)
dlg.next.clicked.connect(add_data)
dlg.return_2.clicked.connect(add_data_back)
dlg.show()
app.exec()