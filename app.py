from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget

import backend

app = QApplication([])
dlg = uic.loadUi("app.ui")


dlg.show()
app.exec()