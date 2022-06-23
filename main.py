# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import _thread
import json
import random
import sys
import time
from lxml import etree

import requests

import xlrd as xlrd
import xlwt
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QBasicTimer
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QTableWidget, QTableWidgetItem, QProgressDialog, QMessageBox, \
    QDialog, QProgressBar, QWidget

import filedialog
import xls_dealwith

app = QtWidgets.QApplication(sys.argv)
tableWidget: QTableWidget
targetlanguage = "en"
workbook = None

def readXls(strpath=""):
    print(strpath)
    global workbook
    workbook = xlrd.open_workbook_xls(strpath[0][0])
    table = workbook.sheets()[0]
    # 按行读取
    tableWidget.setColumnCount(table.ncols)
    tableWidget.setRowCount(table.nrows)
    for i in range(table.nrows):
        print(table.row_values(i))
        for j in range(table.ncols):
            value = table.cell(i, j).value
            if isinstance(value, float):
                value = str(int(value))
            tableWidget.setItem(i, j, QTableWidgetItem(value))
    return table

def writeXls(strpath=""):
    global workbook
    savebook = xlwt.Workbook('utf-8')
    sheet = savebook.add_sheet(workbook.sheet_names()[0])
    oldsheet = workbook.sheets()[0]
    for i in range(oldsheet.nrows):
        for j in range(oldsheet.ncols):
            sheet.write(i, j,oldsheet.cell(i, j).value)
            print(oldsheet.cell(i, j).value)
    print(strpath)
    savebook.save(strpath[0])


class parentWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.main_ui = xls_dealwith.Ui_MainWindow()
        self.main_ui.setupUi(self)
        self.setWindowTitle("xls 处理")


def openfile():
    openfile_name = QFileDialog.getOpenFileNames(None, "请选择要添加的文件", "./", "Text Files (*.xls);;All Files (*)")
    print(openfile_name)
    return readXls(openfile_name)

def savefile():
    savefile_name = QFileDialog.getSaveFileName(None, "保存文件", "./", "Text Files (*.xls);;All Files (*)")
    print(savefile_name)
    writeXls(savefile_name)

def getProxyAddress():
        # 网站地址
        url = 'https://proxy.seofangfa.com/'
        head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
            "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
        }
        r = requests.get(url, headers=head)
        dom = etree.HTML(r.text)
        url_path = '//td'
        urls = dom.xpath(url_path)
        ipaddress = 'http://'+ urls[0].text + ':' + urls[1].text
        print("the len(selectedlist) is %s:",ipaddress)
        return ipaddress



def networkrequest(tarlan="", tableItem=QTableWidgetItem, len = 0,proxie = ""):
    try:
        # 网站地址
        url = 'https://translate.google.cn/translate_a/single?client=gtx&sl=auto&tl=' + tarlan + '&dt=t&q=' + tableItem.text()
        head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
            "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
        }
        # 用户代理，表示告诉豆瓣服务器，我们是什么类型的机器、浏览器（本质上是告诉浏览器，我们可以接收什么水平的文件内容）
        proxies = {'http': proxie}
        # 获取网页
        r = requests.get(url, headers=head, proxies=proxies)

        load = json.loads(r.text)
        result = load[0][0][0]
        print("the %s translat result is %s:", tableItem.text(), result)
        tableWidget.setItem(tableItem.row(), tableItem.column(), QTableWidgetItem(result))
        global translatenum
        translatenum = translatenum + 1
        progress = int(translatenum / len * 100)
        # print("the translatenum is %s:", translatenum)
        # print("the len(selectedlist) is %s:", len)
        childView.timerEvent(progress)
    except requests.exceptions.ConnectionError:
        print("Error: unable to start thread")


#翻译选中的单元格的内容为指定语言
def translate():
    proxie = getProxyAddress()

    global translatenum
    translatenum = 0
    global childView
    selectedlist = []
    childView = ProgressBar()

    for i in range(len(tableWidget.selectedItems())):
        selectedlist.append(tableWidget.selectedItems()[i])

    print("size = %d", len(selectedlist))
    translatelist = []
    for i in range(len(selectedlist)):
        inputContent = selectedlist[i].text()
        if len(inputContent) > 0:
            translatelist.append(selectedlist[i])



    #多线程调用网络接口翻译
    for i in range(len(translatelist)):
        _thread.start_new_thread(networkrequest, (targetlanguage, translatelist[i], len(translatelist)), proxie)
        time.sleep(0.1)


class openFileDialog(QFileDialog):
    def __init__(self):
        QFileDialog.__init__(self)
        self.child = filedialog.Ui_Dialog()
        self.child.setupUi(self)

def selecttargetlanguage(lan = ""):
    global targetlanguage
    targetlanguage = lan
    print('targetlanguage %s', targetlanguage)


class ProgressBar(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(80, 20, 300, 30)

        self.timer = QBasicTimer()
        self.step = 0

        self.setGeometry(650, 500, 420, 70)
        self.setWindowTitle('The Progress of Translate')
        self.show()

    def timerEvent(self, e):
        if e != self.step-1:
            self.step = e+1
            print("self.step = %s", self.step)
            self.pbar.setValue(self.step)

        if self.step >= 100:
            self.timer.stop()
            self.close()
            tableWidget.viewport().update()
            return

def convertxls():
    if workbook is None:
        QMessageBox.about(QDialog(), "Notice", "please open a xls file frist!")
    else:
        sheets_ = workbook.sheets()[0]
        contentxls = '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n'
        # eg:  <string name="authentication_title">Two-factor Authentication</string>
        if mainView.main_ui.includeHeader.isChecked():
            for i in range(sheets_.nrows):
                if sheets_.cell(i, int(mainView.main_ui.keyEdit.text()) - 1).value is not None:
                    contentxls += '\t<string name="'+ str(sheets_.cell(i, int(mainView.main_ui.keyEdit.text()) - 1).value) + '">' \
                                  + str(sheets_.cell(i, int(mainView.main_ui.valueEdit.text()) - 1).value)+'</string>\n'
        else:
            for i in range(sheets_.nrows):
                if sheets_.cell(i, int(mainView.main_ui.keyEdit.text()) - 1).value is not None and i > 0:
                    contentxls += '\t<string name="'+ str(sheets_.cell(i, int(mainView.main_ui.keyEdit.text()) - 1).value) + '">' \
                                  + str(sheets_.cell(i, int(mainView.main_ui.valueEdit.text()) - 1).value)+'</string>\n'
        contentxls +='</resources>'
        print(contentxls)

        savefile_name = QFileDialog.getSaveFileName(None, "保存文件", "./", "Text Files (*.xml);;All Files (*)")
        if len(savefile_name[0]) > 0:
            savexml = open(savefile_name[0], 'w', encoding="utf-8")
            savexml.write(contentxls)
            savexml.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    mainView = parentWindow()

    tableWidget = mainView.main_ui.tableWidget
    mainView.main_ui.openFile.clicked.connect(openfile)
    mainView.main_ui.translate.clicked.connect(translate)
    mainView.main_ui.saveFile.clicked.connect(savefile)

    mainView.main_ui.toChina.clicked.connect(lambda: selecttargetlanguage("zh"))
    mainView.main_ui.toJapan.clicked.connect(lambda: selecttargetlanguage("ja"))
    mainView.main_ui.toEnglish.clicked.connect(lambda: selecttargetlanguage("en"))
    mainView.main_ui.toKorean.clicked.connect(lambda: selecttargetlanguage("ko"))
    mainView.main_ui.toGerman.clicked.connect(lambda: selecttargetlanguage("de"))
    mainView.main_ui.toFrench.clicked.connect(lambda: selecttargetlanguage("fr"))

    mainView.main_ui.toXml.clicked.connect(convertxls)


    mainView.show()
    sys.exit(app.exec_())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
