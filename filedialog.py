# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FileDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
from os import path

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog


class Ui_Dialog(object):

    def setupUi(self, QFileDialog):
        QFileDialog.setObjectName("Dialog")
        QFileDialog.resize(640, 480)
        self.retranslateUi(QFileDialog)
        QtCore.QMetaObject.connectSlotsByName(QFileDialog)

    def retranslateUi(self, QFileDialog):
        _translate = QtCore.QCoreApplication.translate
        QFileDialog.setWindowTitle(_translate("Dialog", "select xls to open"))

