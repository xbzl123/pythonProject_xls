# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import _thread
import json
import sys
import threading
import time
from lxml import etree

import requests

import xlrd as xlrd
import xlwt
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QBasicTimer, QObject
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QTableWidget, QTableWidgetItem, QProgressDialog, QMessageBox, \
    QDialog, QProgressBar, QWidget, QApplication

import filedialog
import xls_dealwith

app = QtWidgets.QApplication(sys.argv)
tableWidget: QTableWidget
targetlanguage = "en"
workbook = None
translatenum = 0

def readXls(strpath=""):
    print(strpath)
    global workbook
    if strpath[1] == "":
        return
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
            sheet.write(i, j, oldsheet.cell(i, j).value)
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
    if workbook == None:
        QMessageBox.about(QDialog(), "Notice", "please open a xls file frist!")
        return
    savefile_name = QFileDialog.getSaveFileName(None, "保存文件", "./", "Text Files (*.xls);;All Files (*)")
    print(savefile_name)
    writeXls(savefile_name)


class MyThread(threading.Thread):
    #  通过类成员对象定义信号对象
    _signal = pyqtSignal(int, int, int)

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        for i in range(100):
            self._signal.emit(i)  # 发送实时任务进度和总任务进度
            time.sleep(0.1)


activedproxies = []
checkactivedipnum = 0

def getproxyaddress():
    try:
        # 网站地址
        url = 'https://proxy.seofangfa.com/'
        head = {  # 模拟浏览器头部信息，向服务器发送消息
            "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
        }
        r = requests.get(url, headers=head)
        dom = etree.HTML(r.text)
        url_path = '//td'
        urls = dom.xpath(url_path)
        proxies = []
        for i in range(10):
            print("i is %d:", i)
            proxie = 'http://' + urls[i * 5].text + ':' + urls[i * 5 + 1].text
            proxies.append(proxie)
        print("the len(selectedlist) is %s:", proxies)
    except requests.exceptions.ConnectionError:
        print("Error: unable to connect success")
    finally:
        urls = ["http://httpbin.org/ip", "https://www.baidu.com", "https://www.google.com.hk", "https://www.sohu.com",
                "https://mail.qq.com", "https://www.sina.com.cn", "https://mail.10086.cn", "https://www.sogou.com",
                "https://juejin.cn", "https://mail.sina.com.cn"]
        print('开始IP检测')
        global checkactivedipnum
        checkactivedipnum = 0
        global activedproxies
        activedproxies = []
        try:
            for i in range(len(proxies)):
                _thread.start_new_thread(checkactivedip, (proxies[i], urls[i], len(proxies)))
        except Exception as e:
            print('start thread :' + e.args[0])
        finally:
            if len(activedproxies) > 0:
                while True:
                    if checkactivedipnum == len(proxies):
                        starttranslate(activedproxies,True)
                        print('结束IP检测'+str(len(proxies)))
                        break
            else:
                starttranslate(activedproxies, False)


# 筛选有效的代理IP
def checkactivedip(proxy="", url="", num=0):
    try:
        head = {  # 模拟浏览器头部信息，向服务器发送消息
            "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
        }
        proxieswrap = {'http': proxy}
        response = requests.get(url, headers=head, proxies=proxieswrap, timeout=0.1)
        print(response.status_code)
        print('当前IP有效:' + proxy)
        global activedproxies
        activedproxies.append(proxy)
        # starttranslate(proxies[i])
    except Exception as e:
        print('当前IP无效:' + proxy)
    finally:
        global checkactivedipnum
        checkactivedipnum = checkactivedipnum+1
        if checkactivedipnum == num:
            print('代理IP的长度:' + str(len(activedproxies)))

def pbar_change(progress):
    global so
    so.progress_update.emit(progress)

class TranslateItem:
    def __init__(self, pos=0, content=[]):
        self.pos = pos
        self.content = content

#并发任务进行翻译
def multinetworktranslate(targetlanguage="", translatelist=[]):
    num = len(activedproxies)
    #转整形列表
    totalpos = []
    for i in range(len(translatelist)):
        totalpos.append(i)

    temp = []
    for i in range(num):
        data = []
        for j in range(len(totalpos)):
            if totalpos[j]%num == i:
                data.append(totalpos[j])
        threads = TranslateItem(i, data)
        temp.append(threads)

    print('temp的长度:' + str(temp[0].content))

    for i in range(num):
        _thread.start_new_thread(networktranslatesingle, (targetlanguage, translatelist, temp[i].content, activedproxies[i]))



def networktranslatesingle(tarlan="", translatelist=[], translatescope = [], proxy = ""):
    print("00the length is %s:", activedproxies)
    for i in range(len(translatelist)):
        if i in translatescope:
            # print('i的值:%s'+ str(i))
            try:
                # 网站地址
                url = 'https://translate.google.hk/translate_a/single?client=gtx&sl=auto&tl=' + tarlan + '&dt=t&q=' + translatelist[i].text()
                head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
                    "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
                }
                # 用户代理，表示告诉豆瓣服务器，我们是什么类型的机器、浏览器（本质上是告诉浏览器，我们可以接收什么水平的文件内容）
                proxieswrap = {'http': proxy}

                # 获取网页
                r = requests.get(url, headers=head, proxies=proxieswrap)
                if r.status_code == 200:
                    load = json.loads(r.text)
                    result = load[0][0][0]
                    print("the %s translat result is %s:", translatelist[i].text(), result)
                    tableWidget.setItem(translatelist[i].row(), translatelist[i].column(), QTableWidgetItem(result))
                    global translatenum, so
                    translatenum = translatenum + 1
                    progress = int(translatenum / len(translatelist) * 100)
                    # childView.setProgress(progress)
                    worker = threading.Thread(target=pbar_change(progress))
                    worker.start()
                else:
                    QMessageBox.about(QDialog(), "Notice", r.text)
            except requests.exceptions.ConnectionError:
                print("Error: unable to start thread")
            time.sleep(0.05)


#串联任务进行翻译
def networkrequest(tarlan="", translatelist=[], proxies=""):
    for i in range(len(translatelist)):
        try:
            # 网站地址
            url = 'https://translate.google.hk/translate_a/single?client=gtx&sl=auto&tl=' + tarlan + '&dt=t&q=' + \
                  translatelist[i].text()
            head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
                "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
            }
            # 用户代理，表示告诉豆瓣服务器，我们是什么类型的机器、浏览器（本质上是告诉浏览器，我们可以接收什么水平的文件内容）
            proxieswrap = {'http': proxies}
            # 获取网页
            r = requests.get(url, headers=head, proxies=proxieswrap)
            if r.status_code == 200:
                load = json.loads(r.text)
                result = load[0][0][0]
                print("the %s translat result is %s:", translatelist[i].text(), result)
                tableWidget.setItem(translatelist[i].row(), translatelist[i].column(), QTableWidgetItem(result))
                global translatenum, so
                translatenum = translatenum + 1
                progress = int(translatenum / len(translatelist) * 100)
                print("the progress is %s:", progress)
                # childView.setProgress(progress)
                worker = threading.Thread(target=pbar_change(progress))
                worker.start()
            else:
                QMessageBox.about(QDialog(), "Notice", r.text)
        except requests.exceptions.ConnectionError:
            print("Error: unable to start thread")
        time.sleep(0.05)


# 翻译选中的单元格的内容为指定语言
def translate():
    getproxyaddress()


def starttranslate(proxies,isMulti = False):
    global translatenum
    translatenum = 0
    global childView
    selectedlist = []
    if workbook == None:
        QMessageBox.about(QDialog(), "Notice", "please open a xls file frist!")
        return
    elif len(tableWidget.selectedItems()) < 1:
        QMessageBox.about(QDialog(), "Notice", "please select data to translate!")
        return

    for i in range(len(tableWidget.selectedItems())):
        selectedlist.append(tableWidget.selectedItems()[i])

    print("size = %d", len(selectedlist))
    translatelist = []
    for i in range(len(selectedlist)):
        inputContent = selectedlist[i].text()
        if len(inputContent) > 0:
            translatelist.append(selectedlist[i])
    # 实例化
    global so
    so = SignalStore()
    childView = ProgressBar()

    # 多线程调用网络接口翻译
    if isMulti:
        multinetworktranslate(targetlanguage, translatelist)
    else:
        _thread.start_new_thread(networkrequest, (targetlanguage, translatelist, ""))


class openFileDialog(QFileDialog):
    def __init__(self):
        QFileDialog.__init__(self)
        self.child = filedialog.Ui_Dialog()
        self.child.setupUi(self)


def selecttargetlanguage(lan=""):
    global targetlanguage
    targetlanguage = lan
    print('targetlanguage %s', targetlanguage)


# 信号库
class SignalStore(QObject):
    # 定义一种信号
    progress_update = pyqtSignal(int)
    # 还可以定义其他作用的信号


class ProgressBar(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global so
        so.progress_update.connect(self.setProgress)
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(80, 20, 300, 30)

        self.timer = QBasicTimer()
        self.step = 0
        # 窗口初始化
        self.setGeometry(650, 500, 420, 70)
        self.setWindowTitle('The Progress of Translate')
        self.show()

    def setProgress(self, e):
        if self.step == e:
            return
        print("e= %s", e)
        self.pbar.setValue(e)
        self.step = e

        if e >= 100:
            self.close()
            # global progress
            # progress = 0
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
                    contentxls += '\t<string name="' + str(
                        sheets_.cell(i, int(mainView.main_ui.keyEdit.text()) - 1).value) + '">' \
                                  + str(
                        sheets_.cell(i, int(mainView.main_ui.valueEdit.text()) - 1).value) + '</string>\n'
        else:
            for i in range(sheets_.nrows):
                if sheets_.cell(i, int(mainView.main_ui.keyEdit.text()) - 1).value is not None and i > 0:
                    contentxls += '\t<string name="' + str(
                        sheets_.cell(i, int(mainView.main_ui.keyEdit.text()) - 1).value) + '">' \
                                  + str(
                        sheets_.cell(i, int(mainView.main_ui.valueEdit.text()) - 1).value) + '</string>\n'
        contentxls += '</resources>'
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
