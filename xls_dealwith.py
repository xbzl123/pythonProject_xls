# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'xls_dealwith.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import json

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QCompleter

from jsonReader import readLanguageJson


class Ui_MainWindow(object):
    def __init__(self):
        self.data = readLanguageJson()

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

        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setEditable(True)
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout.addWidget(self.comboBox)

        for i in range(len(self.data)):
            self.comboBox.addItem("")

        self.lgLabel = QtWidgets.QLabel(self.centralwidget)
        self.lgLabel.setObjectName("lgLabel")
        self.horizontalLayout.addWidget(self.lgLabel)

        self.toAllLanguage = QtWidgets.QRadioButton(self.centralwidget)
        self.toAllLanguage.setObjectName("toAllLanguage")
        self.horizontalLayout.addWidget(self.toAllLanguage)

        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)


        self.toXmlLayout = QtWidgets.QHBoxLayout()
        self.toXmlLayout.setObjectName("toXmlLayout")
        self.toXml = QtWidgets.QPushButton(self.centralwidget)
        self.toXml.setObjectName("toXml")
        self.toXmlLayout.addWidget(self.toXml)

        self.keyLabel = QtWidgets.QLabel(self.centralwidget)
        self.keyLabel.setObjectName("keyLabel")
        self.toXmlLayout.addWidget(self.keyLabel)

        self.keyEdit = QtWidgets.QLineEdit()
        self.keyEdit.setObjectName("keyEdit")
        self.keyEdit.setText("1")
        self.toXmlLayout.addWidget(self.keyEdit)

        self.valueLabel = QtWidgets.QLabel(self.centralwidget)
        self.valueLabel.setObjectName("valueLabel")
        self.toXmlLayout.addWidget(self.valueLabel)

        self.valueEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.valueEdit.setObjectName("valueEdit")
        self.valueEdit.setText("2")
        self.toXmlLayout.addWidget(self.valueEdit)


        self.itemLabel = QtWidgets.QLabel(self.centralwidget)
        self.itemLabel.setObjectName("itemLabel")
        self.toXmlLayout.addWidget(self.itemLabel)

        self.itemEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.itemEdit.setObjectName("itemEdit")
        self.itemEdit.setText("string")
        self.toXmlLayout.addWidget(self.itemEdit)


        self.includeHeader = QtWidgets.QCheckBox(self.centralwidget)
        self.includeHeader.setObjectName("includeHeader")
        self.toXmlLayout.addWidget(self.includeHeader)

        self.gridLayout.addLayout(self.toXmlLayout, 1, 0, 1, 1)

        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.tableWidget.verticalHeader().setStretchLastSection(True)
        self.gridLayout.addWidget(self.tableWidget, 2, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)

        self.toAllLanguage.clicked.connect(self.swithNotSimple)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.openFile.setText(_translate("MainWindow", "打开文件"))
        self.saveFile.setText(_translate("MainWindow", "保存"))
        self.translate.setText(_translate("MainWindow", "翻译成"))

        self.toAllLanguage.setText(_translate("MainWindow", "全部语言"))
        self.toXml.setText(_translate("MainWindow", "toXml"))
        self.keyLabel.setText(_translate("MainWindow", "keyColunm:"))
        self.valueLabel.setText(_translate("MainWindow", "valueColunm:"))
        self.itemLabel.setText(_translate("MainWindow", "item:"))
        self.includeHeader.setText(_translate("MainWindow", "包含首行？"))
        for i in range(len(self.data)):
            self.comboBox.setItemText(i, _translate("MainWindow", self.data[i]['DisplayName']))

    def swithNotSimple(self):
        self.comboBox.clear()
        list = []
        self.data = readLanguageJson(self.toAllLanguage.isChecked())
        for i in range(len(self.data)):
            list.append(self.data[i]['DisplayName'])
        qCompleter1 = QCompleter(list)  # 列表填充
        qCompleter1.setCaseSensitivity(Qt.CaseInsensitive)
        self.comboBox.setCompleter(qCompleter1)
        self.comboBox.addItems(list)  # 添加列表






