from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QMainWindow

class MyDailogBox(QMessageBox):
    def __init__(self):
        QMessageBox.__init__(self)
        self.mw = QMainWindow()
        self.mw.setWindowIcon(QIcon("icons/notice.jpg"))