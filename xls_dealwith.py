# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'xls_dealwith.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 480)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.openFile = QtWidgets.QPushButton(self.centralwidget)
        self.openFile.setObjectName("openFile")
        self.horizontalLayout.addWidget(self.openFile)
        self.saveFile = QtWidgets.QPushButton(self.centralwidget)
        self.saveFile.setObjectName("saveFile")
        self.horizontalLayout.addWidget(self.saveFile)
        self.translate = QtWidgets.QPushButton(self.centralwidget)
        self.translate.setObjectName("translate")
        self.horizontalLayout.addWidget(self.translate)
        self.toChina = QtWidgets.QRadioButton(self.centralwidget)
        self.toChina.setObjectName("toChina")
        self.horizontalLayout.addWidget(self.toChina)
        self.toEnglish = QtWidgets.QRadioButton(self.centralwidget)
        self.toEnglish.setObjectName("toEnglish")
        self.horizontalLayout.addWidget(self.toEnglish)
        self.toFrench = QtWidgets.QRadioButton(self.centralwidget)
        self.toFrench.setObjectName("toFrench")
        self.horizontalLayout.addWidget(self.toFrench)
        self.toJapan = QtWidgets.QRadioButton(self.centralwidget)
        self.toJapan.setObjectName("toJapan")
        self.horizontalLayout.addWidget(self.toJapan)

        self.toGerman = QtWidgets.QRadioButton(self.centralwidget)
        self.toGerman.setObjectName("toGerman")
        self.horizontalLayout.addWidget(self.toGerman)

        self.toKorean = QtWidgets.QRadioButton(self.centralwidget)
        self.toKorean.setObjectName("toKorean")
        self.horizontalLayout.addWidget(self.toKorean)

        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.verticalHeader().setStretchLastSection(True)
        self.gridLayout.addWidget(self.tableWidget, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.openFile.setText(_translate("MainWindow", "打开文件"))
        self.saveFile.setText(_translate("MainWindow", "保存"))
        self.translate.setText(_translate("MainWindow", "翻译成"))
        self.toChina.setText(_translate("MainWindow", "中文"))
        self.toEnglish.setText(_translate("MainWindow", "英文"))
        self.toFrench.setText(_translate("MainWindow", "法语"))
        self.toJapan.setText(_translate("MainWindow", "日语"))
        self.toGerman.setText(_translate("MainWindow", "德语"))
        self.toKorean.setText(_translate("MainWindow", "韩语"))


