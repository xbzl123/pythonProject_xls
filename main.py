# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys
import tkinter

import xlrd as xlrd
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QTableWidget, QTableWidgetItem

import filedialog
import xls_dealwith

app = QtWidgets.QApplication(sys.argv)
tableWidget : QTableWidget

def readXls(strpath=""):
    workbook = xlrd.open_workbook_xls(strpath[0][0])
    table = workbook.sheets()[0]
    tableWidget.setItem(3,1,QTableWidgetItem('test'))
    # table0 = workbook.sheet_by_index(0)
    # 按行读取
    for i in range(table.nrows):
        for j in range(table.ncols):
            tableWidget.setItem(i, j, QTableWidgetItem(table.cell(i, j).value))
        # tableWidget.viewport().update()
    # 按列读取
    # for i in range(table.ncols):
    #     print(table.col_values(i))
    # print(table.cell(3, 2).value)
    pass


class parentWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.main_ui = xls_dealwith.Ui_MainWindow()
        self.main_ui.setupUi(self)
        self.setWindowTitle("xls 处理")

def openfile():
        openfile_name =QFileDialog.getOpenFileNames(None, "请选择要添加的文件", "./", "Text Files (*.xls);;All Files (*)")
        print(openfile_name)
        readXls(openfile_name)



class openFileDialog(QFileDialog):
    def __init__(self):
        QFileDialog.__init__(self)
        self.child = filedialog.Ui_Dialog()
        self.child.setupUi(self)



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

    mainView.show()
    sys.exit(app.exec_())



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
