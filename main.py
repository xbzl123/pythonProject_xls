# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import _thread
import json
import sys
import threading
import time

from PyQt5.QtGui import QIcon
from lxml import etree

import requests

import xlrd as xlrd
import xlwt
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QTableWidget, QTableWidgetItem, QProgressBar, QWidget

import filedialog
import xls_dealwith
from MyDialogBox import MyDailogBox
from jsonReader import readLanguageJson

app = QtWidgets.QApplication(sys.argv)
tableWidget: QTableWidget
targetLanguage = "en"
workbook = None
translateNum = 0
ActiveProxies = []
checkActiveIpNum = 0


def readXls(strpath=""):
    # print(strpath)
    global workbook
    if strpath[1] == "":
        return
    workbook = xlrd.open_workbook_xls(strpath[0][0])
    table = workbook.sheets()[0]
    # 按行读取
    tableWidget.setColumnCount(table.ncols)
    tableWidget.setRowCount(table.nrows)
    for i in range(table.nrows):
        # print(table.row_values(i))
        for j in range(table.ncols):
            value = table.cell(i, j).value
            if isinstance(value, float):
                value = str(int(value))
            tableWidget.setItem(i, j, QTableWidgetItem(value))
    return table


def writeXls(strpath=""):
    global workbook
    save_book = xlwt.Workbook('utf-8')
    sheet = save_book.add_sheet(workbook.sheet_names()[0])
    oldsheet = workbook.sheets()[0]
    for i in range(oldsheet.nrows):
        for j in range(oldsheet.ncols):
            sheet.write(i, j, oldsheet.cell(i, j).value)
            # print(oldsheet.cell(i, j).value)
    # print(strpath)
    try:
        save_book.save(strpath[0])
    except Exception as e:
        showdialog("失败", e.args[0])
        return
    finally:
        showdialog("注意", "文件保存成功!")


class ParentWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.main_ui = xls_dealwith.Ui_MainWindow()
        self.main_ui.setupUi(self)
        self.setWindowTitle("xls 文件翻译")
        self.setWindowIcon(QIcon("icons/xls.jpg"))


def openfile():
    openfile_name = QFileDialog.getOpenFileNames(None, "请选择要添加的.xls格式文件", "./", "Text Files (*.xls);;All Files (*)")
    # print(openfile_name)
    return readXls(openfile_name)


def showdialog(title='', message=''):
    box = MyDailogBox()
    box.warning(box.mw, title, message)


def savefile():
    if workbook is None:
        showdialog("注意", "请先打开一个.xls格式的文件!")
        return
    savefile_name = QFileDialog.getSaveFileName(None, "保存文件", "./", "Text Files (*.xls);;All Files (*)")
    # print(savefile_name)
    if len(savefile_name[0]) < 1:
        return
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


# 获取代理IP
def getProxyAddress():
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
            proxie = 'http://' + urls[i * 5].text + ':' + urls[i * 5 + 1].text
            proxies.append(proxie)
    except requests.exceptions.ConnectionError:
        showdialog("注意", "网络连接出现错误!")
        print("Error: unable to connect success")
    finally:
        # 检测代理IP是否有效
        urls = ["http://httpbin.org/ip", "https://www.baidu.com", "https://www.google.com.hk", "https://www.sohu.com",
                "https://mail.qq.com", "https://www.sina.com.cn", "https://mail.10086.cn", "https://www.sogou.com",
                "https://juejin.cn", "https://mail.sina.com.cn"]
        print('开始IP检测')
        global checkActiveIpNum
        checkActiveIpNum = 0
        global ActiveProxies
        ActiveProxies = []
        try:
            for i in range(len(proxies)):
                _thread.start_new_thread(checkActiveIp, (proxies[i], urls[i], len(proxies)))
        except Exception as e:
            print('start thread :' + e.args[0])
        finally:
            if len(proxies) > 0:
                print('开始多线程翻译')
                while True:
                    if checkActiveIpNum == len(proxies):
                        startTranslate(True)
                        break
            else:
                print('开始单线程翻译')
                startTranslate(False)


# 筛选有效的代理IP
def checkActiveIp(proxy="", url="", num=0):
    try:
        head = {  # 模拟浏览器头部信息，向服务器发送消息
            "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
        }
        proxies_wrap = {'http': proxy}
        requests.get(url, headers=head, proxies=proxies_wrap, timeout=0.1)
        print('当前IP有效:' + proxy)
        global ActiveProxies
        ActiveProxies.append(proxy)
    except Exception as e:
        print('当前IP无效:' + proxy)
    finally:
        global checkActiveIpNum
        checkActiveIpNum = checkActiveIpNum + 1
        if checkActiveIpNum == num:
            print('代理IP的长度:' + str(len(ActiveProxies)))


def progressbarChange(progress):
    global so
    so.progress_update.emit(progress)


class TranslateItem:
    def __init__(self, pos=0, content=[]):
        self.pos = pos
        self.content = content


# 并发任务进行翻译
def multiNetworkTranslate(tarLan="", translateList=[]):
    num = len(ActiveProxies)
    # 转整形列表
    total_pos = []
    for i in range(len(translateList)):
        total_pos.append(i)

    temp = []
    for i in range(num):
        data = []
        for j in range(len(total_pos)):
            if total_pos[j] % num == i:
                data.append(total_pos[j])
        threads = TranslateItem(i, data)
        temp.append(threads)
    for i in range(num):
        _thread.start_new_thread(networkTranslateSingle,
                                 (tarLan, translateList, temp[i].content, ActiveProxies[i]))


def networkTranslateSingle(tarLan="", translateList=[], translateScope=[], proxy=""):
    for i in range(len(translateList)):
        if i in translateScope:
            try:  # 网站地址
                url = 'https://translate.google.hk/translate_a/single?client=gtx&sl=auto&tl=' + tarLan + '&dt=t&q=' + \
                      translateList[i].text()
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
                    tableWidget.setItem(translateList[i].row(), translateList[i].column(), QTableWidgetItem(result))
                    global translateNum, so
                    translateNum = translateNum + 1
                    progress = int(translateNum / len(translateList) * 100)
                    worker = threading.Thread(target=progressbarChange(progress))
                    worker.start()
                else:
                    showdialog("注意", r.text)
            except requests.exceptions.ConnectionError:
                print("Error: unable to start thread")
            time.sleep(0.05)


# 串联任务进行翻译
def networkRequest(tarLan="", translateList=[], proxies=""):
    for i in range(len(translateList)):
        try:
            # 网站地址
            url = 'https://translate.google.hk/translate_a/single?client=gtx&sl=auto&tl=' + tarLan + '&dt=t&q=' + \
                  translateList[i].text()
            head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息
                "User-Agent": "Mozilla / 5.0(Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 80.0.3987.122  Safari / 537.36"
            }
            # 用户代理，表示告诉豆瓣服务器，我们是什么类型的机器、浏览器（本质上是告诉浏览器，我们可以接收什么水平的文件内容）
            proxies_wrap = {'http': proxies}
            # 获取网页
            r = requests.get(url, headers=head, proxies=proxies_wrap)
            if r.status_code == 200:
                load = json.loads(r.text)
                result = load[0][0][0]
                print("the %s translates is :%s" % (translateList[i].text(), result))
                tableWidget.setItem(translateList[i].row(), translateList[i].column(), QTableWidgetItem(result))
                global translateNum, so
                translateNum = translateNum + 1
                progress = int(translateNum / len(translateList) * 100)
                print("the progress is %s:", progress)
                worker = threading.Thread(target=progressbarChange(progress))
                worker.start()
            else:
                showdialog("注意", r.text)
        except requests.exceptions.ConnectionError:
            print("Error: unable to start thread")
        time.sleep(0.05)


# 翻译选中的单元格的内容为指定语言
def translate():
    if workbook is None:
        showdialog("注意", "请先打开一个.xls格式的文件!")
        return
    elif len(tableWidget.selectedItems()) < 1:
        showdialog("注意", "请选择你需要翻译的单元格区域!")
        return
    selectTargetLanguage()
    if len(tableWidget.selectedItems()) < 10:
        startTranslate(False)
    else:
        getProxyAddress()


def startTranslate(isMulti=False):
    global translateNum
    translateNum = 0
    global childView
    selectedlist = []

    for i in range(len(tableWidget.selectedItems())):
        selectedlist.append(tableWidget.selectedItems()[i])

    print("size = %d", len(selectedlist))
    translate_list = []
    for i in range(len(selectedlist)):
        input_content = selectedlist[i].text()
        if len(input_content) > 0:
            translate_list.append(selectedlist[i])
    # 实例化
    global so
    so = SignalStore()
    childView = ProgressBar()

    # 多线程调用网络接口翻译
    if isMulti:
        multiNetworkTranslate(targetLanguage, translate_list)
    else:
        _thread.start_new_thread(networkRequest, (targetLanguage, translate_list, ""))


def selectTargetLanguage():
    data = readLanguageJson(mainView.main_ui.toAllLanguage.isChecked())
    global targetLanguage
    targetLanguage = data[mainView.main_ui.comboBox.currentIndex()]['LangCultureName']
    print('targetlanguage %s', targetLanguage)


# 信号库
class SignalStore(QObject):
    # 定义一种信号
    progress_update = pyqtSignal(int)
    # 还可以定义其他作用的信号


class ProgressBar(QWidget):
    def __init__(self):
        super().__init__()
        self.pbar = QProgressBar(self)
        self.step = 0
        self.initUI()

    def initUI(self):
        global so
        so.progress_update.connect(self.setProgress)
        self.pbar.setGeometry(80, 20, 300, 30)
        # 窗口初始化
        self.setGeometry(650, 500, 420, 70)
        self.setWindowTitle('当前翻译的进度是：')
        self.setWindowIcon(QIcon('icons/xls-1.jpg'))
        self.show()

    def setProgress(self, e):
        if self.step == e:
            return
        print("e= %s", e)
        self.pbar.setValue(e)
        self.step = e

        if e >= 100:
            self.close()
            tableWidget.viewport().update()
            return


def convertxls():
    if workbook is None:
        showdialog("注意", "请先打开一个.xls格式的文件!")
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
    mainView = ParentWindow()
    tableWidget = mainView.main_ui.tableWidget
    mainView.main_ui.openFile.clicked.connect(openfile)
    mainView.main_ui.translate.clicked.connect(translate)
    mainView.main_ui.saveFile.clicked.connect(savefile)
    mainView.main_ui.toXml.clicked.connect(convertxls)
    mainView.show()
    sys.exit(app.exec_())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
