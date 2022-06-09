# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import _thread
import json
import sys

import requests

import xlrd as xlrd
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QTableWidget, QTableWidgetItem, QProgressDialog, QMessageBox
from xlrd.sheet import Sheet

import filedialog
import xls_dealwith

app = QtWidgets.QApplication(sys.argv)
tableWidget: QTableWidget
table: Sheet
list = []
translatenum = 0


def readXls(strpath=""):
    workbook = xlrd.open_workbook_xls(strpath[0][0])
    global table
    table = workbook.sheets()[0]
    # table0 = workbook.sheet_by_index(0)
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
        # tableWidget.viewport().update()
    # 按列读取
    # for i in range(table.ncols):
    #     print(table.col_values(i))
    # print(table.cell(3, 2).value)
    return table


class parentWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.main_ui = xls_dealwith.Ui_MainWindow()
        self.main_ui.setupUi(self)
        self.setWindowTitle("xls 处理")

def openfile():
        openfile_name =QFileDialog.getOpenFileNames(None, "请选择要添加的文件", "./", "Text Files (*.xls);;All Files (*)")
        print(openfile_name)
        return readXls(openfile_name)

def networkrequest(tarlan = "en", content = "", colpos = 0):
    # 网站地址
    url = 'https://translate.google.cn/translate_a/single?client=gtx&sl=auto&tl=' + tarlan + '&dt=t&q=' + content
    header = {'Connection': 'close'}

    # 获取网页
    r = requests.request('GET', url)
    # requests.adapters.DEFAULT_RETRIES = 5
    # r.encoding = r.apparent_encoding
    load = json.loads(r.text)
    result = load[0][0][0]
    # print("the %s translat result is %s:", content, result)
    # tableWidget.setItem(colpos, 1, QTableWidgetItem(result))
    global translatenum
    translatenum = translatenum+1
    print(translatenum)
    dialog.refreshProgress(translatenum)
    return result


def translate():
    global list,dialog
    for i in range(table.nrows):
        inputContent = table.cell(i, 1).value
        if len(inputContent) > 0:
            list.append(i)
            # print("inputContent = "+inputContent)
    dialog = myProgressDialog(int(list.count()))
    for i in range(list.count()):
        inputContent = table.cell(list[i], 1).value
        try:
            _thread.start_new_thread(networkrequest, ("en", inputContent, i))
        except requests.exceptions.ConnectionError:
            print("Error: unable to start thread")



class openFileDialog(QFileDialog):
    def __init__(self):
        QFileDialog.__init__(self)
        self.child = filedialog.Ui_Dialog()
        self.child.setupUi(self)

class myProgressDialog:
    global progress,num
    def __init__(self,num):
        progress = QProgressDialog(QProgressDialog())
        progress.setWindowTitle("请稍等")
        progress.setLabelText("正在操作...")
        progress.setMinimumDuration(1)
        progress.setWindowModality(Qt.WindowModal)
        progress.setRange(0, num)

    def refreshProgress(self, pos):
        if pos < num:
            progress.setValue(pos)
            if progress.wasCanceled():
                QMessageBox.warning(QProgressDialog(),"提示","操作失败")
        else:
            progress.setValue(list.count())
            QMessageBox.information(QProgressDialog(),"提示","操作成功")

dialog: myProgressDialog

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # root = tkinter.Tk()
    # root.title("test demo")
    # # root.geometry("200x500")
    # # 创建窗口对象的背景色
    # # 创建两个列表
    # li = ['C', 'python', 'php', 'html', 'SQL', 'java']
    # movie = ['CSS', 'jQuery', 'Bootstrap']
    # listb = tkinter.Listbox(root)  # 创建两个列表组件
    # listb2 = tkinter.Listbox(root)
    # for item in li:  # 第一个小部件插入数据
    #     listb.insert(0, item)
    #
    # for item in movie:  # 第二个小部件插入数据
    #     listb2.insert(0, item)
    #
    # listb.pack()  # 将小部件放置到主窗口中
    # listb2.pack()
    # root.mainloop()


    # dialog = QtWidgets.QDialog()
    # ui = untitled.Ui_Dialog()
    # ui.setupUi(dialog)
    # dialog.show()

    # mainView = QtWidgets.QMainWindow()
    # mainView.setWindowTitle("xls 处理")
    # mainView.showMaximized()
    # sys.exit(app.exec_())

    mainView = parentWindow()

    # childView = openFileDialog()

    tableWidget = mainView.main_ui.tableWidget
    mainView.main_ui.openFile.clicked.connect(openfile)
    mainView.main_ui.translate.clicked.connect(translate)

    mainView.show()
    sys.exit(app.exec_())



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
